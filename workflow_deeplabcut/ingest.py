# from pathlib import Path
import csv
import ruamel.yaml as yaml
from element_interface.utils import find_full_path, ingest_csv_to_table

from .pipeline import subject, session, train, model
from .paths import get_dlc_root_data_dir


def ingest_subjects(
    subject_csv_path="./user_data/subjects.csv",
    skip_duplicates=True,
    verbose=True,
):
    """
    Inserts data from ./user_data/subject.csv into corresponding subject schema tables

    :param subject_csv_path:     relative path of subject csv
    :param skip_duplicates=True: datajoint insert function param
    """
    csvs = [subject_csv_path]
    tables = [subject.Subject()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_sessions(
    session_csv_path="./user_data/sessions.csv", skip_duplicates=True, verbose=True
):
    """
    Ingests to session schema from ./user_data/sessions.csv
    """
    csvs = [session_csv_path, session_csv_path, session_csv_path]
    tables = [session.Session(), session.SessionDirectory(), session.SessionNote()]

    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates)


def ingest_train_params(config_params_csv_path, verbose=True):
    """Use provided path to load TrainingParamSet with relative path to config.yaml"""
    if verbose:
        previous_length = len(train.TrainingParamSet.fetch())
    with open(config_params_csv_path, newline="") as f:
        config_csv = list(csv.DictReader(f, delimiter=","))
    for line in config_csv:
        paramset_idx = line.pop("paramset_idx")
        paramset_desc = line.pop("paramset_desc")
        config_path = find_full_path(get_dlc_root_data_dir(), line.pop("config_path"))
        assert config_path.exists(), f"Could not find config_path: {config_path}"
        with open(config_path, "rb") as y:
            params = yaml.safe_load(y)
        params.update({**line})

        train.TrainingParamSet.insert_new_params(
            paramset_idx=paramset_idx, paramset_desc=paramset_desc, params=params
        )
    if verbose:
        insert_length = len(train.TrainingParamSet.fetch()) - previous_length
        print(
            f"\n---- Inserting {insert_length} entry(s) into #model_training_param_set "
            + "----"
        )


def ingest_train_vids(train_video_csv_path, skip_duplicates=True, verbose=False):
    """Use provided CSV to insert into train.VideoSet and train.VideoSet.File"""
    csvs = [train_video_csv_path, train_video_csv_path]
    tables = [train.VideoSet(), train.VideoSet.File()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_model_vids(model_video_csv_path, skip_duplicates=True, verbose=False):
    """Use provided CSV to insert into model.VideoRecording and VideoRecording.File"""
    csvs = [model_video_csv_path, model_video_csv_path]
    tables = [model.VideoRecording(), model.VideoRecording.File()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_dlc_items(
    config_params_csv_path="./user_data/config_params.csv",
    train_video_csv_path="./user_data/train_videosets.csv",
    model_video_csv_path="./user_data/model_videos.csv",
    skip_duplicates=True,
    verbose=True,
):
    """
    Ingests to DLC schema from CSVs

    :param config_params_csv_path: csv path for model training config and parameters
    :param train_video_csv_path: csv path for list of training videosets
    :param model_csv_path: csv path for list of modeling videos for pose estimation
    """
    ingest_train_params(config_params_csv_path=config_params_csv_path, verbose=verbose)
    ingest_train_vids(
        train_video_csv_path=train_video_csv_path,
        skip_duplicates=skip_duplicates,
        verbose=verbose,
    )
    ingest_model_vids(
        model_video_csv_path=model_video_csv_path,
        skip_duplicates=skip_duplicates,
        verbose=verbose,
    )


if __name__ == "__main__":
    ingest_subjects()
    ingest_sessions()
    ingest_dlc_items()
