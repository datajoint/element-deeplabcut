# DataJoint Element - DeepLabCut

DataJoint Element for markerless pose estimation with [DeepLabCut](https://www.deeplabcut.org/).  DataJoint Elements collectively standardize and automate data collection and analysis for neuroscience experiments.  Each Element is a modular pipeline of data storage and processing steps with corresponding database tables that can be combined with other Elements to assemble a fully functional behavioral pipeline.

Installation and usage instructions can be found at the [DataJoint Element DeepLabCut docs](datajoint.com/docs/elements/element-deeplabcut).

![element-deeplabcut diagram](https://raw.githubusercontent.com/datajoint/element-deeplabcut/main/images/diagram_dlc.svg)
The pipeline presented here is not a complete pipeline by itself, but rather a modular
design of tables and dependencies specific to the behavior tracking workflow. This
modular pipeline element can be flexibly attached downstream to any particular design
of experiment session, thus assembling a fully functional behavior pipeline (see the
example [workflow-deeplabcut](https://github.com/datajoint/workflow-deeplabcut)).



