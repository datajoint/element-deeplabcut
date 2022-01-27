'''Tests ingestion into schema tables: Lab, Subject, Session
    1. Assert length of populating data from __innit__
    2. Assert exact matches of inserted data fore key tables
'''

__all__ = ['dj_config', 'pipeline', 'subjects_csv', 'ingest_subjects', 'sessions_csv',
           'ingest_sessions', ]

from . import (dj_config, pipeline,
               subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions)


def test_ingest_subjects(pipeline, subjects_csv, ingest_subjects):
    """Check length of subject.Subject"""
    subject = pipeline['subject']
    assert len(subject.Subject()) == 2

    subjects, _ = subjects_csv
    for this_subject in subjects[1:]:
        subject_values = this_subject.split(",")
        assert (subject.Subject & {'subject': subject_values[0]}
                ).fetch1('subject_description') == subject_values[3]


def test_ingest_sessions(pipeline, sessions_csv, ingest_sessions):
    """Check length/contents of Session.SessionDirectory"""
    session = pipeline['session']
    assert len(session.Session()) == 2

    sessions, _ = sessions_csv
    for sess in sessions[1:]:
        sess = sess.split(",")
        assert (session.SessionDirectory
                & {'subject': sess[0]}
                ).fetch1('session_dir') == sess[2]
