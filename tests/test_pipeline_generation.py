__all__ = ["pipeline"]


def test_upstream_pipeline(pipeline):
    session = pipeline["session"]
    subject = pipeline["subject"]

    # test connection Subject->Session
    assert subject.Subject.full_table_name == session.Session.parents()[0]


def test_train_pipeline(pipeline):
    train = pipeline["train"]

    # test connection train.TrainingTask
    traintask_parent_links = train.TrainingTask.parents()
    traintask_parent_list = [
        train.VideoSet,
        train.TrainingParamSet,
    ]
    for parent in traintask_parent_list:
        assert (
            parent.full_table_name in traintask_parent_links
        ), f"train.TrainingTask.parents() did not include {parent.full_table_name}"


def test_model_pipeline(pipeline):
    model = pipeline["model"]

    # test connection model.VideoRec -> schema children
    modelvids_children_links = model.VideoRecording.children()
    modelvids_children_list = [
        model.VideoRecording.File,
        model.PoseEstimationTask,
        model.RecordingInfo,
    ]
    for child in modelvids_children_list:
        assert (
            child.full_table_name in modelvids_children_links
        ), f"model.VideoRecording.children() did not include {child.full_table_name}"

    # test connection model.Model -> schema children
    model_children_links = model.Model.children()
    model_children_list = [
        model.Model.BodyPart,
        model.ModelEvaluation,
        model.PoseEstimationTask,
    ]
    for child in model_children_list:
        assert (
            child.full_table_name in model_children_links
        ), f"model.Model.children() did not include {child.full_table_name}"
