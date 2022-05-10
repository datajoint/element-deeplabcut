# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: venv-dlc
#     language: python
#     name: venv-dlc
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown] pycharm={"name": "#%% md\n"}
# ## Workflow Automation
#
# In the previous notebook [03-Process](./03-Process.ipynb), we ran through the workflow in detailed steps. For daily running routines, the current notebook provides a more succinct and automatic approach to run through the pipeline using some utility functions in the workflow.
#
# The commands here run a workflow using [example data](https://downgit.github.io/#/home?url=https://github.com/DeepLabCut/DeepLabCut/tree/master/examples/openfield-Pranav-2018-10-30) from the [00-DownloadData](./00-DataDownload_Optional.ipynb) notebook, but note where placeholders could be changed for a different dataset.

# %% tags=[]
import os
from pathlib import Path

# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
assert os.path.basename(os.getcwd()) == "workflow-deeplabcut", (
    "Please move to the " + "workflow directory"
)
from workflow_deeplabcut.pipeline import lab, subject, session, train, model
from workflow_deeplabcut import process

# %% [markdown]
# We'll be using the `process.py` script to automatically loop through all `make` functions, as a shortcut for calling each individually.
#
# If you previously completed the [03-Process notebook](./03-Process.ipynb), you may want to delete the contents ingested there, to avoid duplication errors.

# %%
safemode = None  # Set to false to turn off confirmation prompts
(session.Session & 'subject="subject6"').delete(safemode=safemode)
train.TrainingParamSet.delete(safemode=safemode)
train.VideoSet.delete(safemode=safemode)

# %% [markdown]
# ## Ingestion of subjects, sessions, videos and training parameters
#
# Refer to the `user_data` folder in the workflow.
#
# 1. Fill subject and session information in files `subjects.csv` and `sessions.csv`
# 2. Fill in recording and parameter information in `recordings.csv` and `config_params.csv`
#     + Add both training and estimation videos to the recording list
#     + Additional columns in `config_params.csv` will be treated as model training parameters
# 3. Run automatic scripts prepared in `workflow_deeplabcut.ingest` for ingestion:
#     + `ingest_subjects` for `subject.Subject`
#     + `ingest_sessions` - for session tables `Session`, `SessionDirectory`, and `SessionNote`
#     + `ingest_dlc_items` - for ...
#         - `train.ModelTrainingParamSet`
#         - `train.VideoSet` and the corresponding `File` part table
#         - `model.VideoRecording` and the corresponding `File` part table

# %%
from workflow_deeplabcut.ingest import (
    ingest_subjects,
    ingest_sessions,
    ingest_dlc_items,
)

ingest_subjects()
ingest_sessions()
ingest_dlc_items()

# %% [markdown]
# ## Setting project variables
#
# 1. Set your root directory in your DataJoint config file, under `custom` as `dlc_root_data_dir`.

# %%
import datajoint as dj

dj.config.load("dj_local_conf.json")
from element_interface.utils import find_full_path

data_dir = find_full_path(
    dj.config["custom"]["dlc_root_data_dir"],  # root from config
    "openfield-Pranav-2018-10-30",
)  # DLC project dir
config_path = data_dir / "config.yaml"

# %% [markdown]
# 2. For the purposes of this demo, we will
#    1. ask DeepLabCut to structure the demo config file with `load_demo_data`. If you already did this in the [00-DataDownload notebook](./00-DataDownload_Optional.ipynb), skip this step.
#    2. generate a copy to show pose estimation. This is `recording_id` 2 in `recordings.csv`. If you already did this in the [00-DataDownload notebook](./00-DataDownload_Optional.ipynb), skip this step.

# %%
# A
from deeplabcut.create_project.demo_data import load_demo_data

# load_demo_data(config_path)
# B
vid_path = str(data_dir).replace(" ", "\ ") + "/videos/m3v1mp4"
cmd = (
    f"ffmpeg -n -hide_banner -loglevel error -ss 0 -t 2 -i {vid_path}.mp4 -vcodec copy "
    + f"-acodec copy {vid_path}-copy.mp4"
)  # New video copy, first 2 seconds
os.system(cmd)

# %% [markdown]
# 3. Next, we pair training files with training parameters, and launch training via `process`.
#    - Some tables may try to populate without upstream keys.
#    - Others, like `RecordingInfo` already have keys loaded.
#    - Note: DLC's model processes (e.g., Training, Evaluation) log a lot of information to the console, to quiet this, pass `verbose=False` to `process`

# %%
key = {
    "paramset_idx": 1,
    "training_id": 1,
    "video_set_id": 1,
    "project_path": "openfield-Pranav-2018-10-30/",
}
train.TrainingTask.insert1(key, skip_duplicates=True)
process.run(verbose=True)
model.RecordingInfo()

# %% [markdown]
# 4. Now to add such an upstream key: a model to the `Model` table, and `process` to evaluate.
#    - Include a user-friendly `model_name`
#    - Include the relative path for the project's `config.yaml`
#    - Add `shuffle` and `trainingsetindex`
#    - `insert_new_model` will prompt before inserting, but this can be skipped with `prompt=False`

# %%
model.Model.insert_new_model(
    model_name="OpenField-5",
    dlc_config=config_path,
    shuffle=1,
    trainingsetindex=0,
    paramset_idx=1,
    prompt=True,  # True is the default behavior
    model_description="Open field model trained 5 iterations",
)
process.run()

# %% [markdown]
# 5. Add a pose estimation task, and launch via `process`.
#    - Get all primary key information for a given recording
#    - Add the model and `task_mode` (i.e., load vs. trigger) to be applied
#    - Add any additional analysis parameters for `deeplabcut.analyze_videos`

# %%
key = (model.VideoRecording & "recording_id=2").fetch1("KEY")
key.update({"model_name": "OpenField-5", "task_mode": "trigger"})
analyze_params = {"save_as_csv": True}  # add any others from deeplabcut.analyze_videos
model.PoseEstimationTask.insert_estimation_task(key, params=analyze_params)
process.run()

# %% [markdown]
# 6. Retrieve estimated position data.

# %%
model.PoseEstimation.get_trajectory(key)

# %% [markdown]
# ## Summary and next step
#
# + This notebook runs through the workflow in an automatic manner.
#
# + The next notebook [06-Drop](06-Drop_Optional.ipynb) shows how to drop schemas and tables if needed.
