# from pathlib import Path
import csv
import ruamel.yaml as yaml
from element_interface.utils import find_full_path  # , ingest_csv_to_table

from .pipeline import subject, session, train, model
from .paths import get_dlc_root_data_dir


## TODO: why did pip install git+URL not have this function from element-interface?
def ingest_csv_to_table(csvs, tables, verbose=True, skip_duplicates=True,
                        ignore_extra_fields=True, allow_direct_insert=False):
    """
    Inserts data from a series of csvs into their corresponding table:
        e.g., ingest_csv_to_table(['./lab_data.csv', './proj_data.csv'],
                                 [lab.Lab(),lab.Project()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=True)
        :param csvs: list of relative paths to CSV files.  CSV are delimited by commas.
        :param tables: list of datajoint tables with ()
        :param verbose: print number inserted (i.e., table length change)
        :param skip_duplicates: skip duplicate entries
        :param ignore_extra_fields: if a csv feeds multiple tables, the subset of
                                    columns not applicable to a table will be ignored
        :param allow_direct_insert: permit insertion into Imported and Computed tables
    """
    for csv_filepath, table in zip(csvs, tables):
        with open(csv_filepath, newline='') as f:
            data = list(csv.DictReader(f, delimiter=','))
        if verbose:
            prev_len = len(table)
        table.insert(data, skip_duplicates=skip_duplicates,
                     # Ignore extra fields because some CSVs feed multiple tables
                     ignore_extra_fields=ignore_extra_fields,
                     # Allow direct bc element-event uses dj.Imported w/o `make` funcs
                     allow_direct_insert=allow_direct_insert)
        if verbose:
            insert_len = len(table) - prev_len
            print(f'\n---- Inserting {insert_len} entry(s) '
                  + f'into {table.table_name} ----')


def ingest_subjects(subject_csv_path='./user_data/subjects.csv',
                    skip_duplicates=True):
    """
    Inserts data from ./user_data/subject.csv into corresponding subject schema tables

    :param subject_csv_path:     relative path of subject csv
    :param skip_duplicates=True: datajoint insert function param
    """
    csvs = [subject_csv_path]
    tables = [subject.Subject()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates)


def ingest_sessions(session_csv_path='./user_data/sessions.csv',
                    skip_duplicates=True):
    """
    Ingests to session schema from ./user_data/sessions.csv
    """
    csvs = [session_csv_path, session_csv_path, session_csv_path]
    tables = [session.Session(), session.SessionDirectory(),
              session.SessionNote()]

    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates)


def ingest_dlc_items(config_params_csv_path='./user_data/config_params.csv',
                     train_video_csv_path='./user_data/train_videosets.csv',
                     model_video_csv_path='./user_data/model_videos.csv',
                     skip_duplicates=True):
    """
    Ingests to DLC schema from ./user_data/{config_params,recordings}.csv

    First, loads config.yaml info to train.TrainingParamSet. Requires paramset_idx,
        paramset_desc and relative config_path. Other columns overwrite config variables
    Next, loads recording info into VideoRecording and VideoRecording.File
    :param config_params_csv_path: csv path for model training config and parameters
    :param train_video_csv_path: csv path for list of training videosets
    :param recording_csv_path: csv path for list of modeling videos for pose estimation
    """

    previous_length = len(train.TrainingParamSet.fetch())
    with open(config_params_csv_path, newline='') as f:
        config_csv = list(csv.DictReader(f, delimiter=','))
    for line in config_csv:
        paramset_idx = line.pop('paramset_idx')
        paramset_desc = line.pop('paramset_desc')
        config_path = find_full_path(get_dlc_root_data_dir(),
                                     line.pop('config_path'))
        assert config_path.exists(), f'Could not find config_path: {config_path}'
        with open(config_path, 'rb') as y:
            params = yaml.safe_load(y)
        params.update({**line})

        train.TrainingParamSet.insert_new_params(paramset_idx=paramset_idx,
                                                 paramset_desc=paramset_desc,
                                                 params=params)
    insert_length = len(train.TrainingParamSet.fetch()) - previous_length
    print(f'\n---- Inserting {insert_length} entry(s) into #model_training_param_set '
          + '----')

    # Next, recordings and config files
    csvs = [train_video_csv_path, train_video_csv_path,
            model_video_csv_path, model_video_csv_path]
    tables = [train.VideoSet(), train.VideoSet.File(),
              model.VideoRecording(), model.VideoRecording.File()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates)

if __name__ == '__main__':
    ingest_subjects()
    ingest_sessions()
    ingest_dlc_items()
