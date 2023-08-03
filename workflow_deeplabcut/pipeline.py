import datajoint as dj
from element_lab import lab
from element_animal import subject
from element_session import session_with_datetime as session
from element_deeplabcut import train, model

from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Project

from .paths import get_dlc_root_data_dir, get_dlc_processed_data_dir

__all__ = [
    "get_dlc_root_data_dir",
    "get_dlc_processed_data_dir",
    "Subject",
    "Source",
    "Lab",
    "Protocol",
    "User",
    "Project",
    "Session",
]

if "custom" not in dj.config:
    dj.config["custom"] = {}

db_prefix = dj.config["custom"].get("database.prefix", "")

# Activate "lab", "subject", "session" schema -------------

lab.activate(db_prefix + "lab")

subject.activate(db_prefix + "subject", linking_module=__name__)

Experimenter = lab.User
Session = session.Session
session.activate(db_prefix + "session", linking_module=__name__)

# Activate equipment table ------------------------------------


@lab.schema
class Device(dj.Lookup):
    """Table for managing lab equipment.

    In Element DeepLabCut, this table is referenced by `model.VideoRecording`.
    The primary key is also used to generate inferred output directories when
    running pose estimation inference. Refer to the `definition` attribute
    for the table design.

    Attributes:
        device ( varchar(32) ): Device short name.
        modality ( varchar(64) ): Modality for which this device is used.
        description ( varchar(256) ): Optional. Description of device.
    """

    definition = """
    device             : varchar(32)
    ---
    modality           : varchar(64)
    description=null   : varchar(256)
    """
    contents = [
        ["Camera1", "Pose Estimation", "Panasonic HC-V380K"],
        ["Camera2", "Pose Estimation", "Panasonic HC-V770K"],
    ]


# Activate DeepLabCut schema -----------------------------------


train.activate(db_prefix + "train", linking_module=__name__)
model.activate(db_prefix + "model", linking_module=__name__)
