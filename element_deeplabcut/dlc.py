"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""

import datajoint as dj
import importlib
import inspect
import os
import numpy as np
from deeplabcut.version import __version__ as dlc_version
from deeplabcut.utils.auxiliaryfunctions import GetScorerName, GetEvaluationFolder
from deeplabcut.utils.auxiliaryfunctions import GetModelFolder
from pathlib import Path
from element_interface.utils import find_full_path, dict_to_uuid
from datetime import datetime


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
                + Session: parent table to VideoRecording, identifying a recording session
                + Device: parent table to VideoRecording, identifying video recording device
            Functions:
                + get_dlc_root_data_dir() -> list
                    Retrieve the root data director(y/ies) with behavioral
                    recordings for all subject/sessions.
                    :return: a string for full path to the root data directory
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
        root_directories.append(_linking_module.get_dlc_processed_data_dir(None))

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
class VideoRecording(dj.Manual):
    definition = """
    -> Session
    -> Device
    recording_id: int
    ---
    recording_start_time: datetime
    """

    class File(dj.Part):
        definition = """
        -> master
        file_path: varchar(255)  # filepath of video, relative to root data directory
        """


@schema
class ModelTrainingParamSet(dj.Lookup):
    definition = """
    # Parameters to specify a DLC model training instance
    paramset_idx    : smallint
    ---
    paramset_desc: varchar(128)
    param_set_hash  : uuid        # hash identifying this parameterset
    unique index (param_set_hash)
    params: longblob  # dictionary of all applicable parameters
    """

    required_parameters = ('shuffle', 'trainingsetindex')

    @classmethod
    def insert_new_params(cls, paramset_desc: str, params: dict, paramset_idx: int = None):
        for required_param in cls.required_parameters:
            assert required_param in params, f'Missing required parameter: {required_param}'

        if paramset_idx is None:
            paramset_idx = (dj.U().aggr(cls, n='max(paramset_idx)').fetch1('n') or 0) + 1

        param_dict = {'paramset_idx': paramset_idx,
                      'paramset_desc': paramset_desc,
                      'params': params,
                      'param_set_hash':  dict_to_uuid(params)
                      }
        param_query = cls & {'param_set_hash': param_dict['param_set_hash']}

        if param_query:  # If the specified param-set already exists
            existing_paramset_idx = param_query.fetch1('paramset_idx')
            if existing_paramset_idx == paramset_idx:  # If the existing set has the same paramset_idx: job done
                return
            else:  # If not same name: human error, trying to add the same paramset with different name
                raise dj.DataJointError(
                    f'The specified param-set already exists'
                    f' - with paramset_idx: {existing_paramset_idx}')
        else:
            if {'paramset_idx': paramset_idx} in cls.proj():
                raise dj.DataJointError(
                    f'The specified paramset_idx {paramset_idx} already exists,'
                    f' please pick a different one.')
            cls.insert1(param_dict)


@schema
class TrainingTask(dj.Manual):
    definition = """      # Specification for a DLC model training instance
    -> VideoRecording     # labeled video for training
    -> ConfigParamSet
    training_id: int
    ---
    model_prefix='': varchar(32)
    project_path='': varchar(255) # DLC's project_path in config relative to root, to save the trained results
    """


@schema
class ModelTraining(dj.Computed):
    definition = """
    -> TrainingTask
    ---
    latest_snapshot: int unsigned # latest exact snapshot index (i.e., never -1)
    config_template: longblob     # stored full config file
    """

    def make(self, key):
        import inspect
        from deeplabcut import train_network
        from deeplabcut.utils.auxiliaryfunctions import GetModelFolder

        training_id, project_path, model_prefix = (TrainingTask & key).fetch1(
            'training_id', 'project_path', 'model_prefix')

        project_path = find_full_path(get_dlc_root_data_dir(), project_path)

        # ---- Build and save DLC configuration (yaml) file ----
        dlc_config = (ModelTrainingParamSet & key).fetch1('params')
        dlc_config['project_path'] = dlc_project_path.as_posix()
        dlc_config['modelprefix'] = model_prefix

        video_filepaths = [find_full_path(get_dlc_root_data_dir(), fp).as_posix()
                           for fp in (VideoRecording.File & key).fetch('file_path')]
        dlc_config['video_sets'] = video_filepaths

        # ---- Write DLC and basefolder yaml (config) files ----

        # Write dlc config file to base (data) folder
        # This is important for parsing the DLC in datajoint imaging
        output_dir.mkdir(exist_ok=True)
        dlc_cfg_filepath = project_path / 'config.yaml'
        with open(dlc_cfg_filepath, 'w') as f:
            yaml.dump(dlc_config, f)

        # ---- Trigger DLC model training job ----
        train_network_input_args = list(inspect.signature(train_network).parameters)
        train_network_kwargs = {k: v for k, v in dlc_config.items() if k in train_network_input_args}
        try:
            train_network(dlc_cfg_filepath, **train_network_kwargs)
        except KeyboardInterrupt:  # Instructions indicate to train until interrupt
            pass

        snapshots = list((project_path /
                          GetModelFolder(trainFraction=dlc_config['train_fraction'],
                                         shuffle=dlc_config['shuffle'],
                                         cfg=dlc_config,
                                         modelprefix=dlc_config['modelprefix'])
                          / 'train').glob('*index*'))
        max_modified_time = 0
        for snapshot in snapshots:
            modified_time = os.path.getmtime(snapshot)
            if modified_time > max_modified_time:
                latest_snapshot = int(snapshot.stem[9:])
                max_modified_time = modified_time

        self.insert1({**key,
                      'latest_snapshot': latest_snapshot,
                      'config_template': config_template})


@schema
class BodyPart(dj.Lookup):
    definition = """
    body_part: varchar(32)
    ---
    body_part_description='': varchar(1000)
    """

    @classmethod
    def insert_from_config(cls, dlc_config: dict):
        # handle dlc_config being a yaml file
        if not isinstance(dlc_config, dict):
            dlc_config_fp = pathlib.Path(dlc_config)
            if dlc_config_fp.exists() and dlc_config_fp.suffix in ('.yml', '.yaml'):
                with open(dlc_config, 'rb') as f:
                    dlc_config = yaml.safe_load(f)
        # -- Check and insert new BodyPart --
        if 'bodyparts' in dlc_config:
            tracked_body_parts = cls.fetch('body_part')
            new_body_parts = np.setdiff1d(dlc_config['bodyparts'], tracked_body_parts)
            if new_body_parts:
                print(f'Existing body parts: {tracked_body_parts}')
                print(f'New body parts: {new_body_parts}')
                if dj.utils.user_choice(f'Insert {len(new_body_parts)} new body part(s)?') == 'yes':
                    cls.insert({'body_part': b} for b in new_body_parts)


@schema
class Model(dj.Manual):
    definition = """
    model_name           : varchar(64)  # user-friendly model name
    ---
    task                 : varchar(32)  # task in the config yaml
    date                 : varchar(16)  # date in the config yaml
    iteration            : int          # iteration/version of this model
    snapshotindex        : int          # which snapshot for prediction (if -1, latest)
    shuffle              : int          # which shuffle of the training dataset
    trainingsetindex     : int          # which training set fraction to generate model
    unique index (task, date, iteration, shuffle, snapshotindex, trainingsetindex)
    scorer               : varchar(64)  # scorer/network name - DLC's GetScorerName()
    config_template      : longblob     # dictionary of the config for analyze_videos()
    project_path         : varchar(255) # DLC's project_path in config relative to root
    dlc_version          : varchar(8)   # keeps the deeplabcut version
    model_prefix=''      : varchar(32)
    model_description='' : varchar(1000)
    -> [nullable] ModelTrainingParamSet
    """

    # NOTE: Previously, nullable ModelTraining entry. If imported, would have duplicate
    #       values for multiple items stored here. Don't want to enforce model training
    #       but I do want to enforce having models stored here for pose estimation later

    class BodyPart(dj.Part):
        definition = """
        -> master
        -> BodyPart
        """

    @classmethod
    def insert_new_model(cls, model_name: str, dlc_config: dict, *,
                         shuffle, trainingsetindex, model_description='', model_prefix=''):
        from deeplabcut.utils.auxiliaryfunctions import GetScorerName

        # handle dlc_config being a yaml file
        if not isinstance(dlc_config, dict):
            dlc_config_fp = pathlib.Path(dlc_config)
            if dlc_config_fp.exists() and dlc_config_fp.suffix in ('.yml', '.yaml'):
                with open(dlc_config, 'rb') as f:
                    dlc_config = yaml.safe_load(f)

        # ---- Get and resolve project path ----
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      dlc_config['project_path'])
        root_dir = find_root_directory(get_dlc_root_data_dir(), project_path)

        # ---- Build config ----
        template_attributes = ['Task', 'date', 'TrainingFraction', 'iteration', 'snapshotindex',
                               'batch_size', 'cropping', 'x1', 'x2', 'y1', 'y2']
        config_template = {k: v for k, v in dlc_config.items() if k in template_attributes}

        # ---- Get scorer name ----
        dlc_scorer = GetScorerName(cfg=config_template,
                                   shuffle=shuffle,
                                   trainFraction=dlc_config['TrainingFraction'][trainingsetindex],
                                   modelprefix=model_prefix)
        if config_template['snapshotindex'] == -1:
            dlc_scorer = ''.join(dlc_scorer.split('_')[:-1])

        # ---- Insert ----
        model_dict = {'model_name': model_name,
                      'model_description': model_description,
                      'scorer': dlc_scorer,
                      'task': config_template['Task'],
                      'date': config_template['date'],
                      'iteration': config_template['iteration'],
                      'snapshotindex': config_template['snapshotindex'],
                      'shuffle': shuffle,
                      'trainingsetindex': trainingsetindex,
                      'project_path': project_path.relative_to(root_dir).as_posix(),
                      'config_template': config_template}

        # -- prompt for confirmation --
        print('--- DLC Model specification to be inserted ---')
        for k, v in model_dict.items():
            if k != 'config_template':
                print('\t{}: {}'.format(k, v))
            else:
                print('\t-- Template for config.yaml --')
                for k, v in model_dict['config_template'].items():
                    print('\t\t{}: {}'.format(k, v))

        if dj.utils.user_choice('Proceed with new DLC model insert?') == 'yes':
            with cls.connection.transaction:
                cls.insert1(model_dict)
                BodyPart.insert_from_config(dlc_config)


@schema
class ModelEvaluation(dj.Computed):
    definition = """
    -> Model
    ---
    train_iterations : int   # Training iterations
    train_error      : float # Train error (px)
    test_error       : float # Test error (px)
    p_cutoff         : float # p-cutoff used
    train_error_p    : float # Train error with p-cutoff
    test_error_p     : float # Test error with p-cutoff
    """

    def make(self, key):
        import csv
        from deeplabcut import evaluate_network
        from deeplabcut.utils.auxiliaryfunctions import GetEvaluationFolder

        dlc_config, project_path, model_prefix, shuffle, trainingsetindex = (Model & key).fetch1(
            'config_template', 'project_path', 'model_prefix', 'shuffle', 'trainingsetindex')

        project_path = find_full_path(get_dlc_root_data_dir(), project_path)

        evaluate_network(
            project_path / 'config.yaml',
            Shuffles=[shuffle],  # this needs to be a list
            trainingsetindex=trainingsetindex,
            comparisonbodyparts='all')

        evaluation_folder = GetEvaluationFolder(trainFraction=dlc_config['TrainingFraction'][trainingsetindex],
                                                shuffle=shuffle,
                                                cfg=dlc_config,
                                                modelprefix=model_prefix)
        eval_path = project_path / evaluation_folder
        assert eval_path.exists(), f'Couldn\'t find evaluation folder:\n{eval_path}'

        eval_csvs = list(eval_path.glob('*csv'))
        max_modified_time = 0
        for eval_csv in eval_csvs:
            modified_time = os.path.getmtime(eval_csv)
            if modified_time > max_modified_time:
                eval_csv_latest = eval_csv
        with open(eval_csv_latest, newline='') as f:
            results = list(csv.DictReader(f, delimiter=','))[0]
        self.insert1(dict(key,
                          train_iterations=results['Training iterations:'],
                          train_error=results[' Train error(px)'],
                          test_error=results[' Test error(px)'],
                          p_cutoff=results['p-cutoff used'],
                          train_error_p=results['Train error with p-cutoff'],
                          test_error_p=results['Test error with p-cutoff']))


@schema
class PoseEstimationTask(dj.Manual):
    definition = """
    -> VideoRecording
    -> Model
    ---
    task_mode='load' : enum('load', 'trigger')   # load results or trigger computation
    pose_estimation_output_dir='': varchar(255)  # output directory relative to the root data directory
    """

    @classmethod
    def infer_output_dir(cls, key, relative=False, mkdir=False):
        """
        Given a 'key' to an entry in this table
        Return the expected pose_estimation_output_dir based on the following convention:
            processed_dir / video_dir / device_{}_recording_{}_model_{}
        """
        processed_dir = pathlib.Path(get_processed_root_data_dir())

        video_filepath = find_full_path(get_dlc_root_data_dir(),
                                        (VideoRecording.File & key).fetch('file_path', limit=1)[0]).as_posix()

        video_dir = video_filepath.parent
        root_dir = find_root_directory(get_ephys_root_data_dir(), video_dir)

        device = '-'.join((_linking_module.Device & key).fetch1('KEY').values())

        output_dir = (processed_dir
                      / video_dir.relative_to(root_dir)
                      / f'device_{device}_recording_{key["recording_id"]}_model_{key["model_name"]}')

        if mkdir:
            output_dir.mkdir(parents=True, exist_ok=True)
            log.info(f'{output_dir} created!')

        return output_dir.relative_to(processed_dir) if relative else output_dir


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
        -> BodyPart
        ---
        frame_index : longblob     # frame index in model
        x_pos       : longblob
        y_pos       : longblob
        z_pos=null  : longblob
        likelihood  : longblob
        """

    def make(self, key):
        from .readers import dlc_reader

        # ID model and directories
        dlc_model = (Model & key).fetch1()
        task_mode, output_dir = (PoseEstimationTask & key).fetch1('task_mode', 'pose_estimation_output_dir')

        output_dir = find_full_path(get_dlc_root_data_dir(), output_dir)

        video_filepaths = [find_full_path(get_dlc_root_data_dir(), fp).as_posix()
                           for fp in (VideoRecording.File & key).fetch('file_path')]

        project_path = find_full_path(get_dlc_root_data_dir(), dlc_model['project_path'])

        # Triger estimation,
        if task_mode == 'trigger':
            dlc_reader.do_pose_estimation(video_filepaths, dlc_model, project_path, output_dir)
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
        Returns a dataframe of x, y and z coordinates of the specified body_parts
        :param key: A query specifying one PoseEstimation entry, else error is thrown.
        :param body_parts: optional, joint(s) as a list. If none, all joints
        returns df: multi index dataframe with DLC scorer names, body_parts
                    and x/y coordinates of each joint name for a camera_id,
                    similar to output of DLC dataframe.
        """
        import pandas as pd
        model_name = key['model_name']
        if body_parts == 'all':
            body_parts = (cls.BodyPartPosition & key).fetch('body_part')
        else:
            body_parts = list(body_parts)

        df = None
        for body_part in body_parts:
            x_pos, y_pos, z_pos, likelihood = (cls.BodyPartPosition & {'body_part': body_part}).fetch1(
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
