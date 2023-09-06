# PATHS OF INPUT FILES: Extract abs and rel paths from .json file
import os

if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
assert os.path.basename(os.getcwd()) == "element-deeplabcut", "Please move to the "

import datajoint as dj
from pathlib import Path
import yaml

dj.conn()


### DLC Project
dlc_project_path_abs = Path(dj.config["custom"]["dlc_root_data_dir"]) / Path(
    dj.config["custom"]["current_project_folder"]
)  # use pathlib to join; abs path
dlc_project_folder = Path(
    dj.config["custom"]["current_project_folder"]
)  # relative path

### Config file
config_file_abs = dlc_project_path_abs / "config.yaml"  # abs path
assert (
    config_file_abs.exists()
), "Please check the that you have the Top_tracking folder"

### Labeled-data
labeled_data_path_abs = dlc_project_path_abs / "labeled-data"
labeled_files_abs = list(
    list(labeled_data_path_abs.rglob("*"))[1].rglob("*")
)  # substitute 'training_files'; absolute path
labeled_files_rel = []
for file in labeled_files_abs:
    labeled_files_rel.append(
        file.relative_to(dlc_project_path_abs)
    )  # substitute 'training_files'; relative path


from tutorial_pipeline import (
    lab,
    subject,
    session,
    train,
    model,
)  # after creating json file

# Empty the session in case of rerunning
# session.Session.delete()
# train.TrainingTask.delete()
# train.TrainingParamSet.delete()
# train.VideoSet.delete()

# Insert some data in session and train tables
# TO-DO: substitute lab.project by project schema.


# Subject and Session tables
subject.Subject.insert1(
    dict(
        subject="subject6",
        sex="F",
        subject_birth_date="2020-01-01",
        subject_description="hneih_E105",
    ),
    skip_duplicates=True,
)
session_keys = [
    dict(subject="subject6", session_datetime="2021-06-02 14:04:22"),
    dict(subject="subject6", session_datetime="2021-06-03 14:43:10"),
]

session.Session.insert(session_keys, skip_duplicates=True)
session.Session() & "session_datetime > '2021-06-01 12:00:00'" & "subject='subject6'"

# Videoset tabley
train.VideoSet.insert1({"video_set_id": 0}, skip_duplicates=True)

# training_files = #['labeled-data/train1_trimmed/CollectedData_DataJoint.h5',
#'labeled-data/train1_trimmed/CollectedData_DataJoint.csv']
#'labeled-data/train1_trimmed/img00674.png'] #TO-DO: CHECK IF ALL THE PNGS ARE NECESSARY FOR TRAINING
#'videos/train1.mp4']
# for idx, filename in enumerate(training_files):
for idx, filename in enumerate(labeled_files_rel):
    train.VideoSet.File.insert1(
        {"video_set_id": 0, "file_id": idx, "file_path": dlc_project_folder / filename},
        skip_duplicates=True,
    )  # Changed from + to /; #relative_path

# Restrict the training interations to 5 modifying the default parameters in config.yaml
paramset_idx = 0
paramset_desc = "First training test with DLC using shuffle 1 and maxiters = 5"

# default parameters
with open(config_file_abs, "rb") as y:
    config_params = yaml.safe_load(y)
config_params.keys()

# new parameters
training_params = {
    "shuffle": "1",
    "trainingsetindex": "0",
    "maxiters": "5",
    "scorer_legacy": "False",  # For DLC ≤ v2.0, include scorer_legacy = True in params
    "maxiters": "5",
    "multianimalproject": "False",
}
config_params.update(training_params)

train.TrainingParamSet.insert_new_params(
    paramset_idx=paramset_idx,
    paramset_desc=paramset_desc,
    params=config_params,
)

# TrainingTask table
key = {
    "video_set_id": 0,
    "paramset_idx": 0,
    "training_id": 1,
    "project_path": dlc_project_folder,
}
train.TrainingTask.insert1(key, skip_duplicates=True)
train.TrainingTask()
train.ModelTraining.populate(display_progress=True)
train.ModelTraining.fetch()

model.BodyPart()
new_body_parts = [
    dict(body_part="subject6", session_datetime="2021-06-02 14:04:22"),
    dict(subject="subject6", session_datetime="2021-06-03 14:43:10"),
]
session.Session.insert(session_keys, skip_duplicates=True)
model.BodyPart.extract_new_body_parts(config_file_abs)

bp_desc = []
model.BodyPart.insert_from_config(config_file_abs, bp_desc)

model.BodyPart()
model.Model.insert_new_model(
    model_name="FromTop-latest",
    dlc_config=config_file_abs,
    shuffle=1,
    trainingsetindex=0,
    model_description="FromTop - latest snapshot",
    paramset_idx=0,
    params={"snapshotindex": -1},
)
model.Model()
model.ModelEvaluation.heading
model.ModelEvaluation.populate()
model.ModelEvaluation()
model.VideoRecording()
key = {
    "subject": "subject6",
    "session_datetime": "2021-06-02 14:04:22",
    "recording_id": "1",
    "device": "Camera1",
}
model.VideoRecording.insert1(key, skip_duplicates=True)

_ = key.pop("device")  # get rid of secondary key from master table
key.update(
    {
        "file_id": 1,
        "file_path": "/Users/milagros/Documents/DeepLabCut_testing/Top_tracking-DataJoint-2023-08-03/videos/train1_trimmed.mp4",
    }
)
model.VideoRecording.File.insert1(key, skip_duplicates=True)
model.VideoRecording.File()
# model.RecordingInfo.populate()
model.RecordingInfo()
key = (model.VideoRecording & {"recording_id": "1"}).fetch1("KEY")
key.update({"model_name": "FromTop-latest", "task_mode": "trigger"})
# videotype, gputouse, save_as_csv, batchsize, cropping, TFGPUinference, dynamic, robust_nframes, allow_growth, use_shelve
analyze_videos_params = {"save_as_csv": True}

# key.update(analyze_videos_params={"save_as_csv": True})
# model.PoseEstimationTask.insert_estimation_task(key)
model.PoseEstimationTask.insert_estimation_task(
    key, model_name=key["model_name"], analyze_videos_params=analyze_videos_params
)

model.PoseEstimation.populate()
model.PoseEstimation.coordinates_dataframe(key)
