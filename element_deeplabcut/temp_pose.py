"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""

import datajoint as dj
import importlib
import inspect
import numpy as np
from pathlib import Path
import pathlib
from element_interface.utils import find_full_path, find_root_directory
from datetime import datetime


schema = dj.schema()
_linking_module = None


def activate(dlc_schema_name, *, create_schema=True, create_tables=True,
             linking_module=None):
    """
    activate(schema_name, *, create_schema=True, create_tables=True,
             linking_module=None)
        :param schema_name: schema name on the database server to activate the
                            `deeplabcut` element

        :param create_schema: when True (default), create schema in the database if it
                              does not yet exist.
        :param create_tables: when True (default), create schema in the database if it
                              does not yet exist.
        :param linking_module: a module (or name) containing the required dependencies
                               to activate the `session` element:
        Upstream tables:
            + Session: parent table to VideoRecording, identifying a recording session
            + Device: parent table to VideoRecording, identifying video recording device
        Functions:
            + get_dlc_root_data_dir() -> list Retrieve the root data director(y/ies)
                with behavioral recordings for all subject/sessions.
                :return: a string for full path to the root data directory
            + get_dlc_processed_data_dir(session_key: dict) -> str
                Optional function to retrive the desired output directory for DeepLabCut
                files for a given session. If unspecified,
                output stored in the session video folder, per DLC default
                :return: a string for the absolute path of output directory
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module),\
        "The argument 'dependency' must be a module's name or a module"
    assert hasattr(linking_module, 'get_dlc_root_data_dir'),\
        "The linking module must specify a lookup funtion for a root data directory"

    global _linking_module
    _linking_module = linking_module

    # activate
    schema.activate(dlc_schema_name, create_schema=create_schema,
                    create_tables=create_tables,
                    add_objects=_linking_module.__dict__)


# -------------- Functions required by element-deeplabcut ---------------

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
    if isinstance(root_directories, (str, Path)):
        root_directories = [root_directories]

    if hasattr(_linking_module, 'get_dlc_processed_data_dir'):
        root_directories.append(_linking_module.get_dlc_processed_data_dir())

    return root_directories


def get_dlc_processed_data_dir() -> str:
    """
    If specified by the user, this function provides DeepLabCut with an output
    directory for processed files. If unspecified, output files will be stored
    in the session directory 'videos' folder, per DeepLabCut default

    get_dlc_processed_data_dir -> str
        This user-provided function specifies where DeepLabCut output files
        will be stored.
    """
    if hasattr(_linking_module, 'get_dlc_processed_data_dir'):
        return _linking_module.get_dlc_processed_data_dir()
    else:
        return get_dlc_root_data_dir()[0]


# ----------------------------- Table declarations ----------------------

@schema
class EstimationTask(dj.Manual):
    definition = """
    -> VideoRecording                           # Session -> Recording + File part table
    -> model.Model                              # Must specify a DLC project_path
    ---
    task_mode='load' : enum('load', 'trigger')  # load results or trigger computation
    pose_estimation_output_dir='': varchar(255) # output dir relative to the root dir
    pose_estimation_params=null  : longblob     # analyze_videos params, if not default
    """

    @classmethod
    def infer_output_dir(cls, key, relative=False, mkdir=False):
        """ Return the expected pose_estimation_output_dir based on the convention
                 / video_dir / device_{}_recording_{}_model_{}
        Spaces in model name are replaced with hyphens
        :param key: key specifying a pairing of VideoRecording and Model
        :param relative: report directory relative to get_dlc_processed_data_dir()
        :param mkdir: default False, make directory if it doesn't exist
        """
        processed_dir = pathlib.Path(get_dlc_processed_data_dir())
        video_filepath = find_full_path(get_dlc_root_data_dir(),
                                        (_linking_module.VideoRecording.File & key
                                         ).fetch('file_path', limit=1)[0])
        root_dir = find_root_directory(get_dlc_root_data_dir(), video_filepath.parent)
        device = '-'.join(str(v) for v in (_linking_module.Device & key
                                           ).fetch1('KEY').values())
        output_dir = (processed_dir
                      / video_filepath.parent.relative_to(root_dir)
                      / (f'device_{device}_recording_{key["recording_id"]}_model_'
                         + key["model_name"].replace(" ", "-"))
                      )
        if mkdir:
            output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir.relative_to(processed_dir) if relative else output_dir

    @classmethod
    def insert_estimation_task(cls, key, task_mode='trigger', params: dict = None,
                               relative=True, mkdir=True, skip_duplicates=False):
        """ Insert EstimationTask with inferred output dir based on the convention
                processed_dir / video_dir / device_{}_recording_{}_model_{}
        :param key: key specifying a pairing of VideoRecording and Model
        :param task_mode: default 'trigger' computation. Or 'load' existing results
        :param params: DLC's analyze_videos parameters if other than the defaults:
            videotype, gputouse, save_as_csv, batchsize, cropping, TFGPUinference,
            dynamic, robust_nframes, allow_growth, use_shelve
        :param relative: report directory relative to get_dlc_processed_data_dir()
        :param mkdir: default False, make directory if it doesn't exist
        """
        output_dir = cls.infer_output_dir(key, relative=relative, mkdir=mkdir)

        cls.insert1({**key, 'task_mode': task_mode,
                     'pose_estimation_params': params,
                     'pose_estimation_output_dir': output_dir},
                    skip_duplicates=skip_duplicates)


@schema
class Estimation(dj.Computed):
    definition = """
    -> EstimationTask
    ---
    post_estimation_time: datetime  # time of generation of this set of DLC results
    """

    class BodyPartPosition(dj.Part):
        definition = """ # uses DeepLabCut h5 output for body part position
        -> master
        -> model.BodyPart
        ---
        frame_index : longblob     # frame index in model
        x_pos       : longblob
        y_pos       : longblob
        z_pos=null  : longblob
        likelihood  : longblob
        """

    def make(self, key):
        """.populate() method will launch training for each EstimationTask
        """
        from .readers import dlc_reader

        # ID model and directories
        dlc_model = (_linking_module.model.Model & key).fetch1()
        assert dlc_model['project_path'], ("Your model table must have a 'project_path'"
                                           + "field pointing to a DLC directory")
        task_mode, analyze_video_params, output_dir = (
            EstimationTask & key).fetch1('task_mode', 'pose_estimation_params',
                                         'pose_estimation_output_dir')
        analyze_video_params = analyze_video_params or {}
        output_dir = find_full_path(get_dlc_root_data_dir(), output_dir)
        video_filepaths = [find_full_path(get_dlc_root_data_dir(), fp).as_posix()
                           for fp in (_linking_module.VideoRecording.File & key
                                      ).fetch('file_path')]
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      dlc_model['project_path'])

        # Triger estimation,
        if task_mode == 'trigger':
            dlc_reader.do_pose_estimation(video_filepaths, dlc_model, project_path,
                                          output_dir, **analyze_video_params)
        dlc_result = dlc_reader.PoseEstimation(output_dir)
        creation_time = datetime.fromtimestamp(dlc_result.creation_time
                                               ).strftime('%Y-%m-%d %H:%M:%S')

        body_parts = [{**key,
                       'body_part': k,
                       'frame_index': np.arange(dlc_result.nframes),
                       'x_pos': v['x'],
                       'y_pos': v['y'],
                       'z_pos': v.get('z'),
                       'likelihood': v['likelihood']}
                      for k, v in dlc_result.data.items()]

        self.insert1({**key, 'post_estimation_time': creation_time})
        self.BodyPartPosition.insert(body_parts)

    @classmethod
    def get_trajectory(cls, key, body_parts='all'):
        """
        Returns a pandas dataframe of x, y and z coordinates of the specified body_parts
        :param key: A query specifying one Estimation entry, else error is thrown.
        :param body_parts: optional, body parts as a list. If none, all joints
        returns df: multi index pandas dataframe with DLC scorer names, body_parts
                    and x/y coordinates of each joint name for a camera_id,
                    similar to output of DLC dataframe. If 2D, z is set of zeros
        """
        import pandas as pd
        model_name = key['model_name']
        if body_parts == 'all':
            body_parts = (cls.BodyPartPosition & key).fetch('body_part')
        else:
            body_parts = list(body_parts)

        df = None
        for body_part in body_parts:
            x_pos, y_pos, z_pos, likelihood = (cls.BodyPartPosition
                                               & {'body_part': body_part}).fetch1(
                                               'x_pos', 'y_pos', 'z_pos', 'likelihood')
            if not z_pos:
                z_pos = np.zeros_like(x_pos)

            a = np.vstack((x_pos, y_pos, z_pos, likelihood))
            a = a.T
            pdindex = pd.MultiIndex.from_product([[model_name], [body_part],
                                                 ['x', 'y', 'z', 'likelihood']],
                                                 names=['scorer', 'bodyparts',
                                                        'coords'])
            frame = pd.DataFrame(a, columns=pdindex, index=range(0, a.shape[0]))
            df = pd.concat([df, frame], axis=1)
        return df
