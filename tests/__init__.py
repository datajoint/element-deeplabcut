""" deeplabcut
fresh docker:
    docker run --name wf-sess -p 3306:3306 -e \
    MYSQL_ROOT_PASSWORD=tutorial datajoint/mysql
dependencies: pip install pytest pytest-cov
run all tests:
    pytest -sv --cov-report term-missing --cov=workflow-session \
    -p no:warnings tests/
run one test, debug:
    pytest [above options] --pdb tests/tests_name.py -k function_name
"""

import os
import sys
import pytest
import pathlib
import datajoint as dj

# ------------------- SOME CONSTANTS -------------------

_tear_down = True
verbose = False

test_user_data_dir = pathlib.Path("./tests/user_data")
test_user_data_dir.mkdir(exist_ok=True)

# ------------------ GENERAL FUCNTION ------------------


def write_csv(content, path):
    """
    General function for writing strings to lines in CSV
    :param path: pathlib PosixPath
    :param content: list of strings, each as row of CSV
    """
    with open(path, "w") as f:
        for line in content:
            f.write(line + "\n")


class QuietStdOut:
    """If verbose set to false, used to quiet tear_down table.delete prints"""

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


# ------------------- FIXTURES -------------------


@pytest.fixture(autouse=True)
def dj_config():
    """If dj_local_config exists, load"""
    if pathlib.Path("./dj_local_conf.json").exists():
        dj.config.load("./dj_local_conf.json")
    dj.config["safemode"] = False
    dj.config["database.host"] = os.environ.get("DJ_HOST") or dj.config["database.host"]
    dj.config["database.password"] = (
        os.environ.get("DJ_PASS") or dj.config["database.password"]
    )
    dj.config["database.user"] = os.environ.get("DJ_USER") or dj.config["database.user"]
    dj.config["custom"] = {
        "database.prefix": (
            os.environ.get("DATABASE_PREFIX") or dj.config["custom"]["database.prefix"]
        )
    }
    return


@pytest.fixture
def pipeline():
    """Loads workflow_deeplabcut.pipeline lab, session, subject, dlc"""
    from workflow_deeplabcut import pipeline

    yield {
        "dlc": pipeline.dlc,
        "subject": pipeline.subject,
        "session": pipeline.session,
        "lab": pipeline.lab,
    }

    if _tear_down:
        if verbose:
            pipeline.dlc.VideoRecording.delete()
            pipeline.subject.Subject.delete()
            pipeline.session.Session.delete()
            pipeline.lab.Lab.delete()
        else:
            with QuietStdOut():
                pipeline.dlc.VideoRecording.delete()
                pipeline.subject.Subject.delete()
                pipeline.session.Session.delete()
                pipeline.lab.Lab.delete()


#  Subject data and ingestion
@pytest.fixture
def subjects_csv():
    """Create a 'subjects.csv' file"""
    subject_content = [
        "subject,sex,subject_birth_date,subject_description,"
        + "death_date,cull_method",
        "subject5,F,2020-01-01 00:00:01,rich," + "2020-10-02 00:00:01,natural causes",
        "subject6,M,2020-01-01 00:00:01,manuel," + "2020-10-03 00:00:01,natural causes",
    ]
    subject_csv_path = pathlib.Path("./tests/user_data/subjects.csv")
    write_csv(subject_content, subject_csv_path)

    yield subject_content, subject_csv_path
    subject_csv_path.unlink()


@pytest.fixture
def ingest_subjects(pipeline, subjects_csv):
    """From workflow_deeplabcut ingest.py, import ingest_subjects, run"""
    from workflow_deeplabcut.ingest import ingest_subjects

    _, subject_csv_path = subjects_csv
    ingest_subjects(subject_csv_path=subject_csv_path)
    return


# Session data and ingestion
@pytest.fixture
def sessions_csv():
    """Create a 'sessions.csv' file"""
    session_csv_path = pathlib.Path("./tests/user_data/sessions.csv")
    session_content = [
        "subject,session_datetime,session_dir,session_note",
        "subject,session_datetime,session_dir,session_note",
        "subject5,2020-04-15 11:16:38,example-dir/subject5/,"
        + "Successful data collection. No notes",
        "subject6,2021-06-02 14:04:22,example-dir/subject6/," + "Model Training Session"
        "subject6,2021-06-03 14:04:22,example-dir/subject6/,Test Session",
    ]
    write_csv(session_content, session_csv_path)

    yield session_content, session_csv_path
    session_csv_path.unlink()


@pytest.fixture
def ingest_sessions(ingest_subjects, sessions_csv):
    """From workflow_deeplabcut ingest.py, import ingest_sessions, run"""
    from workflow_deeplabcut.ingest import ingest_sessions

    _, session_csv_path = sessions_csv
    ingest_sessions(session_csv_path=session_csv_path)
    return


@pytest.fixture
def recordings_csv():
    """Create a 'recordings.csv file"""
    recording_csv_path = pathlib.Path("./tests/user_data/recordings.csv")
    recording_content = [
        "recording_id,subject,session_datetime,recording_start_time,"
        + "file_path,camera_id,paramset_idx",
        "1,subject6,2021-06-02 14:04:22,2021-06-02 14:07:00,"
        + "openfield-Pranav-2018-10-30/videos/m3v1mp4.mp4,1,0",
        "2,subject6,2021-06-03 14:04:22,2021-06-04 14:07:00,"
        + "openfield-Pranav-2018-10-30/videos/m3v1mp4-copy.mp4,1,0",
        "3,subject5,2020-04-15 11:16:38,2020-04-15 11:17:00,"
        + "Reaching-Mackenzie-2018-08-30/videos/reachingvideo1.avi,1,1",
    ]
    write_csv(recording_content, recording_csv_path)

    yield recording_content, recording_csv_path
    recording_csv_path.unlink()


@pytest.fixture
def config_params_csv():
    """Create a 'config_params.csv file"""
    config_params_csv_path = pathlib.Path("./tests/user_data/config_params.csv")
    config_params_content = [
        "paramset_idx,paramset_desc,config_path,shuffle,"
        + "trainingsetindex,filter_type,track_method,"
        + "scorer_legacy,maxiters",
        "1,OpenField,openfield-Pranav-2018-10-30/config.yaml,1,0,," + ",False,5",
        "2,Reaching,Reaching-Mackenzie-2018-08-30/config.yaml,1,0," + ",,False,5",
        "3,ExtraExample,Example/config.yaml,0,0,median,ellipse," + "False,1",
    ]
    write_csv(config_params_content, config_params_csv_path)

    yield config_params_content, config_params_csv_path
    config_params_csv_path.unlink()


@pytest.fixture
def ingest_dlc_items(
    ingest_subjects, ingest_sessions, recordings_csv, config_params_csv
):
    """From workflow_deeplabcut ingest.py, import ingest_dlc_items, run"""
    from workflow_deeplabcut.ingest import ingest_dlc_items

    _, recording_csv_path = recordings_csv
    _, config_params_csv_path = config_params_csv
    ingest_dlc_items(
        config_params_csv_path=config_params_csv_path,
        recording_csv_path=recording_csv_path,
    )
    return
