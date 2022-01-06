"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""

import datajoint as dj
import deeplabcut
import deeplabcut.utils.auxiliaryfunctions as dlc_aux
import importlib
import inspect
import os
import glob
import shutil
import pandas as pd
import numpy as np
from pathlib import Path
from . import treadmill
from element_data_loader.utils import find_full_path

# set constant file paths (edit to where you want data to go):
schema = dj.schema()
_linking_module = None


def activate(dlc_schema_name, treadmill_schema_name=None, *,
             create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, *, create_schema=True, create_tables=True,
             linking_module=None)
        :param schema_name: schema name on the database server to activate
                            the `behavior` element
        :param create_schema: when True (default), create schema in the
                              database if it does not yet exist.
        :param create_tables: when True (default), create tables in the
                              database if they do not yet exist.
        :param linking_module: a module (or name) containing the required
                               dependencies to activate the `session` element:
            Upstream tables:
                + Session: parent table to DLCRecording, identifying a
                           recording session.
            Functions:
                + get_beh_root_dir() -> list
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
    if treadmill_schema_name is not None:
        treadmill.activate(treadmill_schema_name,
                           create_schema=create_schema,
                           create_tables=create_tables)
    schema.activate(dlc_schema_name, create_schema=create_schema,
                    create_tables=create_tables,
                    add_objects=_linking_module.__dict__)


# -------------- Functions required by the elements-ephys  ---------------

def get_beh_root_dir() -> list:
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
    return _linking_module.get_session_directory(session_key)


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
class DLCRecording(dj.Manual):
    definition = """ # DLC raw video filepath
    -> session.Session
    video_path : varchar(128) # raw video path relative to session_dir
    ---
    camera_id  : tinyint      # which camera
    frame_rate : float        # fps, Hz
    """


@schema
class DLCModel(dj.Manual):
    definition = """
    model_name    : varchar(32)   # user-friendly model name
    config_path   : varchar(1024) # path to model config from output directory
    ---
    -> DLCRecording
    iteration     : int           # iteration number
    shuffle       : int           # shuffle number to use (usually 1)
    train_index   : int           # 0-indexed Training fraction to use
    """


@schema
class DeepLabCut(dj.Computed):
    definition = """ # uses DeepLabCut to extract the position of the body_parts
    -> DLCModel
    version          : varchar(8)   # keeps the deeplabcut version
    joint_name       : varchar(512) # Name of the joints
    frame_index      : int          # frame index in model
    ---
    x_pos            : longblob
    y_pos            : longblob
    likelihood       : longblob
    """

    def make(self,  key):
        video_path_relative = Path(DLCRecording() & key).fetch1('video_path')
        video_path = find_full_path(get_beh_root_data_dir(),
                                    video_path_relative)

        # Gather config file information
        cfg = dlc_aux.read_config(key['config_path'])
        cfg['iteration'] = key['iteration']
        cfg_backup = key['config_path'].replace('.yaml', '_backup.yaml')
        dlc_aux.write_config(cfg_backup, cfg)

        # GetScorerName() returns two names [updated, legacy]
        model = dlc_aux.GetScorerName(cfg, key['shuffle'],
                                      cfg['TrainingFraction']\
                                      [key['train_index']])[0]

        # Set output directory if function is available
        if get_beh_output_dir(key) is not None:
            output_dir = get_beh_output_dir(key)
        else:
            output_dir = video_path.parent
        # Standard DLC outputs: h5, meta.pickle
        dlc_output_h5 = Path(output_dir, video_path.stem + model + '.h5')
        dlc_output_pickle = dlc_output_h5.parent / \
                            Path(str(dlc_output_h5.stem) + '_meta.pickle')

        # If h5 not exist, run DLC and remove config backup
        if not os.path.isfile(dlc_output_h5):
            deeplabcut.analyze_videos(cfg_backup, [str(video_path)])
        if os.path.isfile(cfg_backup):
            os.remove(cfg_backup)

        # Load h5 data
        dlc_data = pd.read_hdf(dlc_output_h5)
        body_parts = dlc_data.columns.get_level_values(1)
        _, idx = np.unique(body_parts, return_index=True)
        body_parts = body_parts[np.sort(idx)]

        dlc_insert = key.copy()
        dlc_insert['version'] = deeplabcut.__version__
        dlc_insert['frame_index'] = dlc_data.index
        for bp in body_parts:
            dlc_insert['joint_name'] = bp
            dlc_insert['x_pos'] = df[model][bp]['x'].values
            dlc_insert['y_pos'] = df[model][bp]['y'].values
            dlc_insert['likelihood'] = df[model][bp]['likelihood'].values
            self.insert1(dlc_insert)

        print(f'\nPopulated DeepLabCut data from: {key}\n')
'''
    def get2dJointsTrajectory(self, joint_name=[None]):
        """
        :param self: A query specifying one subject, else error is thrown.
                     Use primary keys to choose the scorer, version etc.
        :param camera_id: camera index as an integer 1 or 2.
                          1 is side camera and 2 is front camera
        :param joint_name: joint(s) as a list or None if all joints
        returns df: multi index dataframe with scorer names, body_parts
                    and x/y coordinates of each joint name for a camera_id,
                    similar to output of DLC dataframe.
            e.g. df = (dlc.DeepLabCut3D() & "mouse_name= 'Xerus'" & 'day=2'
                       & 'attempt=1' & "camera_id = 1"
                       ).get2dJointsTrajectory('backhand')

        """
        scorer = np.unique(self.fetch('scorer'))[0]
        if joint_name is None:
            body_parts = self.fetch('joint_name')
        else:
            body_parts = list(joint_name)
            dataFrame = None
        for bodypart in body_parts:
            x_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('x_pos')
            y_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('y_pos')
            likelihood = (self & ("joint_name='%s'" % bodypart)
                          ).fetch1('likelihood')
            a = np.vstack((x_pos, y_pos, likelihood))
            a = a.T
            pdindex = pd.MultiIndex.from_product([[scorer], [bodypart],
                                                 ['x', 'y', 'likelihood']],
                                                 names=['scorer', 'body_parts',
                                                        'coords'])
            frame = pd.DataFrame(a, columns=pdindex,
                                 index=range(0, a.shape[0]))
            dataFrame = pd.concat([dataFrame, frame], axis=1)
            return(dataFrame)


@schema
class DLC3DModel(dj.Manual):
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
    definition = """ # uses DeepLabCut to extract the 3D position of the body_parts.
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
            dlc_insert = key.copy()
            dlc_insert['version'] = deeplabcut.__version__
            for bp in body_parts:
                dlc_insert['joint_name'] = bp
                dlc_insert['x_pos'] = df[model][bp]['x'].values
                dlc_insert['y_pos'] = df[model][bp]['y'].values
                dlc_insert['z_pos'] = df[model][bp]['z'].values
                self.insert1(dlc_insert)

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
