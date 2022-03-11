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
from pathlib import Path
import pathlib
import yaml
from element_interface.utils import find_full_path, find_root_directory


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
class BodyPart(dj.Lookup):
    definition = """
    body_part                : varchar(32)
    ---
    body_part_description='' : varchar(1000)
    """

    @classmethod
    def extract_new_body_parts(cls, dlc_config: dict):
        """Print a list of new body parts from a dlc config,
        to examine before generating descriptions
        :param dlc_config:  path to a config.y*ml, or dict including contents thereof
        """
        if not isinstance(dlc_config, dict):
            dlc_config_fp = find_full_path(get_dlc_root_data_dir(),
                                           pathlib.Path(dlc_config))
            assert (dlc_config_fp.exists()
                    and dlc_config_fp.suffix in ('.yml', '.yaml')), (
                    f'dlc_config is neither dict nor filepath\n Check: {dlc_config_fp}')
            if dlc_config_fp.suffix in ('.yml', '.yaml'):
                with open(dlc_config_fp, 'rb') as f:
                    dlc_config = yaml.safe_load(f)
        # -- Check and insert new BodyPart --
        assert 'bodyparts' in dlc_config, f'Found no bodyparts section in {dlc_config}'
        tracked_body_parts = cls.fetch('body_part')
        new_body_parts = np.setdiff1d(dlc_config['bodyparts'], tracked_body_parts)
        print(f'Existing body parts: {tracked_body_parts}')
        print(f'New body parts: {new_body_parts}')
        return new_body_parts

    @classmethod
    def insert_from_config(cls, dlc_config: dict, descriptions: list = None,
                           prompt=True):
        """Insert all body parts from a config file

        :param dlc_config: path to a config.y*ml, or dict including contents thereof
        :param descriptions: optional list describing new body parts
        """

        # handle dlc_config being a yaml file
        new_body_parts = cls.extract_new_body_parts(dlc_config)
        if new_body_parts is not None:  # Required bc np.array is ambiguous as bool
            if descriptions:
                assert len(descriptions)\
                        == len(new_body_parts), ('Descriptions list does not match '
                                                 + ' the number of new_body_parts')
                print(f'New descriptions: {descriptions}')
            if descriptions is None:
                descriptions = ["" for x in range(len(new_body_parts))]

            if prompt and dj.utils.user_choice(f'Insert {len(new_body_parts)} new body '
                                               + 'part(s)?') != 'yes':
                print('Canceled insert.')
                return
            cls.insert([{'body_part': b, 'body_part_description': d}
                       for b, d in zip(new_body_parts, descriptions)])


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
    model_prefix=''      : varchar(32)
    model_description='' : varchar(1000)
    -> [nullable] train.TrainingParamSet
    """
    # project_path is the only item required downstream in the pose schema
    # what happens if TrainingParamSet isn't in the namespace?

    class BodyPart(dj.Part):
        definition = """
        -> master
        -> BodyPart
        """

    @classmethod
    def insert_new_model(cls, model_name: str, dlc_config: dict, *, shuffle: int,
                         trainingsetindex, model_description='', model_prefix='',
                         paramset_idx: int = None, prompt=True):
        """Insert new model into the dlc.Model table

        :param model_name: User-friendly name for this model
        :param dlc_config: path to a config.y*ml, or dict including contents thereof
        :param shuffle: integer, shuffle number
        :param trainingsetindex: index of training fraction list in config.yaml
        :param model_description: Description of this model
        :param model_prefix: Filename prefix used across DLC project
        :param body_part_descriptions: optional list for new items in BodyParts table
        :param paramset_idx: optional index from the TrainingParamSet table
        """
        from deeplabcut.utils.auxiliaryfunctions import GetScorerName
        from deeplabcut import __version__ as dlc_version
        from packaging import version
        from distutils.util import strtobool

        # handle dlc_config being a yaml file
        if not isinstance(dlc_config, dict):
            dlc_config_fp = find_full_path(get_dlc_root_data_dir(),
                                           pathlib.Path(dlc_config))
            assert dlc_config_fp.exists(), ('dlc_config is neither dict nor filepath'
                                            + f'\n Check: {dlc_config_fp}')
            if dlc_config_fp.suffix in ('.yml', '.yaml'):
                with open(dlc_config_fp, 'rb') as f:
                    dlc_config = yaml.safe_load(f)

        # ---- Get and resolve project path ----
        project_path = find_full_path(get_dlc_root_data_dir(),
                                      dlc_config['project_path'])
        root_dir = find_root_directory(get_dlc_root_data_dir(), project_path)

        # ---- Build config ----
        template_attributes = ['Task', 'date', 'TrainingFraction', 'iteration',
                               'snapshotindex', 'batch_size', 'cropping',
                               'x1', 'x2', 'y1', 'y2', 'project_path']
        config_template = {k: v for k, v in dlc_config.items()
                           if k in template_attributes}

        # ---- Get scorer name ----
        # "or 'f'" below covers case where config returns None. StrToBool handles else
        scorer_legacy = 1 if (strtobool(dlc_config.get('scorer_legacy') or 'f')
                              or version.parse(dlc_version) < version.parse("2.1")
                              ) else 0  # if old version, or if specified in params

        dlc_scorer = GetScorerName(cfg=config_template,
                                   shuffle=shuffle,
                                   trainFraction=dlc_config['TrainingFraction'
                                                            ][trainingsetindex],
                                   modelprefix=model_prefix)[scorer_legacy]
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
                      'paramset_idx': paramset_idx,
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

        if prompt and dj.utils.user_choice('Proceed with new DLC model insert?'
                                           ) != 'yes':
            print('Canceled insert.')
            return
        with cls.connection.transaction:
            cls.insert1(model_dict)
            if BodyPart.extract_new_body_parts(dlc_config):
                BodyPart.insert_from_config(dlc_config, prompt=prompt)


@schema
class Evaluation(dj.Computed):
    definition = """
    -> Model
    ---
    train_iterations   : int   # Training iterations
    train_error=null   : float # Train error (px)
    test_error=null    : float # Test error (px)
    p_cutoff=null      : float # p-cutoff used
    train_error_p=null : float # Train error with p-cutoff
    test_error_p=null  : float # Test error with p-cutoff
    """

    def make(self, key):
        """.populate() method will launch evaulation for each unique entry in Model"""
        import csv
        from deeplabcut import evaluate_network
        from deeplabcut.utils.auxiliaryfunctions import GetEvaluationFolder

        dlc_config, project_path, model_prefix, shuffle, trainingsetindex = \
            (Model & key).fetch1('config_template', 'project_path', 'model_prefix',
                                 'shuffle', 'trainingsetindex')

        project_path = find_full_path(get_dlc_root_data_dir(), project_path)
        yml_paths = list(project_path.glob('*.y*ml'))
        assert len(yml_paths) == 1, ('Unable to find one unique .yaml file in: '
                                     + f'{project_path} - Found: {len(yml_paths)}')

        evaluate_network(
            yml_paths[0],
            Shuffles=[shuffle],  # this needs to be a list
            trainingsetindex=trainingsetindex,
            comparisonbodyparts='all')

        eval_folder = GetEvaluationFolder(trainFraction=dlc_config['TrainingFraction'
                                                                   ][trainingsetindex],
                                          shuffle=shuffle,
                                          cfg=dlc_config,
                                          modelprefix=model_prefix)
        eval_path = project_path / eval_folder
        assert eval_path.exists(), f'Couldn\'t find evaluation folder:\n{eval_path}'

        eval_csvs = list(eval_path.glob('*csv'))
        max_modified_time = 0
        for eval_csv in eval_csvs:
            modified_time = os.path.getmtime(eval_csv)
            if modified_time > max_modified_time:
                eval_csv_latest = eval_csv
        with open(eval_csv_latest, newline='') as f:
            results = list(csv.DictReader(f, delimiter=','))[0]
        # in testing, test_error_p returned empty string
        self.insert1(dict(key,
                          train_iterations=results['Training iterations:'],
                          train_error=results[' Train error(px)'],
                          test_error=results[' Test error(px)'],
                          p_cutoff=results['p-cutoff used'],
                          train_error_p=results['Train error with p-cutoff'],
                          test_error_p=results['Test error with p-cutoff']))
