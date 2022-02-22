import datajoint as dj
from element_animal import subject
from element_lab import lab
from element_session import session
from element_deeplabcut import dlc

from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Project
from element_session.session import Session

from .paths import get_dlc_root_data_dir, get_session_directory
from .paths import get_dlc_processed_data_dir

__all__ = ['get_dlc_root_data_dir', 'get_session_directory',
           'get_dlc_processed_data_dir', 'Subject', 'Source', 'Lab', 'Protocol', 'User',
           'Project', 'Session']

if 'custom' not in dj.config:
    dj.config['custom'] = {}

db_prefix = dj.config['custom'].get('database.prefix', '')

# Activate "lab", "subject", "session" schema -------------

lab.activate(db_prefix + 'lab')

subject.activate(db_prefix + 'subject', linking_module=__name__)

Experimenter = lab.User
session.activate(db_prefix + 'session', linking_module=__name__)

# Activate equipment table ------------------------------------


@lab.schema
class Device(dj.Lookup):
    definition = """
    camera_id   : int
    """
    contents = zip([1, 2])

# Activate "behavior" schema -----------------------------------


dlc.activate(db_prefix + 'dlc', linking_module=__name__)
