# Element DeepLabCut

## Pose Estimation
<!-- Info from previous element README -->

This Element features a schema for pose estimation via 
[***DeepLabCut***](https://www.deeplabcut.org/), which is a
software tool for markerless pose estimation. DeepLabCut uses image
recognition machine learning models to generate animal position estimates. Unlike
traditional motion capture techniques, this is achievable with consumer grade video
equipment. 

The Element itself is composed of two sets of tables, or schema: `train`,
which manages model training, and `model`, which mangages models and launches pose
estimation. `model` can be used without the `train` schema. For more information on 
Pose Estimation software and the development of the Element, see the 
[concepts page](./concepts.md). 

<!-- TODO: simplified diagram -->
![element-deeplabcut diagram](https://raw.githubusercontent.com/datajoint/element-deeplabcut/main/images/diagram_dlc.svg)

## Citation

If your work DataJoint Elements, please cite the following manuscript and Research
Resource Identifier (RRID).

+ Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D,
  Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for
  Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

+ DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) -
  Element DeepLabCut (version `<Enter version number>`)