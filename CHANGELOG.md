# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and 
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [0.2.1] - Unreleased

+ Update - Docstrings for mkdocs deployment
+ Update - Doc website styling including logos, navigation, social icons
+ Add - Flow diagram in svg and drawio formats

## [0.2.0] - 2022-10-10

+ Update - Remove direct dependency (`element-interface`) for PyPI release.
+ Update - Docstring PEP257 compliance #24 
+ Update - Explicit handling of KeyboardInterrupt #26
+ Update - Streamline insert_new_params #27
+ Update - Relocate module imports to the top of the files
+ Update - Missing f for formatted string in read_yaml
+ Change - Rename datajoint-saved config to `dj_dlc_config.yaml`
+ Add - Call reusable CICD
+ Add - NWB export
+ Add - mkdocs deployment with workflow API docs

## [0.1.1] - 2022-06-10

+ Fix - Replace lazy imports
+ Fix - Project path in the model.Model

## [0.1.0] - 2022-05-10

+ Add - Adopted black formatting into code base
+ Add - Table for RecordingInfo
+ Add - File ID for tracking updatable secondary key filepaths
+ Add - `make` functions for Computed/Imported tables

## [0.0.0a] - 2021-11-15

+ Add - Drafts from a collection of precursor pipelines, including
  [DataJoint_Demo_DeepLabCut](https://github.com/MMathisLab/DataJoint_Demo_DeepLabCut)
  graciously provided by the Mathis Lab.
+ Add - Support for 2d single-animal models

[0.2.1]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.1
[0.2.0]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.0
[0.1.1]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.1.1
[0.1.0]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.1.0
[0.0.0a]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.0.0a
