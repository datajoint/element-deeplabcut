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

# %% [markdown]
# ## Download example data

# %% [markdown]
# These notebooks are built around data provided by DataJoint, including a well-trained model. For similar content using data from DeepLabCut, see [09-AlternateDataset](./09-AlternateDataset.ipynb).
#
# DataJoint provides various datasets via `djarchive`. To pip install...

# %% vscode={"languageId": "shellscript"}
pip install git+https://github.com/datajoint/djarchive-client.git

# %%
import os; import djarchive_client
client = djarchive_client.client()

# %% [markdown]
# We can browse available datasets:

# %%
list(client.datasets())

# %% [markdown]
# Datasets have different versions available:

# %%
list(client.revisions())

# %% [markdown]
# We can make a directory for downloading:

# %%
os.makedirs('/tmp/test_data', exist_ok=True)

# %% [markdown]
# Then run download for a given set and the revision:

# %%
client.download('workflow-dlc-data',
                target_directory='/tmp/test_data/', 
                revision='v1')

# %% [markdown]
# ## Directory organization
#
# After downloading, the directory will be organized as follows:

# %% [markdown]
# ```
# /tmp/test_data/from_top_tracking/
# - config.yml
# - dlc-models/iteration-0/from_top_trackingFeb23-trainset95shuffle1/
#     - test/pose_cfg.yaml
#     - train/
#         - checkpoint
#         - checkpoint_orig
#         ─ learning_stats.csv
#         ─ log.txt
#         ─ pose_cfg.yaml
#         ─ snapshot-10300.data-00000-of-00001
#         ─ snapshot-10300.index
#         ─ snapshot-10300.meta   # same for 103000
# - labeled-data/
#     - train1/
#         - CollectedData_DJ.csv
#         - CollectedData_DJ.h5
#         - img00674.png          # and others
#     - train2/                   # similar to above
# - videos/
#     - test.mp4
#     - train1.mp4
# ```

# %% [markdown]
# We will use this dataset as an example across this series of notebooks. If you use another dataset, change the path accordingly.
#
# - `config.yaml` contains key parameters of the project
# - `labeled-data` includes pixel coordinates for each body part
# - `videos` includes the full training and inference videos
#
# This workflow contains additional functions for setting up this demo data, including adding absolute paths to config files and shortening the inference video to speed up pose estimation.

# %%
from workflow_deeplabcut.load_demo_data import setup_bare_project, shorten_video

setup_bare_project(project="/tmp/test_data/from_top_tracking", 
                   net_type = "mobilenet_v2_1.0") # sets paths
shorten_video("/tmp/test_data/from_top_tracking/videos/test.mp4",
              output_path=None,first_n_sec=2) # makes test-2s.mp4

# %% [markdown]
# For your own data, we recommend using the DLC gui to intitialize your project and label the data. 
#
# In the next notebook, [01-Configure](./01-Configure.ipynb), we'll set up the DataJoint config file with a pointer to your root data directory.
