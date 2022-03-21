import datajoint as dj
from element_lab import lab
from element_animal import subject
from element_session import session_with_datetime as session
from element_deeplabcut import train, model

from element_animal.subject import Subject
from element_session.session_with_datetime import Session
from element_lab.lab import Source, Lab, Protocol, User, Project

from .paths import get_dlc_root_data_dir, get_dlc_processed_data_dir

__all__ = ['get_dlc_root_data_dir', 'get_dlc_processed_data_dir',
           'Subject', 'Source', 'Lab', 'Protocol', 'User',
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


@session.schema
class VideoRecording(dj.Manual):
    definition = """
    -> Session
    -> Device
    recording_id: int
    ---
    recording_start_time: datetime
    """

    class File(dj.Part):
        definition = """
        -> master
        file_path: varchar(255)  # filepath of video, relative to root data directory
        """

# Activate DeepLabCut schema -----------------------------------


train.activate(db_prefix + 'train', linking_module=__name__)
model.activate(db_prefix + 'model', linking_module=__name__)
