"""Run each populate command - for computed/imported tables
"""

import logging
from .conftest import find_full_path, get_dlc_root_data_dir

from time import time
import pytest
import logging


def test_training(setup, test_data, pipeline, populate_settings, training_task):
    verbose_context, verbose = setup
    train = pipeline["train"]

    # Run training
    with verbose_context:
        train.ModelTraining.populate(**populate_settings)

    if not verbose:  # train command in DLC resets logger
        logging.getLogger("deeplabcut").setLevel(logging.WARNING)

    project_path = find_full_path(
        get_dlc_root_data_dir(), train.TrainingTask.fetch("project_path", limit=1)[0]
    )

    # Examine results
    snapshot_path = sorted(project_path.rglob("snapshot-5.index"))  # 5 bc maxiter
    assert snapshot_path, f"Counldn't find trained snapshot-5.index in {project_path}"
    snapshot_filetime = snapshot_path[0].stat().st_ctime
    assert time() == pytest.approx(  # approx equal, within 2nd delta
        snapshot_filetime, 1e4  # 1e4s is 2.7 hour delta
    ), f"Training file is old: {snapshot_path[0]}"


def test_record_info(setup, test_data, pipeline, populate_settings, ingest_csvs):
    verbose_context, _ = setup
    model = pipeline["model"]

    # Run recording info populate
    with verbose_context:
        model.RecordingInfo.populate(**populate_settings)

    # Check success
    assert len(model.RecordingInfo()), f"Recording info didn't populate"
    fps = model.RecordingInfo.fetch("fps", limit=1)[0]
    assert fps == 60, f"Test video fps didn't match 60: {fps}"


def test_model_eval(
    setup, test_data, pipeline, populate_settings, ingest_csvs, revert_checkpoint
):
    """Test model evaluation"""
    verbose_context, _ = setup
    model = pipeline["model"]

    # Run model evaluation
    with verbose_context:
        model.ModelEvaluation.populate(**populate_settings)

    # Check results. First appropriate number of iters, Next results recent
    iter_eval = model.ModelEvaluation.fetch("train_iterations", limit=1)[0]
    assert iter_eval > 5, f"Did not eval prev model. Iterations eval'd {iter_eval}"

    eval_file = list(
        find_full_path(
            get_dlc_root_data_dir(), model.Model.fetch("project_path", limit=1)[0]
        ).rglob(f"*{iter_eval}-results.csv")
    )[0]
    eval_time = eval_file.stat().st_ctime
    assert time() == pytest.approx(eval_time, 1e4), f"Eval result is old: {eval_file}"


def test_pose_estim(setup, test_data, pipeline, pose_output_path):
    """Test pose estimation"""
    output_path = pose_output_path

    # Check output path, and that results files exist
    assert output_path.exists(), f"Missing output of `infer_output_dir`: {output_path}"
    assert (
        len(list(output_path.glob("test-2s*"))) == 3
    ), f"Should be 3 output files in  {output_path}"


def test_get_trajectory(get_trajectory):
    data = get_trajectory
    assert data.shape[1] == 12, f"Expected 12 columns. Found\n{data.columns}"

    names = ["x mean", "y mean", "z mean", "liklihood mean"]
    means = data.mean(axis=0)
    expected = [231, 250, 0, 1]
    delta = [10, 10, 0, 0.01]
    # averaging across body parts: zip x/y coords, means, and permissible delta
    for n, m, e, d in zip(names, means, expected, delta):
        assert m == pytest.approx(  # assert mean is within delta of expected value
            e, d
        ), f"Issues with data for {n}. Expected {e} ±{d}, Found {m}"
