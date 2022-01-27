"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""

import datajoint as dj
from deeplabcut.pose_estimation_tensorflow import analyze_videos as dlc_analyze_videos
from deeplabcut.version import __version__ as dlc_version
import deeplabcut.utils.auxiliaryfunctions as dlc_aux
import importlib
import inspect
# import os
# import glob
# import shutil
# import pickle
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from element_interface.utils import find_full_path, dict_to_uuid

# set constant file paths (edit to where you want data to go):
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
                + get_beh_root_data_dir() -> list
                    Retrieve the root data director(y/ies) with behavioral
                    recordings for all subject/sessions.
                    :return: a string for full path to the root data directory
                + get_session_dir(session_key: dict) -> str
                    Retrieve the session directory containing the recording(s)
                    for a given Session
                    :param session_key: a dictionary of one Session `key`
                    :return: a string for full path to the session directory
                + get_beh_output_dir(session_key: dict) -> str
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

def get_beh_root_data_dir() -> list:
    """
    It is recommended that all paths in DataJoint Elements stored as relative
    paths, with respect to some user-configured "root" director(y/ies). The
    root(s) may vary between data modalities and user machines

    get_beh_root_data_dir() -> list
        This user-provided function retrieves the possible root data
        director(y/ies) containing continuous behavioral data for all subjects
        and sessions (e.g. acquired video or treadmill raw files)
        :return: a string for full path to the behavioral root data directory,
         or list of strings for possible root data directories
    """
    return _linking_module.get_beh_root_data_dir()


def get_session_dir(session_key: dict) -> str:
    """
    get_session_dir(session_key: dict) -> str
        Retrieve the session directory containing the recorded
        data for a given Session
        :param session_key: a dictionary of one Session `key`
        :return: a string for full path to the session directory
    """
    return _linking_module.get_session_dir(session_key)


def get_beh_output_dir(session_key: dict) -> str:
    """
    If specified by the user, this function provides DeepLabCut with an output
    directory for processed files. If unspecified, output files will be stored
    in the session directory 'videos' folder, per DeepLabCut default

    get_beh_output_dir -> str
        This user-provided function specifies where DeepLabCut output files
        will be stores.
    """
    if _linking_module.get_beh_output_dir(session_key):
        return _linking_module.get_beh_output_dir(session_key)
    else:
        return None

# ----------------------------- Table declarations ----------------------


@schema
class Recording(dj.Manual):
    definition = """          # DLC raw video filepath
    -> session.Session
    video_path : varchar(128) # raw video path relative to session_dir
    ---
    camera_id  : tinyint      # which camera
    """


@schema
class ConfigParamSet(dj.Lookup):
    definition = """
    # Parameters that uniquely identify a DLC model
    paramset_idx    : smallint
    ---
    shuffle         : int         # shuffle number to use (usually 1)
    train_fraction  : float       # training fraction
    snapshot_index  : int         # snapshot index, -1 for most recent
    filter_type=""  : varchar(16) # filter type, blank if none (e.g., median, arima)
    track_method="" : varchar(16) # tracking method, blank if none (e.g,. box, ellipse)
    scorer_legacy='False' : enum('True','False')  # legacy naming for DLC < v2.1.0
    param_set_hash  : uuid        # hash identifying this parameterset
    unique index (param_set_hash)
    """

    @classmethod
    def insert_new_params(cls, paramset_idx: int, shuffle: int, train_fraction: int,
                          snapshot_index: int, filter_type: str, track_method: str,
                          scorer_legacy=False, skip_duplicates=False):
        param_dict = {'paramset_idx': paramset_idx, 'shuffle': shuffle,
                      'train_fraction': train_fraction,
                      'snapshot_index': snapshot_index, 'filter_type': filter_type,
                      'track_method': track_method, 'scorer_legacy': scorer_legacy}

        param_set_hash = dict_to_uuid(param_dict)
        param_query = cls & {'param_set_hash': param_set_hash}

        if param_query:  # If the specified param-set already exists
            existing_paramset_idx = param_query.fetch1('paramset_idx')
            if skip_duplicates or existing_paramset_idx == paramset_idx:
                return  # If the existing set has the same paramset_idx: job done
            else:       # If not: human error adding same paramset with new index
                raise dj.DataJointError(
                    'The specified parameter set already exists - paramset_idx: '
                    + f'{existing_paramset_idx}')
        else:
            param_dict.update({'param_set_hash': param_set_hash})
            cls.insert1(param_dict, skip_duplicates=skip_duplicates)


@schema
class Config(dj.Manual):
    definition = """                  # Info required to specify 1 model
    -> Recording
    -> ConfigParamSet
    config_path       : varchar(1024) # config.yaml relative to session_dir
    ---
    config_notes=''   : varchar(1024)
    """


@schema
class Model(dj.Imported):
    definition = """
    -> Config
    ---
    task            : varchar(32) # task description
    scorer          : varchar(32) # scorer/network name in config, human labeler
    multianimal     : bool        # true for multi-animal
    iteration       : int         # iteration number
    pcutoff         : float       # threshold of likelihood
    model           : varchar(64) # DLC's GetScorerName()
    start_time      : datetime    # When the model started training
    run_duration    : float       # Seconds model run
    fps             : float       # Source video framerate, frames per second
    dlc_version     : varchar(8)  # keeps the deeplabcut version
    """

    class Data(dj.Part):
        definition = """ # uses DeepLabCut h5 output for body part position
        -> master
        joint_name  : varchar(64)  # Name of the joints
        ---
        frame_index : longblob     # frame index in model
        x_pos       : longblob
        y_pos       : longblob
        likelihood  : longblob
        """

    def make(self, key, skip_duplicates=False, ingest_data=True, analyze_videos=True):
        """
        Params maintained for testing only, to be removed after alpha
        :param skip_duplicates: Skip duplicates on insertion of master & part
        :param ingest_data: Ingest data from model. Set to False if unavailable
        :param analyze_videos: If no output exists, attempt to run DLC's analyze_videos
        """
        # ---------------------- Source video directory ----------------------
        session_dir_full = find_full_path(get_beh_root_data_dir(),
                                          get_session_dir(key))
        video_path_relative = Path((Recording & key).fetch1('video_path'))
        video_path = Path(session_dir_full, video_path_relative)

        # ------------------ Gather config file information ------------------
        config_path_full = Path(session_dir_full, key['config_path'])
        cfg = dlc_aux.read_config(config_path_full)
        cfg_paramset = (ConfigParamSet & key).fetch1()
        cfg.update(cfg_paramset)
        # Multianimal in the config may be blank if single-animal
        cfg['multianimalproject'] = bool(cfg['multianimalproject'])

        train_fraction = (ConfigParamSet & key).fetch1('train_fraction')
        if train_fraction not in cfg['TrainingFraction']:
            # Config lists fractions used. If user provided val not exist, raise Err
            raise FileNotFoundError(f'Training fraction {train_fraction} was not found '
                                    + f'in the config file\n{config_path_full}')
        cfg['train_fraction'] = train_fraction
        # GetScorerName() returns two model names [updated, legacy]
        scorer_legacy = 0 if ((ConfigParamSet & key).fetch1('scorer_legacy')
                              ) == 'False' else 1
        cfg['model'] = dlc_aux.GetScorerName(cfg, cfg['shuffle'],
                                             cfg['train_fraction'])[scorer_legacy]

        # ---------------------- Output directory/files ----------------------
        if get_beh_output_dir(key):
            output_dir = get_beh_output_dir(key)
        else:
            output_dir = video_path.parent
        # Standard DLC outputs: h5, meta.pickle
        try:
            dlc_output_h5, _, _ = dlc_aux.find_analyzed_data(
                folder=output_dir, videoname=video_path.stem, scorer=cfg['model'],
                filtered=False if len(cfg['filter_type']) == 0 else cfg['filter_type'],
                track_method=cfg['track_method'])
        except FileNotFoundError as err:
            print(f'{err}\nDataJoint will attempt to run the analysis...')
            if analyze_videos:
                try:
                    dlc_analyze_videos(config_path_full, [str(video_path)])
                except FileNotFoundError as err:
                    print(f'{err}\nDataJoint will continue to next ingestion...')
                    return  # Stop processing current key, continue to next
        dlc_meta_data = dlc_aux.load_video_metadata(folder=output_dir,
                                                    videoname=video_path.stem,
                                                    scorer=cfg['model'])['data']
        # Info in meta: start_time, stop_time, run_duration, batch_size,
        #               frame_dimensions, crop_bool, crop_param
        cfg['start_time'] = datetime.fromtimestamp(dlc_meta_data['start'])
        cfg['run_duration'] = dlc_meta_data['run_duration']
        cfg['fps'] = dlc_meta_data['fps']
        cfg['nframes'] = dlc_meta_data['nframes']

        # -------------- Insert into DataJoint dlc.Model table --------------
        self.insert1(dict(key,
                          task=cfg['Task'],
                          scorer=cfg['scorer'],
                          multianimal=cfg['multianimalproject'],
                          fps=cfg['fps'],
                          iteration=cfg['iteration'],
                          pcutoff=cfg['pcutoff'],
                          model=cfg['model'],
                          start_time=cfg['start_time'],
                          run_duration=cfg['run_duration'],
                          dlc_version=dlc_version,
                          ),
                     skip_duplicates=skip_duplicates)

        # ------------ Insert into DataJoint dlc.Model.Data table ------------
        if ingest_data:
            # Load h5 data. Future to do: swap pd for h5py?
            # CURRENTLY FAILS ON MULTIANIMAL. WOULD NEED TO LOOP THRU EACH ANIMAL
            # FOR MULTIANIMAL get_level_values(1) is animal name, (2) is bodypart
            dlc_data = pd.read_hdf(dlc_output_h5)
            body_parts = dlc_data.columns.get_level_values(1)
            _, idx = np.unique(body_parts, return_index=True)
            body_parts = body_parts[np.sort(idx)]
            # Precursor project inserted as numpy arrays, should future drafts
            # remove this dependency?

            for bp in body_parts:
                dlc_bp_data = dlc_data[cfg['model']][bp]
                self.Data.insert1(dict(key,
                                       joint_name=bp,
                                       frame_index=np.array(cfg['nframes']),
                                       x_pos=dlc_bp_data['x'].values,
                                       y_pos=dlc_bp_data['y'].values,
                                       likelihood=dlc_bp_data['likelihood'
                                                              ].values
                                       ),
                                  skip_duplicates=skip_duplicates)
            print('Populated Model and Data tables from: '
                  + f'{Path(dlc_output_h5).stem}\n')
        else:
            print(f'Populated Model table from: {Path(dlc_output_h5).stem}\n')

    def Get2DTrajectory(self, joint_name=[None]):
        """
        :param self: A query specifying one subject, else error is thrown.
                     Use primary keys to choose the model, version etc.
        :param joint_name: joint(s) as a list or None if all joints
        returns df: multi index dataframe with DLC scorer names, body_parts
                    and x/y coordinates of each joint name for a camera_id,
                    similar to output of DLC dataframe.
            e.g. df = (dlc.Model & "subject = 'subject5'"
                       & 'session_datetime > "2021-06-03"'
                       ).get2dJointsTrajectory('backhand')

        """
        model = np.unique(self.fetch('model'))[0]
        if joint_name is None:
            body_parts = self.Data().fetch('joint_name')
        else:
            body_parts = list(joint_name)
            dataFrame = None
        for bodypart in body_parts:
            x_pos = (self.Data() & ("joint_name='%s'" % bodypart)).fetch1('x_pos')
            y_pos = (self.Data() & ("joint_name='%s'" % bodypart)).fetch1('y_pos')
            likelihood = (self.Data() & ("joint_name='%s'" % bodypart)
                          ).fetch1('likelihood')
            a = np.vstack((x_pos, y_pos, likelihood))
            a = a.T
            pdindex = pd.MultiIndex.from_product([[model], [bodypart],
                                                 ['x', 'y', 'likelihood']],
                                                 names=['scorer', 'body_parts',
                                                        'coords'])
            frame = pd.DataFrame(a, columns=pdindex,
                                 index=range(0, a.shape[0]))
            dataFrame = pd.concat([dataFrame, frame], axis=1)
            return(dataFrame)


'''
@schema
class 3DModel(dj.Manual):
    definition = """
    # Keeps the model info for 3D DeepLabCut pose estimation
    # Training index and shuffle numbers pased as lists (e.g.[0,0] or [1,1])
    -> session.Session
    config_path     : varchar(1024) # path project config in deeplabcut_weights
    scorer          : varchar(512)  # scorer/network name for 3d project.
    pcutoff         : float         # specifies threshold of the likelihood
    ---
    trainingindex   : longblob      # index of Training fract for each camera
    shuffle         : longblob      # shuffle #s for each camera
    """


@schema
class DeepLabCut3D(dj.Computed):
    definition = """ # uses DLC to extract the 3D position of the body_parts.
    -> DLC3DModel
    version         : varchar(8) # keeps the deeplabcut version
    joint_name      : varchar(512) # Name of the joints
    ---
    x_pos           : longblob
    y_pos           : longblob
    z_pos           : longblob
    """

    def make(self,  key):
        videos = (DLCRecording() & key).fetch('video_path')
        cfg3d = key['config_path']
        model = key['scorer']
        try:
            deeplabcut.triangulate(cfg3d, [videos], destfolder=save_dlc_path)
            string_to_search = str('*mouse-'+key['mouse_name']+'_day-'
                                   + str(key['day'])+'_attempt-'
                                   + str(key['attempt'])
                                   + '*' + key['scorer']+'.h5')
            dlc_output_h5_filename = glob.glob(os.path.join(save_dlc_path,
                                                           string_to_search)
                                              )[0]
            df = pd.read_hdf(dlc_output_h5_filename, 'df_with_missing')
            body_parts = df.columns.get_level_values(1)
            _, idx = np.unique(body_parts, return_index=True)
            body_parts = body_parts[np.sort(idx)]
            dlc_data = key.copy()
            dlc_data['version'] = deeplabcut.__version__
            for bp in body_parts:
                dlc_data['joint_name'] = bp
                dlc_data['x_pos'] = dlc_data[model][bp]['x'].values
                dlc_data['y_pos'] = dlc_data[model][bp]['y'].values
                dlc_data['z_pos'] = dlc_data[model][bp]['z'].values
                self.insert1(dlc_data)

            print("\n")
            print(f'Populated 3D data from {key}')
            print("mouse = %s // day = %d // attempt = %d" %
                  (key['mouse_name'], key['day'], key['attempt']))
        except FileNotFoundError:
            print(f'No videos found for {key}')

    def get3dJointsTrajectory(self, joint_name=[None]):
        """
        :param self: query identifying one mouse
                    Use primary keys to choose right scorer or version etc.
        :param joint_name: joint(s) as a list or None if all joints
        returns df: multi index dataframe with scorer names, body_parts
                    and x, y, z coordinates of each joint name,
                    similar to output of DLC dataframe.
            e.g. df = (dlc.DeepLabCut3D() & "mouse_name= 'Xerus'" & 'day=2'
                       & 'attempt=1').get3dJointsTrajectory(None)

        """
        scorer = np.unique(self.fetch('scorer'))[0]
        if joint_name[0] is None:
            body_parts = self.fetch('joint_name')
        else:
            body_parts = list(joint_name)

        dataFrame = None
        for bodypart in body_parts:
            x_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('x_pos')
            y_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('y_pos')
            z_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('z_pos')
        a = np.vstack((x_pos, y_pos, z_pos))
        a = a.T
        pdindex = pd.MultiIndex.from_product(
                  [[scorer], [bodypart], ['x', 'y', 'z']],
                  names=['scorer', 'body_parts', 'coords'])
        frame = pd.DataFrame(a, columns=pdindex,
                             index=range(0, a.shape[0]))
        dataFrame = pd.concat([dataFrame, frame], axis=1)
        return(dataFrame)
'''
