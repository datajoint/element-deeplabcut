from pathlib import Path

import datajoint as dj


logger = dj.logger


def plotting_results(pose_estimation_key: dict):
    """
    Wrapper for deeplabcut.utils.plotting.PlottingResults,
        using dlc_result object from `dlc_reader.PoseEstimation`
    Args:
        pose_estimation_key (dict): PoseEstimation key

    Returns:
        plots_dir (Path): Path to the folder containing the plots
    """
    import deeplabcut
    from element_deeplabcut import model
    from element_deeplabcut.readers import dlc_reader

    output_dir = (model.PoseEstimationTask & pose_estimation_key).fetch1(
        "pose_estimation_output_dir"
    )
    try:
        output_dir = model.find_full_path(model.get_dlc_root_data_dir(), output_dir)
    except FileNotFoundError:
        # not on local disk yet: restore it under the processed-data root
        output_dir = Path(model.get_dlc_root_data_dir()[-1]) / output_dir

    # fetch result files
    try:
        pose_estimation_folder = (model.PoseEstimation & pose_estimation_key).fetch1(
            "pose_estimation_folder"
        )
        if pose_estimation_folder is not None:
            pose_estimation_folder.download(output_dir)
    except Exception as e:
        logger.warning(
            f"Error downloading PoseEstimation files - assuming all files are available locally\n{e}"
        )

    dlc_result = dlc_reader.PoseEstimation(output_dir.as_posix())

    plots_dir = output_dir / "plots"
    plots_dir.mkdir(exist_ok=True)

    deeplabcut.utils.plotting.PlottingResults(
        tmpfolder=plots_dir,
        Dataframe=dlc_result.rawdata,
        cfg=dlc_result.yml,
        bodyparts2plot=dlc_result.body_parts.to_list(),
        individuals2plot="",
        showfigures=False,
        suffix=".png",
        resolution=100,
        linewidth=1.0,
    )

    return plots_dir
