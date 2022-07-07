from cgi import test
from deeplabcut.utils.auxiliaryfunctions import get_deeplabcut_path
from deeplabcut.utils.auxiliaryfunctions import read_plainconfig, write_plainconfig
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


def update_pose_cfg(project="from_top_tracking", update_snapshot=0):
    """Updates weight paths to absolute. If update_snapshot, changes weights to snap #


    Parameters
    ---------
    project: Poject name, matching folder in dlc_root_data_dir
    update_snapshot: Optional, default 0 = no. If -1, highest integer value available.
                     If integer, look for that snapshot.
    """
    project_path = find_full_path(get_dlc_root_data_dir(), f"{project}/")
    for phase in ["test", "train"]:
        config_search = list(project_path.rglob(f"{phase}/pose_cfg.yaml"))
        if not config_search:
            print(f"Couldn't find cfg for {phase}")
        config_path = config_search[0]
        cfg = read_plainconfig(config_path)
        if update_snapshot and phase == "train":
            snaps_on_disk = set(  # get all snapshots on disk
                [
                    int(i.split("-")[1])
                    for i in [f.stem for f in list(project_path.rglob("snapshot-*"))]
                ]
            )
            if update_snapshot == -1:  # optionally take last in set
                update_snapshot = snaps_on_disk.pop()
            else:
                assert (  # if desired snap not available
                    update_snapshot in snaps_on_disk
                ), f"Couldn't find snapshot {update_snapshot} in {config_path.parent}"
            cfg["init_weights"] = str(
                config_path.parent / f"snapshot-{update_snapshot}"
            )
        else:
            init_weights = Path(cfg["init_weights"])
            cfg["init_weights"] = str(
                find_full_path(get_deeplabcut_path(), init_weights.parent)
                / init_weights.name
            )
        write_plainconfig(config_path, cfg)


def setup_bare_project(project="from_top_tracking"):
    """Adds absolute paths to config files and generates training-datasets folder"""
    from deeplabcut import create_training_dataset

    # from deeplabcut import merge_datasets # creates new iteration, requires retrain
    # NOTE: variable conventions following DLC for potential PR
    # _ = merge_datasets(config)

    # ---- Write roots to project config ----
    project_path = find_full_path(get_dlc_root_data_dir(), f"{project}/")
    project_config_path = project_path / "config.yaml"
    project_cfg = read_plainconfig(project_config_path)
    project_cfg["project_path"] = str(project_path)
    cfg_videoset_paths = {}  # separate to not change during loop
    for video, value in project_cfg["video_sets"].items():  # add absolute video path
        cfg_videoset_paths[os.path.join(project_path, video)] = value
    project_cfg["video_sets"] = cfg_videoset_paths  # save new fullpaths
    write_plainconfig(project_config_path, project_cfg)
    # Update train/test pose_cfg
    update_pose_cfg(project=project, update_snapshot=-1)

    # ---- Create training dataset ----
    # Folder deleted from publicly available data to cut down on size
    _ = create_training_dataset(
        project_config_path,
        num_shuffles=1,
        posecfg_template=str(next(Path(project_path).rglob("train/pose_cfg.y?ml"))),
    )


def download_weights(weights="mobilenet_v2_1.0"):
    """Downloads model to default DLC path. For from-top project, use default model

    Parameters
    ---------
    model: Optional, default mobilenet v2_1.0. Which model to download
    force: Optional, default False. Even if files already present, download again.
    """
    from deeplabcut.utils.auxfun_models import Check4weights
    from deeplabcut.utils.auxiliaryfunctions import get_deeplabcut_path

    Check4weights(weights, get_deeplabcut_path(), 0)


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
    cmd = (  # adjust -ss 0 to start later
        f"ffmpeg -n -hide_banner -loglevel error -ss 0 -t {first_n_sec} -i "
        + f"{vid_path_full} -vcodec copy -acodec copy {output_path_full}"
    )
    _ = os.system(cmd)
