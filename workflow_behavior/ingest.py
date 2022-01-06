import pathlib
import csv
import re

from workflow_behavior.pipeline import lab, subject, session, pose
from workflow_behavior.paths import get_root_data_dir
import element_data_loader.utils

def ingest_sessions(session_csv_path='./user_data/sessions.csv'):
    """
    Ingests DeepLabCut files from directories listed
    in the sess_dir column of ./user_data/sessions.csv
    """
    # ---------- Insert new "Session" and "ProbeInsertion" ---------
    with open(session_csv_path, newline= '') as f:
        input_sessions = list(csv.DictReader(f, delimiter=','))

    # Folder structure: root / subject / session / probe / .ap.meta
    session_list, sess_dir_list, = [], []

    for sess in input_sessions:
        sess_dir = element_data_loader.utils.find_full_path(
                                                    get_root_data_dir(),
                                                    sess['session_dir'])
        session_datetimes, model_list = [], []

        # search session dir and determine acquisition software
        for file_pattern, acq_type in zip(['*.yaml', '*.other'], ['DeepLabCut', 'OtherUnspecified']):
            beh_model_filepaths = [fp for fp in sess_dir.rglob(file_pattern)]
            if len(beh_model_filepaths):
                acq_software = acq_type
                break
        else:
            raise FileNotFoundError(f'Recording files not found! Checked for files found in: {sess_dir}')

        if acq_software == 'DeepLabCut':
            pass
            # NEEDS WORK HERE
        else:
            raise NotImplementedError(f'Unknown acquisition software: {acq_software}')

        # new session/probe-insertion
        session_key = {'subject': sess['subject'], 'session_datetime': min(session_datetimes)}
        if session_key not in session.Session():
            session_list.append(session_key)
            root_dir = element_data_loader.utils.find_root_directory(
                                                    get_root_data_dir(), sess_dir)
            sess_dir_list.append({**session_key, 'session_dir': sess_dir.relative_to(root_dir).as_posix()})

    print(f'\n---- Insert {len(session_list)} entry(s) into session.Session ----')
    session.Session.insert(session_list, skip_duplicates=True)
    session.SessionDirectory.insert(sess_dir_list, skip_duplicates=True)

    print(f'\n---- Insert {len(probe_list)} entry(s) into probe.Probe ----')
    dlc.DLCModel.insert(model_list, skip_duplicates=True)

    print('\n---- Successfully completed workflow_behavior/ingest.py ----')


if __name__ == '__main__':
    ingest_subjects()
    ingest_sessions()
