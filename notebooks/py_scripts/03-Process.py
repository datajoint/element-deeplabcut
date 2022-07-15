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
#     display_name: Python 3.8.11 ('ele')
#     language: python
#     name: python3
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown] tags=[]
# ## Interactively run the workflow
#
# The workflow requires a DeepLabCut project with labeled data.
# - If you haven't configured the data, refer to [00-DataDownload](./00-DataDownload_Optional.ipynb) and [01-Configure](./01-Configure.ipynb).
# - To overview the schema structures, refer to [02-WorkflowStructure](02-WorkflowStructure_Optional.ipynb).
# - If you'd likea more automatic approach, refer to [03-Automate](03-Automate_optional.ipynb).

# %% [markdown]
# Let's change the directory to the package root directory to load the local config, `dj_local_conf.json`.

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
                             'openfield-Pranav-2018-10-30/config.yaml')

# %% [markdown] tags=[]
# ### Inserting entries into upstream tables

# %% [markdown]
# In general, you can manually insert entries into each table by directly providing values for each column as a dictionary. Be sure to follow the type specified in the table definition.

# %%
subject.Subject.heading

# %%
subject.Subject.insert1(dict(subject='subject6', 
                             sex='F', 
                             subject_birth_date='2020-01-01', 
                             subject_description='hneih_E105'))

# %%
subject.Subject & "subject='subject6'"

# %%
session.Session.describe();

# %%
session.Session.heading

# %%
session_keys = [dict(subject='subject6', session_datetime='2021-06-02 14:04:22'),
                dict(subject='subject6', session_datetime='2021-06-03 14:43:10')]
session.Session.insert(session_keys)

# %%
session.Session() & "session_datetime > '2021-06-01 12:00:00'" & "subject='subject6'"

# %% [markdown] tags=[]
# ### Inserting recordings

# %% [markdown]
# The `VideoSet` table handles all files generated in the video labeling process, including the `h5`, `csv`, and `png` files under the `labeled-data` directory. While these aren't required for launching DLC training, it may be helpful to retain records. DLC will instead refer to the `mat` file located under the `training-datasets` directory.

# %%
train.VideoSet.insert1({'video_set_id': 1})
labeled_dir = 'openfield-Pranav-2018-10-30/labeled-data/m4s1/'
training_files = ['CollectedData_Pranav.h5',
                  'CollectedData_Pranav.csv',
                  'img0000.png']
for file in training_files:
    train.VideoSet.File.insert1({'video_set_id': 1,
                                 'file_path': (labeled_dir + file)})
train.VideoSet.File.insert1({'video_set_id':1, 'file_path': 
                            'openfield-Pranav-2018-10-30/videos/m3v1mp4.mp4'})

# %%
train.VideoSet.File()

# %% [markdown] tags=[]
# ### Training a DLC Network

# %% [markdown]
# First, we'll add a `ModelTrainingParamSet`. This is a lookup table that we can reference when training a model.

# %%
train.TrainingParamSet.heading

# %% [markdown]
# The `params` longblob should be a dictionary that includes all items to be included in model training via the `train_network` function. At minimum, this is the contents of the project's config file, as well as `suffle` and `trainingsetindex`, which are not included in the config. 

# %%
from deeplabcut import train_network
help(train_network) # for more information on optional parameters

# %% [markdown]
# Below, we give the parameters and index and description and load the config contents. We can then overwrite any defaults, including `maxiters`, to restrict our training iterations to 5.

# %%
import yaml

paramset_idx = 1; paramset_desc='OpenField'

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
# Then we add training to the the `TrainingTask` table. The `ModelTraining` table can automatically train and populate all tasks outlined in `TrainingTask`.

# %%
train.TrainingTask.heading

# %%
key={'video_set_id': 1, 'paramset_idx':1,'training_id':1,
     'project_path':'openfield-Pranav-2018-10-30/'}
train.TrainingTask.insert1(key, skip_duplicates=True)
train.TrainingTask()

# %% tags=[]
train.ModelTraining.populate()

# %%
train.ModelTraining()

# %% [markdown]
# To start training from a previous instance, one would need to 
# [edit the relevant config file](https://github.com/DeepLabCut/DeepLabCut/issues/70) and
# adjust the `maxiters` paramset (if present) to a higher threshold (e.g., 10 for 5 more itterations).
# Emperical work from the Mathis team suggests 200k iterations for any true use-case.

# %% [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ### Tracking Joints/Body Parts

# %% [markdown]
# The `model` schema uses a lookup table for managing Body Parts tracked across models.

# %%
model.BodyPart.heading

# %% [markdown]
# This table is equipped with two helper functions. First, we can identify all the new body parts from a given config file.

# %%
model.BodyPart.extract_new_body_parts(config_path)

# %% [markdown]
# Now, we can make a list of descriptions in the same order, and insert them into the table

# %%
bp_desc=['Left Ear', 'Right Ear', 'Snout Position', 'Base of Tail']
model.BodyPart.insert_from_config(config_path,bp_desc)

# %% [markdown]
# If we skip this step, body parts (without descriptions) will be added when we insert a model. We can [update](https://docs.datajoint.org/python/v0.13/manipulation/3-Cautious-Update.html) empty descriptions at any time.

# %% [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ### Declaring a Model

# %% [markdown]
# If training appears successful, the result can be inserted into the `Model` table for automatic evaluation.

# %%
model.Model.insert_new_model(model_name='OpenField-5',dlc_config=config_path,
                             shuffle=1,trainingsetindex=0,
                             model_description='Open field model trained 5 iterations',
                             paramset_idx=1)

# %%
model.Model()

# %% [markdown]
# ### Model Evaluation

# %% [markdown]
# Next, all inserted models can be evaluated with a similar `populate` method, which will
# insert the relevant output from DLC's `evaluate_network` function.

# %%
model.ModelEvaluation.heading

# %% [markdown]
# If your project was initialized in a version of DeepLabCut other than the one you're currently using, model evaluation may report key errors. Specifically, your `config.yaml` may not specify `multianimalproject: false`.

# %%
model.ModelEvaluation.populate()

# %%
model.ModelEvaluation()

# %% [markdown]
# ### Pose Estimation

# %% [markdown]
# To put this model to use, we'll conduct pose estimation on the video generated in the [DataDownload notebook](./00_DataDownload_Optional.ipynb). First, we need to update the `VideoRecording` table with the recording from a session.

# %%
key = {'subject': 'subject6',
       'session_datetime': '2021-06-02 14:04:22',
       'recording_id': '1', 'equipment': 'Camera1'}
model.VideoRecording.insert1(key)

# %% [markdown]
# Note that `/` at the beginning of a path implies the machine's root directory. Do not include an initial `/` in relative file paths.

# %%
_ = key.pop('equipment') # get rid of secondary key from master table
key.update({'file_id': 1, 
            'file_path': 'openfield-Pranav-2018-10-30/videos/m3v1mp4-copy.mp4'})
model.VideoRecording.File.insert1(key)

# %%
model.VideoRecording.File()

# %% [markdown]
# To automatically get recording information about this file, we can use the `make` function of the `RecordingInfo` table.

# %%
model.RecordingInfo.populate()
model.RecordingInfo()

# %% [markdown]
#  Next, we need to specify if the `PoseEstimation` table should load results from an existing file or trigger the estimation command. Here, we can also specify parameters accepted by the `analyze_videos` function as a dictionary.

# %%
key = (model.VideoRecording & {'recording_id': '1'}).fetch1('KEY')
key.update({'model_name': 'OpenField-5', 'task_mode': 'trigger'})
key

# %%
model.PoseEstimationTask.insert_estimation_task(key,params={'save_as_csv':True})

# %%
model.PoseEstimation.populate()

# %% [markdown]
# By default, DataJoint will store the results of pose estimation in a subdirectory
# >  processed_dir / videos / device_<#>_recording_<#>_model_<name>
#
# Pulling processed_dir from `get_dlc_processed_dir`, and device/recording information 
# from the `VideoRecording` table. The model name is taken from the primary key of the
# `Model` table, with spaced replaced by hyphens.
#     
# We can get this estimation directly as a pandas dataframe.

# %%
model.PoseEstimation.get_trajectory(key)

# %% [markdown]
# <!-- Next Steps -->
# .
