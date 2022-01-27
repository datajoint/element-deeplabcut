# DataJoint Element - DeepLabCut

This repository features a draft of a DataJoint pipeline design for behavior tracking and pose estimation via ***DeepLabCut***. This project is a part of our U24 itiative.

The pipeline presented here is not a complete pipeline by itself, but rather a modular design of tables and dependencies specific to the behavior tracking workflow. This modular pipeline element can be flexibly attached downstream to any particular design of experiment session, thus assembling a fully functional
behavior pipeline (see the example [workflow-behavior](https://github.com/datajoint/workflow-behavior)).

## The Pipeline Architecture

![element-behavior diagram](images/MISSING_DIAGRAM.svg)

As the diagram depicts, the DeepLabCut element starts immediately downstream from ***Session***.

### DeepLabCut recordings

+ ***DLCModel*** -
+ ***OtherTable*** -

## Installation

+ Install `element-behavior`
    ```
    pip install element-behavior
    ```

+ Upgrade `element-behavior` previously installed with `pip`
    ```
    pip install --upgrade element-behavior
    ```

+ Install `element-data-loader`

    + `element-data-loader` is a dependency of `element-behavior`, however it is not contained within `requirements.txt`.

    ```
    pip install "element-data-loader @ git+https://github.com/datajoint/element-data-loader"
    ```

## Usage

### Element activation

To activate the `element-behavior`, one needs to provide:

1. Schema names
    + schema name for the dlc module
    + optional: schema name for the treadmill module

2. Upstream tables
    + Session table

3. Utility functions
    + get_beh_root_data_dir()
    + get_session_directory()
    + optional: get_beh_root_output_dir()

For more detail, check the docstring of the `element-behavior`:
```python
help(dlc.activate)
```
### Example usage

See [this project](https://github.com/datajoint/workflow-behavior) for an example usage of this Behavior Element.
