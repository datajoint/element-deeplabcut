from element_interface.utils import find_full_path, find_root_directory
from workflow_deeplabcut.paths import get_dlc_root_data_dir
from pathlib import Path
import os


def download_djarchive_dlc_data(target_directory="/tmp/workflow_dlc_data/"):
    """Download DLC demo data from djarchive"""
    import djarchive_client
    from workflow_deeplabcut import version

    client = djarchive_client.client()
    revision = version.__version__.replace(".", "_")
    os.makedirs(target_directory)

    client.download(
        "workflow-dlc-data", target_directory=target_directory, revision=revision
    )


def setup_bare_project(project="from_top_tracking"):
    """Adds absolute paths to config files and generates training-datasets folder"""
    from deeplabcut.utils.auxiliaryfunctions import read_config, write_config
    from deeplabcut import create_training_dataset

    # ---- Write roots to project config ----
    # Note: variable conventions following DLC for potential PR
    config = find_full_path(get_dlc_root_data_dir(), f"{project}/config.yaml")
    cfg = read_config(config)
    project_path = str(Path(config).parents[0])  # Add absolute project path
    cfg["project_path"] = project_path
    cfg_videoset_paths = {}  # separate to not change during loop
    for video, value in cfg["video_sets"].items():  # add absolute video path
        cfg_videoset_paths[os.path.join(project_path, video)] = value
    cfg["video_sets"] = cfg_videoset_paths  # save new fullpaths
    write_config(config, cfg)

    # ---- Create training dataset ----
    # Folder deleted from publicly available data to cut down on size
    _ = create_training_dataset(
        config,
        num_shuffles=1,
        posecfg_template=str(next(Path(project_path).rglob("train/pose_cfg.y?ml"))),
    )


def shorten_video(
    vid_path="from_top_tracking/videos/test.mp4",
    output_path=None,
    first_n_sec=2,
):
    """Save the first 2 seconds of a video relative to dlc root dir.

    Parameters
    ----------
    vid_path: Default "videos/test_full.mp4". Relative to get_dlc_root_data_dir
    output_path: Destination relative to vid_path root. If none, adds '-Ns' to filename
                 Where N in first_n_sec
    first_n_sec: Default 2. Number of seconds to extract from beginning of video
    """
    vid_path_full = find_full_path(get_dlc_root_data_dir(), vid_path)
    vid_path_root = find_root_directory(get_dlc_root_data_dir(), vid_path_full)
    if not output_path:
        output_path = vid_path_full.with_name(
            vid_path_full.stem + f"-{first_n_sec}s" + vid_path_full.suffix
        )
    output_path_full = vid_path_root / output_path
    _ = os.system(  # adjust -ss 0 to start later
        f"ffmpeg -n -hide_banner -loglevel error -ss 0 -t {first_n_sec} -i "
        + f"{vid_path_full} -vcodec copy -acodec copy {output_path_full}"
    )
