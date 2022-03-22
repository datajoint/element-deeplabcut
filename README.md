# DataJoint Workflow - DeepLabCut

Workflow for pose estimation using 
[DeepLabCut](http://www.mackenziemathislab.org/deeplabcut). This workflow assumes you have 
already declared your project and labeled training data. Then, DataJoint can be used to
launch model training and run pose estimation inferences.

A complete DeeLabCut workflow can be built using DataJoint Elements.
+ [element-lab](https://github.com/datajoint/element-lab)
+ [element-animal](https://github.com/datajoint/element-animal)
+ [element-session](https://github.com/datajoint/element-session)
+ [element-deeplabcut](https://github.com/datajoint/element-deeplabcut)

This repository provides demonstrations for:
1. Setting up a workflow using different elements (see [pipeline.py](workflow_deeplabcut/pipeline.py))
2. Ingestion of model training parameters, and launching training.
3. Ingestion of model information, and launching evaluation.
4. Using an ingested model to run pose estimation.

## Workflow architecture

The deeplabcut workflow presented here uses components from 4 DataJoint elements
(`element-lab`, `element-animal`, `element-session`, and `element-deeplabcut`)
assembled together to a functional workflow.

### element-lab

![element-lab](
https://github.com/datajoint/element-lab/raw/main/images/element_lab_diagram.svg)

### element-animal

![element-animal](
https://github.com/datajoint/element-animal/blob/main/images/subject_diagram.svg)

### element-session

![session](https://github.com/datajoint/element-session/blob/main/images/session_diagram.svg)

### Assembled with element-deeplabcut

The DeepLabCut Element is split into `train` and `model` schemas. To manage both model
training and pose estimation within DataJoint, one would activate both schemas, as
shown below.

![assembled-both](https://github.com/datajoint/element-deeplabcut/blob/main/images/diagram_dlc.svg)

If training is managed outside DataJoint, one could only activate the `model` schema to
still manage various models and execute pose estimation.

![assembled-model](https://github.com/datajoint/element-deeplabcut/blob/main/images/diagram_dlc_model.svg)

## Installation instructions

+ The installation instructions can be found at the 
[datajoint-elements repository](https://github.com/datajoint/datajoint-elements/blob/main/gh-pages/docs/install.md).

## Interacting with the DataJoint workflow

Please refer to the following workflow-specific
[Jupyter notebooks](/notebooks) for an in-depth explanation of how to ...
+ download example data ([00-DataDownload.ipynb](notebooks/00-DataDownload_Optional.ipynb))
+ configure DataJoint settings ([01-Configure.ipynb](notebooks/01-Configure.ipynb))
+ run the workflow ([01-WorkflowStructure.ipynb](notebooks/01-WorkflowStructure_Optional.ipynb))
+ ingest data and launch tasks ([03-Process.ipynb](notebooks/03-Process.ipynb))
+ automate tasks ([04-Automate.ipynb](notebooks/04-Automate_Optional.ipynb))
+ drop tables ([05-Drop](notebooks/05-Drop_Optional.ipynb))
