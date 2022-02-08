import datatajoint as dj
import importlib
import inspect
from datetime import datetime
import pandas as pd
import numpy as np
from element_interface.utils import find_full_path, dict_to_uuid


schema = dj.schema()
_linking_module = None


def activate(dlc_schema_name, *, create_schema=True, create_tables=True,
             linking_module=None):
    """
    activate(schema_name, *, create_schema=True, create_tables=True,
             linking_module=None)
        :param schema_name: schema name on the database server to activate the
                            `behavior` element
        :param create_schema: when True (default), create schema in the database if it
                              does not yet exist.
        :param create_tables: when True (default), create schema in the database if it
                              does not yet exist.
        :param linking_module: a module (or name) containing the required dependencies
                               to activate the `session` element:
            Upstream tables:
                + Session: parent table to Recording, identifying a recording session
            Functions:
                + get_dlc_root_data_dir() -> list
                    Retrieve the root data director(y/ies) with behavioral
                    recordings for all subject/sessions.
                    :return: a string for full path to the root data directory
                + get_session_directory(session_key: dict) -> str
                    Retrieve the session directory containing the recording(s)
                    for a given Session
                    :param session_key: a dictionary of one Session `key`
                    :return: a string for full path to the session directory
                + get_dlc_processed_data_dir(session_key: dict) -> str
                    Optional function to retrive the desired output directory
                    for DeepLabCut files for a given session. If unspecified,
                    output stored in the session video folder, per DLC default
                    :return: a string for the absolute path of output directory
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module),\
        "The argument 'dependency' must be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    # activate
    schema.activate(dlc_schema_name, create_schema=create_schema,
                    create_tables=create_tables,
                    add_objects=_linking_module.__dict__)


# -------------- Functions required by the elements-ephys  ---------------

def get_dlc_root_data_dir() -> list:
    """
    It is recommended that all paths in DataJoint Elements stored as relative
    paths, with respect to some user-configured "root" director(y/ies). The
    root(s) may vary between data modalities and user machines

    get_dlc_root_data_dir() -> list
        This user-provided function retrieves the possible root data
        director(y/ies) containing continuous behavioral data for all subjects
        and sessions (e.g. acquired video or treadmill raw files)
        :return: a string for full path to the behavioral root data directory,
         or list of strings for possible root data directories
    """
    root_directories = _linking_module.get_dlc_root_data_dir()
    if isinstance(root_directories, (str, pathlib.Path)):
        root_directories = [root_directories]

    if hasattr(_linking_module, 'get_dlc_processed_data_dir'):
        root_directories.append(_linking_module.get_dlc_processed_data_dir())

    return root_directories


def get_session_directory(session_key: dict) -> str:
    """
    get_session_directory(session_key: dict) -> str
        Retrieve the session directory containing the
         recorded Neuropixels data for a given Session
        :param session_key: a dictionary of one Session `key`
        :return: a string for full path to the session directory
    """
    return _linking_module.get_session_directory(session_key)


def get_dlc_processed_data_dir() -> str:
    """
    If specified by the user, this function provides DeepLabCut with an output
    directory for processed files. If unspecified, output files will be stored
    in the session directory 'videos' folder, per DeepLabCut default

    get_dlc_processed_data_dir -> str
        This user-provided function specifies where DeepLabCut output files
        will be stores.
    """
    if hasattr(_linking_module, 'get_dlc_processed_data_dir'):
        return _linking_module.get_dlc_processed_data_dir()
    else:
        return get_ephys_root_data_dir()[0]


# ----------------------------- Table declarations ----------------------


@schema
class VideoRecording(dj.Manual):
    definition = """      
    -> Session
    -> Device
    recording_start_time: datetime
    """

    class File(dj.Part):
        definition = """
        -> master
        file_path: varchar(255)  # filepath of the video, relative to root data directory
        """


@schema
class ConfigParamSet(dj.Lookup):
    definition = """
    # Parameters to specify a DLC model training instance
    paramset_idx    : smallint
    ---
    shuffle         : int         # shuffle number to use (usually 1)
    train_fraction  : float       # training fraction
    filter_type=""  : varchar(16) # filter type, blank if none (e.g., median, arima)
    track_method="" : varchar(16) # tracking method, blank if none (e.g,. box, ellipse)
    scorer_legacy=0 : bool        # legacy naming for DLC < v2.1.0
    param_set_hash  : uuid        # hash identifying this parameterset
    unique index (param_set_hash)
    """


@schema
class TrainingTask(dj.Manual):
    definition = """                  # Info required to specify 1 model
    -> VideoRecording                 # labeled video for training
    -> ConfigParamSet
    training_id: int           
    """


@schema
class ModelTraining(dj.Computed):
    definition = """
    -> TrainingTask
    ---
    snapshot_index_exact  : int unsigned   # exact snapshot index (i.e., never -1)
    config_template : longblog       # stored full config file
    """

    """TODO: ingestion of config w/ understanding that
        config gets updated on snapshots"""

    def make(self, key):
        # command line to trigger a model training event
        # from jupyter notebook?
        raise NotImplementedError


@schema
class BodyPart(dj.Lookup):
    definition = """
    body_part: varchar(32)
    ---
    body_part_description='': varchar(1000)
    """


@schema
class Model(dj.Manual):
    definition = """
    model_name           : varchar(32) # user-friendly model name
    ---
    task                 : varchar(32)  # task in the config yaml
    date                 : varchar(16)  # date in the config yaml
    iteration            : int  # iteration/version of this model
    snapshotindex        : int  # which snapshot index used for prediction (if -1 then use the latest snapshot)
    shuffle              : int  # which shuffle of the training dataset used for training the network (typically 1)
    trainingsetindex     : int  # which training set fraction used to generate the model (typically 0)
    unique index (task, date, iteration, shuffle, trainingsetindex, snapshotindex)
    model                : varchar(64) # scorer/network name for a particular shuffle, training fraction etc. - DLC's GetScorerName()
    config_template      : longblob  # dictionary of the config yaml needed to run the deeplabcut.analyze_videos()
    model_description='' : varchar(1000)
    project_path         : varchar(255)  # relative path of the DLC project, appended to the root_dir to be used for the project_path var in the config.yaml
    -> [nullable] ModelTraining
    """

    class BodyPart(dj.Part):
        definition = """
        -> master
        -> BodyPart
        """


@schema
class PoseEstimationTask(dj.Computed):
    definition = """
    -> VideoRecording
    -> Model
    ---
    dlc_output_dir='': varchar(255)  # output directory of the DLC results relative to the root data directory
    task_mode='load': enum('load', 'trigger')  # 'load': load computed analysis results, 'trigger': trigger computation
    """


@schema
class PoseEstimation(dj.Computed):
    definition = """
    -> PoseEstimationTask
    ---
    post_estimation_time: datetime  # time of generation of this set of DLC results 
    """

    class BodyPartPosition(dj.Part):
        definition = """ # uses DeepLabCut h5 output for body part position
        -> master
        -> Model.BodyPart
        ---
        frame_index : longblob     # frame index in model
        x_pos       : longblob
        y_pos       : longblob
        z_pos=null  : longblob
        likelihood  : longblob
        """

    def make(self, key):
        from .readers import dlc

        task_mode, output_dir = (PoseEstimationTask & key).fetch1('task_mode', 'dlc_output_dir')
        dlc_model = (Model & key).fetch1()

        output_dir = find_full_path(get_dlc_root_data_dir(), output_dir)

        video_filepaths = [find_full_path(get_dlc_root_data_dir(), fp)
                           for fp in (VideoRecording.File & key).fetch('file_path')]

        project_path = find_full_path(get_dlc_root_data_dir(), dlc_model['project_path'])

        if task_mode == 'trigger':
            do_pose_estimation(video_filepaths, dlc_model, project_path, output_dir)

        dlc_result = dlc.PoseEstimation(output_dir)

        body_parts = [{**key,
                       'body_part': k,
                       'frame_index': np.arange(dlc_result.nframes),
                       'x_pos': v['x_pos'],
                       'y_pos': v['y_pos'],
                       'z_pos': v.get('z_pos'),
                       'likelihood': v['likelihood']}
                      for k, v in dlc_result.data.items()]

        self.insert1({**key, 'post_estimation_time': dlc_result.creation_time})
        self.BodyPartPosition.insert(body_parts)
