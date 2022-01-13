# from pathlib import Path
import csv

from workflow_behavior.pipeline import subject, session, dlc
# from workflow_behavior.paths import get_root_data_dir
# from element_data_loader.utils import find_full_path


def ingest_general(csvs, tables,
                   skip_duplicates=True):
    """
    Inserts data from a series of csvs into their corresponding table:
        e.g., ingest_general(['./lab_data.csv', './proj_data.csv'],
                                 [lab.Lab(),lab.Project()]
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
    Inserts data from a subject csv into corresponding subject schema tables
    By default, uses data from workflow_session/user_data/
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
    # ingest to session schema
    csvs = [session_csv_path, session_csv_path, session_csv_path]
    tables = [session.Session(), session.SessionDirectory(),
              session.SessionNote()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)


def ingest_dlc_configs(recording_csv_path='./user_data/recordings.csv',
                       skip_duplicates=True):
    """
    Ingests to DLC schema from ./user_data/recordings.csv
    """
    csvs = [recording_csv_path,recording_csv_path]
    tables = [dlc.Recording(),dlc.Config()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates)


if __name__ == '__main__':
    ingest_subjects()
    ingest_sessions()
    ingest_dlc_configs()

'''
# Folder structure: root / subject / session / [fill in here]
# session_list, sess_dir_list = [], []

for sess in input_sessions:
    sess_dir = element_data_loader.utils.find_full_path(
                                                get_root_data_dir(),
                                                sess['session_dir'])
    session_datetimes, dlcmodel_list = [], []

    # search session dir and determine acquisition software
    for file_pattern, acq_type in zip(['*.yaml', '*.other'],
                                      ['DeepLabCut', 'OtherUnspecified']):
        beh_model_filepaths = [fp for fp in sess_dir.rglob(file_pattern)]
        if len(beh_model_filepaths):
            acq_software = acq_type
            break
    else:
        raise FileNotFoundError('Recording files not found! Checked for '
                                + f'files found in: {sess_dir}')

    if acq_software == 'DeepLabCut':
        pass
        # NEEDS WORK HERE
    else:
        raise NotImplementedError('Unknown acquisition software: '
                                  + f'{acq_software}')

    # new session/probe-insertion
    session_key = {'subject': sess['subject'],
                   'session_datetime': min(session_datetimes)}
    if session_key not in session.Session():
        session_list.append(session_key)
        root_dir = element_data_loader.utils.find_root_directory(
                                                get_root_data_dir(),
                                                sess_dir)
        sess_dir_list.append({**session_key,
                              'session_dir': sess_dir.\
                              relative_to(root_dir).as_posix()})

print(f'\n---- Insert {len(session_list)} entry(s) '
      + 'into session.Session ----')
session.Session.insert(session_list, skip_duplicates=True)
session.SessionDirectory.insert(sess_dir_list, skip_duplicates=True)

print(f'\n---- Insert {len(dlcmodel_list)} entry(s) '
      + 'into dlc.DLCModel ----')
dlc.DLCModel.insert(dlcmodel_list, skip_duplicates=True)
'''
