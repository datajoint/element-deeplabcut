# Concepts

## Pose Estimation in Neurophysiology

Studying the inner workings of the brain requires understanding the relationship between
neural activity and environmental stimuli, natural behavior, or inferred cognitive
states. Pose estimation is a computer vision method to track the position, and thereby
behavior, of the subject over the course of an experiment, which can then be paired with
neuronal recordings to answer scientific questions about the brain.

Previous pose estimation methods required reflective markers placed on a subject, as
well as multiple expensive high-frame-rate infrared cameras to triangulate position
within a limited field. Recent advancements in machine learning have facilitated
dramatic advancements in capturing pose data with a video camera alone. In particular,
[DeepLabCut](http://deeplabcut.org/) (DLC) facilitates the use of pre-trained machine
learning models for 2-D and
3-D non-invasive markerless pose estimation.

DeepLabCut offers the ability to continue training an exisiting object detection model
to further specialize in videos in the training data set. In other words, researchers
can take a well-known generalizable machine learning model and apply it to their
experimental setup, making it relatively easy to produce pose estimation inferences
for subsequent experimental sessions.

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
creator- and peer-support. Other comparable tools include
[mmpose](https://github.com/open-mmlab/mmpose),
[idtracker.ai]([idtracker.ai](https://idtrackerai.readthedocs.io/en/latest/)),
[TREBA](https://github.com/neuroethology/TREBA),
[B-KinD](https://github.com/neuroethology/BKinD),
[VAME](https://github.com/LINCellularNeuroscience/VAME), and
[MARS](https://github.com/neuroethology/MARS).

## Key Partnerships

[Mackenzie Mathis](http://www.mackenziemathislab.org/) (Swiss Federal Institute of
Technology Lausanne) is both a lead developer of DLC and a key advisor on DataJoint open
source development as a member of the [Scientific Steering
Committee](datajoint.com/docs/elements/management/governance).

DataJoint is also partnered with a number of groups who use DLC as part of broader
workflows. In these collaborations, members of the DataJoint team have interviewed
the scientists to understand their needs in experimental setup, pipeline design, and
interfaces.

These teams include:

- Moser Group (Norwegian University of Science and Technology) - see [pipeline
  design](https://moser-pipelines.readthedocs.io/en/latest/imaging/dlc.html)

- Mesoscale Activity Project (Janelia Research Campus/Baylor College of Medicine/New
  York University)

- Hui-Chen Lu Lab (Indiana University)

- Tobias Rose Lab (University of Bonn)

- James Cotton Lab (Northwestern University)

## Element Features

Development of the Element began with an 
[open source repository](https://github.com/MMathisLab/DataJoint_Demo_DeepLabCut) shared
by the Mathis team. We further identified common needs across our respective
partnerships to offer the following features for single-camera 2D models:

- Manage training data and configuration parameters
- Launch model training
- Evaluate models automatically and directly compare models
- Manage model metadata
- Launch inference video analysis
- Capture pose estimation output for each session

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow and the
corresponding tables in the database.  Within the workflow, Element DeepLabCut connects
to upstream Elements including Lab, Animal, and Session.  For more detailed
documentation on each table, see the API docs for the respective schemas.

![pipeline](https://raw.githubusercontent.com/datajoint/element-deeplabcut/main/images/pipeline.svg)

### `lab` schema ([API docs](../api/workflow_deeplabcut/pipeline/#workflow_deeplabcut.pipeline.Device))

| Table | Description |
| --- | --- |
| Device | Camera metadata |

### `subject` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/subject))

- Although not required, most choose to connect the `Session` table to a `Subject` table.

| Table | Description |
| --- | --- |
| Subject | Basic information of the research subject |

### `session` schema ([API docs](https://datajoint.com/docs/elements/element-session/api/element_session/session_with_datetime))

| Table | Description |
| --- | --- |
| Session | Unique experimental session identifier |

### `train` schema ([API docs](../api/element_deeplabcut/train))

- Optional tables related to model training.

| Table | Description |
| --- | --- |
| VideoSet | Set of files corresponding to a training dataset. |
| TrainingParamSet | A collection of model training parameters, represented by an index. |
| TrainingTask | A set of tasks specifying model training methods. |
| ModelTraining | A record of training iterations launched by `TrainingTask`. |

### `model` schema ([API](../api/element_deeplabcut/model))

- Tables related to DeepLabCut models and pose estimation. The `model` schema can be
  used without the `train` schema.

| Table | Description |
| --- | --- |
| VideoRecording | Video(s) from one recording session, for pose estimation. |
| BodyPart | Unique body parts (a.k.a. joints) and descriptions thereof. |
| Model | A central table for storing unique models. |
| ModelEvaluation | Evaluation results for each model. |
| PoseEstimationTask | A series of pose estimation tasks to be completed. Pairings of video recordings with models to be use for pose estimation. |
| PoseEstimation | Results of pose estimation using a given model. |

## Data Export and Publishing

Element DeepLabCut includes an export function that saves the outputs as a Neurodata
Without Borders (NWB) file.  By running a single command, the data from an experimental
session is saved to a NWB file.

For more details on the export function, see the [Tutorials page](/tutorials).

Once NWB files are generated they can be readily shared with collaborators and published
on [DANDI Archive](https://dandiarchive.org/).  The DataJoint Elements ecosystem
includes a function to upload the NWB files to DANDI (see [Element
Interface](datajoint.com/docs/elements/element-interface/)).

```python
dlc_session_to_nwb(pose_key, use_element_session, session_kwargs)
```

## Roadmap

Further development of this Element is community driven.  Upon user requests and based
on guidance from the Scientific Steering Group we will add the following features to
this Element:

- Support for multi-animal or multi-camera models
- Tools to label training data
