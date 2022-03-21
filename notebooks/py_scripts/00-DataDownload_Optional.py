# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: venv-dlc
#     language: python
#     name: venv-dlc
# ---

# %% [markdown] tags=[]
# # DataJoint U24 - Workflow DeepLabCut

# %% [markdown]
# ## Download example data

# %% [markdown]
# We've structured this tool around the example data available from the DLC. If you've already cloned the [main DLC repository](https://github.com/DeepLabCut/DeepLabCut), you already have this folder under `examples/openfield-Pranav-2018-10-30`.

# %% [markdown]
# [This link](https://downgit.github.io/#/home?url=https://github.com/DeepLabCut/DeepLabCut/tree/master/examples/openfield-Pranav-2018-10-30) via [DownGit](https://downgit.github.io/) will start the single-directory download 
# automatically as a zip. Unpack this zip and place it in a directory we'll refer to as your root.

# %% [markdown]
# ## Directory structure

# %% [markdown]
# After downloading, the directory will be organized as follows within your chosen root
# directory.
#
# ```
#  /your-root/openfield-Pranav-2018-10-30/
#    - config.yaml
#    - labeled-data
#       - m4s1
#           - CollectedData_Pranav.csv
#           - CollectedData_Pranav.h5
#           - img0000.png
#           - img0001.png
#           - img0002.png
#           - img{...}.png
#           - img0114.png
#           - img0115.png
#    - videos
#        - m3v1mp4.mp4
# ```

# %% [markdown]
# For those unfamiliar with DLC...
# - `config.yaml` contains all the key parameters of the project, including
#    - file locations (currently empty)
#    - body parts
#    - cropping information
# - `labeled-data` includes the frames coordinates for each body part in the training video
# - `videos` includes the full training video for this example
#
# As part of the DeepLabCut demo setup process, you would run the following additional
# command, as outlined in their 
# [demo notebook](https://github.com/DeepLabCut/DeepLabCut/blob/master/examples/JUPYTER/Demo_labeledexample_Openfield.ipynb).
# These establishes the project path within the demo config file as well as the `training-datasets` directory, which DLC will use for model training

# %%
your_root='/fill/in/your/root/with\ escaped\ spaces'
from deeplabcut.create_project.demo_data import load_demo_data as dlc_load_demo
dlc_load_demo(your_root+'/openfield-Pranav-2018-10-30/config.yaml')

# %% [markdown]
# For your own data, we recommend using the DLC gui to intitialize your project and label the data. 

# %% [markdown]
# ## Make new video

# %% [markdown]
# Later, we'll use the first few seconds of the training video as a 'separate session' to model
# the pose estimation feature of this pipeline. `ffmpeg` is a dependency of DeepLabCut
# that can splice the training video for a demonstration purposes. The command below saves
# the first 2 seconds of the training video as a copy.
#
# - `-n` do not overwrite
# - `-hide_banner -loglevel error` less verbose output
# - `-ss 0 -t 2` start at second 0, add 2 seconds
# - `-i {vid_path}` input this video
# - `-{v/a}codec copy` copy the video and audio codecs of the input
# - `{vid_path}-copy.mp4` output file

# %% tags=[]
vid_path = your_root + '/openfield-Pranav-2018-10-30/videos/m3v1mp4'
cmd = (f'ffmpeg -n -hide_banner -loglevel error -ss 0 -t 2 -i {vid_path}.mp4 '
       + f'-vcodec copy -acodec copy {vid_path}-copy.mp4')
import os; os.system(cmd)

# %% [markdown]
# In the next notebook, [01-Configure](./01-Configure.ipynb), we'll set up the DataJoint config file with a pointer to your root data directory.
