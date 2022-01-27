'''Test pipeline construction
    1. Assert lab link to within-schema children
    2. Assert lab link to subject
    3. Assert subject link to session
'''

__all__ = ['pipeline']

from . import pipeline


def test_generate_pipeline(pipeline):
    session = pipeline['session']
    subject = pipeline['subject']

    # test connection Subject->Session
    subject_tbl, *_ = session.Session.parents(as_objects=True)
    assert subject_tbl.full_table_name == subject.Subject.full_table_name


''' TO DO
- Add relative table assertions for DLC schema
'''
