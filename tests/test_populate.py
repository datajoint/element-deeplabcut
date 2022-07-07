"""Run each populate command - for computed/imported tables
"""

from element_deeplabcut.model import get_dlc_root_data_dir
from .conftest import find_full_path

from time import time
import pytest


def test_training(setup, test_data, pipeline, populate_settings, training_task):
    verbose_context = setup
    train = pipeline["train"]
    get_dlc_root_data_dir = pipeline["get_dlc_root_data_dir"]
    with verbose_context:
        train.ModelTraining.populate(**populate_settings)
    project_path = find_full_path(
        get_dlc_root_data_dir(), train.TrainingTask.fetch("project_path", limit=1)[0]
    )
    snapshot_path = sorted(project_path.rglob("snapshot-5.index"))  # 5 bc maxiter
    assert snapshot_path, f"Counldn't find trained snapshot-5.index in {project_path}"
    snapshot_filetime = snapshot_path[0].stat().st_ctime
    assert time() == pytest.approx(  # approx equal, within 2nd delta
        snapshot_filetime, 1e4  # 1e4s is 2.7 hour delta
    ), f"Training file is old: {snapshot_path[0]}"


def test_record_info(setup, test_data, pipeline, populate_settings, ingest_csvs):
    verbose_context = setup
    model = pipeline["model"]
    with verbose_context:
        model.RecordingInfo.populate(**populate_settings)
    assert len(model.RecordingInfo()), f"Recording info didn't populate"
    fps = model.RecordingInfo.fetch("fps", limit=1)[0]
    assert fps == 60, f"Test video fps didn't match 60: {fps}"


def test_model_eval(setup, test_data, pipeline, populate_settings, ingest_csvs):
    """Failing cause setup process establishes resnet not mobilenet"""
    verbose_context = setup
    model = pipeline["model"]

    with verbose_context:
        model.ModelEvaluation.populate(**populate_settings)
    project_path = find_full_path(
        get_dlc_root_data_dir(), model.Model.fetch("project_path", limit=1)[0]
    )
    iter_eval = model.ModelEvaluation.fetch("train_iterations", limit=1)[0]
    assert iter_eval > 5, f"Did not eval prev model. Iterations eval'd {iter_eval}"
    eval_file = list(project_path.rglob(f"*{iter_eval}-results.csv"))[0]
    eval_time = eval_file.stat().st_ctime
    assert time() == pytest.approx(eval_time, 1e4), f"Eval result is old: {eval_file}"


def test_pose_estim(setup, test_data, pipeline, populate_settings, pose_estim_task):
    verbose_context = setup
    model = pipeline["model"]
    with verbose_context:
        model.PoseEstimation.populate(**populate_settings)
    import pdb

    pdb.set_trace()
