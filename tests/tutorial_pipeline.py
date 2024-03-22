import os
import datajoint as dj
from collections import abc
from element_lab import lab
from element_animal import subject
from element_session import session_with_datetime as session
from element_deeplabcut import train, model

from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Project


if "custom" not in dj.config:
    dj.config["custom"] = {}

# overwrite dj.config['custom'] values with environment variables if available

dj.config["custom"]["database.prefix"] = os.getenv(
    "DATABASE_PREFIX", dj.config["custom"].get("database.prefix", "")
)

dj.config["custom"]["dlc_root_data_dir"] = os.getenv(
    "DLC_ROOT_DATA_DIR", dj.config["custom"].get("dlc_root_data_dir", "")
)

dj.config["custom"]["dlc_processed_data_dir"] = os.getenv(
    "DLC_PROCESSED_DATA_DIR", dj.config["custom"].get("dlc_processed_data_dir", "")
)

if "custom" not in dj.config:
    dj.config["custom"] = {}

db_prefix = dj.config["custom"].get("database.prefix", "")


# Declare functions for retrieving data
def get_dlc_root_data_dir() -> list:
    """Returns a list of root directories for Element DeepLabCut"""
    dlc_root_dirs = dj.config.get("custom", {}).get("dlc_root_data_dir")
    if not dlc_root_dirs:
        return None
    elif not isinstance(dlc_root_dirs, abc.Sequence):
        return list(dlc_root_dirs)
    else:
        return dlc_root_dirs


def get_dlc_processed_data_dir() -> str:
    """Returns an output directory relative to custom 'dlc_output_dir' root"""
    from pathlib import Path

    dlc_output_dir = dj.config.get("custom", {}).get("dlc_processed_data_dir")
    if dlc_output_dir:
        return Path(dlc_output_dir)
    else:
        return None


__all__ = [
    "lab",
    "subject",
    "session",
    "train",
    "model",
    "Device"
]

# Activate schemas -------------

lab.activate(db_prefix + "lab")
subject.activate(db_prefix + "subject", linking_module=__name__)
Experimenter = lab.User
Session = session.Session
session.activate(db_prefix + "session", linking_module=__name__)


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
