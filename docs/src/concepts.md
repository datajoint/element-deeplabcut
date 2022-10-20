# Concepts

## Pose Estimation in Neurophysiology

Neurophysiology is concerned not only with the inner workings of the brain, but the
relationship between neural firings and environmental stimuli, natural behavior, or
inferred cognitive states. One approach is to present a stationary subject with planned
stimuli. More naturalistic paradigms permit spontaneous behavior, and add some mechanism
measure subject responses. Through pose estimation, we capture the richness of a
subject's natural behavior, which can then be paired with neuronal recordings.

Previous pose estimation methods required reflective markers placed on a subject, as
well as multiple expensive high-frame-rate infrared cameras to triangulate position
within a limited field. Recent advancements in machine learning have facilitated
dramatic advancements in capturing pose data with a video camera alone. In particular,
[DeepLabCut](http://deeplabcut.org/) (DLC) facilitates the use of pre-trained machine 
learning models for 2-D and
3-D non-invasive markerless pose estimation. 

By training a model, DLC takes a machine learning process in its current state
and refining it to specialize in the video data collected in our experiment. This 
process works best when the camera has a consistent field of view across sessions, and
when generating pose estimation inferences on consistent data sets (e.g., subjects with 
similar characteristics). DLC saves models at various checkpoints and recommends
training for approximately 200,000 iterations. When DLC generates pose estimation 
inferences, this model is applied to novel videos, generating predictions of where the
same set of training points would be in this new situation.

While some alternative tools are either species-specific (e.g.,
[DeepFly3D](https://github.com/NeLy-EPFL/DeepFly3D)) or uniquely 2D (e.g.,
[DeepPoseKit](https://github.com/jgraving/DeepPoseKit)), DLC highlights a diversity of
use-cases via a [Model Zoo](http://www.mackenziemathislab.org/dlc-modelzoo). Even
compared to tools with similar functionality (e.g.,
[SLEAP](https://github.com/murthylab/sleap) and
[dannce](https://github.com/spoonsso/dannce)), DLC has more users, as measured by either
GitHub forks or more citations (1600 vs. 900). DLC's trajectory toward an industry
standard is attributable to [continued
funding](http://www.mackenziemathislab.org/deeplabcutblog/2020/11/18/czidlc), [extensive
documentation](https://deeplabcut.github.io/DeepLabCut/docs/intro.html) and both
creator- and peer-support. Other comperable tools include
[mmpose](https://github.com/open-mmlab/mmpose),
[idtracker.ai]([idtracker.ai](https://idtrackerai.readthedocs.io/en/latest/)),
[TREBA](https://github.com/neuroethology/TREBA),
[B-KinD](https://github.com/neuroethology/BKinD),
[VAME](https://github.com/LINCellularNeuroscience/VAME), and
[MARS](https://github.com/neuroethology/MARS).

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow for Element DeepLabCut and corresponding table in the database.  Within the workflow, Element DeepLabCut connects to upstream Elements including Lab, Animal, and Session.

![element-deeplabcut diagram](https://raw.githubusercontent.com/datajoint/element-deeplabcut/main/images/diagram_dlc.svg)

### `lab` schema

| Table | Description |
| --- | --- |
| Device | Camera metadata |

### `subject` schema
- Although not required, most choose to connect the `Session` table to a `Subject` table.

| Table | Description |
| --- | --- |
| Subject | Basic information of the research subject |

### `session` schema

| Table | Description |
| --- | --- |
| Session | Unique experimental session identifier |

### `train` schema
- Tables related to model training. Optional.

| Table | Description |
| --- | --- |
| VideoSet | Set of files corresponding to a training dataset. |
| TrainingParamSet | A collection of model training parameters, represented by an index. |
| TrainingTask | A set of tasks specifying model training methods. |
| ModelTraining | A record of training iterations launched by `TrainingTask`. |

### `model` schema
- Tables related to DeepLabCut models and pose estimation. The `model` can be used without the `train` schema.

| Table | Description |
| --- | --- |
| VideoRecording | Video(s) from one recording session, for pose estimation. |
| BodyPart | Unique body parts (a.k.a. joints) and descriptions thereof. |
| Model | A central table for storing unique models. |
| ModelEvaluation | Evaluation results for each model. |
| PoseEstimationTask | A series of pose estimation tasks to be completed. Pairings of video recordings with models to be use for pose estimation. |
| PoseEstimation | Results of pose estimation using a given model. |

## Key Partnerships

[Mackenzie Mathis](http://www.mackenziemathislab.org/) (Swiss Federal Institute of Technology Lausanne) is both a lead
developer of DLC and a key advisor on DataJoint open source development as a member of
the [Scientific Steering Committee](datajoint.com/docs/elements/management/governance).

DataJoint is also partnered with a number of groups who use DLC as part of broader
workflows. In these collaborations, members of the DataJoint team have interviewed
researchers to understand their needs in experiment workflow, pipeline design, and
interfaces.

These teams include:

- Moser Group (Norwegian University of Science and Technology) - see [pipeline
  design](https://moser-pipelines.readthedocs.io/en/latest/imaging/dlc.html)

- Mesoscale Activity Project (Janelia Research Campus/Baylor College of Medicine/New
  York University)

- Hui-Chen Lu Lab (Indiana University)

- Tobias Rose Lab (University of Bonn)

- James Cotton Lab (Northwestern University)

## Element Development

Development of the Element began with an [open source
repository](https://github.com/MMathisLab/DataJoint_Demo_DeepLabCut) shared by the
Mathis team. We further identified common needs across our respective partnerships to
offer the following features for single-camera 2D models:

- Training data and parameter management
- Launching model training and automatic model evaluation
- Model metadata management
- Launching inference video analysis and capturing pose estimation output

The workflow handles training data as file sets stored within DLC's project directory.
Parameters of the configuration file are captured and preserved. Model evaluation
permits direct model comparison, and, when combined with upstream Elements, Element
DeepLabCut can be used to generate pose estimation information for each session.

## Data Export and Publishing

DeepLabCut's official [export package](https://github.com/DeepLabCut/DLC2NWB/) is best
method for turning DeepLabCut pose estimation data into standard Neurodata Without
Borders (NWB) files. This makes it easy to share files with collaborators and publish
results on [DANDI Archive](https://dandiarchive.org/). [NWB](https://www.nwb.org/), as
an organization, is dedicated to standardizing data formats and maximizing
interoperability across tools for neurophysiology. For more information on uploading
NWB files to DANDI within the DataJoint Elements ecosystem, visit our documentation
for the DANDI upload feature of 
[Element Interface](datajoint.com/docs/elements/element-interface/).

Pose data, however, is not yet specified in NWB Core and is instead an 
[extension of NWB](https://training.incf.org/lesson/how-build-and-share-extensions-nwb),
via [`ndx-pose`](https://github.com/rly/ndx-pose). Future versions of the NWB standard
might adopt this exension in it's current form or make modifications. 

## Roadmap

Further development of this Element is community driven.  Upon user requests and based on guidance from the Scientific Steering Group we will add the following features to this Element:

- Support for multi-animal or multi-camera models
- Tools to label training data
