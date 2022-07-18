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

# %% [markdown]
# Change into the parent directory to find the `dj_local_conf.json` file. 

# %% tags=[]
import os; from pathlib import Path
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# ## Drop schemas
#
# + Schemas are not typically dropped in a production workflow with real data in it. 
# + At the developmental phase, it might be required for the table redesign.
# + When dropping all schemas is needed, drop items starting with the most downstream.

# %%
from workflow_deeplabcut.pipeline import *

# %%
# model.schema.drop()
# train.schema.drop()
# session.schema.drop()
# subject.schema.drop()
# lab.schema.drop()
