# Element DeepLabCut

## Pose Estimation

This Element features a schema for pose estimation via ***DeepLabCut***, which is a
software tool for markerless pose estimation. DeepLabCut and others use image
recognition machine learning models to generate animal position estimates. Unlike
traditional motion capture techniques, this is achievable with consumer grade video
equipment. The Element itself is composed of two sets of tables, or schema: `train`,
which manages model training, and `model`, which mangages models and launches pose
estimation. `model` can be used without the `train` schema. For more information on 
Pose Estimation software and the development of the Element, see the 
[background page](https://elements.datajoint.org/description/deeplabcut/). 

## Table Architecture

Each of the DataJoint Elements are a set of tables for common neuroinformatics
modalities to organize, preprocess, and analyze data. Each node in the following diagram
is either a table in the Element itself or a table that would be connected to the
Element.

![element-deeplabcut diagram](https://raw.githubusercontent.com/datajoint/element-deeplabcut/main/images/diagram_dlc.svg)

- Upstream: 

    - Element DeepLabCut connects to a a ***Session*** table, which is modeled in our 
    [workflow pipeline](https://github.com/datajoint/workflow-deeplabcut/blob/main/workflow_deeplabcut/pipeline.py). 
    
    - Although not requried, most choose to connect ***Session*** to a ***Subject** 
    table for managing research subjects.

- `train` schema: Tables related to model training. Optional.
    
    + ***VideoSet***: The set of files corresponding to a training dataset.
    
    + ***TrainingParamSet***: A collection of model training parameters, represented by an index.
    
    + ***TrainingTask***: A set of tasks specifying model training methods.
    
    + ***ModelTraining***: A record of training iterations launched by ***TrainingTask***.

- `model` schema: Tables related to DeepLabCut models and pose estimation.
    
    + ***VideoRecording***: Video(s) from one recording session, for pose estimation.
    
    + ***BodyPart***: Unique body parts (a.k.a. joints) and descriptions thereof.
    
    + ***Model***: A central table for storing unique models.
    
    + ***ModelEvaluation***: Evaluation results for each model.
    
    + ***PoseEstimationTask***: A series of pose estimation tasks to be completed. 
        Pairings of video recordings with models to be use for pose estimation.
    
    + ***PoseEstimation***: Results of pose estimation using a given model. 

## Citation

+ If your work uses DataJoint and DataJoint Elements, please cite the respective Research Resource Identifiers (RRIDs) and manuscripts.

+ DataJoint for Python or MATLAB
    + Yatsenko D, Reimer J, Ecker AS, Walker EY, Sinz F, Berens P, Hoenselaar A, Cotton RJ, Siapas AS, Tolias AS. DataJoint: managing big scientific data using MATLAB or Python. bioRxiv. 2015 Jan 1:031658. doi: https://doi.org/10.1101/031658

    + DataJoint ([RRID:SCR_014543](https://scicrunch.org/resolver/SCR_014543)) - DataJoint for `<Select Python or MATLAB>` (version `<Enter version number>`)

+ DataJoint Elements
    + Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D, Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

    + DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) - Element DeepLabCut (version `<Enter version number>`)

## Limitations

This Element currently supports single-animal, single-camera 2D models, and does not yet
support multi-animal or multi-camera models. This Element does not offer any features
for labeling training data. Users should to use native DeepLabCut tools for
intitializing a project and labeling training data.

+ See the [Element DeepLabCut documentation](https://elements.datajoint.org/description/deeplabcut/) for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit https://elements.datajoint.org.  This work is supported by the National Institutes of Health.