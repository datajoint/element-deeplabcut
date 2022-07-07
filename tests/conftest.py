import os
import sys
import pytest
from pathlib import Path
from contextlib import nullcontext
from element_deeplabcut.model import str_to_bool
import datajoint as dj
from element_interface.utils import find_full_path
from workflow_deeplabcut.paths import get_dlc_root_data_dir
from workflow_deeplabcut.ingest import (
    ingest_subjects,
    ingest_sessions,
    ingest_train_params,
    ingest_train_vids,
    ingest_model_vids,
    ingest_model,
)

__all__ = [
    "ingest_subjects",
    "ingest_sessions",
    "ingest_train_params",
    "ingest_train_vids",
    "ingest_model_vids",
]

# ---------------------- CONSTANTS ---------------------

test_data_project = "from_top_tracking"
inference_vid = f"{test_data_project}/videos/test.mp4"
inf_vid_short = f"{test_data_project}/videos/test-2s.mp4"
model_name = "FromTop-latest"


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

    verbose = str_to_bool(request.config.getoption("--dj-verbose"))
    _tear_down = str_to_bool(request.config.getoption("--dj-teardown"))
    test_user_data_dir = Path(request.config.getoption("--dj-datadir"))
    test_user_data_dir.mkdir(exist_ok=True)

    if verbose:
        verbose_context = nullcontext()
    else:
        verbose_context = QuietStdOut()

    yield verbose_context


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

    dj.config.update(
        {
            "safemode": False,
            "database.host": os.environ.get("DJ_HOST") or dj.config["database.host"],
            "database.password": os.environ.get("DJ_PASS")
            or dj.config["database.password"],
            "database.user": os.environ.get("DJ_USER") or dj.config["database.user"],
            "custom": {
                "database.prefix": os.environ.get("DATABASE_PREFIX")
                or dj.config["custom"]["database.prefix"],
                "dlc_root_data_dir": os.environ.get("DLC_ROOT_DATA_DIR")
                or dj.config["custom"]["dlc_root_data_dir"],
            },
        }
    )

    return


@pytest.fixture()
def test_data(dj_config):
    """Load demo data. Try local path. Try DJArchive w/either os environ or config"""
    try:
        test_data_dir = find_full_path(get_dlc_root_data_dir(), test_data_project)
    except FileNotFoundError:
        try:  # prefer from os env for docker testing
            djarchive_from_os = {
                "djarchive.endpoint": os.environ["DJARCHIVE_CLIENT_ENDPOINT"],
                "djarchive.bucket": os.environ["DJARCHIVE_CLIENT_BUCKET"],
                "djarchive.access_key": os.environ["DJARCHIVE_CLIENT_ACCESSKEY"],
                "djarchive.secret_key": os.environ["DJARCHIVE_CLIENT_SECRETKEY"],
            }
            dj.config["custom"].update(djarchive_from_os)
        except KeyError as e:
            if not all(  # if not in env, permit from config
                [
                    k in dj.config["custom"].keys()  # if config, assume default bucket
                    for k in ["djarchive.access_key", "djarchive.secret_key"]
                ]
            ):
                raise FileNotFoundError(
                    f"Local: Test data not available from root(s):\n\t"
                    f"{get_dlc_root_data_dir()}"
                    f"DJArchive: Missing environment variables:\n\t{str(e)}"
                    f"DJArchive: Missing config custom variables:\n\t"
                    "djarchive.access_key and/or djarchive.secret_key"
                )
        from workflow_deeplabcut.load_demo_data import download_djarchive_dlc_data

        download_djarchive_dlc_data(get_dlc_root_data_dir()[0])

    else:  # if local version, check for training-dataset dir and full project path
        from deeplabcut.utils.auxiliaryfunctions import read_config

        training_dataset_exists = (test_data_dir / "training-datasets").exists()
        project_path_in_config = (
            True
            if read_config(test_data_dir / "config.yaml").get("project_path", False)
            else False
        )

        if training_dataset_exists and project_path_in_config:  # skip project setup
            return

    with verbose_context:  # Setup - expand relative paths, make a shorter video
        from workflow_deeplabcut.load_demo_data import (
            download_weights,
            setup_bare_project,
            shorten_video,
        )

        download_weights()
        setup_bare_project(project=test_data_project)
        shorten_video(vid_path=inference_vid)

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
        "get_dlc_root_data_dir": get_dlc_root_data_dir,
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
            pipeline.train.TrainingParamSet.delete()


@pytest.fixture(scope="session")
def ingest_csvs(setup, pipeline):
    """For each input, generates csv in test_user_data_dir and ingests in schema"""
    # CSV as list of 3: relevant insert func, filename, content
    all_csvs = [
        [  # 0
            ingest_subjects,
            "subjects.csv",
            [
                "subject,sex,subject_birth_date,subject_description,"
                + "death_date,cull_method",
                "subject6,M,2020-01-01 00:00:01,manuel,2020-10-03 00:00:01,natural",
            ],
        ],
        [  # 1
            ingest_sessions,
            "sessions.csv",
            [
                "subject,session_datetime,session_dir,session_note",
                f"subject6,2021-06-01 13:33:33,{test_data_project}/,Model Training",
                f"subject6,2021-06-02 14:04:22,{test_data_project}/,Test Session",
            ],
        ],
        [  # 2
            ingest_train_params,
            "config_params.csv",
            [
                "paramset_idx,paramset_desc,config_path,shuffle,"
                + "trainingsetindex,filter_type,track_method,"
                + "scorer_legacy,maxiters",
                f"0,{test_data_project},{test_data_project}/config.yaml,1,0,,,False,5",
                "1,OpenField,openfield-Pranav-2018-10-30/config.yaml,1,0,,,False,5",
                "2,Reaching,Reaching-Mackenzie-2018-08-30/config.yaml,1,0,,,False,5",
            ],
        ],
        [  # 3
            ingest_train_vids,
            "train_videosets.csv",
            [
                "video_set_id,file_id,file_path",
                f"0,1,{test_data_project}/labeled-data/train1/CollectedData_DJ.h5",
                f"0,2,{test_data_project}/labeled-data/train2/CollectedData_DJ.h5",
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
        [  # 4
            ingest_model_vids,
            "model_videos.csv",
            [
                "recording_id,subject,session_datetime,file_id,file_path,device,paramset_idx",
                f"1,subject6,2021-06-02 14:04:22,1,{inf_vid_short},Camera1,0",
            ],
        ],
        [
            ingest_model,
            "model_model.csv",
            [
                "model_name,config_relative_path,shuffle,trainingsetindex,paramset_idx,prompt,model_description,params",
                f"{model_name},{test_data_project}/config.yaml,1,0,0,False,FromTop - latest snapshot,{{'snapshotindex':4}}",
            ],
        ],
    ]

    # When not tearing down, and if there's already data in last table, can skip insert
    if len(pipeline["model"].Model()) == 0:
        for csv_info in all_csvs:
            csv_path = test_user_data_dir / csv_info[1]
            write_csv(csv_path, csv_info[2])
            csv_info[0](csv_path, skip_duplicates=True, verbose=verbose)

    yield

    if _tear_down:
        with verbose_context:
            for csv_info in all_csvs:
                csv_path = test_user_data_dir / csv_info[1]
                csv_path.unlink()


@pytest.fixture(scope="session")
def populate_settings():
    yield dict(display_progress=verbose, reserve_jobs=False, suppress_errors=False)


@pytest.fixture()
def training_task(pipeline, ingest_csvs):
    if 0 not in pipeline["train"].TrainingTask.fetch("training_id"):
        pipeline["train"].TrainingTask.insert1(
            {
                "paramset_idx": 0,
                "training_id": 0,
                "video_set_id": 1,
                "project_path": test_data_project,
            },
            skip_duplicates=True,
        )
        with verbose_context:
            print("Added training task")


@pytest.fixture()
def pose_estim_task(pipeline, ingest_csvs):

    key = (pipeline["model"].VideoRecording & "recording_id=1").fetch1("KEY")
    key.update({"model_name": model_name, "task_mode": "trigger"})
    analyze_params = {"save_as_csv": True}

    if 1 not in pipeline["model"].PoseEstimationTask.fetch("recording_id"):
        pipeline["model"].PoseEstimationTask.insert_estimation_task(
            key, params=analyze_params
        )
        with verbose_context:
            print("Added estimation task")
