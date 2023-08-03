# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3.8.11 ('ele')
#     language: python
#     name: python3
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown] pycharm={"name": "#%% md\n"}
# ## Workflow Automation
#
# In the previous notebook [03-Process](./03-Process.ipynb), we ran through the workflow in detailed steps, manually adding each. The current notebook provides a more automated approach.
#
# The commands here run a workflow using example data from the [00-DownloadData](./00-DataDownload_Optional.ipynb) notebook, but note where placeholders could be changed for a different dataset.

# %% tags=[]
import os; from pathlib import Path
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")
from workflow_deeplabcut.pipeline import lab, subject, session, train, model
from workflow_deeplabcut import process

# %% [markdown]
# We'll be using the `process.py` script to automatically loop through all `make` functions, as a shortcut for calling each individually.
#
# If you previously completed the [03-Process notebook](./03-Process.ipynb), you may want to delete the contents ingested there, to avoid duplication errors.

# %%
safemode=True # Set to false to turn off confirmation prompts
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
from workflow_deeplabcut.ingest import ingest_subjects, ingest_sessions, ingest_dlc_items
ingest_subjects()
ingest_sessions()
ingest_dlc_items()

# %% [markdown]
# ## Setting project variables
#
# 1. Set your root directory in your DataJoint config file, under `custom` as `dlc_root_data_dir`. 

# %%
import datajoint as dj; dj.config.load('dj_local_conf.json')
from element_interface.utils import find_full_path
data_dir = find_full_path(dj.config['custom']['dlc_root_data_dir'], # root from config
                          'from_top_tracking')                      # DLC project dir
config_path = (data_dir / 'config.yaml')

# %% [markdown]
# 2. Next, we pair training files with training parameters, and launch training via `process`. 
#    - Some tables may try to populate without upstream keys. 
#    - Others, like `RecordingInfo` already have keys loaded.
#    - Note: DLC's model processes (e.g., Training, Evaluation) log a lot of information to the console, to quiet this, pass `verbose=False` to `process`

# %%
key={'paramset_idx':0,'training_id':0,'video_set_id':0, 
     'project_path':'from_top_tracking/'}
train.TrainingTask.insert1(key, skip_duplicates=True)
process.run(verbose=True, display_progress=True)
model.RecordingInfo()

# %% [markdown]
# For the purposes of this demo, we'll want to use an older model, so the folling function will reload the original checkpoint file.

# %%
from workflow_deeplabcut.load_demo_data import revert_checkpoint_file
revert_checkpoint_file()

# %% [markdown]
# 3. Now to add such a model upstream key
#    - Include a user-friendly `model_name`
#    - Include the relative path for the project's `config.yaml`
#    - Add `shuffle` and `trainingsetindex`
#    - `insert_new_model` will prompt before inserting, but this can be skipped with `prompt=False`

# %%
model.Model.insert_new_model(model_name='FromTop-latest', 
                             dlc_config=config_path,
                             shuffle=1,
                             trainingsetindex=0,
                             paramset_idx=1, 
                             prompt=True, # True is the default behavior
                             model_description='FromTop - latest snapshot',
                             params={"snapshotindex":-1})
process.run()

# %% [markdown]
# 4. Add a pose estimation task, and launch via `process`.
#    - Get all primary key information for a given recording
#    - Add the model and `task_mode` (i.e., load vs. trigger) to be applied
#    - Add any additional analysis parameters for `deeplabcut.analyze_videos`

# %%
key=(model.VideoRecording & 'recording_id=1').fetch1('KEY')
key.update({'model_name': 'FromTop-latest', 'task_mode': 'trigger'})
analyze_params={'save_as_csv':True} # add any others from deeplabcut.analyze_videos
model.PoseEstimationTask.insert_estimation_task(key,params=analyze_params)
process.run()

# %% [markdown]
# 5. Retrieve estimated position data.

# %%
model.PoseEstimation.get_trajectory(key)

# %% [markdown]
# ## Summary and next step
#
# + This notebook runs through the workflow in an automatic manner.
#
# + The next notebook [05-Visualization](./05-Visualization_Optional.ipynb) demonstrates how to plot this data and label videos on disk.
