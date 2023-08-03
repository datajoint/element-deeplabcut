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
# ## Configure DataJoint

# %% [markdown] tags=[]
# - To run `workflow-deeplabcut`, we need to set up the DataJoint config file, called `dj_local_conf.json`, unique to each machine.
#
# - The config only needs to be set up once. If you already have one, skip to [02-Workflow-Structure](./02-WorkflowStructure_Optional.ipynb).
#
# - By convention, we set a local config in the workflow directory. You may be interested in [setting a global config](https://docs.datajoint.org/python/setup/01-Install-and-Connect.html).

# %%
import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# ### Configure database host address and credentials

# %% [markdown]
# Now we can set up credentials following [instructions here](https://tutorials.datajoint.io/setting-up/get-database.html).

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
# ### Configure the `custom` field

# %% [markdown]
# #### Prefix

# %% [markdown]
# A schema prefix can help manage privelages on a server. Teams who work on the same schemas should use the same prefix
#
# Setting the prefix to `neuro_` means that every schema we then create will start with `neuro_` (e.g. `neuro_lab`, `neuro_subject`, `neuro_model` etc.)

# %%
dj.config['custom'] = {'database.prefix': 'neuro_'}

# %% [markdown]
# #### Root directory

# %% [markdown]
# `dlc_root_data_dir` sets the root path(s) for the Element. Given multiple, the Element will always figure out which root to use based on the files it expects there. This should be the directory above your DeepLabCut project path.

# %%
dj.config['custom'] = {'dlc_root_data_dir' : ['/tmp/test_data/', '/tmp/example/']}

# Check the connection with `find_full_path`
from element_interface.utils import find_full_path
data_dir = find_full_path(dj.config['custom']['dlc_root_data_dir'],
                          'from_top_tracking')
assert data_dir.exists(), "Please check the that you have the from_top_tracking folder"

# %% [markdown]
# ## Save the config as a json
#
# Once set, the config can either be saved locally or globally. 
#
# - The local config would be saved as `dj_local_conf.json` in the workflow directory. This is usefull for managing multiple (demo) pipelines.
# - A global config would be saved as `datajoint_config.json` in the home directory.
#
# When imported, DataJoint will first check for a local config. If none, it will check for a global config.

# %%
dj.config.save_local()
# dj.config.save_global()

# %% [markdown]
# In the [next notebook](./02-WorkflowStructure_Optional.ipynb) notebook, we'll explore the workflow structure.
