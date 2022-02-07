


def do_pose_estimation(video_filepaths, dlc_model, project_path, output_dir):
    import scanreader
    from natsort import natsorted
    import re
    from datetime import datetime
    import deeplabcut

    # ---- Build and save DLC configuration (yaml) file ----
    dlc_config = dlc_model['config_template']
    dlc_project_path = pathlib.Path(project_path)

    assert dlc_project_path.exists(), f'DLC project path ({dlc_project_path}) not found on this machine'

    dlc_config['project_path'] = dlc_project_path.as_posix()

    # ---- Write DLC and basefolder yaml (config) files ----

    # Write dlc config file to base (data) folder
    # This is important for parsing the DLC in datajoint imaging
    output_dir.mkdir(exist_ok=True)
    dlc_cfg_filepath = output_dir / 'dlc_config_file.yaml'
    with open(dlc_cfg_filepath, 'w') as f:
        yaml.dump(dlc_config, f)

    # ---- Trigger DLC prediction job ----
    deeplabcut.analyze_videos(config=dlc_cfg_filepath, videos=video_filepaths,
                              shuffle=dlc_model['shuffle'],
                              trainingsetindex=dlc_model['trainingsetindex'],
                              destfolder=output_dir)
