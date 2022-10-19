# Element DeepLabCut

## Pose Estimation
<!-- Info from previous element README -->

DataJoint Element for markerless pose estimation with
[DeepLabCut](https://www.deeplabcut.org/).  DataJoint Elements collectively standardize
and automate data collection and analysis for neuroscience experiments.  Each Element is
a modular pipeline for data storage and processing with corresponding database
tables that can be combined with other Elements to assemble a fully functional pipeline.

Element DeepLabCut runs DeepLabCut which uses image
recognition machine learning models to generate animal position estimates from consumer grade video equipment.  The Element is composed of two schemas for storing data and running analysis:
- `train` - Manages model training
- `model` - Manages models and launches pose
estimation

Visit the [Concepts page](./concepts.md) for more information on 
pose estimation and Element DeepLabCut.  To get started with building your data pipeline visit the [Tutorials page](./tutorials.md).

<!-- TODO: simplified diagram -->
![element-deeplabcut diagram](https://raw.githubusercontent.com/datajoint/element-deeplabcut/main/images/diagram_dlc.svg)

## Citation

If your work uses DataJoint Elements, please cite the following manuscript and Research
Resource Identifier (RRID).

+ Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D,
  Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for
  Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

+ DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) -
  Element DeepLabCut (version `<Enter version number>`)