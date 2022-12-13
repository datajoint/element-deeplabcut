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
#     display_name: Python 3.9.13 ('ele')
#     language: python
#     name: python3
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown] tags=[]
# ## Interactively run the workflow

# %% [markdown]
#
# The workflow requires a DeepLabCut project with labeled data.
# - If you don't have data, refer to [00-DataDownload](./00-DataDownload_Optional.ipynb) and [01-Configure](./01-Configure.ipynb).
# - For an overview of the schema, refer to [02-WorkflowStructure](02-WorkflowStructure_Optional.ipynb).
# - For a more automated approach, refer to [03-Automate](03-Automate_Optional.ipynb).

# %% [markdown]
# Let's change the directory to load the local config, `dj_local_conf.json`.

# %%
import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# `Pipeline.py` activates the DataJoint `elements` and declares other required tables.

# %%
import datajoint as dj
from workflow_deeplabcut.pipeline import lab, subject, session, train, model

# Directing our pipeline to the appropriate config location
from element_interface.utils import find_full_path
from workflow_deeplabcut.paths import get_dlc_root_data_dir
config_path = find_full_path(get_dlc_root_data_dir(), 
                             'from_top_tracking/config.yaml')

# %% [markdown] tags=[]
# ## Manually Inserting Entries

# %% [markdown]
# ### Upstream tables

# %% [markdown]
# We can insert entries into `dj.Manual` tables (green in diagrams) by providing values as a dictionary or a list of dictionaries. 

# %%
session.Session.heading

# %%
subject.Subject.insert1(dict(subject='subject6', 
                             sex='F', 
                             subject_birth_date='2020-01-01', 
                             subject_description='hneih_E105'))
session_keys = [dict(subject='subject6', session_datetime='2021-06-02 14:04:22'),
                dict(subject='subject6', session_datetime='2021-06-03 14:43:10')]
session.Session.insert(session_keys)

# %% [markdown]
# We can look at the contents of this table and restrict by a value.

# %%
session.Session() & "session_datetime > '2021-06-01 12:00:00'" & "subject='subject6'"

# %% [markdown] tags=[]
# #### DeepLabcut Tables

# %% [markdown]
# The `VideoSet` table in the `train` schema retains records of files generated in the video labeling process (e.g., `h5`, `csv`, `png`). DeepLabCut will refer to the `mat` file located under the `training-datasets` directory.
#
# We recommend storing all paths as relative to the root in your config.

# %%
train.VideoSet.insert1({'video_set_id': 0})
project_folder = 'from_top_tracking/'
training_files = ['labeled-data/train1/CollectedData_DJ.h5',
                  'labeled-data/train1/CollectedData_DJ.csv',
                  'labeled-data/train1/img00674.png',
                  'videos/train1.mp4']
for idx, filename in enumerate(training_files):
    train.VideoSet.File.insert1({'video_set_id': 0,
                                 'file_id': idx,
                                 'file_path': (project_folder + filename)})

# %%
train.VideoSet.File()

# %% [markdown] tags=[]
# ### Training a Network

# %% [markdown]
# First, we'll add a `ModelTrainingParamSet`. This is a lookup table that we can reference when training a model.

# %%
train.TrainingParamSet.heading

# %% [markdown]
# The `params` longblob should be a dictionary that captures all items for DeepLabCut's `train_network` function. At minimum, this is the contents of the project's config file, as well as `suffle` and `trainingsetindex`, which are not included in the config. 

# %%
from deeplabcut import train_network
help(train_network) # for more information on optional parameters

# %% [markdown]
# Here, we give these items, load the config contents, and overwrite some defaults, including `maxiters`, to restrict our training iterations to 5.

# %%
import yaml

paramset_idx = 0; paramset_desc='from_top_tracking'

with open(config_path, 'rb') as y:
    config_params = yaml.safe_load(y)
training_params = {'shuffle': '1',
                   'trainingsetindex': '0',
                   'maxiters': '5',
                   'scorer_legacy': 'False',
                   'maxiters': '5', 
                   'multianimalproject':'False'}
config_params.update(training_params)
train.TrainingParamSet.insert_new_params(paramset_idx=paramset_idx,
                                         paramset_desc=paramset_desc,
                                         params=config_params)

# %% [markdown]
# Now, we add a `TrainingTask`. As a computed table, `ModelTraining` will reference this to start training when calling `populate()`

# %%
train.TrainingTask.heading

# %%
key={'video_set_id': 0,
     'paramset_idx':0,
     'training_id': 1,
     'project_path':'from_top_tracking/'
     }
train.TrainingTask.insert1(key, skip_duplicates=True)
train.TrainingTask()

# %% tags=[]
train.ModelTraining.populate()

# %% [markdown]
# (Output cleared for brevity)
# ```
# The network is now trained and ready to evaluate. Use the function 'evaluate_network' to evaluate the network.
# ```

# %%
train.ModelTraining()

# %% [markdown]
# To resume training from a checkpoint, we would need to 
# [edit the relevant config file](https://github.com/DeepLabCut/DeepLabCut/issues/70) (see also `update_pose_cfg` in `workflow_deeplabcut.load_demo_data`).
# Emperical work suggests 200k iterations for any true use-case.
#
# For better quality predictions in this demo, we'll revert the checkpoint file and use a pretrained model.

# %%
from workflow_deeplabcut.load_demo_data import revert_checkpoint_file
revert_checkpoint_file()

# %% [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ### Tracking Joints/Body Parts

# %% [markdown]
# The `model` schema uses a lookup table for managing Body Parts tracked across models.

# %%
model.BodyPart.heading

# %% [markdown]
# Helper functions allow us to first, identify all the new body parts from a given config, and, second, insert them with user-friendly descriptions.

# %%
model.BodyPart.extract_new_body_parts(config_path)

# %%
bp_desc=['Body Center', 'Head', 'Base of Tail']
model.BodyPart.insert_from_config(config_path,bp_desc)

# %% [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ### Declaring/Evaluating a Model

# %% [markdown]
# We can insert into `Model` table for automatic evaluation

# %%
model.Model.insert_new_model(model_name='FromTop-latest',dlc_config=config_path,
                             shuffle=1,trainingsetindex=0,
                             model_description='FromTop - latest snapshot',
                             paramset_idx=0,
                             params={"snapshotindex":-1})

# %%
model.Model()

# %% [markdown]
# `ModelEvaluation` will reference the `Model` using the `populate` method and insert the  output from DeepLabCut's `evaluate_network` function

# %%
model.ModelEvaluation.heading

# %%
model.ModelEvaluation.populate()

# %%
model.ModelEvaluation()

# %% [markdown]
# ### Pose Estimation

# %% [markdown]
# To use our model, we'll first need to insert a session recoring into `VideoRecording`

# %%
model.VideoRecording()

# %%
key = {'subject': 'subject6',
       'session_datetime': '2021-06-02 14:04:22',
       'recording_id': '1', 'device': 'Camera1'}
model.VideoRecording.insert1(key)

_ = key.pop('device') # get rid of secondary key from master table
key.update({'file_id': 1, 
            'file_path': 'from_top_tracking/videos/test-2s.mp4'})
model.VideoRecording.File.insert1(key)

# %%
model.VideoRecording.File()

# %% [markdown]
# `RecordingInfo` automatically populates with file information

# %%
model.RecordingInfo.populate()
model.RecordingInfo()

# %% [markdown]
# Next, we specify if the `PoseEstimation` table should load results from an existing file or trigger the estimation command. Here, we can also specify parameters for DeepLabCut's `analyze_videos` as a dictionary.

# %%
key = (model.VideoRecording & {'recording_id': '1'}).fetch1('KEY')
key.update({'model_name': 'FromTop-latest', 'task_mode': 'trigger'})
key

# %%
model.PoseEstimationTask.insert_estimation_task(key,params={'save_as_csv':True})
model.PoseEstimation.populate()

# %% [markdown]
# By default, DataJoint will store results in a subdirectory
# >       <processed_dir> / videos / device_<name>_recording_<#>_model_<name>
# where `processed_dir` is optionally specified in the datajoint config. If unspecified, this will be the project directory. The device and model names are specified elsewhere in the schema.
#
# We can get this estimation directly as a pandas dataframe.

# %%
model.PoseEstimation.get_trajectory(key)

# %% [markdown]
# In the [next notebook](./04-Automate_Optional.ipynb), we'll look at additional tools in the workflow for automating these steps.
