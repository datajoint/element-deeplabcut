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
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown]
# ## Introduction

# %% [markdown]
# This notebook introduces some useful DataJoint for exploring pipelines featuring the DeepLabCut Element.
#
# + DataJoint needs to be configured before running this notebook (see [01-Configure](./01-Configure.ipynb)).
# + Those familar with the structure of DataJoint workflows can skip to [03-Process](./03-Process.ipynb).
# + The playground tutorial on [CodeBook](http://codebook.datajoint.io/) provides a more  thorough introduction. 

# %% [markdown]
# To load the local config, we move to the package root.

# %%
import os
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# ## Schemas, Diagrams and Tables

# %% [markdown]
# Schemas are conceptually related sets of tables. By importing schemas from `workflow_deeplabcut.pipeline`, we'll declare the tables on the server with the prefix in the config (if we have permission to do so). If these tables are already declared, we'll gain access. 
#
# - `dj.list_schemas()` lists all schemas a user has access to in the current database
# - `<schema>.schema.list_tables()` will provide names for each table in the format used under the hood.

# %%
import datajoint as dj
from workflow_deeplabcut.pipeline import lab, subject, session, train, model

dj.list_schemas()

# %%
train.schema.list_tables()

# %% [markdown]
# `dj.Diagram()` plots tables and dependencies in a schema. To see additional upstream or downstream connections, add `- N` or `+ N`.
#
# - `train`: Optional schema to manage model training within DataJoint
# - `model`: Schema to manage pose estimation

# %% `dj.Diagram()`: plot tables and dependencies
dj.Diagram(train)

# %%
dj.Diagram(model) - 1

# %% [markdown]
# ### Table Types
#
# - **Manual table**: green box, manually inserted table, expect new entries daily, e.g. Subject, ProbeInsertion.  
# - **Lookup table**: gray box, pre inserted table, commonly used for general facts or parameters. e.g. Strain, ClusteringMethod, ClusteringParamSet.  
# - **Imported table**: blue oval, auto-processing table, the processing depends on the importing of external files. e.g. process of Clustering requires output files from kilosort2.  
# - **Computed table**: red circle, auto-processing table, the processing does not depend on files external to the database, commonly used for     
# - **Part table**: plain text, as an appendix to the master table, all the part entries of a given master entry represent a intact set of the master entry. e.g. Unit of a CuratedClustering.
#
# ### Table Links
#
# - **One-to-one primary**: thick solid line, share the exact same primary key, meaning the child table inherits all the primary key fields from the parent table as its own primary key.     
# - **One-to-many primary**: thin solid line, inherit the primary key from the parent table, but have additional field(s) as part of the primary key as well
# - **Secondary dependency**: dashed line, the child table inherits the primary key fields from parent table as its own secondary attribute.

# %% [markdown]
# ## Common Table Functions

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

# %% ephys [markdown]
# ## Other Elements installed with the workflow
#
# - [`lab`](https://github.com/datajoint/element-lab): lab management related information, such as Lab, User, Project, Protocol, Source.
# - [`subject`](https://github.com/datajoint/element-animal): general animal information, User, Genetic background, Death etc.
# - [`session`](https://github.com/datajoint/element-session): General information of experimental sessions.
#
# For more information about these Elements, see [workflow session](https://github.com/datajoint/workflow-session).

# %%
dj.Diagram(lab) + dj.Diagram(subject) + dj.Diagram(session)

# %% [session](https://github.com/datajoint/element-session): experimental session information
session.Session.describe()

# %% [markdown]
# ## Summary and next step
#
# - This notebook introduced the overall structures of the schemas and tables in the workflow and relevant tools to explore the schema structure and table definitions.
#
# - The [next notebook](./03-Process.ipynb) will introduce the detailed steps to run through `workflow-deeplabcut`.
