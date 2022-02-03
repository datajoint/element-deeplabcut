'''
fresh docker:
    docker run --name wf-sess -p 3306:3306 -e \
    MYSQL_ROOT_PASSWORD=tutorial datajoint/mysql
dependencies: pip install pytest pytest-cov
run all tests:
    pytest -sv --cov-report term-missing --cov=workflow-session \
    -p no:warnings tests/
run one test, debug:
    pytest [above options] --pdb tests/tests_name.py -k function_name
'''

import os
import pytest
import pathlib
import datajoint as dj

# ------------------- SOME CONSTANTS -------------------

_tear_down = True

test_user_data_dir = pathlib.Path('./tests/user_data')
test_user_data_dir.mkdir(exist_ok=True)

# ------------------ GENERAL FUCNTION ------------------


def write_csv(content, path):
    """
    General function for writing strings to lines in CSV
    :param path: pathlib PosixPath
    :param content: list of strings, each as row of CSV
    """
    with open(path, 'w') as f:
        for line in content:
            f.write(line+'\n')

# ------------------- FIXTURES -------------------


@pytest.fixture(autouse=True)
def dj_config():
    """ If dj_local_config exists, load"""
    if pathlib.Path('./dj_local_conf.json').exists():
        dj.config.load('./dj_local_conf.json')
    dj.config['safemode'] = False
    dj.config['custom'] = {
        'database.prefix': (os.environ.get('DATABASE_PREFIX')
                            or dj.config['custom']['database.prefix'])}
    return


@pytest.fixture
def pipeline():
    """ Loads workflow_trial.pipeline lab, session, subject"""
    from workflow_trial import pipeline

    yield {'event': pipeline.event,
           'trial': pipeline.trial,
           'subject': pipeline.subject,
           'session': pipeline.session,
           'lab': pipeline.lab}

    if _tear_down:
        pipeline.event.BehaviorEvent.delete()
        pipeline.trial.Trial.delete()
        pipeline.subject.Subject.delete()
        pipeline.session.Session.delete()
        pipeline.lab.Lab.delete()


# Subject data and ingestion
@pytest.fixture
def subjects_csv():
    """ Create a 'subjects.csv' file"""
    subject_content = ["subject,sex,subject_birth_date,subject_description,"
                       + "death_date,cull_method",
                       "subject5,F,2020-01-01 00:00:01,rich,"
                       + "2020-10-02 00:00:01,natural causes",
                       "subject6,M,2020-01-01 00:00:01,manuel,"
                       + "2020-10-03 00:00:01,natural causes"]
    subject_csv_path = pathlib.Path('./tests/user_data/subject/subjects.csv')
    write_csv(subject_content, subject_csv_path)

    yield subject_content, subject_csv_path
    subject_csv_path.unlink()


@pytest.fixture
def ingest_subjects(pipeline, subjects_csv):
    """From workflow_trial ingest.py, import ingest_subjects, run"""
    from workflow_trial.ingest import ingest_subjects
    _, subject_csv_path = subjects_csv
    ingest_subjects(subject_csv_path=subject_csv_path)
    return


# Session data and ingestion
@pytest.fixture
def sessions_csv():
    """ Create a 'sessions.csv' file"""
    session_csv_path = pathlib.Path('./tests/user_data/session/sessions.csv')
    session_content = ["subject,session_datetime,session_dir,session_note",
                       "subject5,2020-04-15 11:16:38,/subject5/session1,"
                       + "'Successful data collection, no notes'",
                       "subject6,2021-06-02 14:04:22,/subject6/session1,"
                       + "'Ambient temp abnormally low'"]
    write_csv(session_content, session_csv_path)

    yield session_content, session_csv_path
    session_csv_path.unlink()


@pytest.fixture
def ingest_sessions(ingest_subjects, sessions_csv):
    """From workflow_trial ingest.py, import ingest_sessions, run"""
    from workflow_trial.ingest import ingest_sessions
    _, session_csv_path = sessions_csv
    ingest_sessions(session_csv_path=session_csv_path)
    return

''' TO DO
- Add csv and ingestion fixtures for config params and recordings
'''
