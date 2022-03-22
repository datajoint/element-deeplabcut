# from pathlib import Path
import csv
import ruamel.yaml as yaml
from element_interface.utils import find_full_path

from .pipeline import subject, session, train, model
from .paths import get_dlc_root_data_dir


def ingest_general(csvs, tables,
                   skip_duplicates=True):
    """
    Inserts data from a series of csvs into their corresponding table:
        e.g., ingest_general(['./lab.csv', './subject.csv'],
                                 [lab.Lab(),subject.Subject()]
    ingest_general(csvs, tables, skip_duplicates=True)
        :param csvs: list of relative paths to CSV files
        :param tables: list of datajoint tables with ()
    """
    for insert, table in zip(csvs, tables):
        with open(insert, newline='') as f:
            data = list(csv.DictReader(f, delimiter=','))
        prev_len = len(table)
        table.insert(data, skip_duplicates=skip_duplicates,
                     ignore_extra_fields=True)
        insert_len = len(table) - prev_len     # report length change
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
    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)


def ingest_sessions(session_csv_path='./user_data/sessions.csv',
                    skip_duplicates=True):
    """
    Ingests to session schema from ./user_data/sessions.csv
    """
    csvs = [session_csv_path, session_csv_path, session_csv_path]
    tables = [session.Session(), session.SessionDirectory(),
              session.SessionNote()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)


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
    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)


if __name__ == '__main__':
    ingest_subjects()
    ingest_sessions()
    ingest_dlc_items()
