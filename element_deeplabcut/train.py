"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""

import datajoint as dj
import inspect
import importlib
import re
from pathlib import Path
import yaml

from element_interface.utils import find_full_path, dict_to_uuid
from .readers import dlc_reader

schema = dj.schema()
_linking_module = None


def activate(
    train_schema_name: str,
    *,
    create_schema: bool = True,
    create_tables: bool = True,
    linking_module: str = None,
):
    """Activate this schema.

    Args:
        train_schema_name (str): schema name on the database server
        create_schema (bool): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (bool): when True (default), create schema tables in the database
                             if they do not yet exist.
        linking_module (str): a module (or name) containing the required dependencies.

    Dependencies:
    Functions:
        get_dlc_root_data_dir(): Returns absolute path for root data director(y/ies)
                                 with all behavioral recordings, as (list of) string(s).
        get_dlc_processed_data_dir(): Optional. Returns absolute path for processed
                                      data. Defaults to session video subfolder.
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'dependency' must be a module's name or a module"
    assert hasattr(
        linking_module, "get_dlc_root_data_dir"
    ), "The linking module must specify a lookup function for a root data directory"

    global _linking_module
    _linking_module = linking_module

    # activate
    schema.activate(
        train_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=_linking_module.__dict__,
    )


# -------------- Functions required by element-deeplabcut ---------------


def get_dlc_root_data_dir() -> list:
    """Pulls relevant func from parent namespace to specify root data dir(s).

    It is recommended that all paths in DataJoint Elements stored as relative
    paths, with respect to some user-configured "root" director(y/ies). The
    root(s) may vary between data modalities and user machines. Returns a full path
    string or list of strings for possible root data directories.
    """
    root_directories = _linking_module.get_dlc_root_data_dir()
    if isinstance(root_directories, (str, Path)):
        root_directories = [root_directories]

    if (
        hasattr(_linking_module, "get_dlc_processed_data_dir")
        and get_dlc_processed_data_dir() not in root_directories
    ):
        root_directories.append(_linking_module.get_dlc_processed_data_dir())

    return root_directories


def get_dlc_processed_data_dir() -> str:
    """Pulls relevant func from parent namespace. Defaults to DLC's project /videos/.

    Method in parent namespace should provide a string to a directory where DLC output
    files will be stored. If unspecified, output files will be stored in the
    session directory 'videos' folder, per DeepLabCut default.
    """
    if hasattr(_linking_module, "get_dlc_processed_data_dir"):
        return _linking_module.get_dlc_processed_data_dir()
    else:
        return get_dlc_root_data_dir()[0]


# ----------------------------- Table declarations ----------------------


@schema
class VideoSet(dj.Manual):
    """Collection of videos included in a given training set.

    Attributes:
        video_set_id (int): Unique ID for collection of videos."""

    definition = """ # Set of vids in training set
    video_set_id: int
    """

    class File(dj.Part):
        """File IDs and paths in a given VideoSet

        Attributes:
            VideoSet (foreign key): VideoSet key.
            file_path ( varchar(255) ): Path to file on disk relative to root."""

        definition = """ # Paths of training files (e.g., labeled pngs, CSV or video)
        -> master
        file_id: int
        ---
        file_path: varchar(255)
        """


@schema
class TrainingParamSet(dj.Lookup):
    """Parameters used to train a model

    Attributes:
        paramset_idx (smallint): Index uniqely identifying paramset.
        paramset_desc ( varchar(128) ): Description of paramset.
        param_set_hash (uuid): Hash identifying this paramset.
        params (longblob): Dictionary of all applicable parameters.
        Note: param_set_hash must be unique."""

    definition = """
    # Parameters to specify a DLC model training instance
    # For DLC ≤ v2.0, include scorer_legacy = True in params
    paramset_idx                  : smallint
    ---
    paramset_desc: varchar(128)
    param_set_hash                : uuid      # hash identifying this parameterset
    unique index (param_set_hash)
    params                        : longblob  # dictionary of all applicable parameters
    """

    required_parameters = ("shuffle", "trainingsetindex")
    skipped_parameters = ("project_path", "video_sets")

    @classmethod
    def insert_new_params(
        cls, paramset_desc: str, params: dict, paramset_idx: int = None
    ):
        """
        Insert a new set of training parameters into dlc.TrainingParamSet.

        Args:
            paramset_desc (str): Description of parameter set to be inserted
            params (dict): Dictionary including all settings to specify model training.
                        Must include shuffle & trainingsetindex b/c not in config.yaml.
                        project_path and video_sets will be overwritten by config.yaml.
                        Note that trainingsetindex is 0-indexed
            paramset_idx (int): optional, integer to represent parameters.
        """

        for required_param in cls.required_parameters:
            assert required_param in params, (
                "Missing required parameter: " + required_param
            )
        for skipped_param in cls.skipped_parameters:
            if skipped_param in params:
                params.pop(skipped_param)

        if paramset_idx is None:
            paramset_idx = (
                dj.U().aggr(cls, n="max(paramset_idx)").fetch1("n") or 0
            ) + 1

        param_dict = {
            "paramset_idx": paramset_idx,
            "paramset_desc": paramset_desc,
            "params": params,
            "param_set_hash": dict_to_uuid(params),
        }
        param_query = cls & {"param_set_hash": param_dict["param_set_hash"]}
        # If the specified param-set already exists
        if param_query:
            existing_paramset_idx = param_query.fetch1("paramset_idx")
            if existing_paramset_idx == int(paramset_idx):  # If existing_idx same:
                return  # job done
        else:
            cls.insert1(param_dict)  # if duplicate, will raise duplicate error


@schema
class TrainingTask(dj.Manual):
    """Staging table for pairing videosets and training parameter sets

    Attributes:
        VideoSet (foreign key): VideoSet Key.
        TrainingParamSet (foreign key): TrainingParamSet key.
        training_id (int): Unique ID for training task.
        model_prefix ( varchar(32) ): Optional. Prefix for model files.
        project_path ( varchar(255) ): Optional. DLC's project_path in config relative
                                       to get_dlc_root_data_dir
    """

    definition = """      # Specification for a DLC model training instance
    -> VideoSet           # labeled video(s) for training
    -> TrainingParamSet
    training_id     : int
    ---
    model_prefix='' : varchar(32)
    project_path='' : varchar(255) # DLC's project_path in config relative to root
    """


@schema
class ModelTraining(dj.Computed):
    """Automated Model training information.

    Attributes:
        TrainingTask (foreign key): TrainingTask key.
        latest_snapshot (int unsigned): Latest exact snapshot index (i.e., never -1).
        config_template (longblob): Stored full config file."""

    definition = """
    -> TrainingTask
    ---
    latest_snapshot: int unsigned # latest exact snapshot index (i.e., never -1)
    config_template: longblob     # stored full config file
    """

    # To continue from previous training snapshot, devs suggest editing pose_cfg.yml
    # https://github.com/DeepLabCut/DeepLabCut/issues/70

    def make(self, key):
        import deeplabcut

        try:
            from deeplabcut.utils.auxiliaryfunctions import (
                get_model_folder,
                edit_config,
            )  # isort:skip
        except ImportError:
            from deeplabcut.utils.auxiliaryfunctions import (
                GetModelFolder as get_model_folder,
            )  # isort:skip

        """Launch training for each train.TrainingTask training_id via `.populate()`."""
        project_path, model_prefix = (TrainingTask & key).fetch1(
            "project_path", "model_prefix"
        )

        project_path = find_full_path(get_dlc_root_data_dir(), project_path)

        # ---- Build and save DLC configuration (yaml) file ----
        _, dlc_config = dlc_reader.read_yaml(project_path)  # load existing
        dlc_config.update((TrainingParamSet & key).fetch1("params"))
        dlc_config.update(
            {
                "project_path": project_path.as_posix(),
                "modelprefix": model_prefix,
                "train_fraction": dlc_config["TrainingFraction"][
                    int(dlc_config["trainingsetindex"])
                ],
                "training_filelist_datajoint": [  # don't overwrite origin video_sets
                    find_full_path(get_dlc_root_data_dir(), fp).as_posix()
                    for fp in (VideoSet.File & key).fetch("file_path")
                ],
            }
        )
        # Write dlc config file to base project folder
        dlc_cfg_filepath = dlc_reader.save_yaml(project_path, dlc_config)

        # ---- Update the project path in the DLC pose configuration (yaml) files ----
        model_folder = get_model_folder(
            trainFraction=dlc_config["train_fraction"],
            shuffle=dlc_config["shuffle"],
            cfg=dlc_config,
            modelprefix=dlc_config["modelprefix"],
        )
        model_train_folder = project_path / model_folder / "train"

        # update path of the init_weight
        with open(model_train_folder / "pose_cfg.yaml", "r") as f:
            pose_cfg = yaml.safe_load(f)
        init_weights_path = Path(pose_cfg["init_weights"])

        if (
            "pose_estimation_tensorflow/models/pretrained"
            in init_weights_path.as_posix()
        ):
            # this is the res_net models, construct new path here
            init_weights_path = (
                Path(deeplabcut.__path__[0])
                / "pose_estimation_tensorflow/models/pretrained"
                / init_weights_path.name
            )
        else:
            # this is existing snapshot weights, update path here
            init_weights_path = model_train_folder / init_weights_path.name

        edit_config(
            model_train_folder / "pose_cfg.yaml",
            {
                "project_path": project_path.as_posix(),
                "init_weights": init_weights_path.as_posix(),
                "dataset": Path(pose_cfg["dataset"]).as_posix(),
                "metadataset": Path(pose_cfg["metadataset"]).as_posix(),
            },
        )

        # ---- Trigger DLC model training job ----
        train_network_input_args = list(
            inspect.signature(deeplabcut.train_network).parameters
        )
        train_network_kwargs = {
            k: int(v) if k in ("shuffle", "trainingsetindex", "maxiters") else v
            for k, v in dlc_config.items()
            if k in train_network_input_args
        }
        for k in ["shuffle", "trainingsetindex", "maxiters"]:
            train_network_kwargs[k] = int(train_network_kwargs[k])

        try:
            deeplabcut.train_network(dlc_cfg_filepath, **train_network_kwargs)
        except KeyboardInterrupt:  # Instructions indicate to train until interrupt
            print("DLC training stopped via Keyboard Interrupt")

        # DLC goes by snapshot magnitude when judging 'latest' for evaluation
        # Here, we mean most recently generated
        snapshots = sorted(model_train_folder.glob("snapshot*.index"))
        max_modified_time = 0
        for snapshot in snapshots:
            modified_time = snapshot.stat().st_mtime
            if modified_time > max_modified_time:
                latest_snapshot_file = snapshot
                latest_snapshot = int(
                    re.search(r"(\d+)\.index", latest_snapshot_file.name).group(1)
                )
                max_modified_time = modified_time

        # update snapshotindex in the config
        snapshotindex = snapshots.index(latest_snapshot_file)

        dlc_config["snapshotindex"] = snapshotindex
        edit_config(
            dlc_cfg_filepath,
            {"snapshotindex": snapshotindex},
        )

        self.insert1(
            {**key, "latest_snapshot": latest_snapshot, "config_template": dlc_config}
        )
