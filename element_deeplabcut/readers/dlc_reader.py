import re
import logging
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import ruamel.yaml as yaml
from element_interface.utils import find_root_directory, dict_to_uuid
from .. import model
from ..model import get_dlc_root_data_dir
from datajoint.errors import DataJointError

logger = logging.getLogger("datajoint")


class PoseEstimation:
    """Class for handling DLC pose estimation files."""

    def __init__(
        self,
        dlc_dir: str = None,
        pkl_path: str = None,
        h5_path: str = None,
        yml_path: str = None,
        filename_prefix: str = "",
    ):
        if dlc_dir is None:
            assert pkl_path and h5_path and yml_path, (
                'If "dlc_dir" is not provided, then pkl_path, h5_path, and yml_path '
                + "must be provided"
            )
        else:
            self.dlc_dir = Path(dlc_dir)
            assert self.dlc_dir.exists(), f"Unable to find {dlc_dir}"

        # meta file: pkl - info about this DLC run (input video, configuration, etc.)
        if pkl_path is None:
            self.pkl_paths = sorted(
                self.dlc_dir.rglob(f"{filename_prefix}*meta.pickle")
            )
            assert (
                len(self.pkl_paths) > 0
            ), f"No meta file (.pickle) found in: {self.dlc_dir}"
        else:
            pkl_path = Path(pkl_path)
            assert pkl_path.exists()
            self.pkl_paths = [pkl_path]

        # data file: h5 - body part outputs from the DLC post estimation step
        if h5_path is None:
            self.h5_paths = sorted(self.dlc_dir.rglob(f"{filename_prefix}*.h5"))
            assert (
                len(self.h5_paths) > 1
            ), f"No DLC output file (.h5) found in: {self.dlc_dir}"
        else:
            h5_path = Path(h5_path)
            assert h5_path.exists()
            self.h5_paths = [h5_path]

        # validate number of files
        assert len(self.h5_paths) == len(
            self.pkl_paths
        ), f"Unequal number of .h5 files ({len(self.h5_paths)}) and .pickle files ({len(self.pkl_paths)})"

        assert (
            self.pkl_paths[0].stem == self.h5_paths[0].stem + "_meta"
        ), f"Mismatching h5 ({self.h5_paths[0].stem}) and pickle {self.pkl_paths[0].stem}"

        # config file: yaml - configuration for invoking the DLC post estimation step
        if yml_path is None:
            yml_paths = list(self.dlc_dir.glob(f"{filename_prefix}*.y*ml"))
            # If multiple, defer to the one we save.
            if len(yml_paths) > 1:
                yml_paths = [val for val in yml_paths if val.stem == "dj_dlc_config"]
            assert len(yml_paths) == 1, (
                "Unable to find one unique .yaml file in: "
                + f"{dlc_dir} - Found: {len(yml_paths)}"
            )
            self.yml_path = yml_paths[0]
        else:
            self.yml_path = Path(yml_path)
            assert self.yml_path.exists()

        self._pkl = None
        self._rawdata = None
        self._yml = None
        self._data = None

        train_idx = np.where(
            (np.array(self.yml["TrainingFraction"]) * 100).astype(int)
            == int(self.pkl["training set fraction"] * 100)
        )[0][0]
        train_iter = int(self.pkl["Scorer"].split("_")[-1])

        self.model = {
            "Scorer": self.pkl["Scorer"],
            "Task": self.yml["Task"],
            "date": self.yml["date"],
            "iteration": self.pkl["iteration (active-learning)"],
            "shuffle": int(re.search(r"shuffle(\d+)", self.pkl["Scorer"]).groups()[0]),
            "snapshotindex": self.yml["snapshotindex"],
            "trainingsetindex": train_idx,
            "training_iteration": train_iter,
        }

        self.fps = self.pkl["fps"]
        self.nframes = self.pkl["nframes"]
        self.creation_time = self.h5_paths[0].stat().st_mtime

    @property
    def pkl(self):
        """Pickle file contents"""
        if self._pkl is None:
            nframes = 0
            meta_hash = None
            for fp in self.pkl_paths:
                with open(fp, "rb") as f:
                    meta = pickle.load(f)
                nframes += meta["data"].pop("nframes")

                # remove variable fields
                for k in ("start", "stop", "run_duration"):
                    meta["data"].pop(k)

                # confirm identical setting in all .pickle files
                if meta_hash is None:
                    meta_hash = dict_to_uuid(meta)
                else:
                    assert meta_hash == dict_to_uuid(
                        meta
                    ), f"Inconsistent DLC-model-config file used: {fp}"

            self._pkl = meta["data"]
            self._pkl["nframes"] = nframes
        return self._pkl

    @property
    def yml(self):
        """json-structured config.yaml file contents"""
        if self._yml is None:
            with open(self.yml_path, "rb") as f:
                self._yml = yaml.safe_load(f)
        return self._yml

    @property
    def rawdata(self):
        """Raw data from h5 file"""
        if self._rawdata is None:
            self._rawdata = pd.concat([pd.read_hdf(fp) for fp in self.h5_paths])
        return self._rawdata

    @property
    def data(self):
        """Data from the h5 file, restructured as a dict"""
        if self._data is None:
            self._data = self.reformat_rawdata()
        return self._data

    @property
    def df(self):
        """Data as dataframe"""
        top_level = self.rawdata.columns.levels[0][0]
        return self.rawdata.get(top_level)

    @property
    def body_parts(self):
        """Set of body parts present in data file"""
        return self.df.columns.levels[0]

    def reformat_rawdata(self):
        """Transform raw h5 data into dict"""
        error_message = (
            f"Total frames from .h5 file ({len(self.rawdata)}) differs "
            + f'from .pickle ({self.pkl["nframes"]})'
        )
        assert len(self.rawdata) == self.pkl["nframes"], error_message

        body_parts_position = {}
        for body_part in self.body_parts:
            body_parts_position[body_part] = {
                c: self.df.get(body_part).get(c).values
                for c in self.df.get(body_part).columns
            }

        return body_parts_position


def read_yaml(fullpath: str, filename: str = "*") -> tuple:
    """Return contents of yml in fullpath. If available, defer to DJ-saved version

    Args:
        fullpath (str): String or pathlib path. Directory with yaml files
        filename (str, optional): Filename, no extension. Permits wildcards.

    Returns:
        Tuple of (a) filepath as pathlib.PosixPath and (b) file contents as dict
    """
    from deeplabcut.utils.auxiliaryfunctions import read_config

    # Take the DJ-saved if there. If not, return list of available
    yml_paths = list(Path(fullpath).glob("dj_dlc_config.yaml")) or sorted(
        list(Path(fullpath).glob(f"{filename}.y*ml"))
    )

    assert (  # If more than 1 and not DJ-saved,
        len(yml_paths) == 1
    ), f"Found more yaml files than expected: {len(yml_paths)}\n{fullpath}"

    return yml_paths[0], read_config(yml_paths[0])


def save_yaml(
    output_dir: str,
    config_dict: dict,
    filename: str = "dj_dlc_config",
    mkdir: bool = True,
) -> str:
    """Save config_dict to output_path as filename.yaml. By default, preserves original.

    Args:
        output_dir (str): where to save yaml file
        config_dict (str): dict of config params or element-deeplabcut model.Model dict
        filename (str, optional): default 'dj_dlc_config' or preserve original 'config'
            Set to 'config' to overwrite original file.
            If extension is included, removed and replaced with "yaml".
        mkdir (bool): Optional, True. Make new directory if output_dir not exist

    Returns:
        path of saved file as string - due to DLC func preference for strings
    """
    from deeplabcut.utils.auxiliaryfunctions import write_config

    if "config_template" in config_dict:  # if passed full model.Model dict
        config_dict = config_dict["config_template"]
    if mkdir:
        output_dir.mkdir(exist_ok=True)
    if "." in filename:  # if user provided extension, remove
        filename = filename.split(".")[0]

    output_filepath = Path(output_dir) / f"{filename}.yaml"
    write_config(output_filepath, config_dict)
    return str(output_filepath)


def do_pose_estimation(
    video_filepaths: list,
    dlc_model: dict,
    project_path: str,
    output_dir: str,
    videotype="",
    gputouse=None,
    save_as_csv=False,
    batchsize=None,
    cropping=None,
    TFGPUinference=True,
    dynamic=(False, 0.5, 10),
    robust_nframes=False,
    allow_growth=False,
    use_shelve=False,
):
    """Launch DLC's analyze_videos within element-deeplabcut.

    Also saves a copy of the current config in the output dir, with ensuring analyzed
    videos in the video_set. NOTE: Config-specificed cropping not supported when adding
    to config in this manner.

    Args:
        video_filepaths (list): list of videos to analyze
        dlc_model (dict): element-deeplabcut dlc.Model
        project_path (str): path to project config.yml
        output_dir (str): where to save output
            # BELOW FROM DLC'S DOCSTRING

        videotype (str, optional, default=""):
            Checks for the extension of the video in case the input to the video is a
            directory. Only videos with this extension are analyzed. If unspecified,
            videos with common extensions ('avi', 'mp4', 'mov', 'mpeg', 'mkv') are kept.
        gputouse (int or None, optional, default=None):
            Indicates the GPU to use (see number in ``nvidia-smi``). If none, ``None``.
            See: https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
        save_as_csv (bool, optional, default=False):
            Saves the predictions in a .csv file.
        batchsize (int or None, optional, default=None):
            Change batch size for inference; if given overwrites ``pose_cfg.yaml``
        cropping (list or None, optional, default=None):
            List of cropping coordinates as [x1, x2, y1, y2].
            Note that the same cropping parameters will then be used for all videos.
            If different video crops are desired, run ``analyze_videos`` on individual
            videos with the corresponding cropping coordinates.
        TFGPUinference (bool, optional, default=True):
            Perform inference on GPU with TensorFlow code. Introduced in "Pretraining
            boosts out-of-domain robustness for pose estimation" by Alexander Mathis,
            Mert Yüksekgönül, Byron Rogers, Matthias Bethge, Mackenzie W. Mathis.
            Source https://arxiv.org/abs/1909.11229
        dynamic (tuple(bool, float, int) triple (state, detectiontreshold, margin)):
            If the state is true, then dynamic cropping will be performed. That means
            that if an object is detected (i.e. any body part > detectiontreshold),
            then object boundaries are computed according to the smallest/largest x
            position and smallest/largest y position of all body parts. This  window is
            expanded by the margin and from then on only the posture within this crop
            is analyzed (until the object is lost, i.e. <detectiontreshold). The
            current position is utilized for updating the crop window for the next
            frame (this is why the margin is important and should be set large enough
            given the movement of the animal).
        robust_nframes (bool, optional, default=False):
            Evaluate a video's number of frames in a robust manner.
            This option is slower (as the whole video is read frame-by-frame),
            but does not rely on metadata, hence its robustness against file corruption.
        allow_growth (bool, optional, default=False.):
            For some smaller GPUs the memory issues happen. If ``True``, the memory
            allocator does not pre-allocate the entire specified GPU memory region,
            instead starting small and growing as needed.
            See issue: https://forum.image.sc/t/how-to-stop-running-out-of-vram/30551/2
        use_shelve (bool, optional, default=False):
            By default, data are dumped in a pickle file at the end of the video
            analysis. Otherwise, data are written to disk on the fly using a "shelf";
            i.e., a pickle-based, persistent, database-like object by default,
            resulting in constant memory footprint.

    """
    from deeplabcut.pose_estimation_tensorflow import analyze_videos

    # ---- Build and save DLC configuration (yaml) file ----
    dlc_config = dlc_model["config_template"]
    dlc_project_path = Path(project_path)
    dlc_config["project_path"] = dlc_project_path.as_posix()

    # ---- Add current video to config ---
    for video_filepath in video_filepaths:
        if video_filepath not in dlc_config["video_sets"]:
            root_dir = find_root_directory(get_dlc_root_data_dir(), video_filepath)
            relative_path = Path(video_filepath).relative_to(root_dir)
            recording_id = (
                model.VideoRecording.File & f'file_path="{relative_path}"'
            ).fetch1("recording_id")
            try:
                px_width, px_height = (
                    model.RecordingInfo & f'recording_id="{recording_id}"'
                ).fetch1("px_width", "px_height")
            except DataJointError:
                logger.warn(
                    f"Could not find RecordingInfo for {video_filepath.stem}"
                    + "\n\tUsing zeros for crop value in config."
                )
                px_height, px_width = 0, 0
            dlc_config["video_sets"].update(
                {str(video_filepath): {"crop": f"0, {px_width}, 0, {px_height}"}}
            )

    # ---- Write config files ----
    # To output dir: Important for loading/parsing output in datajoint
    _ = save_yaml(output_dir, dlc_config)
    # To project dir: Required by DLC to run the analyze_videos
    if dlc_project_path != output_dir:
        config_filepath = save_yaml(dlc_project_path, dlc_config)

    # ---- Trigger DLC prediction job ----
    analyze_videos(
        config=config_filepath,
        videos=video_filepaths,
        shuffle=dlc_model["shuffle"],
        trainingsetindex=dlc_model["trainingsetindex"],
        destfolder=output_dir,
        modelprefix=dlc_model["model_prefix"],
        videotype=videotype,
        gputouse=gputouse,
        save_as_csv=save_as_csv,
        batchsize=batchsize,
        cropping=cropping,
        TFGPUinference=TFGPUinference,
        dynamic=dynamic,
        robust_nframes=robust_nframes,
        allow_growth=allow_growth,
        use_shelve=use_shelve,
    )
