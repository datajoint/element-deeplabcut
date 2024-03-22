import datetime


def test_generate_pipeline(pipeline):
    subject = pipeline["subject"]
    session = pipeline["session"]
    train = pipeline["train"]
    model = pipeline["model"]
    Device = pipeline["Device"]

    # Test connection from Subject to Session
    assert subject.Subject.full_table_name in session.Session.parents()

    # Test connection from Session and Equipment to Scan
    assert session.Session.full_table_name in model.VideoRecording.parents()
    assert Device.full_table_name in model.VideoRecording.parents()

    assert "snapshotindex" in model.Model.heading.secondary_attributes
    assert "trainingsetindex" in model.Model.heading.secondary_attributes
    assert "x_pos" in model.PoseEstimation.BodyPartPosition.heading.secondary_attributes
    assert "y_pos" in model.PoseEstimation.BodyPartPosition.heading.secondary_attributes
    assert (
        "likelihood"
        in model.PoseEstimation.BodyPartPosition.heading.secondary_attributes
    )

    assert len(train.schema.list_tables()) == 5


def test_recording_info(pipeline, recording_info):
    model = pipeline["model"]
    expected_rec_info = {
        "subject": "subject6",
        "session_datetime": datetime.datetime(2021, 6, 2, 14, 4, 22),
        "recording_id": 1,
        "px_height": 500,
        "px_width": 500,
        "nframes": 60000,
        "fps": 60,
        "recording_datetime": None,
        "recording_duration": 1000.0,
    }

    rec_info = model.RecordingInfo.fetch1()

    assert rec_info == expected_rec_info


def test_pose_estimation(pipeline, pose_estimation):
    model = pipeline["model"]

    body_parts = model.PoseEstimation.BodyPartPosition.fetch("body_part")

    assert set(body_parts) == {"head", "tailbase"}

    head_x = (model.PoseEstimation.BodyPartPosition & {"body_part": "head"}).fetch1(
        "x_pos"
    )
    tail_y = (model.PoseEstimation.BodyPartPosition & {"body_part": "tailbase"}).fetch1(
        "y_pos"
    )

    assert len(head_x) == len(tail_y)
    assert (round(head_x.std())) == 129
    assert (round(tail_y.std())) == 133
