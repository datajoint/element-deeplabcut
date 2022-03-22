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

# %% [markdown] tags=[]
# ## Configure DataJoint

# %% [markdown] tags=[]
# - To run `workflow-deeplabcut`, we need to set up the DataJoint configuration file, called `dj_local_conf.json`, unique to each machine.
#
# - The config only needs to be set up once. If you have gone through the configuration before, directly go to [02-Workflow-Structure](./02-WorkflowStructure_Optional.ipynb).
#
# - By convention, we set the config up in the root directory of `workflow-deeplabcut` package. After you set up DataJoint once, you may be interested in [setting a global config](https://docs.datajoint.org/python/setup/01-Install-and-Connect.html).

# %%
import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# ### Configure database host address and credentials

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
# ### Configure the `custom` field in `dj.config` for element-deeplabcut

# %% [markdown]
# #### Prefix

# %% [markdown]
# Giving a prefix to your schema could help manage privelages on a server. 
# - If we set prefix `neuro_`, every schema created with the current workflow will start with `neuro_`, e.g. `neuro_lab`, `neuro_subject`, `neuro_imaging` etc.
# - Teams who work on the same schemas should use the same prefix, set as follows:

# %%
dj.config['custom'] = {'database.prefix': 'neuro_'}

# %% [markdown]
# #### Root directory

# %% [markdown]
# The `custom` field also keeps track of your root directory with `dlc_root_data_dir`. It can even accept roots. element-deeplabcut will always figure out which root to use based on the files it expects there. 
#
# - Please set one root to the parent directory of DLC's `openfield-Pranav-2018-10-30` example.
# - In other cases, this should be the parent of your DLC project path.

# %%
dj.config['custom'] = {'dlc_root_data_dir' : ['your-root1', 'your-root2']}

# %% [markdown]
# Let's check that find the path connects with a tool from [element-interface](https://github.com/datajoint/element-interface).

# %%
from element_interface.utils import find_full_path
data_dir = find_full_path(dj.config['custom']['dlc_root_data_dir'],
                          'openfield-Pranav-2018-10-30')
assert data_dir.exists(), "Please check the that you have the folder openfield-Pranav"

# %% [markdown]
# ## Save the config as a json file
#
# With the proper configurations, we could save this as a file, either as a local json file, or a global file.

# %%
dj.config.save_local()

# %% [markdown]
# The local config is saved as `dj_local_conf.json` in the root directory of this `workflow-deeplabcut`. Next time you import DataJoint while in this directory, the same settings will be loaded.
#
# If saved globally, there will be a hidden configuration file saved in your computer's root directory that will be loaded when no local version is present.

# %%
# dj.config.save_global()

# %% [markdown]
# In the [next notebook](./02-WorkflowStructure_Optional.ipynb) notebook, we'll explore the workflow structure.
