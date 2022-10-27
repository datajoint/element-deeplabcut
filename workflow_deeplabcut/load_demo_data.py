from deeplabcut.utils.auxiliaryfunctions import get_deeplabcut_path
from deeplabcut.utils.auxiliaryfunctions import read_plainconfig, write_plainconfig
from element_interface.utils import find_full_path, find_root_directory
from workflow_deeplabcut.paths import get_dlc_root_data_dir
from pathlib import Path
import os


def download_djarchive_dlc_data(target_directory: str = "/tmp/test_data/"):
    """Download DLC demo data from djarchive. Approx .3 GB

    Args:
        target_directory (str, optional): Where to store the downloaded data.
    """
    import djarchive_client

    client = djarchive_client.client()
    os.makedirs(target_directory, exist_ok=True)

    client.download(
        "workflow-dlc-data", target_directory=target_directory, revision="v1"
    )


def update_pose_cfg(
    project: str = "from_top_tracking", net_type: str = None, update_snapshot: int = 0
):
    """Updates weight paths to absolute. If update_snapshot, changes weights to snap #

    Args:
        project (str, optional): Default from 'from_top_tracking'. Poject name/folder in
            dlc_root_data_dir
        net_type (str, optional): Project net weights (e.g., resnet50)
            If project is 'from_top_tracking', 'mobilenet_v2_1.0'
        update_snapshot (int, optional): Default 0 = no. If -1, highest integer value
            available. If integer, look for that snapshot.
    """
    project_path = find_full_path(get_dlc_root_data_dir(), f"{project}/")
    if project == "from_top_tracking":
        net_type == "mobilenet_v2_1.0"
    for phase in ["test", "train"]:
        config_search = list(project_path.rglob(f"{phase}/pose_cfg.yaml"))
        if not config_search:
            print(f"Couldn't find cfg for {phase}")
        config_path = config_search[0]
        cfg = read_plainconfig(config_path)
        if update_snapshot and phase == "train":
            # Get available snapshots
            snaps_on_disk = set(
                [
                    int(i.split("-")[1])
                    for i in [f.stem for f in list(project_path.rglob("snapshot-*"))]
                ]
            )
            # If -1, take most recent
            if update_snapshot == -1:
                update_snapshot = snaps_on_disk.pop()  # last in sorted set
            else:
                # Assert desired snapshot is available
                assert (
                    update_snapshot in snaps_on_disk
                ), f"Couldn't find snapshot {update_snapshot} in {config_path.parent}"
            # Set snaphot value
            cfg["init_weights"] = str(
                config_path.parent / f"snapshot-{update_snapshot}"
            )
        else:
            init_weights = Path(
                cfg["init_weights"]
            )  # e.g., path/to/snapshot-1 (no ext)
            cfg["init_weights"] = str(
                find_full_path(get_deeplabcut_path(), init_weights.parent)
                / init_weights.name  # need parent/name bc it isn't on disk
            )

        if net_type:  # if net_type explicitly provided, update
            cfg["net_type"] = net_type

        # For train, pull datatype_set for next function
        if phase == "train":
            augmenter_type = cfg.get("dataset_type")

        write_plainconfig(config_path, cfg)

    return augmenter_type


def setup_bare_project(project: str = "from_top_tracking", net_type: str = None):
    """Adds absolute paths to config files and generates training-datasets folder

    Args:
        project (str, optional): Default 'from_top_tracking'. DLC project folder
        net_type (str, optional): Project net (e.g., resnet50) passed to
                        creat_training_dataset. If 'from_top', 'mobilenet_v2_1.0'
    """
    from deeplabcut import create_training_dataset

    if "from_top_tracking" in project:  # set net_type for example data
        net_type = "mobilenet_v2_1.0"

    if os.path.isabs(project) and Path(project).exists():
        project_path = Path(project)
    else:
        project_path = find_full_path(get_dlc_root_data_dir(), f"{project}/")

    # ---- Write roots to project config ----
    project_config_path = project_path / "config.yaml"
    project_cfg = read_plainconfig(project_config_path)
    project_cfg["project_path"] = str(project_path)
    cfg_videoset_paths = {}  # separate to not change during loop
    for video, value in project_cfg["video_sets"].items():  # add absolute video path
        cfg_videoset_paths[os.path.join(project_path, video)] = value
    project_cfg["video_sets"] = cfg_videoset_paths  # save new fullpaths
    write_plainconfig(project_config_path, project_cfg)
    # Update train/test pose_cfg, return augmenter type
    augmenter_type = update_pose_cfg(
        project=project, net_type=net_type, update_snapshot=-1
    )

    # ---- Create training dataset ----
    # Folder deleted from publicly available data to cut down on size
    _ = create_training_dataset(
        project_config_path,
        num_shuffles=1,
        net_type=net_type,
        augmenter_type=augmenter_type,
        posecfg_template=str(next(Path(project_path).rglob("train/pose_cfg.y?ml"))),
    )


def shorten_video(
    vid_path: str = "from_top_tracking/videos/test.mp4",
    output_path: str = None,
    first_n_sec: int = 2,
):
    """Save the first 2 seconds of a video relative to dlc root dir.

    Args:
        vid_path (str, optional): Default "from_top_tracking/videos/test_full.mp4". Path
            relative to get_dlc_root_data_dir() root directory
        output_path (str, optional): Destination relative to vid_path root. If none,
            adds '-Ns' to filename, where N in first_n_sec
        first_n_sec (int, optional): Default 2. # of seconds to extract from beginning
            of video
    """

    if os.path.isabs(vid_path) and Path(vid_path).exists():
        vid_path_full = Path(vid_path)
    else:
        vid_path_full = find_full_path(get_dlc_root_data_dir(), vid_path)

    if not output_path:
        output_path_full = vid_path_full.with_name(
            vid_path_full.stem + f"-{first_n_sec}s" + vid_path_full.suffix
        )
    else:
        output_path_full = (
            find_root_directory(get_dlc_root_data_dir(), vid_path_full) / output_path
        )

    cmd = (  # adjust -ss 0 to start later
        f"ffmpeg -n -hide_banner -loglevel error -ss 0 -t {first_n_sec} -i "
        + f"{vid_path_full} -vcodec copy -acodec copy {output_path_full}"
    )
    _ = os.system(cmd)


def revert_checkpoint_file(
    project="from_top_tracking", original_checkpoint="checkpoint_orig"
):
    """Delete existing checkpoint file and replace with original_checkpoint

    Args:
        project (str, optional): DLC project name. Defaults to "from_top_tracking".
        original_checkpoint (str, optional): Original checkpoint file ot use in the
            revert, in the same directory as the checkpoint file. Defaults to
            "checkpoint_orig".
    """
    import shutil

    project_path = find_full_path(get_dlc_root_data_dir(), f"{project}/")
    original_checkpoint_path = list(project_path.rglob(original_checkpoint))
    assert (
        len(original_checkpoint_path) == 1
    ), f"Found more than one original checkpoint:\n{original_checkpoint_path}"
    shutil.copy(
        original_checkpoint_path[0], original_checkpoint_path[0].parent / "checkpoint"
    )
