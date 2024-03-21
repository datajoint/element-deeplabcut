import os
from pathlib import Path
import datajoint as dj
import pytest


logger = dj.logger
_tear_down = True

# ---------------------- FIXTURES ----------------------


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
        }
    )
    os.environ["DATABASE_PREFIX"] = "test_"
    return


@pytest.fixture(autouse=True, scope="session")
def pipeline():
    from . import tutorial_pipeline as pipeline

    yield {
        "lab": pipeline.lab,
        "subject": pipeline.subject,
        "session": pipeline.session,
        "model": pipeline.model,
        "train": pipeline.train,
        "Device": pipeline.Device
    }

    if _tear_down:
        pipeline.model.schema.drop()
        pipeline.train.schema.drop()
        pipeline.session.schema.drop()
        pipeline.subject.schema.drop()
        pipeline.lab.schema.drop()


@pytest.fixture(scope="session")
def insert_upstreams(pipeline):
    subject = pipeline["subject"]
    session = pipeline["session"]
    model = pipeline["model"]

    subject.Subject.insert1(
        dict(
            subject="subject6",
            sex="F",
            subject_birth_date="2020-01-01",
            subject_description="hneih_E105",
        ),
        skip_duplicates=True,
    )

    session_keys = [
        dict(subject="subject6", session_datetime="2021-06-02 14:04:22"),
        dict(subject="subject6", session_datetime="2021-06-03 14:43:10"),
    ]

    session.Session.insert(session_keys, skip_duplicates=True)

    recording_key = {
        "subject": "subject6",
        "session_datetime": "2021-06-02 14:04:22",
        "recording_id": "1",
    }
    model.VideoRecording.insert1(
        {**recording_key, "device": "Camera1"}, skip_duplicates=True
    )
    
    video_files = [
    "./example_data/inbox/from_top_tracking-DataJoint-2023-10-11/videos/train1.mp4"
    ]

    model.VideoRecording.File.insert(
        [{**recording_key, "file_id": v_idx, "file_path": Path(f)}
        for v_idx, f in enumerate(video_files)], skip_duplicates=True
    )

    yield

    if _tear_down:
        subject.Subject.delete()


@pytest.fixture(scope="session")
def recording_info(pipeline, insert_upstreams):
    model = pipeline["model"]
    model.RecordingInfo.populate()

    yield

    if _tear_down:
        model.RecordingInfo.delete()


@pytest.fixture(scope="session")
def insert_dlc_model(pipeline):
    model = pipeline["model"]

    if not model.Model & {"model_name": "from_top_tracking_model_test"}:
        config_file_rel = "from_top_tracking-DataJoint-2023-10-11/config.yaml"

        model.Model.insert_new_model(
        model_name="from_top_tracking_model_test",
        dlc_config=config_file_rel,
        shuffle=1,
        trainingsetindex=0,
        model_description="Model in example data: from_top_tracking model",
        prompt=False
    )

    yield

    if _tear_down:
        model.Model.delete()
    

@pytest.fixture(scope="session")
def insert_pose_estimation_task(pipeline, recording_info, insert_dlc_model):
    model = pipeline["model"]

    recording_key = {
        "subject": "subject6",
        "session_datetime": "2021-06-02 14:04:22",
        "recording_id": "1",
    }
    task_key = {**recording_key, "model_name": "from_top_tracking_model_test"}
    
    model.PoseEstimationTask.insert1(
        {
            **task_key,
            "task_mode": "load",
            "pose_estimation_output_dir": "from_top_tracking-DataJoint-2023-10-11/videos/device_1_recording_1_model_from_top_tracking_100000_maxiters",
        }
    )

    yield

    if _tear_down:
        model.PoseEstimationTask.delete()


@pytest.fixture(scope="session")
def pose_estimation(pipeline, insert_pose_estimation_task):
    model = pipeline["model"]

    model.PoseEstimation.populate()

    yield

    if _tear_down:
        model.PoseEstimation.delete()
