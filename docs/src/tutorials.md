# Tutorials

The best tutorial of Element DeepLabcut is the corresponding [workflow](https://github.com/datajoint/workflow-deeplabcut). This repository can help you quickly set this Element and others on your machine.

Our [YouTube tutorial](https://www.youtube.com/watch?v=8FDjTuQ52gQ) gives an overview of the workflow directory as well as core concepts related to DeepLabCut itself.

[![YouTube tutorial](https://img.youtube.com/vi/8FDjTuQ52gQ/0.jpg)](https://www.youtube.com/watch?v=8FDjTuQ52gQ)

Each of the [notebooks](https://github.com/datajoint/workflow-deeplabcut/tree/main/notebooks) in Workflow DeepLabcut steps through ways to interact with the Element itself.

- [00-DataDownload](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/00-DataDownload_Optional.ipynb) highlights how to use DataJoint tools to download a sample model for trying out the Element.
- [01-Configure](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/01-Configure.ipynb) helps configure your local DataJoint installation to point to the correct database.
- [02-WorkflowStructure](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/02-WorkflowStructure_Optional.ipynb) demonstrates the table architecture of the Element and key DataJoint basics for interacting with these tables.
- [03-Process](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/03-Process.ipynb) steps through adding data to these tables and launching key DeepLabCut features, like model training.
- [04-Automate](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/04-Automate_Optional.ipynb) highlights the same steps as above, but utilizing all built-in automation tools.
- [05-Visualization](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/05-Visualization_Optional.ipynb) demonstrates how to fetch data from the Element to generate figures and label data.
- [06-Drop](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/06-Drop_Optional.ipynb) provides the steps for dropping all the tables to start fresh.
- [09-AlternateDataset](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/09-AlternateDataset.ipynb) does all of the above, but with a [dataset from DeepLabCut](https://github.com/DeepLabCut/DeepLabCut/tree/master/examples/openfield-Pranav-2018-10-30).