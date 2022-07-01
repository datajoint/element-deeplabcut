import os, sys
import pytest
from pathlib import Path
from contextlib import nullcontext
from distutils.util import strtobool
import datajoint as dj
from workflow_deeplabcut.ingest import (
    ingest_subjects,
    ingest_sessions,
    ingest_train_params,
    ingest_train_vids,
    ingest_model_vids,
)

__all__ = [
    "ingest_subjects",
    "ingest_sessions",
    "ingest_train_params",
    "ingest_train_vids",
    "ingest_model_vids",
]

# ---------------------- CONSTANTS ---------------------


def pytest_addoption(parser):
    """
    Permit constants when calling pytest at commandline e.g., pytest --dj-verbose False

    Parameters
    ----------
    --dj-verbose (bool):  Default True. Pass print statements from Elements.
    --dj-teardown (bool): Default True. Delete pipeline on close.
    --dj-datadir (str):  Default ./tests/user_data. Relative path of test CSV data.
    """
    parser.addoption(
        "--dj-verbose",
        action="store",
        default="True",
        help="Verbose for dj items: True or False",
        choices=("True", "False"),
    )
    parser.addoption(
        "--dj-teardown",
        action="store",
        default="True",
        help="Verbose for dj items: True or False",
        choices=("True", "False"),
    )
    parser.addoption(
        "--dj-datadir",
        action="store",
        default="./tests/user_data",
        help="Relative path for saving tests data",
    )


@pytest.fixture(scope="session")
def setup(request):
    """Take passed commandline variables, set as global"""
    global verbose, _tear_down, test_user_data_dir, verbose_context

    verbose = strtobool(request.config.getoption("--dj-verbose"))
    _tear_down = strtobool(request.config.getoption("--dj-teardown"))
    test_user_data_dir = Path(request.config.getoption("--dj-datadir"))
    test_user_data_dir.mkdir(exist_ok=True)

    if verbose:
        verbose_context = nullcontext()
    else:
        verbose_context = QuietStdOut()


# ------------------ GENERAL FUCNTION ------------------


def write_csv(path, content):
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
        os.environ["DJ_LOG_LEVEL"] = "WARNING"
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.environ["DJ_LOG_LEVEL"] = "INFO"
        sys.stdout.close()
        sys.stdout = self._original_stdout


# ------------------- FIXTURES -------------------


@pytest.fixture(autouse=True, scope="session")
def dj_config():
    """If dj_local_config exists, load"""
    if Path("./dj_local_conf.json").exists():
        dj.config.load("./dj_local_conf.json")
    dj.config["safemode"] = False
    dj.config["database.host"] = os.environ.get("DJ_HOST") or dj.config["database.host"]
    dj.config["database.password"] = (
        os.environ.get("DJ_PASS") or dj.config["database.password"]
    )
    dj.config["database.user"] = os.environ.get("DJ_USER") or dj.config["database.user"]
    dj.config["custom"] = {
        "database.prefix": os.environ.get("DATABASE_PREFIX")
        or dj.config["custom"]["database.prefix"],
        "dlc_root_data_dir": os.environ.get("DLC_ROOT_DATA_DIR")
        or dj.config["custom"]["dlc_root_data_dir"],
    }
    return


@pytest.fixture(scope="session")
def pipeline(setup):
    """Loads workflow_deeplabcut.pipeline lab, session, subject, dlc"""
    with verbose_context:
        from workflow_deeplabcut import pipeline

    yield {
        "train": pipeline.train,
        "model": pipeline.model,
        "subject": pipeline.subject,
        "session": pipeline.session,
        "lab": pipeline.lab,
    }
    if _tear_down:
        with verbose_context:
            pipeline.model.PoseEstimationTask.delete()
            pipeline.model.VideoRecording.delete()
            pipeline.model.Model.delete()
            pipeline.train.TrainingTask.delete()
            pipeline.train.VideoSet.delete()
            pipeline.subject.Subject.delete()
            pipeline.session.Session.delete()
            pipeline.lab.Lab.delete()
    with verbose_context:
        # even when not teardown, because does not have skip-dupe option.
        pipeline.train.TrainingParamSet.delete()


# CSV filename, content, relevant insert func
@pytest.fixture(
    scope="session",
    params=[
        [
            ingest_subjects,
            "subjects.csv",
            [
                "subject,sex,subject_birth_date,subject_description,"
                + "death_date,cull_method",
                "subject5,F,2020-01-01 00:00:01,rich,2020-10-02 00:00:01,natural",
                "subject6,M,2020-01-01 00:00:01,manuel,2020-10-03 00:00:01,natural",
            ],
        ],
        [
            ingest_sessions,
            "sessions.csv",
            [
                "subject,session_datetime,session_dir,session_note",
                "subject5,2020-04-15 11:16:38,example-dir/subject5/,"
                + "Successful data collection. No notes",
                "subject6,2021-06-02 14:04:22,example-dir/subject6/,Model Training"
                "subject6,2021-06-03 14:04:22,example-dir/subject6/,Test Session",
            ],
        ],
        [
            ingest_train_params,
            "config_params.csv",
            [
                "paramset_idx,paramset_desc,config_path,shuffle,"
                + "trainingsetindex,filter_type,track_method,"
                + "scorer_legacy,maxiters",
                "1,OpenField,openfield-Pranav-2018-10-30/config.yaml,1,0,,,False,5",
                "2,Reaching,Reaching-Mackenzie-2018-08-30/config.yaml,1,0,,,False,5",
                "3,ExtraExample,Example/config.yaml,0,0,median,ellipse,False,1",
            ],
        ],
        [
            ingest_train_vids,
            "train_videosets.csv",
            [
                "video_set_id,file_id,file_path",
                "1,1,openfield-Pranav-2018-10-30/labeled-data/m4s1/CollectedData_Pranav.h5",
                "1,2,openfield-Pranav-2018-10-30/labeled-data/m4s1/CollectedData_Pranav.csv",
                "1,3,openfield-Pranav-2018-10-30/labeled-data/m4s1/img0000.png",
                "1,4,openfield-Pranav-2018-10-30/videos/m3v1mp4.mp4",
                "2,1,Reaching-Mackenzie-2018-08-30/labeled-data/reachingvideo1/CollectedData_Mackenzie.csv",
                "2,2,Reaching-Mackenzie-2018-08-30/labeled-data/reachingvideo1/CollectedData_Mackenzie.h5",
                "2,3,Reaching-Mackenzie-2018-08-30/labeled-data/reachingvideo1/img005.png",
                "2,4,Reaching-Mackenzie-2018-08-30/videos/reachingvideo1.avi",
            ],
        ],
        [
            ingest_model_vids,
            "model_videos.csv",
            [
                "recording_id,subject,session_datetime,file_id,file_path,equipment,paramset_idx",
                "2,subject6,2021-06-03 14:43:10,1,openfield-Pranav-2018-10-30/videos/m3v1mp4-copy.mp4,Camera1,0",
                "3,subject5,2020-04-15 11:16:38,1,Reaching-Mackenzie-2018-08-30/videos/reachingvideo1-copy.avi,Camera1,1",
            ],
        ],
    ],
)
def csvs(request, setup):
    """For each above, generates csv in test_user_data_dir and ingests in schema"""

    csv_path = test_user_data_dir / request.param[1]
    if not csv_path.exists():
        write_csv(csv_path, request.param[2])
    request.param[0](csv_path)
    yield request.param[1], csv_path
    if _tear_down:
        csv_path.unlink()


#  Subject data and ingestion
@pytest.fixture
def subjects_csv():
    """Create a 'subjects.csv' file"""
    subject_content = [
        "subject,sex,subject_birth_date,subject_description,"
        + "death_date,cull_method",
        "subject5,F,2020-01-01 00:00:01,rich,2020-10-02 00:00:01,natural",
        "subject6,M,2020-01-01 00:00:01,manuel,2020-10-03 00:00:01,natural",
    ]
    subject_csv_path = Path("./tests/user_data/subjects.csv")
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
    session_csv_path = Path("./tests/user_data/sessions.csv")
    session_content = [
        "subject,session_datetime,session_dir,session_note",
        "subject,session_datetime,session_dir,session_note",
        "subject5,2020-04-15 11:16:38,example-dir/subject5/,"
        + "Successful data collection. No notes",
        "subject6,2021-06-02 14:04:22,example-dir/subject6/,Model Training Session"
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
    recording_csv_path = Path("./tests/user_data/recordings.csv")
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
    config_params_csv_path = Path("./tests/user_data/config_params.csv")
    config_params_content = [
        "paramset_idx,paramset_desc,config_path,shuffle,"
        + "trainingsetindex,filter_type,track_method,"
        + "scorer_legacy,maxiters",
        "1,OpenField,openfield-Pranav-2018-10-30/config.yaml,1,0,,,False,5",
        "2,Reaching,Reaching-Mackenzie-2018-08-30/config.yaml,1,0,,,False,5",
        "3,ExtraExample,Example/config.yaml,0,0,median,ellipse,False,1",
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
