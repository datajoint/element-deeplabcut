import datajoint as dj
import importlib
import inspect
from deeplabcut.version import __version__ as dlc_version
from deeplabcut.utils.auxiliaryfunctions import GetScorerName, GetEvaluationFolder
from deeplabcut.utils.auxiliaryfunctions import GetModelFolder
import pandas as pd
import numpy as np
from pathlib import Path
from element_interface.utils import find_full_path, find_root_directory, dict_to_uuid


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
    assert hasattr(linking_module, 'get_dlc_root_data_dir'),\
        "The linking module must specify a lookup funtion for a root data directory"
    assert hasattr(linking_module, 'get_session_directory'),\
        "The linking module must specify a lookup funtion for session directories"

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


def get_session_directory(session_key: dict) -> str:
    """
    get_session_directory(session_key: dict) -> str
        Retrieve the session directory containing the
         recorded Neuropixels data for a given Session
        :param session_key: a dictionary of one Session `key`
        :return: a string for full path to the session directory
    """
    return _linking_module.get_session_directory(session_key)


def get_dlc_processed_data_dir(session_key: dict = None) -> str:
    """
    If specified by the user, this function provides DeepLabCut with an output
    directory for processed files. If unspecified, output files will be stored
    in the session directory 'videos' folder, per DeepLabCut default

    get_dlc_processed_data_dir -> str
        This user-provided function specifies where DeepLabCut output files
        will be stored.
    """
    if hasattr(_linking_module, 'get_dlc_processed_data_dir'):
        return _linking_module.get_dlc_processed_data_dir(session_key)
    else:
        return get_dlc_root_data_dir()[0]


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
        file_path: varchar(255)  # filepath of video, relative to root data directory
        """


@schema
class ConfigParamSet(dj.Lookup):
    definition = """
    # Parameters to specify a DLC model training instance
    paramset_idx    : smallint
    ---
    shuffle         : int         # shuffle number to use (usually 1)
    train_fraction  : float       # training fraction
    model_prefix="" : varchar(32) # DLC model prefix,  often empty
    filter_type=""  : varchar(16) # filter type, blank if none (e.g., median, arima)
    track_method="" : varchar(16) # tracking method, blank if none (e.g,. box, ellipse)
    scorer_legacy   : bool        # legacy naming for DLC < v2.1.0
    param_set_hash  : uuid        # hash identifying this parameterset
    unique index (param_set_hash)
    """

    @classmethod
    def insert_new_params(cls, paramset_idx: int, shuffle: int, train_fraction: int,
                          model_prefix: str = "", filter_type: str = "",
                          track_method: str = "", scorer_legacy: bool = False,
                          skip_duplicates=False):
        param_dict = {'paramset_idx': paramset_idx, 'shuffle': shuffle,
                      'train_fraction': train_fraction,  'filter_type': filter_type,
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
class TrainingTask(dj.Manual):
    definition = """      # Info required to specify 1 model
    -> VideoRecording     # labeled video for training
    -> ConfigParamSet
    training_id: int
    """


@schema
class ModelTraining(dj.Manual):
    definition = """
    -> TrainingTask
    ---
    snapshot_index_exact  : int unsigned # latest exact snapshot index (i.e., never -1)
    config_template       : longblob     # stored full config file
    """

    @classmethod
    def train_model(cls, session_key,
                    max_snapshots_to_keep=5,
                    displayiters=None,
                    saveiters=None,
                    maxiters=None,
                    allow_growth=False,
                    gputouse=None,
                    autotune=False,
                    keepdeconvweights=True):
        """ Launches model training, then stores max snapshot number and config
        :param key: Key specifying one ConfigParamSet
        :param project_path: Directory of DLC project
        :param max_snapshots_to_keep: How many snapshots are kept, default to 5
        Optional overrides of settings in pose_config.yaml
            :param displayiters: int, display iterations
            :param saveiters: int, save X iterations
            :param maxiters: int, maximum iterations
        :param allow_growth: bool, default false. True will not pre-allocate gpu memory
        :param gputouse: int, optional. number of your GPU (see number in nvidia-smi).
        :param autotune: bool TensorFlow property, faster if 'false'. Default false
        :param keepdeconvweights: bool, default: true. restore weights from snapshot
                                  If changing bodyparts, set to true
        """
        from deeplabcut import train_network
        from .readers.dlc_reader import PoseEstimation
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      get_session_directory(session_key))
        model = PoseEstimation(project_path)
        params = (ConfigParamSet & session_key).fetch1()
        if params['train_fraction'] not in model.yml['TrainingFraction']:
            # Config lists fractions used. If user provided val not exist, raise Err
            # TODO: move duplicated code to reader
            raise FileNotFoundError('Train Fraction {train_fraction}'.format(**params)
                                    + ' was not found in the config file\n'
                                    + model.yml_path)
        train_fract_idx = model.yml['TrainingFraction'].index(params['train_fraction'])
        try:
            train_network(model.yml_path,
                          shuffle=params['shuffle'],
                          trainingsetindex=train_fract_idx,
                          max_snapshots_to_keep=max_snapshots_to_keep,
                          displayiters=displayiters,
                          saveiters=saveiters,
                          maxiters=maxiters,
                          allow_growth=allow_growth,
                          gputouse=gputouse,
                          autotune=autotune,
                          keepdeconvweights=keepdeconvweights,
                          modelprefix=params['model_prefix'])
        except KeyboardInterrupt:  # Instructions indicate to train until interrupt
            pass
        snapshots = list((project_path /
                          GetModelFolder(params['train_fraction'],
                                         params['shuffle'],
                                         model.yml,
                                         modelprefix=params['model_prefix'])
                          / 'train').glob('*index*'))
        # ACTUALLY NEED MOST RECENT
        snapshot_idx_last = sorted([int(f.stem[9:]) for f in snapshots])[-1]
        model = PoseEstimation(project_path)  # reload for any updates post-train
        cls.insert1({**session_key,
                     'snapshot_index_exact': snapshot_idx_last,
                     'config_template': model.yml})


@schema
class BodyPart(dj.Lookup):
    definition = """
    body_part: varchar(32)
    ---
    body_part_description='': varchar(1000)
    """

    @classmethod
    def insert_all_from_model(cls, session_key, description_list=None,
                              skip_duplicates=True):
        """ Insert all body parts from a given model
        :param key: specifying one training session
        :param description_list: list of string descriptions of each part
        :parm skip_duplicates: skip if already in table
        """
        from .readers.dlc_reader import PoseEstimation
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      get_session_directory(session_key))
        body_parts = PoseEstimation(project_path).body_parts
        if not description_list:
            description_list = [''] * len(body_parts)
        for i in range(len(body_parts)):
            cls.insert1(body_parts=body_parts[i],
                        body_part_description=description_list[i],
                        skip_duplicates=skip_duplicates)


@schema
class Model(dj.Manual):
    definition = """
    model_name           : varchar(64)  # user-friendly model name
    ---
    task                 : varchar(32)  # task in the config yaml
    date                 : varchar(16)  # date in the config yaml
    iteration            : int          # iteration/version of this model
    snapshot_idx         : int          # which snapshot for prediction (if -1, latest)
    shuffle              : int          # which shuffle of the training dataset
    training_fract_idx   : int          # which training set fraction to generate model
    unique index (task, date, iteration, shuffle, snapshot_idx, training_fract_idx)
    scorer               : varchar(64)  # scorer/network name - DLC's GetScorerName()
    config_template      : longblob     # dictionary of the config for analyze_videos()
    project_path         : varchar(255) # DLC's project_path in config relative to root
    dlc_version          : varchar(8)   # keeps the deeplabcut version
    model_description='' : varchar(1000)
    -> ConfigParamSet
    -> [nullable] ModelTraining
    """

    class BodyPart(dj.Part):
        definition = """
        -> master
        -> BodyPart
        """

    def insert_new_model(cls, project_path, config_paramset_idx, model_name=None,
                         model_description='', training_id=None,
                         body_part_descriptions=None):
        """ Add new model to DataJoint framework
        :param project_path: Path of the DLC project with config.yaml
        :param config_paramset_idx: index of ConfigParamSet table
        :param model_name: User friendly model name. If none, DLC's GetScorerName
        :param model_description: Description of this model
        """
        from .readers.dlc_reader import PoseEstimation

        # ------------------------------ Path Information ------------------------------
        if not project_path.exists():  # If relative path, get full
            project_path = find_full_path(get_dlc_root_data_dir(), project_path)
        assert project_path.exists(), f'Could not find {project_path}'
        root_project_path = find_root_directory(get_dlc_root_data_dir(), project_path)
        relative_project_path = project_path.relative_to(root_project_path)  # save rel

        # ------------------------------ Model information -----------------------------
        model = PoseEstimation(project_path)
        BodyPart.insert_all_from_model(project_path,
                                       description_list=body_part_descriptions,
                                       skip_duplicates = True)

        params = (ConfigParamSet & config_paramset_idx).fetch1()
        if params['train_fraction'] not in model.yml['TrainingFraction']:
            # Config lists fractions used. If user provided val not exist, raise Err
            raise FileNotFoundError('Train Fraction {train_fraction}'.format(**params)
                                    + ' was not found in the config file\n'
                                    + model.yml_path)
        train_fract_idx = model.yml['TrainingFraction'].index(params['train_fraction'])
        if bool(model.yml['multianimalproject']):
            raise NotImplementedError('element-deeplabcut cannot yet accomodate '
                                      + 'multi-animal models.')
        if not model_name:
            # GetScorerName() returns two model names [updated, legacy]
            scorer_legacy = 1 if ((params['scorer_legacy']) == 'True') else 0
            model_name = GetScorerName(model.yml, params['shuffle'],
                                       params['train_fraction']
                                       )[scorer_legacy]
        # ------------------------ Insert into DataJoint tables ------------------------
        BodyPart.insert(model.body_parts, skip_duplicates=True)
        # cls.insert1
        print('    ', dict(model_name=model_name,
                           task=model.yml['Task'],
                           date=model.yml['date'],
                           iteration=model.yml['iteration'],
                           snapshot_idx=model.yml['snapshotindex'],
                           shuffle=params['shuffle'],
                           training_fract_idx=train_fract_idx,
                           scorer=model.pkl['Scorer'],
                           config_template=model.yml,
                           model_description=model_description,
                           project_path=relative_project_path,
                           ModelTraining=training_id,
                           dlc_version=dlc_version))


@schema
class ModelEval(dj.Computed):
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

    def make(self, key, comparisonbodyparts='all', gputouse=None, rescale=None):
        import csv
        from deeplabcut import evaluate_network

        model_table = (Model & key)
        params = model_table.fetch1('paramset_idx')
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      model_table.fetch1('project_path'))
        evaluate_network(
            project_path/'config.yml',
            Shuffles=list(model_table.fetch1('shuffle')),
            trainingsetindex=model_table.fetch1('training_fract_idx'),
            comparisonbodyparts=comparisonbodyparts,
            gputouse=gputouse,
            rescale=rescale)

        evaluationfolder = str(GetEvaluationFolder(params['train_fraction'],
                                                   params['shuffle'],
                                                   project_path/'config.yml',
                                                   modelprefix=params['model_prefix']))
        eval_path = project_path / evaluationfolder
        eval_csv = list(eval_path.glob('*csv'))
        assert eval_path.exists(), f'Couldn\'t find evaluation folder:\n{eval_path}'
        assert len(eval_csv) == 1, f'Found multiple evaluation CSVs:\n{eval_csv}'
        with open(eval_csv[0], newline='') as f:
            results = list(csv.DictReader(f, delimiter=','))[0]
        self.insert1(key,
                     train_iterations=results['Training iterations:'],
                     train_error=results[' Train error(px)'],
                     test_error=results[' Test error(px)'],
                     p_cutoff=results['p-cutoff used'],
                     Train_error_p=results['Train error with p-cutoff'],
                     test_error_p=results['Test error with p-cutoff'])


@schema
class PoseEstimationTask(dj.Manual):
    definition = """
    -> VideoRecording
    -> Model
    ---
    dlc_output_dir='': varchar(255)             # output relative to root data directory
    task_mode='load' : enum('load', 'trigger')  # load results or trigger computation
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
        from .readers.dlc_reader import PoseEstimation, do_pose_estimation

        # ID model and directories
        dlc_model = (Model & key).fetch1()
        task_mode, output_dir = (PoseEstimationTask & key
                                 ).fetch1('task_mode', 'dlc_output_dir')
        output_dir = find_full_path(get_dlc_root_data_dir(), output_dir)
        video_filepaths = [find_full_path(get_dlc_root_data_dir(), fp)
                           for fp in (VideoRecording.File & key).fetch('file_path')]
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      dlc_model['project_path'])
        # Triger estimation,
        if task_mode == 'trigger':
            do_pose_estimation(video_filepaths, dlc_model, project_path, output_dir)
        dlc_result = PoseEstimation(output_dir)

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
            body_parts = self.BodyPartPosition().fetch('joint_name')
        else:
            body_parts = list(joint_name)
            dataFrame = None
        for bodypart in body_parts:
            position_data = (PoseEstimation.BodyPartPosition
                             & ("joint_name='%s'" % bodypart))
            x_pos = (position_data).fetch1('x_pos')
            y_pos = (position_data).fetch1('y_pos')
            likelihood = (position_data).fetch1('likelihood')
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
