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

+ See the [Element DeepLabCut documentation](https://elements.datajoint.org/description/deeplabcut/) for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit https://elements.datajoint.org.  This work is supported by the National Institutes of Health.

## Workflow architecture

The deeplabcut workflow presented here uses components from four DataJoint Elements
([element-lab](https://github.com/datajoint/element-lab), 
[element-animal](https://github.com/datajoint/element-animal), 
[element-session](https://github.com/datajoint/element-session), 
[element-deeplabcut](https://github.com/datajoint/element-deeplabcut))
assembled together to a functional workflow.

The DeepLabCut Element is split into `train` and `model` schemas. To manage both model
training and pose estimation within DataJoint, one would activate both schemas, as
shown below.

![assembled-both](https://github.com/datajoint/element-deeplabcut/blob/main/images/diagram_dlc.svg)

If training is managed outside DataJoint, one could only activate the `model` schema to
still manage various models and execute pose estimation.

![assembled-model](https://github.com/datajoint/element-deeplabcut/blob/main/images/diagram_dlc_model.svg)

## Installation instructions

The installation instructions can be found at the 
[DataJoint Elements documentation](https://elements.datajoint.org/usage/install/).

## Interacting with the DataJoint workflow

Please refer to the following workflow-specific
[Jupyter notebooks](/notebooks) for an in-depth explanation of how to ...
+ Download example data ([00-DataDownload.ipynb](notebooks/00-DataDownload_Optional.ipynb))
+ Configure DataJoint settings ([01-Configure.ipynb](notebooks/01-Configure.ipynb))
+ Visualize the workflow ([01-WorkflowStructure.ipynb](notebooks/01-WorkflowStructure_Optional.ipynb))
+ Ingest data and launch tasks ([03-Process.ipynb](notebooks/03-Process.ipynb))
+ Automate tasks ([04-Automate.ipynb](notebooks/04-Automate_Optional.ipynb))
+ Drop tables ([05-Drop](notebooks/05-Drop_Optional.ipynb))

## Citation

+ If your work uses DataJoint and DataJoint Elements, please cite the respective Research Resource Identifiers (RRIDs) and manuscripts.

+ DataJoint for Python or MATLAB
    + Yatsenko D, Reimer J, Ecker AS, Walker EY, Sinz F, Berens P, Hoenselaar A, Cotton RJ, Siapas AS, Tolias AS. DataJoint: managing big scientific data using MATLAB or Python. bioRxiv. 2015 Jan 1:031658. doi: https://doi.org/10.1101/031658

    + DataJoint ([RRID:SCR_014543](https://scicrunch.org/resolver/SCR_014543)) - DataJoint for < Python or MATLAB > (version < enter version number >)

+ DataJoint Elements
    + Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D, Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

    + DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) - Element DeepLabCut (version < enter version number >)