"""Run each populate command - for computed/imported tables
"""

from .conftest import verbose_context, find_full_path
from time import time
import pytest


def test_training(pipeline, populate_settings, training_task):
    train = pipeline["train"]
    roots = pipeline["get_dlc_root_data_dir"]
    with verbose_context:
        train.ModelTraining.populate(**populate_settings)
    project_path = find_full_path(
        roots, train.TrainingTask.fetch("project_path", limit=1)[0]
    )
    snapshot_path = sorted(project_path.rglob("snapshot-5.index"))
    assert snapshot_path, f"Counldn't find snapshot-5.index in {project_path}"
    filetime = snapshot_path[0].stat().st_ctime
    assert time() == pytest.approx(  # approx equal, withing 2nd arg delta
        filetime, 1e4  # 1e4s is 2.7 hour delta
    ), f"Training file is old{snapshot_path[0]}"


def test_record_info(pipeline, populate_settings, ingest_csvs):
    model = pipeline["model"]
    with verbose_context:
        model.RecordingInfo.populate(**populate_settings)
    assert len(model.RecordingInfo()), f"Recording info didn't populate"
    fps = model.RecordingInfo.fetch("fps", limit=1)[0]
    assert fps == 60, f"Test video fps didn't match 60: {fps}"


def test_model_eval(pipeline, populate_settings, ingest_csvs):
    with verbose_context:
        pipeline["model"].ModelEvaluation.populate(**populate_settings)
    import pdb

    pdb.set_trace()


def test_pose_estim(pipeline, populate_settings, pose_estim_task):
    with verbose_context:
        pipeline["model"].PoseEstimation.populate(**populate_settings)
    import pdb

    pdb.set_trace()
