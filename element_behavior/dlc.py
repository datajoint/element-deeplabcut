"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""

import datajoint as dj
from pathlib import Path
import deeplabcut
import os
import glob
import shutil
import pandas as pd
import numpy as np
from . import treadmill
import importlib
import inspect
# from element_data_loader.utils import find_root_directory, find_full_path

# set constant file paths (edit to where you want data to go):
save_dlc_path = Path('/data/processeddata/deeplabcut2.0_analysed')
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
                + Session: parent table to ProbeInsertion, typically
                           identifying a recording session.
            Functions:
                + get_trial_root_dir() -> list
                    Retrieve the root data director(y/ies) with behavioral
                    recordings (e.g., bpod files) for all subject/sessions.
                    :return: a string for full path to the root data directory
                + get_trial_sess_dir(session_key: dict) -> str
                    Retrieve the session directory containing the recording(s)
                    for a given Session
                    :param session_key: a dictionary of one Session `key`
                    :return: a string for full path to the session directory
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


def get_session_directory(session_key: dict) -> str:
    """
    get_session_directory(session_key: dict) -> str
        Retrieve the session directory containing the
         recorded Neuropixels data for a given Session
        :param session_key: a dictionary of one Session `key`
        :return: a string for full path to the session directory
    """
    return _linking_module.get_session_directory(session_key)


def get_beh_root_output_dir():
    """
    If specified by the user, this function provides DeepLabCut with an output
    directory for processed files. If unspecified, output files will be stored
    in the relevant session directory.

    get_beh_root_output_dir -> str
        This user-provided function
    """
    if _linking_module.get_beh_root_output_dir():
        return _linking_module.get_beh_root_output_dir()
    else:
        return None

# ----------------------------- Table declarations ----------------------

@schema
class DLCModel(dj.Manual):
    definition = """             # Keeps the model title to use for prediction
    -> exp.RawVideo
    config_path  : varchar(1024) # path config file be in dlc weights folder
    iteration    : int           # iteration number
    shuffle      : int           # shuffle number to use (usually 1)
    trainingindex: int           # index of the Training fraction to use
    scorer       : varchar(512)  # scorer/network name
    pcutoff      : float         # specifies threshold of the likelihood
    """


@schema
class DeepLabCut(dj.Computed):
    definition = """ # uses DeepLabCut to extract the position of the bodyparts.
    -> DLCModel
    version            : varchar(8) # keeps the deeplabcut version
    joint_name          : varchar(512) # Name of the joints
    ---
    x_pos                : longblob
    y_pos                : longblob
    likelihood          : longblob
    time             : longblob   # time in session for each frame
    """

    def make(self,  key):

        import deeplabcut
        import deeplabcut.utils.auxiliaryfunctions as dlc_aux

        video_path = (exp.RawVideo() & key).fetch1('video_path')
        video_path = Path(video_path)
        cfg = dlc_aux.read_config(key['config_path'])
        # cfg['iteration'] = key['iteration']
        cfg_tmp = key['config_path'].replace('.yaml', '_tmp.yaml')
        dlc_aux.write_config(cfg_tmp, cfg)
        model = dlc_aux.GetScorerName(cfg, key['shuffle'],
                                      cfg['TrainingFraction'][0])

        # analyze video
        dlc_output_h5 = video_path.parent / Path(str(video_path.stem) + model
                                                 + '.h5')
        dj_output_h5 = os.path.join(str(save_dlc_path),
                                    str(str(video_path.stem)
                                        + model + '.h5'))
        dlc_output_pickle = dlc_output_h5.parent / \
            Path(str(dlc_output_h5.stem) + 'includingmetadata.pickle')
        if not os.path.isfile(dj_output_h5):
            deeplabcut.analyze_videos(cfg_tmp, [str(video_path)])
        if os.path.isfile(dlc_output_h5):
            shutil.move(dlc_output_h5, dj_output_h5)
        if os.path.isfile(dlc_output_pickle):
            os.remove(dlc_output_pickle)
        if os.path.isfile(cfg_tmp):
            os.remove(cfg_tmp)

        df = pd.read_hdf(dj_output_h5, 'df_with_missing')
        bodyParts = df.columns.get_level_values(1)
        _, idx = np.unique(bodyParts, return_index=True)
        bodyParts = bodyParts[np.sort(idx)]
        frame_times = np.load((exp.RawVideo()
                               & key).fetch1('camera_timestamps_path'))
        tuple_ = key.copy()
        tuple_['version'] = deeplabcut.__version__
        tuple_['time'] = frame_times
        for bp in bodyParts:
            tuple_['joint_name'] = bp
            tuple_['x_pos'] = df[model][bp]['x'].values
            tuple_['y_pos'] = df[model][bp]['y'].values
            tuple_['likelihood'] = df[model][bp]['likelihood'].values
            self.insert1(tuple_)

        print("\n")
        print("Populated DeepLabCut data from:")
        print("mouse = %s // day = %d // attempt = %d // video = %s" %
              (key['mouse_name'], key['day'],
               key['attempt'], key['camera_id']))
        print("\n")

    def get2dJointsTrajectory(self, joint_name=[None]):
        """
            :param self: A query specifying one subject, else error is thrown.
                         Use primary keys to choose the scorer, version etc.
            :param camera_id: camera index as an integer 1 or 2.
                              1 is side camera and 2 is front camera
            :param joint_name: joint(s) as a list or None if all joints
            returns df: multi index dataframe with scorer names, bodyparts
                        and x/y coordinates of each joint name for a camera_id,
                        similar to output of DLC dataframe.
                e.g. df = (dlc.DeepLabCut3D() & "mouse_name= 'Xerus'" & 'day=2'
                           & 'attempt=1' & "camera_id = 1"
                           ).get2dJointsTrajectory('backhand')

        """
        scorer = np.unique(self.fetch('scorer'))[0]
        if joint_name is None:
            bodyparts = self.fetch('joint_name')
        else:
            bodyparts = list(joint_name)
            dataFrame = None
        for bodypart in bodyparts:
            x_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('x_pos')
            y_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('y_pos')
            likelihood = (self & ("joint_name='%s'" % bodypart)
                          ).fetch1('likelihood')
            a = np.vstack((x_pos, y_pos, likelihood))
            a = a.T
            pdindex = pd.MultiIndex.from_product([[scorer], [bodypart],
                                                 ['x', 'y', 'likelihood']],
                                                 names=['scorer', 'bodyparts',
                                                        'coords'])
            frame = pd.DataFrame(a, columns=pdindex,
                                 index=range(0, a.shape[0]))
            dataFrame = pd.concat([dataFrame, frame], axis=1)
            return(dataFrame)


@schema
class DLC3DModel(dj.Manual):
    definition = """ # Keeps the model info for 3D DeepLabCut pose estimation
    -> exp.Session
    config_path     : varchar(1024) # path of 3d project config file in deeplabcut_weights folder
    scorer          : varchar(512)  # scorer/network name for 3d project.
    pcutoff         : float         # specifies threshold of the likelihood
    """
    # trainingindex : longblob      # index of the Training fraction to use for each camera. Pass as list e.g.[0,0]
    # shuffle       : longblob      # shuffle #s for each camera. Pass as list e.g.[1,1]


@schema
class DeepLabCut3D(dj.Computed):
    definition = """ # uses DeepLabCut to extract the 3D position of the bodyparts.
    -> DLC3DModel
    version              : varchar(8) # keeps the deeplabcut version
    joint_name          : varchar(512) # Name of the joints
    ---
    x_pos              : longblob
    y_pos              : longblob
    z_pos              : longblob
    """

    def make(self,  key):
        videos = (exp.RawVideo() & key).fetch('video_path')
        cfg3d = key['config_path']
        model = key['scorer']
        try:
            deeplabcut.triangulate(cfg3d, [videos], destfolder=save_dlc_path)
            string_to_search = str('*mouse-'+key['mouse_name']+'_day-'
                                   + str(key['day'])+'_attempt-'
                                   + str(key['attempt'])
                                   + '*' + key['scorer']+'.h5')
            dj_output_h5_filename = glob.glob(os.path.join(save_dlc_path,
                                                           string_to_search)
                                              )[0]
            df = pd.read_hdf(dj_output_h5_filename, 'df_with_missing')
            bodyParts = df.columns.get_level_values(1)
            _, idx = np.unique(bodyParts, return_index=True)
            bodyParts = bodyParts[np.sort(idx)]
            tuple_ = key.copy()
            tuple_['version'] = deeplabcut.__version__
            for bp in bodyParts:
                tuple_['joint_name'] = bp
                tuple_['x_pos'] = df[model][bp]['x'].values
                tuple_['y_pos'] = df[model][bp]['y'].values
                tuple_['z_pos'] = df[model][bp]['z'].values
                self.insert1(tuple_)

            print("\n")
            print("Populated 3D data from:")
            print("mouse = %s // day = %d // attempt = %d" %
                  (key['mouse_name'], key['day'], key['attempt']))
            print("\n")
        except FileNotFoundError:
            print("No videos found for mouse %s day %s and attempt %s "
                  % (key['mouse_name'], str(key['day']), str(key['attempt'])))

        def get3dJointsTrajectory(self, joint_name=[None]):
            """
            :param self: query identifying one mouse
                        Use primary keys to choose right scorer or version etc.
            :param joint_name: joint(s) as a list or None if all joints
            returns df: multi index dataframe with scorer names, bodyparts
                        and x, y, z coordinates of each joint name,
                        similar to output of DLC dataframe.
                e.g. df = (dlc.DeepLabCut3D() & "mouse_name= 'Xerus'" & 'day=2'
                           & 'attempt=1').get3dJointsTrajectory(None)

            """
            scorer = np.unique(self.fetch('scorer'))[0]
            if joint_name[0] is None:
                bodyparts = self.fetch('joint_name')
            else:
                bodyparts = list(joint_name)

            dataFrame = None
            for bodypart in bodyparts:
                x_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('x_pos')
                y_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('y_pos')
                z_pos = (self & ("joint_name='%s'" % bodypart)).fetch1('z_pos')
            a = np.vstack((x_pos, y_pos, z_pos))
            a = a.T
            pdindex = pd.MultiIndex.from_product(
                      [[scorer], [bodypart], ['x', 'y', 'z']],
                      names=['scorer', 'bodyparts', 'coords'])
            frame = pd.DataFrame(a, columns=pdindex,
                                 index=range(0, a.shape[0]))
            dataFrame = pd.concat([dataFrame, frame], axis=1)
            return(dataFrame)
