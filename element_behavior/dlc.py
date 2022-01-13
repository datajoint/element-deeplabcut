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
# import glob
# import shutil
import pickle
from datetime import datetime
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

    get_beh_root_dir() -> list
        This user-provided function retrieves the possible root data
        director(y/ies) containing continuous behavioral data for all subjects
        and sessions (e.g. acquired video or treadmill raw files)
        :return: a string for full path to the behavioral root data directory,
         or list of strings for possible root data directories
    """
    return _linking_module.get_beh_root_dir()


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
    frame_rate : float        # fps, Hz
    """


@schema
class Config(dj.Manual):
    definition = """                 # Info required to specify 1 model
    -> Recording
    config_path      : varchar(1024) # config.yaml relative to session_dir
    shuffle=1        : int           # shuffle number to use (usually 1)
    train_index=0    : int           # train fract of those in yaml, 0-indexed
    snapshot_index=-1: int           # snapshot index, -1 for most recent
    ---
    config_notes=''  : varchar(1024)
    """


@schema
class Model(dj.Imported):
    definition = """
    -> Config
    ---
    task            : varchar(32) # task description
    scorer          : varchar(32) # scorer/network name in config
    multianimal     : bool        # true for multi-animal
    train_fraction  : float       # training fraction specified by train_index
    iteration       : int         # iteration number
    pcutoff         : float       # threshold of likelihood
    model           : varchar(64) # DLC's updated GetScorerName()
    start_time      : datetime    # When the model started training
    run_duration    : float       # Seconds model run
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

    def make(self, key, skip_duplicates=False, ingest_data=True):
        """
        :param skip_duplicates: Skip duplicates on insertion of master & part
        :param ingest_data: Ingest data from model. Set to False if unavailable
        """
        # ---------------------- Source video directory ----------------------
        session_dir_full = find_full_path(get_beh_root_dir(),
                                          get_session_dir(key))
        video_path_relative = Path((Recording & key).fetch1('video_path'))
        video_path = Path(session_dir_full, video_path_relative)

        # ------------------ Gather config file information ------------------
        config_path_full = Path(session_dir_full, key['config_path'])
        cfg = dlc_aux.read_config(config_path_full)
        cfg_backup = str(config_path_full).replace('.yaml', '_backup.yaml')
        dlc_aux.write_config(Path(cfg_backup), cfg)
        cfg_adds = ['shuffle', 'train_index', 'snapshot_index']
        cfg.update({item: key[item] for item in cfg_adds})
        # Multianimal in the config may be blank if single-animal
        cfg['multianimalproject'] = bool(cfg['multianimalproject'])
        # Of train_fractions listed, selected the indexed one
        cfg['train_fraction'] = cfg['TrainingFraction'][key['train_index']]

        # GetScorerName() returns two model names [*updated*, legacy]
        cfg['model'] = dlc_aux.GetScorerName(cfg, cfg['shuffle'],
                                             cfg['train_fraction'])[0]

        # ---------------------- Output directory/files ----------------------
        if get_beh_output_dir(key) is not None:
            output_dir = get_beh_output_dir(key)
        else:
            output_dir = video_path.parent
        # Standard DLC outputs: h5, meta.pickle
        dlc_output_h5 = Path(output_dir, video_path.stem
                             + cfg['model'] + '.h5')
        dlc_output_pickle = Path(str(dlc_output_h5.parent),
                                 str(dlc_output_h5.stem + '_meta.pickle'))
        with open(dlc_output_pickle, 'rb') as f:
            dlc_meta_data = pickle.load(f)['data']
        # Info in meta: start_time, stop_time, run_duration, fps,
        #               batch_size, frame_dimensions, crop_bool, crop_param
        cfg['start_time'] = datetime.fromtimestamp(dlc_meta_data['start'])
        cfg['run_duration'] = dlc_meta_data['run_duration']
        cfg['nframes'] = dlc_meta_data['nframes']

        # If outputh5 not exist, run DLC and remove config backup
        if not os.path.isfile(dlc_output_h5):
            dlc_h5_basename = os.path.basename(dlc_output_h5)
            if dj.utils.user_choice(f'{dlc_h5_basename} not found. Analyze '
                                    + 'videos?', default='no') == 'yes':
                try:
                    deeplabcut.analyze_videos(cfg_backup, [str(video_path)])
                # If model hasn't been trained, dlc FileNotFoundError
                except FileNotFoundError as err:
                    if dj.utils.user_choice(f'{err}\n Proceed with DataJoint '
                                            + 'model ingestion?', default='no'
                                            ) != 'yes':
                        # Should stop processing current key, continue to next
                        return
                    else:
                        # Can ingest model, but will need to skip data
                        ingest_data = False
        if os.path.isfile(cfg_backup):
            os.remove(cfg_backup)

        # -------------- Insert into DataJoint dlc.Model table --------------
        self.insert1(dict(key,
                          task=cfg['Task'],
                          scorer=cfg['scorer'],
                          multianimal=cfg['multianimalproject'],
                          train_fraction=cfg['train_fraction'],
                          iteration=cfg['iteration'],
                          pcutoff=cfg['pcutoff'],
                          model=cfg['model'],
                          start_time=cfg['start_time'],
                          run_duration=cfg['run_duration'],
                          dlc_version=deeplabcut.__version__,
                          ),
                     skip_duplicates=skip_duplicates)

        # ------------ Insert into DataJoint dlc.Model.Data table ------------
        if ingest_data:
            # Load h5 data
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
            print(f'\nPopulated Model and Data tables from: {key}\n')
        else:
            print(f'\nPopulated Model table from: {key}\n')


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
