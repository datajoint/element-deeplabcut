# -*- coding: utf-8 -*-
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
# # Workflow DeepLabCut - Alternate Data

# %% [markdown]
# ## Introduction

# %% [markdown]
#
# This notebook provides a general introduction to DataJoint use via Element DeepLabcut. It follows the same structure as other notebooks in this directory, but uses data from the DeepLabCut team. 
#
# We recommend the other notebooks as they provide access to a pretrained model and allow for a more in-depth exploration of the features of the Element.

# %% [markdown]
# ## Example data

# %% [markdown]
#
# ### Download
#
# If you've already cloned the [main DLC repository](https://github.com/DeepLabCut/DeepLabCut), you already have this folder under `examples/openfield-Pranav-2018-10-30`. [This link](https://downgit.github.io/#/home?url=https://github.com/DeepLabCut/DeepLabCut/tree/master/examples/openfield-Pranav-2018-10-30) via [DownGit](https://downgit.github.io/) will start the single-directory download automatically as a zip. Unpack this zip and place it in a directory we'll refer to as your root.

# %% [markdown]
# ### Structure

# %% [markdown]
# The directory will be organized as follows within your chosen root
# directory.
#
# ```
#  /your-root/openfield-Pranav-2018-10-30/
#    - config.yaml
#    - labeled-data
#       - m4s1
#           - CollectedData_Pranav.csv
#           - CollectedData_Pranav.h5
#           - img0000.png
#           - img0001.png
#           - img0002.png
#           - img{...}.png
#           - img0114.png
#           - img0115.png
#    - videos
#        - m3v1mp4.mp4
# ```

# %% [markdown]
# For those unfamiliar with DLC...
# - `config.yaml` contains all the key parameters of the project, including
#    - file locations (currently empty)
#    - body parts
#    - cropping information
# - `labeled-data` includes the frames coordinates for each body part in the training video
# - `videos` includes the full training video for this example
#
# Part of the demo setup involves an additional
# command (as [shown here](https://github.com/DeepLabCut/DeepLabCut/blob/master/examples/JUPYTER/Demo_labeledexample_Openfield.ipynb)) to revise the project path within config file as well as generate the `training-datasets` directory.

# %%
your_root='/fill/in/your/root/with\ escaped\ spaces'
from deeplabcut.create_project.demo_data import load_demo_data
load_demo_data(your_root+'/openfield-Pranav-2018-10-30/config.yaml')

# %% [markdown]
# ### New video

# %% [markdown]
# Later, we'll use the first few seconds of the training video as a 'separate session' to demonstrate pose estimation within the Element. `ffmpeg` is a dependency of DeepLabCut
# that can splice the training video for a demonstration purposes. The command below saves
# the first 2 seconds of the training video as a copy.
#
# - `-n` do not overwrite
# - `-hide_banner -loglevel error` less verbose output
# - `-ss 0 -t 2` start at second 0, add 2 seconds
# - `-i {vid_path}` input this video
# - `-{v/a}codec copy` copy the video and audio codecs of the input
# - `{vid_path}-copy.mp4` output file

# %% tags=[]
vid_path = your_root + '/openfield-Pranav-2018-10-30/videos/m3v1mp4'
cmd = (f'ffmpeg -n -hide_banner -loglevel error -ss 0 -t 2 -i {vid_path}.mp4 '
       + f'-vcodec copy -acodec copy {vid_path}-copy.mp4')
import os; os.system(cmd)

# %% [markdown] tags=[]
# ## Configuring DataJoint

# %% [markdown]
# ### DataJoint Local Config

# %% [markdown] tags=[]
# - To run `workflow-deeplabcut`, we need to set up the DataJoint configuration file, called `dj_local_conf.json`, unique to each machine.
#
# - The config only needs to be set up once, skip to the next section.
#
# - By convention, we set a local config in the workflow directory. You may be interested in [setting a global config](https://docs.datajoint.org/python/setup/01-Install-and-Connect.html).

# %%
import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# ### Configure database credentials

# %% [markdown]
# Now let's set up the host, user and password in the `dj.config` following [instructions here](https://tutorials.datajoint.io/setting-up/get-database.html).

# %%
import datajoint as dj
import getpass
dj.config['database.host'] = '{YOUR_HOST}'
dj.config['database.user'] = '{YOUR_USERNAME}'
dj.config['database.password'] = getpass.getpass() # enter the password securely

# %% [markdown]
# You should be able to connect to the database at this stage.

# %%
dj.conn()

# %% [markdown]
# ### Workflow-specific items

# %% [markdown]
# **Prefix:** Giving a prefix to your schema could help manage privelages on a server. 
# - If we set prefix `neuro_`, every schema created with the current workflow will start with `neuro_`, e.g. `neuro_lab`, `neuro_subject`, `neuro_imaging` etc.
# - Teams who work on the same schemas should use the same prefix, set as follows:

# %%
dj.config['custom'] = {'database.prefix': 'neuro_'}

# %% [markdown]
# **Root dir:** `custom` keeps track of your root directory for this project. With multiple roots the Element will figure out which to use based on the files it expects. 
#
# - Please set one root to the parent directory of DLC's `openfield-Pranav-2018-10-30` example.
# - In other cases, this should be the parent of your DLC project path.
#
# We can then check that the path connects with a tool from [element-interface](https://github.com/datajoint/element-interface).

# %%
dj.config['custom'] = {'dlc_root_data_dir' : ['your-root1', 'your-root2']}

from element_interface.utils import find_full_path
data_dir = find_full_path(dj.config['custom']['dlc_root_data_dir'],
                          'openfield-Pranav-2018-10-30')
assert data_dir.exists(), "Please check the that you have the folder openfield-Pranav"

# %% [markdown]
# ### Saving the config

# %% [markdown]
#
# With the proper configurations, we could save this as a file, either as a local json file, or a global file. DataJoint will default to a local file, then check for a global if none is found.

# %%
dj.config.save_local() # saved as dj_local_conf.json in the root workflow dir
# dj.config.save_global() # saved as .datajoint_config.json in your home dir

# %% [markdown] tags=[]
# ## Workflow Structure

# %% [markdown]
# ### Schemas, Diagrams and Tables

# %% [markdown]
# Schemas are conceptually related sets of tables. By importing schemas from `workflow_deeplabcut.pipeline`, we'll declare the tables on the server with the prefix we set. If these tables are already declared, we'll gain access. For more information about lab, animal and session Elements, see [session workflow](https://github.com/datajoint/workflow-session).
#
# - `dj.list_schemas()` lists all schemas a user has access to in the current database
# - `<schema>.schema.list_tables()` will provide names for each table in the format used under the hood.

# %%
import datajoint as dj
from workflow_deeplabcut.pipeline import lab, subject, session, train, model

dj.list_schemas()

train.schema.list_tables()

# %% [markdown]
# `dj.Diagram()` plots tables and dependencies in a schema. To see additional upstream or downstream connections, add `- N` or `+ N`.
#
# - `train`: Optional schema to manage model training within DataJoint
# - `model`: Schema to manage pose estimation

# %% [markdown]
# #### Table Types
#
# - **Manual table**: green box, manually inserted table, expect new entries daily, e.g. Subject, ProbeInsertion.  
# - **Lookup table**: gray box, pre inserted table, commonly used for general facts or parameters. e.g. Strain, ClusteringMethod, ClusteringParamSet.  
# - **Imported table**: blue oval, auto-processing table, the processing depends on the importing of external files. e.g. process of Clustering requires output files from kilosort2.  
# - **Computed table**: red circle, auto-processing table, the processing does not depend on files external to the database, commonly used for     
# - **Part table**: plain text, as an appendix to the master table, all the part entries of a given master entry represent a intact set of the master entry. e.g. Unit of a CuratedClustering.
#
# #### Table Links
#
# - **One-to-one primary**: thick solid line, share the exact same primary key, meaning the child table inherits all the primary key fields from the parent table as its own primary key.     
# - **One-to-many primary**: thin solid line, inherit the primary key from the parent table, but have additional field(s) as part of the primary key as well
# - **Secondary dependency**: dashed line, the child table inherits the primary key fields from parent table as its own secondary attribute.

# %% `dj.Diagram()`: plot tables and dependencies
dj.Diagram(train) #- 1

# %%
dj.Diagram(model)

# %% [markdown]
# ### Common Table Functions

# %% [markdown]
#
# - `<table>()` show table contents
# - `heading` shows attribute definitions
# - `describe()` show table defintiion with foreign key references

# %% Each datajoint table class inside the module corresponds to a table inside the schema. For example, the class `ephys.EphysRecording` correponds to the table `_ephys_recording` in the schema `neuro_ephys` in the database.
model.VideoRecording.File()

# %% `heading`: show table attributes regardless of foreign key references.
model.Model.heading

# %%
train.TrainingTask.describe()

# %% [markdown] tags=[]
# ## Running the Workflow

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
# ### Manually Inserting Entries

# %% [markdown]
# #### Upstream tables

# %% [markdown]
# We can insert entries into `dj.Manual` tables (green in diagrams) by directly providing values as a dictionary. 

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

# %%
train.VideoSet.insert1({'video_set_id': 1})
labeled_dir = 'openfield-Pranav-2018-10-30/labeled-data/m4s1/'
training_files = ['CollectedData_Pranav.h5',
                  'CollectedData_Pranav.csv',
                  'img0000.png']
for idx, filename in training_files:
    train.VideoSet.File.insert1({'video_set_id': 1,
                                 'file_id': idx,   
                                 'file_path': (labeled_dir + file)})
train.VideoSet.File.insert1({'video_set_id':1, 'file_id': 4, 'file_path': 
                            'openfield-Pranav-2018-10-30/videos/m3v1mp4.mp4'})

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
# Now, we add a `TrainingTask`. As a computed table, `ModelTraining` will reference this to start training when calling `populate()`

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
# To resume training from a checkpoint, we would need to 
# [edit the relevant config file](https://github.com/DeepLabCut/DeepLabCut/issues/70).
# Emperical work from the Mathis team suggests 200k iterations for any true use-case.

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
bp_desc=['Left Ear', 'Right Ear', 'Snout Position', 'Base of Tail']
model.BodyPart.insert_from_config(config_path,bp_desc)

# %% [markdown] jp-MarkdownHeadingCollapsed=true tags=[]
# ### Declaring/Evaluating a Model

# %% [markdown]
# We can insert into `Model` table for automatic evaluation

# %%
model.Model.insert_new_model(model_name='OpenField-5',dlc_config=config_path,
                             shuffle=1,trainingsetindex=0,
                             model_description='Open field model trained 5 iterations',
                             paramset_idx=1)

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
key = {'subject': 'subject6',
       'session_datetime': '2021-06-02 14:04:22',
       'recording_id': '1', 'device': 'Camera1'}
model.VideoRecording.insert1(key)

_ = key.pop('device') # get rid of secondary key from master table
key.update({'file_id': 1, 
            'file_path': 'openfield-Pranav-2018-10-30/videos/m3v1mp4-copy.mp4'})
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
key.update({'model_name': 'OpenField-5', 'task_mode': 'trigger'})
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
# <!-- Next Steps -->
# .

# %% [markdown] pycharm={"name": "#%% md\n"}
# ## Workflow Automation

# %% [markdown]
# Below is a more automatic approach to run through the pipeline using some utility functions in the workflow using the `process.py` script to automatically trigger all computed tables.
#
# Because we just inserted all the data, we'll delete using the command below to start over.

# %%
from workflow_deeplabcut.process import run
safemode=None # Set to false to turn off confirmation prompts
(session.Session & 'subject="subject6"').delete(safemode=safemode)
train.TrainingParamSet.delete(safemode=safemode)
train.VideoSet.delete(safemode=safemode)

# %% [markdown]
# #### Automated Ingestion
#
# Refer to the `user_data` folder in the workflow for CSVs to fill in various tables.
#
# 1. Upstream tables:
#    - `subject.Subject` via `subjects.csv` 
#    - `session.Session` via `sessions.csv`
# 2. `train` schema:
#    - `train.TrainingParamSet` via `config_params.csv`
#    - `train.VideoSet` via `train_videosets.csv`
# 3. `model` schema:
#    - `model.VideoRecording` via `model_videos.csv`
#    - `model.Model` via `model_model.csv`
#   
# Run automatic ingestion via functions in `workflow_deeplabcut.ingest` 

# %%
from workflow_deeplabcut.ingest import ingest_subjects, ingest_sessions, ingest_dlc_items
ingest_subjects(); ingest_sessions(); ingest_dlc_items()

# %% [markdown]
# #### Setting project variables
#
# Set your root directory in your DataJoint config file, under `custom` as `dlc_root_data_dir`. 

# %%
import datajoint as dj; dj.config.load('dj_local_conf.json')
from element_interface.utils import find_full_path
data_dir = find_full_path(dj.config['custom']['dlc_root_data_dir'], # root from config
                          'openfield-Pranav-2018-10-30')            # DLC project dir
config_path = (data_dir / 'config.yaml')

# %% [markdown]
# #### Launching trainig
#
# Pair training files with training parameters, and launch training via `process`. 
#
# Note: DLC's model processes (e.g., Training, Evaluation) log a lot of information to the console, to quiet this, pass `verbose=False` to `process`

# %%
key={'paramset_idx':1,'training_id':1,'video_set_id':1, 
     'project_path':'openfield-Pranav-2018-10-30/'}
train.TrainingTask.insert1(key, skip_duplicates=True)
run(verbose=True)
model.RecordingInfo()

# %% [markdown]
# Now, add to `Model`, including
# - Include a user-friendly `model_name`
# - Include the relative path for the project's `config.yaml`
# - Add `shuffle` and `trainingsetindex`
# - `insert_new_model` will prompt before inserting, but this can be skipped with `prompt=False`

# %%
model.Model.insert_new_model(model_name='OpenField-5', 
                             dlc_config=config_path,
                             shuffle=1,
                             trainingsetindex=0,
                             paramset_idx=1, 
                             prompt=True, # True is the default behavior
                             model_description='Open field model trained 5 iterations')
run()

# %% [markdown]
# Add a pose estimation task, using
# - All primary key information for a given recording
# - Add the model and `task_mode` (i.e., load vs. trigger) to be applied
# - Add any additional analysis parameters for `deeplabcut.analyze_videos`

# %%
key=(model.VideoRecording & 'recording_id=2').fetch1('KEY')
key.update({'model_name': 'OpenField-5', 'task_mode': 'trigger'})
analyze_params={'save_as_csv':True} # add any others from deeplabcut.analyze_videos
model.PoseEstimationTask.insert_estimation_task(key,params=analyze_params)
run()

# %% [markdown]
# Retrieve estimated position data:

# %%
model.PoseEstimation.get_trajectory(key)

# %% [markdown] tags=[]
# ## Dropping schemas

# %% [markdown]
# + Schemas are not typically dropped in a production workflow with real data in it. 
# + At the developmental phase, it might be required for the table redesign.
# + When dropping all schemas is needed, drop items starting with the most downstream.

# %%
from workflow_deeplabcut.pipeline import *
# model.schema.drop()
# train.schema.drop()
# session.schema.drop()
# subject.schema.drop()
# lab.schema.drop()
