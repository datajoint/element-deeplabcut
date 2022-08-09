import csv
from pathlib import Path
import ruamel.yaml as yaml
from element_deeplabcut.model import str_to_bool
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

    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_train_params(config_params_csv_path, skip_duplicates=True, verbose=True):
    """Use provided path to load TrainingParamSet with relative path to config.yaml"""
    if verbose:
        previous_length = len(train.TrainingParamSet.fetch())
    with open(config_params_csv_path, newline="") as f:
        config_csv = list(csv.DictReader(f, delimiter=","))
    for line in config_csv:
        paramset_idx = line.pop("paramset_idx")
        if skip_duplicates and (
            paramset_idx in list(train.TrainingParamSet.fetch("paramset_idx"))
        ):
            continue
        paramset_desc = line.pop("paramset_desc")
        try:
            config_path = find_full_path(
                get_dlc_root_data_dir(), line.pop("config_path")
            )
        except FileNotFoundError as e:
            if verbose:
                print(f"Skipping {paramset_desc}:\n\t{e}")
            continue
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


def ingest_train_vids(train_video_csv_path, verbose=False, **kwargs):
    """Use provided CSV to insert into train.VideoSet and train.VideoSet.File"""
    csvs = [train_video_csv_path, train_video_csv_path]
    tables = [train.VideoSet(), train.VideoSet.File()]
    # With current CSV organization, must skip vids, as primary key is duplicated
    ingest_csv_to_table(csvs, tables, skip_duplicates=True, verbose=verbose)


def ingest_model_vids(model_video_csv_path, skip_duplicates=True, verbose=False):
    """Use provided CSV to insert into model.VideoRecording and VideoRecording.File"""
    csvs = [model_video_csv_path, model_video_csv_path]
    tables = [model.VideoRecording(), model.VideoRecording.File()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_model(model_model_csv_path, skip_duplicates=True, verbose=False):
    """Use provided CSV to insert into model.Model table"""
    # NOTE: not included in ingest_dlc_items because not yet included in notebooks

    with open(model_model_csv_path, newline="") as f:
        data = list(csv.DictReader(f, delimiter=","))

    if verbose:
        prev_len = len(model.Model())

    for model_row in data:  # replace relative path with full path
        model_row["dlc_config"] = find_full_path(
            get_dlc_root_data_dir(), model_row.pop("config_relative_path")
        )
        model_row["project_path"] = Path(model_row["dlc_config"]).parent
        model_row["prompt"] = str_to_bool(model_row["prompt"])
        model_name = model_row["model_name"]
        if skip_duplicates and model_name in model.Model.fetch("model_name"):
            if verbose:
                print(f"Skipping model, name already exists: {model_name}")
            continue
        else:
            model.Model.insert_new_model(**model_row)

    if verbose:
        insert_len = len(model.Model()) - prev_len
        print(f"\n---- Inserting {insert_len} entry(s) into model ----")


def ingest_dlc_items(
    config_params_csv_path="./user_data/config_params.csv",
    train_video_csv_path="./user_data/train_videosets.csv",
    model_video_csv_path="./user_data/model_videos.csv",
    skip_duplicates=False,
    verbose=True,
):
    """
    Ingests to DLC schema from CSVs

    :param config_params_csv_path: csv path for model training config and parameters
    :param train_video_csv_path: csv path for list of training videosets
    :param model_csv_path: csv path for list of modeling videos for pose estimation
    """
    ingest_train_params(
        config_params_csv_path=config_params_csv_path,
        skip_duplicates=skip_duplicates,
        verbose=verbose,
    )
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
