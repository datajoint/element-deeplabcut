# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and 
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [0.2.8] - 2023-08-07

+ Update - GitHub Actions with new reusable workflows
+ Update - Readme instructions

## [0.2.7] - 2023-08-04

+ Fix - Update the project path in the pose config file to train the model

## [0.2.6] - 2023-05-22

+ Add - DeepLabCut, NWB, and DANDI citations
+ Update - mkdocs.yaml

## [0.2.5] - 2023-05-11

+ Fix - `.ipynb` dark mode output for all notebooks.
+ Fix - Remove `GOOGLE_ANALYTICS_KEY` from `u24_element_release_call.yml`.

## [0.2.4] - 2023-04-28

+ Fix - `.ipynb` output in tutorials is not visible in dark mode.

## [0.2.3] - 2023-02-28

+ Fix - For cases of multiple subjects/sessions with same recording_id
+ Update - Use posix to handle DLC project path

## [0.2.2] - 2023-01-17

+ Fix - improve function to auto generate PoseEstimationTask
+ Update - loading DLC results handles multiple DLC output files
+ Update - Adopt lazy import strategy for imported DeepLabCut functions

## [0.2.1] - 2022-12-16

+ Update - Requirements to accommodate DLC package requirements changing
+ Fix - Typos in docstrings
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

[0.2.8]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.8
[0.2.7]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.7
[0.2.6]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.6
[0.2.5]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.5
[0.2.4]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.4
[0.2.3]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.3
[0.2.2]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.2
[0.2.1]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.1
[0.2.0]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.2.0
[0.1.1]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.1.1
[0.1.0]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.1.0
[0.0.0a]: https://github.com/datajoint/element-deeplabcut/releases/tag/0.0.0a
