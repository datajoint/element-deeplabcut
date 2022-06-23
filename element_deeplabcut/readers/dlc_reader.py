import re
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import ruamel.yaml as yaml


class PoseEstimation:
    def __init__(
        self,
        dlc_dir=None,
        pkl_path=None,
        h5_path=None,
        yml_path=None,
        filename_prefix="",
    ):
        if dlc_dir is None:
            assert pkl_path and h5_path and yml_path, (
                'If "dlc_dir" is not provided, then pkl_path, h5_path, and yml_path '
                + "must be provided"
            )
        else:
            self.dlc_dir = Path(dlc_dir)
            assert self.dlc_dir.exists(), f"Unable to find {dlc_dir}"

        # meta file: pkl - info about this  DLC run (input video, configuration, etc.)
        if pkl_path is None:
            pkl_paths = list(self.dlc_dir.rglob(f"{filename_prefix}*meta.pickle"))
            assert len(pkl_paths) == 1, (
                "Unable to find one unique .pickle file in: "
                + f"{dlc_dir} - Found: {len(pkl_paths)}"
            )
            self.pkl_path = pkl_paths[0]
        else:
            self.pkl_path = Path(pkl_path)
            assert self.pkl_path.exists()

        # data file: h5 - body part outputs from the DLC post estimation step
        if h5_path is None:
            h5_paths = list(self.dlc_dir.rglob(f"{filename_prefix}*.h5"))
            assert len(h5_paths) == 1, (
                "Unable to find one unique .h5 file in: "
                + f"{dlc_dir} - Found: {len(h5_paths)}"
            )
            self.h5_path = h5_paths[0]
        else:
            self.h5_path = Path(h5_path)
            assert self.h5_path.exists()

        assert (
            self.pkl_path.stem == self.h5_path.stem + "_meta"
        ), f"Mismatching h5 ({self.h5_path.stem}) and pickle {self.pkl_path.stem}"

        # config file: yaml - configuration for invoking the DLC post estimation step
        if yml_path is None:
            yml_paths = list(self.dlc_dir.glob(f"{filename_prefix}*.y*ml"))
            # If multiple, remove the one we save.
            # Otherwise errs when dlc_dir is inferred output_dir
            if len(yml_paths) > 1:
                yml_paths = [
                    val for val in yml_paths if not val.stem == "dlc_config_file"
                ]
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
            "shuffle": int(re.search("shuffle(\d+)", self.pkl["Scorer"]).groups()[0]),
            "snapshotindex": self.yml["snapshotindex"],
            "trainingsetindex": train_idx,
            "training_iteration": train_iter,
        }

        self.fps = self.pkl["fps"]
        self.nframes = self.pkl["nframes"]

        self.creation_time = self.h5_path.stat().st_mtime

    @property
    def pkl(self):
        if self._pkl is None:
            with open(self.pkl_path, "rb") as f:
                self._pkl = pickle.load(f)
        return self._pkl["data"]

    @property  # DLC aux_func has a read_config option, but it rewrites the proj path
    def yml(self):
        if self._yml is None:
            with open(self.yml_path, "rb") as f:
                self._yml = yaml.safe_load(f)
        return self._yml

    @property
    def rawdata(self):
        if self._rawdata is None:
            self._rawdata = pd.read_hdf(self.h5_path)
        return self._rawdata

    @property
    def data(self):
        if self._data is None:
            self._data = self.reformat_rawdata()
        return self._data

    @property
    def df(self):
        top_level = self.rawdata.columns.levels[0][0]
        return self.rawdata.get(top_level)

    @property
    def body_parts(self):
        return self.df.columns.levels[0]

    def reformat_rawdata(self):
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


def do_pose_estimation(
    video_filepaths,
    dlc_model,
    project_path,
    output_dir,
    videotype=None,
    gputouse=None,
    save_as_csv=False,
    batchsize=None,
    cropping=None,
    TFGPUinference=True,
    dynamic=(False, 0.5, 10),
    robust_nframes=False,
    allow_growth=False,
    use_shelve=False,
    modelprefix="",  # need from paramset
):
    """Launch DLC's analyze_videos within element-deeplabcut
    :param video_filepaths: list of videos to analyze
    :param dlc_model: element-deeplabcut dlc.Model dict
    :param project_path: path to project config.yml
    :param output_dir: where to save output
    Remaining parameters are DLC's defaults
    """
    from deeplabcut.pose_estimation_tensorflow import analyze_videos

    # ---- Build and save DLC configuration (yaml) file ----
    dlc_config = dlc_model["config_template"]
    dlc_project_path = Path(project_path)
    dlc_config["project_path"] = dlc_project_path.as_posix()

    # ---- Write DLC and basefolder yaml (config) files ----
    # Write dlc config file to base (data) folder
    # This is important for parsing the DLC in datajoint imaging
    # This is required to load the results
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "dlc_config_file.yaml", "w") as f:
        yaml.dump(dlc_config, f)

    # This is required by DLC to run the analyze_videos
    dlc_cfg_filepath = dlc_project_path / "dlc_config_file.yaml"
    with open(dlc_cfg_filepath, "w") as f:
        yaml.dump(dlc_config, f)

    # ---- Trigger DLC prediction job ----
    analyze_videos(
        config=dlc_cfg_filepath.as_posix(),
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
