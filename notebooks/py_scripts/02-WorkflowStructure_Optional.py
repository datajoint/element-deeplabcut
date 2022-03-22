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
#     display_name: venv-dlc
#     language: python
#     name: venv-dlc
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown]
# ## Introduction

# %% [markdown]
# This notebook gives a brief overview and introduces some useful DataJoint tools to facilitate the exploration.
#
# + DataJoint needs to be configured before running this notebook, if you haven't done so, refer to the [01-Configure](./01-Configure.ipynb) notebook.
# + If you are familar with DataJoint and the workflow structure, proceed to the next notebook [03-Process](./03-Process.ipynb) directly to run the workflow.
# + For a more thorough introduction of DataJoint functionings, please visit our [general tutorial site](http://codebook.datajoint.io/)

# %% [markdown]
# To load the local configuration, we will change the directory to the package root.

# %%
import os
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-deeplabcut', ("Please move to the "
                                                              + "workflow directory")

# %% [markdown]
# ## Schemas and tables

# %% [markdown]
# By importing from `workflow_deeplabcut`, we'll run the activation functions that declare the tables in these schemas. If these tables are already declared, we'll gain access.

# %%
import datajoint as dj
from workflow_deeplabcut.pipeline import lab, subject, session, train, model

# %% [markdown]
# Each module contains a schema object that enables interaction with the schema in the database. For more information abotu managing the upstream tables, see our [session workflow](https://github.com/datajoint/workflow-session). In this case, lab is required because the pipeline adds a `Device` table to the lab schema to keep track of camera IDs. The pipeline also adds a `VideoRecording` table to the session schema.

# %% The schemas and tables will not be re-created when importing modules if they have existed. [markdown]
# `dj.list_schemas()` lists all schemas a user has access to in the current database
# %% `dj.list_schemas()`: list all schemas a user could access.
dj.list_schemas()

# %% [markdown]
# `<schema>.schema.list_tables()` will provide names for each table in the format used under the hood.

# %% Each module imported above corresponds to one schema inside the database. For example, `ephys` corresponds to `neuro_ephys` schema in the database.
train.schema.list_tables()

# %% [markdown]
# `dj.Diagram()` plots tables and dependencies in a schema. To see additional upstream or downstream connections, add `- N` or `+ N` where N is the number of additional links.
#
# While the `model` schema is required for pose estimation, the `train` schema is optional, and can be used to manage model training within DataJoint

# %% `dj.Diagram()`: plot tables and dependencies
dj.Diagram(train) #- 1

# %%
dj.Diagram(model)

# %% [markdown]
# ### Table tiers 
# - **Manual table**: green box, manually inserted table, expect new entries daily, e.g. Subject, ProbeInsertion.  
# - **Lookup table**: gray box, pre inserted table, commonly used for general facts or parameters. e.g. Strain, ClusteringMethod, ClusteringParamSet.  
# - **Imported table**: blue oval, auto-processing table, the processing depends on the importing of external files. e.g. process of Clustering requires output files from kilosort2.  
# - **Computed table**: red circle, auto-processing table, the processing does not depend on files external to the database, commonly used for     
# - **Part table**: plain text, as an appendix to the master table, all the part entries of a given master entry represent a intact set of the master entry. e.g. Unit of a CuratedClustering.
#
# ### Dependencies
#
# - **One-to-one primary**: thick solid line, share the exact same primary key, meaning the child table inherits all the primary key fields from the parent table as its own primary key.     
# - **One-to-many primary**: thin solid line, inherit the primary key from the parent table, but have additional field(s) as part of the primary key as well
# - **secondary dependency**: dashed line, the child table inherits the primary key fields from parent table as its own secondary attribute.

# %% `dj.Diagram()`: plot the diagram of the tables and dependencies. It could be used to plot tables in a schema or selected tables.
# plot diagram of tables in multiple schemas
dj.Diagram(subject.Subject) + dj.Diagram(session.Session) + dj.Diagram(model)

# %%
lab.schema.list_tables()

# %%
# plot diagram of selected tables and schemas
(dj.Diagram(subject.Subject) + dj.Diagram(session.Session) 
 + dj.Diagram(model.VideoRecording) + dj.Diagram(model.PoseEstimationTask)) 

# %% Each datajoint table class inside the module corresponds to a table inside the schema. For example, the class `ephys.EphysRecording` correponds to the table `_ephys_recording` in the schema `neuro_ephys` in the database.
# preview columns and contents in a table
model.VideoRecording.File()

# %% `heading`: [markdown]
# `describe()` shows table definition with foreign key references
# %%
train.TrainingTask.describe()

# %% [markdown]
# `heading` shows attribute definitions regardless of foreign key references

# %% `heading`: show table attributes regardless of foreign key references.
model.Model.heading

# %% ephys [markdown]
# ## Other Elements installed with the workflow
#
# [`lab`](https://github.com/datajoint/element-lab): lab management related information, such as Lab, User, Project, Protocol, Source.

# %%
dj.Diagram(lab)

# %% [markdown]
# [`subject`](https://github.com/datajoint/element-animal): general animal information, User, Genetic background, Death etc.

# %%
dj.Diagram(subject)

# %% [subject](https://github.com/datajoint/element-animal): contains the basic information of subject, including Strain, Line, Subject, Zygosity, and SubjectDeath information.
subject.Subject.describe();

# %% [markdown]
# [`session`](https://github.com/datajoint/element-session): General information of experimental sessions.

# %%
dj.Diagram(session)

# %% [session](https://github.com/datajoint/element-session): experimental session information
session.Session.describe()

# %% [markdown]
# ## Summary and next step
#
# - This notebook introduced the overall structures of the schemas and tables in the workflow and relevant tools to explore the schema structure and table definitions.
#
# - The [next notebook](./03-Process.ipynb) will introduce the detailed steps to run through `workflow-deeplabcut`.
