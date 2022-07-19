"""Tests ingestion into schema tables: Lab, Subject, Session
    1. Assert length of populating data conftest
    2. Assert exact matches of inserted data fore key tables
"""


def test_ingest(pipeline, ingest_csvs):
    """Check successful ingestion of csv data"""
    import datetime

    subject = pipeline["subject"]
    session = pipeline["session"]
    train = pipeline["train"]
    model = pipeline["model"]

    table_lengths = [
        (subject.Subject(), 1, "subject6"),
        (session.Session(), 2, datetime.datetime(2021, 6, 1, 13, 33, 33)),
        (train.TrainingParamSet(), 1, "from_top_tracking"),
        (train.VideoSet(), 3, 0),
        (
            train.VideoSet.File(),
            10,
            "from_top_tracking/labeled-data/train1/CollectedData_DJ.h5",
        ),
        (model.Model(), 1, "FromTop-latest"),
        (model.VideoRecording(), 1, "Camera1"),
        (model.VideoRecording.File(), 1, "from_top_tracking/videos/test-2s.mp4"),
    ]

    for t in table_lengths:
        assert len(t[0]) == t[1], f"Check length of {t[0].full_table_name}"
        assert t[2] in t[0].fetch()[0], f"Check contents of {t[0].full_table_name}"
