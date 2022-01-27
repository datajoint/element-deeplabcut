import datajoint as dj
from element_animal import subject
from element_lab import lab
from element_session import session
from element_behavior import dlc

from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Project
from element_session.session import Session

from .paths import get_beh_root_data_dir, get_session_dir, get_beh_output_dir

__all__ = ['get_beh_root_data_dir', 'get_session_dir', 'get_beh_output_dir',
           'Subject', 'Source', 'Lab', 'Protocol', 'User', 'Project', 'Session']

if 'custom' not in dj.config:
    dj.config['custom'] = {}

db_prefix = dj.config['custom'].get('database.prefix', '')

# Activate "lab", "subject", "session" schema -------------

lab.activate(db_prefix + 'lab')

subject.activate(db_prefix + 'subject', linking_module=__name__)

Experimenter = lab.User
session.activate(db_prefix + 'session', linking_module=__name__)

# Activate "behavior" schema -----------------------------------

dlc.activate(db_prefix + 'dlc', linking_module=__name__)
