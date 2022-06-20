"""
Code adapted from the Mathis Lab
MIT License Copyright (c) 2022 Mackenzie Mathis
DataJoint Schema for DeepLabCut 2.x, Supports 2D and 3D DLC via triangulation.
"""
import datajoint as dj
import os
import yaml
import inspect
import importlib
import numpy as np
from pathlib import Path
from datetime import datetime
from element_interface.utils import find_full_path, find_root_directory


schema = dj.schema()
_linking_module = None


def activate(
    dlc_schema_name, *, create_schema=True, create_tables=True, linking_module=None
):
    """
    activate(schema_name, *, create_schema=True, create_tables=True,
             linking_module=None)
        :param schema_name: schema name on the database server to activate the
                            `deeplabcut` element

        :param create_schema: when True (default), create schema in the database if it
                              does not yet exist.
        :param create_tables: when True (default), create schema in the database if it
                              does not yet exist.
        :param linking_module: a module (or name) containing the required dependencies
                               to activate the `session` element:
        Upstream tables:
            + Session: parent table to VideoRecording, identifying a recording session
            + Equipment: parent table to VideoRecording, identifying recording device
        Functions:
            + get_dlc_root_data_dir() -> list Retrieve the root data director(y/ies)
                with behavioral recordings for all subject/sessions.
                :return: a string for full path to the root data directory
            + get_dlc_processed_data_dir(session_key: dict) -> str
                Optional function to retrive the desired output directory for DeepLabCut
                files for a given session. If unspecified,
                output stored in the session video folder, per DLC default
                :return: a string for the absolute path of output directory
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(
        linking_module
    ), "The argument 'dependency' must be a module's name or a module"
    assert hasattr(
        linking_module, "get_dlc_root_data_dir"
    ), "The linking module must specify a lookup funtion for a root data directory"

    global _linking_module
    _linking_module = linking_module

    # activate
    schema.activate(
        dlc_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=_linking_module.__dict__,
    )


# -------------- Functions required by element-deeplabcut ---------------


def get_dlc_root_data_dir() -> list:
    """
    It is recommended that all paths in DataJoint Elements stored as relative
    paths, with respect to some user-configured "root" director(y/ies). The
    root(s) may vary between data modalities and user machines

    get_dlc_root_data_dir() -> list
        This user-provided function retrieves the possible root data
        director(y/ies) containing continuous behavioral data for all subjects
        and sessions (e.g. acquired video or treadmill raw files)
        :return: a string for full path to the behavioral root data directory,
         or list of strings for possible root data directories
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
    """
    If specified by the user, this function provides DeepLabCut with an output
    directory for processed files. If unspecified, output files will be stored
    in the session directory 'videos' folder, per DeepLabCut default

    get_dlc_processed_data_dir -> str
        This user-provided function specifies where DeepLabCut output files
        will be stored.
    """
    if hasattr(_linking_module, "get_dlc_processed_data_dir"):
        return _linking_module.get_dlc_processed_data_dir()
    else:
        return get_dlc_root_data_dir()[0]


# ----------------------------- Table declarations ----------------------


@schema
class VideoRecording(dj.Manual):
    definition = """
    -> Session
    recording_id: int
    ---
    -> Device
    """

    class File(dj.Part):
        definition = """
        -> master
        file_id: int
        ---
        file_path: varchar(255)  # filepath of video, relative to root data directory
        """


@schema
class RecordingInfo(dj.Imported):
    definition = """
    -> VideoRecording
    ---
    px_height                 : smallint  # height in pixels
    px_width                  : smallint  # width in pixels
    nframes                   : smallint  # number of frames 
    fps = NULL                : int       # (Hz) frames per second
    recording_datetime = NULL : datetime  # Datetime for the start of the recording
    recording_duration        : float     # video duration (s) from nframes / fps
    """

    @property
    def key_source(self):
        return VideoRecording & VideoRecording.File

    def make(self, key):
        import cv2

        file_paths = (VideoRecording.File & key).fetch("file_path")

        nframes = 0
        px_height, px_width, fps = None, None, None

        for file_path in file_paths:
            file_path = (find_full_path(get_dlc_root_data_dir(), file_path)).as_posix()

            cap = cv2.VideoCapture(file_path)
            info = (
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FPS)),
            )
            if px_height is not None:
                assert (px_height, px_width, fps) == info
            px_height, px_width, fps = info
            nframes += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

        self.insert1(
            {
                **key,
                "px_height": px_height,
                "px_width": px_width,
                "nframes": nframes,
                "fps": fps,
                "recording_duration": nframes / fps,
            }
        )


@schema
class BodyPart(dj.Lookup):
    definition = """
    body_part                : varchar(32)
    ---
    body_part_description='' : varchar(1000)
    """

    @classmethod
    def extract_new_body_parts(cls, dlc_config: dict, verbose=True):
        """Print a list of new body parts from a dlc config,
        to examine before generating descriptions
        :param dlc_config:  path to a config.y*ml, or dict including contents thereof
        :param verbose:     default True. Print existing/new items to console
        """
        if not isinstance(dlc_config, dict):
            dlc_config_fp = find_full_path(get_dlc_root_data_dir(), Path(dlc_config))
            assert dlc_config_fp.exists() and dlc_config_fp.suffix in (
                ".yml",
                ".yaml",
            ), f"dlc_config is neither dict nor filepath\n Check: {dlc_config_fp}"
            if dlc_config_fp.suffix in (".yml", ".yaml"):
                with open(dlc_config_fp, "rb") as f:
                    dlc_config = yaml.safe_load(f)
        # -- Check and insert new BodyPart --
        assert "bodyparts" in dlc_config, f"Found no bodyparts section in {dlc_config}"
        tracked_body_parts = cls.fetch("body_part")
        new_body_parts = np.setdiff1d(dlc_config["bodyparts"], tracked_body_parts)
        if verbose:  # Added to silence duplicate prompt during `insert_new_model`
            print(f"Existing body parts: {tracked_body_parts}")
            print(f"New body parts: {new_body_parts}")
        return new_body_parts

    @classmethod
    def insert_from_config(
        cls, dlc_config: dict, descriptions: list = None, prompt=True
    ):
        """Insert all body parts from a config file

        :param dlc_config: path to a config.y*ml, or dict including contents thereof
        :param descriptions: optional list describing new body parts
        """

        # handle dlc_config being a yaml file
        new_body_parts = cls.extract_new_body_parts(dlc_config)
        if new_body_parts is not None:  # Required bc np.array is ambiguous as bool
            if descriptions:
                assert len(descriptions) == len(new_body_parts), (
                    "Descriptions list does not match "
                    + " the number of new_body_parts"
                )
                print(f"New descriptions: {descriptions}")
            if descriptions is None:
                descriptions = ["" for x in range(len(new_body_parts))]

            if (
                prompt
                and dj.utils.user_choice(
                    f"Insert {len(new_body_parts)} new body " + "part(s)?"
                )
                != "yes"
            ):
                print("Canceled insert.")
                return
            cls.insert(
                [
                    {"body_part": b, "body_part_description": d}
                    for b, d in zip(new_body_parts, descriptions)
                ]
            )


@schema
class Model(dj.Manual):
    definition = """
    model_name           : varchar(64)  # User-friendly model name
    ---
    task                 : varchar(32)  # Task in the config yaml
    date                 : varchar(16)  # Date in the config yaml
    iteration            : int          # Iteration/version of this model
    snapshotindex        : int          # which snapshot for prediction (if -1, latest)
    shuffle              : int          # Shuffle (1) or not (0)
    trainingsetindex     : int          # Index of training fraction list in config.yaml
    unique index (task, date, iteration, shuffle, snapshotindex, trainingsetindex)
    scorer               : varchar(64)  # Scorer/network name - DLC's GetScorerName()
    config_template      : longblob     # Dictionary of the config for analyze_videos()
    project_path         : varchar(255) # DLC's project_path in config relative to root
    model_prefix=''      : varchar(32)
    model_description='' : varchar(1000)
    -> [nullable] train.TrainingParamSet
    """
    # project_path is the only item required downstream in the pose schema
    # what happens if TrainingParamSet isn't in the namespace?

    class BodyPart(dj.Part):
        definition = """
        -> master
        -> BodyPart
        """

    @classmethod
    def insert_new_model(
        cls,
        model_name: str,
        dlc_config,
        *,
        shuffle: int,
        trainingsetindex,
        project_path=None,
        model_description="",
        model_prefix="",
        paramset_idx: int = None,
        prompt=True,
    ):
        """Insert new model into the dlc.Model table

        :param model_name: User-friendly name for this model
        :param dlc_config: path to a config.y*ml, or dict including contents thereof
        :param shuffle: integer, shuffle number
        :param trainingsetindex: index of training fraction list in config.yaml
        :param model_description: Description of this model
        :param model_prefix: Filename prefix used across DLC project
        :param body_part_descriptions: optional list for new items in BodyParts table
        :param paramset_idx: optional index from the TrainingParamSet table
        """
        from deeplabcut.utils.auxiliaryfunctions import GetScorerName
        from distutils.util import strtobool

        # handle dlc_config being a yaml file
        if not isinstance(dlc_config, dict):
            dlc_config_fp = find_full_path(get_dlc_root_data_dir(), Path(dlc_config))
            assert dlc_config_fp.exists(), (
                "dlc_config is neither dict nor filepath" + f"\n Check: {dlc_config_fp}"
            )
            if dlc_config_fp.suffix in (".yml", ".yaml"):
                with open(dlc_config_fp, "rb") as f:
                    dlc_config = yaml.safe_load(f)

        # ---- Get and resolve project path ----
        project_path = find_full_path(
            get_dlc_root_data_dir(), project_path or dlc_config["project_path"]
        )
        root_dir = find_root_directory(get_dlc_root_data_dir(), project_path)

        # ---- Build config ----
        template_attributes = [
            "Task",
            "date",
            "TrainingFraction",
            "iteration",
            "snapshotindex",
            "batch_size",
            "cropping",
            "x1",
            "x2",
            "y1",
            "y2",
            "project_path",
        ]
        config_template = {
            k: v for k, v in dlc_config.items() if k in template_attributes
        }

        # ---- Get scorer name ----
        # "or 'f'" below covers case where config returns None. StrToBool handles else
        scorer_legacy = strtobool(dlc_config.get("scorer_legacy") or "f")

        dlc_scorer = GetScorerName(
            cfg=config_template,
            shuffle=shuffle,
            trainFraction=dlc_config["TrainingFraction"][trainingsetindex],
            modelprefix=model_prefix,
        )[scorer_legacy]
        if config_template["snapshotindex"] == -1:
            dlc_scorer = "".join(dlc_scorer.split("_")[:-1])

        # ---- Insert ----
        model_dict = {
            "model_name": model_name,
            "model_description": model_description,
            "scorer": dlc_scorer,
            "task": config_template["Task"],
            "date": config_template["date"],
            "iteration": config_template["iteration"],
            "snapshotindex": config_template["snapshotindex"],
            "shuffle": shuffle,
            "trainingsetindex": trainingsetindex,
            "project_path": project_path.relative_to(root_dir).as_posix(),
            "paramset_idx": paramset_idx,
            "config_template": config_template,
        }

        # -- prompt for confirmation --
        print("--- DLC Model specification to be inserted ---")
        for k, v in model_dict.items():
            if k != "config_template":
                print("\t{}: {}".format(k, v))
            else:
                print("\t-- Template for config.yaml --")
                for k, v in model_dict["config_template"].items():
                    print("\t\t{}: {}".format(k, v))

        if (
            prompt
            and dj.utils.user_choice("Proceed with new DLC model insert?") != "yes"
        ):
            print("Canceled insert.")
            return
        with cls.connection.transaction:
            cls.insert1(model_dict)
            # Returns array, so check size for unambiguous truth value
            if BodyPart.extract_new_body_parts(dlc_config, verbose=False).size > 0:
                BodyPart.insert_from_config(dlc_config, prompt=prompt)
            cls.BodyPart.insert((model_name, bp) for bp in dlc_config["bodyparts"])


@schema
class ModelEvaluation(dj.Computed):
    definition = """
    -> Model
    ---
    train_iterations   : int   # Training iterations
    train_error=null   : float # Train error (px)
    test_error=null    : float # Test error (px)
    p_cutoff=null      : float # p-cutoff used
    train_error_p=null : float # Train error with p-cutoff
    test_error_p=null  : float # Test error with p-cutoff
    """

    def make(self, key):
        """.populate() method will launch evaulation for each unique entry in Model"""
        import csv
        from deeplabcut import evaluate_network
        from deeplabcut.utils.auxiliaryfunctions import get_evaluation_folder

        dlc_config, project_path, model_prefix, shuffle, trainingsetindex = (
            Model & key
        ).fetch1(
            "config_template",
            "project_path",
            "model_prefix",
            "shuffle",
            "trainingsetindex",
        )

        project_path = find_full_path(get_dlc_root_data_dir(), project_path)
        yml_paths = list(project_path.glob("*.y*ml"))
        assert len(yml_paths) == 1, (
            "Unable to find one unique .yaml file in: "
            + f"{project_path} - Found: {len(yml_paths)}"
        )

        evaluate_network(
            yml_paths[0],
            Shuffles=[shuffle],  # this needs to be a list
            trainingsetindex=trainingsetindex,
            comparisonbodyparts="all",
        )

        eval_folder = get_evaluation_folder(
            trainFraction=dlc_config["TrainingFraction"][trainingsetindex],
            shuffle=shuffle,
            cfg=dlc_config,
            modelprefix=model_prefix,
        )
        eval_path = project_path / eval_folder
        assert eval_path.exists(), f"Couldn't find evaluation folder:\n{eval_path}"

        eval_csvs = list(eval_path.glob("*csv"))
        max_modified_time = 0
        for eval_csv in eval_csvs:
            modified_time = os.path.getmtime(eval_csv)
            if modified_time > max_modified_time:
                eval_csv_latest = eval_csv
        with open(eval_csv_latest, newline="") as f:
            results = list(csv.DictReader(f, delimiter=","))[0]
        # in testing, test_error_p returned empty string
        self.insert1(
            dict(
                key,
                train_iterations=results["Training iterations:"],
                train_error=results[" Train error(px)"],
                test_error=results[" Test error(px)"],
                p_cutoff=results["p-cutoff used"],
                train_error_p=results["Train error with p-cutoff"],
                test_error_p=results["Test error with p-cutoff"],
            )
        )


@schema
class PoseEstimationTask(dj.Manual):
    definition = """
    -> VideoRecording                           # Session -> Recording + File part table
    -> Model                                    # Must specify a DLC project_path

    ---
    task_mode='load' : enum('load', 'trigger')  # load results or trigger computation
    pose_estimation_output_dir='': varchar(255) # output dir relative to the root dir
    pose_estimation_params=null  : longblob     # analyze_videos params, if not default
    """

    @classmethod
    def infer_output_dir(cls, key, relative=False, mkdir=False):
        """Return the expected pose_estimation_output_dir based on the convention
                 / video_dir / Equipment_{}_recording_{}_model_{}
        Spaces in model name are replaced with hyphens
        :param key: key specifying a pairing of VideoRecording and Model
        :param relative: report directory relative to get_dlc_processed_data_dir()
        :param mkdir: default False, make directory if it doesn't exist
        """
        processed_dir = Path(get_dlc_processed_data_dir())
        video_filepath = find_full_path(
            get_dlc_root_data_dir(),
            (VideoRecording.File & key).fetch("file_path", limit=1)[0],
        )
        root_dir = find_root_directory(get_dlc_root_data_dir(), video_filepath.parent)
        recording_key = VideoRecording & key
        device = "-".join(
            str(v)
            for v in (_linking_module.Device & recording_key).fetch1("KEY").values()
        )
        output_dir = (
            processed_dir
            / video_filepath.parent.relative_to(root_dir)
            / (
                f'device_{device}_recording_{key["recording_id"]}_model_'
                + key["model_name"].replace(" ", "-")
            )
        )
        if mkdir:
            output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir.relative_to(processed_dir) if relative else output_dir

    @classmethod
    def insert_estimation_task(
        cls,
        key,
        task_mode="trigger",
        params: dict = None,
        relative=True,
        mkdir=True,
        skip_duplicates=False,
    ):
        """Insert PoseEstimationTask with inferred output dir based on the convention
                processed_dir / video_dir / device_{}_recording_{}_model_{}
        :param key: key specifying a pairing of VideoRecording and Model
        :param task_mode: default 'trigger' computation. Or 'load' existing results
        :param params: DLC's analyze_videos parameters if other than the defaults:
            videotype, gputouse, save_as_csv, batchsize, cropping, TFGPUinference,
            dynamic, robust_nframes, allow_growth, use_shelve
        :param relative: report directory relative to get_dlc_processed_data_dir()
        :param mkdir: default False, make directory if it doesn't exist
        """
        output_dir = cls.infer_output_dir(key, relative=relative, mkdir=mkdir)

        cls.insert1(
            {
                **key,
                "task_mode": task_mode,
                "pose_estimation_params": params,
                "pose_estimation_output_dir": output_dir,
            },
            skip_duplicates=skip_duplicates,
        )


@schema
class PoseEstimation(dj.Computed):
    definition = """
    -> PoseEstimationTask
    ---
    post_estimation_time: datetime  # time of generation of this set of DLC results
    """

    class BodyPartPosition(dj.Part):
        definition = """ # uses DeepLabCut h5 output for body part position
        -> master
        -> Model.BodyPart

        ---
        frame_index : longblob     # frame index in model
        x_pos       : longblob
        y_pos       : longblob
        z_pos=null  : longblob
        likelihood  : longblob
        """

    def make(self, key):
        """.populate() method will launch training for each PoseEstimationTask"""
        from .readers import dlc_reader

        # ID model and directories
        dlc_model = (Model & key).fetch1()

        assert dlc_model["project_path"], (
            "Your model table must have a 'project_path'"
            + "field pointing to a DLC directory"
        )
        task_mode, analyze_video_params, output_dir = (PoseEstimationTask & key).fetch1(
            "task_mode", "pose_estimation_params", "pose_estimation_output_dir"
        )
        analyze_video_params = analyze_video_params or {}
        output_dir = find_full_path(get_dlc_root_data_dir(), output_dir)
        video_filepaths = [
            find_full_path(get_dlc_root_data_dir(), fp).as_posix()
            for fp in (VideoRecording.File & key).fetch("file_path")
        ]
        project_path = find_full_path(
            get_dlc_root_data_dir(), dlc_model["project_path"]
        )

        # Triger PoseEstimation,
        if task_mode == "trigger":
            dlc_reader.do_pose_estimation(
                video_filepaths,
                dlc_model,
                project_path,
                output_dir,
                **analyze_video_params,
            )
        dlc_result = dlc_reader.PoseEstimation(output_dir)
        creation_time = datetime.fromtimestamp(dlc_result.creation_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        body_parts = [
            {
                **key,
                "body_part": k,
                "frame_index": np.arange(dlc_result.nframes),
                "x_pos": v["x"],
                "y_pos": v["y"],
                "z_pos": v.get("z"),
                "likelihood": v["likelihood"],
            }
            for k, v in dlc_result.data.items()
        ]

        self.insert1({**key, "post_estimation_time": creation_time})
        self.BodyPartPosition.insert(body_parts)

    @classmethod
    def get_trajectory(cls, key, body_parts="all"):
        """
        Returns a pandas dataframe of x, y and z coordinates of the specified body_parts
        :param key: A query specifying one PoseEstimation entry, else error is thrown.
        :param body_parts: optional, body parts as a list. If "all", all joints
        returns df: multi index pandas dataframe with DLC scorer names, body_parts
                    and x/y coordinates of each joint name for a camera_id,
                    similar to output of DLC dataframe. If 2D, z is set of zeros
        """
        import pandas as pd

        model_name = key["model_name"]

        if body_parts == "all":
            body_parts = (cls.BodyPartPosition & key).fetch("body_part")
        else:
            body_parts = list(body_parts)

        df = None
        for body_part in body_parts:
            x_pos, y_pos, z_pos, likelihood = (
                cls.BodyPartPosition & {"body_part": body_part}
            ).fetch1("x_pos", "y_pos", "z_pos", "likelihood")
            if not z_pos:
                z_pos = np.zeros_like(x_pos)

            a = np.vstack((x_pos, y_pos, z_pos, likelihood))
            a = a.T
            pdindex = pd.MultiIndex.from_product(
                [[model_name], [body_part], ["x", "y", "z", "likelihood"]],
                names=["scorer", "bodyparts", "coords"],
            )
            frame = pd.DataFrame(a, columns=pdindex, index=range(0, a.shape[0]))
            df = pd.concat([df, frame], axis=1)
        return df
