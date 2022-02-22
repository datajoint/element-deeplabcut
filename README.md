# Workflow for continuous behavior tracking

This directory provides an example workflow to save the continuous behavior data, using the following datajoint elements
+ [element-lab](https://github.com/datajoint/element-lab)
+ [element-animal](https://github.com/datajoint/element-animal)
+ [element-session](https://github.com/datajoint/element-session)
+ [element-deeplabcut](https://github.com/datajoint/element-deeplabcut)

This repository provides demonstrations for:
Setting up a workflow using different elements (see [pipeline.py](workflow_deeplabcut/pipeline.py))

## Workflow architecture
The lab and animal management workflow presented here uses components from two DataJoint elements (element-lab, element-animal and element-session) assembled together to a functional workflow.

### element-lab

![element-lab](
https://github.com/datajoint/element-lab/raw/main/images/element_lab_diagram.svg)

### element-animal

![element-animal](
https://github.com/datajoint/element-animal/blob/main/images/subject_diagram.svg)

### element-session
`session` is designed to handle metadata related to data collection, including collection datetime, file paths, and notes. Most workflows will include element-session as a starting point for further data entry.
![session](https://github.com/datajoint/element-session/blob/main/images/session_diagram.svg)

### Assembled with element-deeplabcut
![element-deeplabcut](
https://github.com/datajoint/element-deeplabcut/blob/main/images/diagram_dlc.svg)

### This workflow
This workflow serves as an example of the upstream part of a typical data workflow, for examples using these elements with other data modalities refer to:

+ [workflow-array-ephys](https://github.com/datajoint/workflow-array-ephys)
+ [workflow-calcium-imaging](https://github.com/datajoint/workflow-calcium-imaging)

## Installation instructions

+ The installation instructions can be found at [datajoint-elements/install.md](
     https://github.com/datajoint/datajoint-elements/blob/main/install.md).

## Interacting with the DataJoint workflow

+ Please refer to the following workflow-specific
[Jupyter notebooks](/notebooks) for an in-depth explanation of how to run the
workflow ([01-Explore_Workflow.ipynb](notebooks/01-Explore_Workflow.ipynb)).
