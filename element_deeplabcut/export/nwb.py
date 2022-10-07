"""
Portions of code adapted from DeepLabCut/DLC2NWB
MIT License Copyright (c) 2022 Alexander Mathis
DataJoint export methods for DeepLabCut 2.x
"""
import logging
import warnings
from pathlib import Path
from collections import abc
from pynwb import NWBHDF5IO
from hdmf.build.warnings import DtypeConversionWarning
from .. import model

try:  # Not all users will want NWB export, so dependency not in requirements.
    from dlc2nwb.utils import convert_h5_to_nwb, write_subject_to_nwb
except ImportError:
    raise ImportError(
        "The package `dlc2nwb` is missing. Please run `pip install dlc2nwb`."
    )

logger = logging.getLogger("datajoint")


def dlc_session_to_nwb(keys, use_element_session=True, session_kwargs=None):
    """Using keys from PoseEstimation table, save DLC's h5 output to NWB.

    Calls DLC2NWB to export NWB file using current h5 on disk. If use_element_session,
    calls NWB export function from Elements for lab, animal and session, passing
    session_kwargs. Saves output based on naming convention in DLC2NWB. If output path
    already exists, returns output path without making changes to the file.
    NOTE: does not support multianimal exports

    Parameters
    ----------
    keys: One or more keys from model.PoseEstimation
    use_element_session: Optional. If True, call NWB export from Element Session
    session_kwargs: Optional. Additional keyword arguments for Element Session export

    Returns output path of saved file
    """
    if not isinstance(keys, abc.Sequence):  # Ensure list for following loop
        keys = [keys]

    for key in keys:
        write_file = True
        subject_id = key["subject"]
        output_dir = model.PoseEstimationTask.infer_output_dir(key)
        config_file = str(output_dir / "dj_dlc_config.yaml")
        video_name = Path((model.VideoRecording.File & key).fetch1("file_path")).stem
        h5file = next(output_dir.glob(f"{video_name}*h5"))
        output_path = h5file.replace(".h5", f"_{subject_id}.nwb")  # DLC2NWB convention

        if Path(output_path).exists():
            logger.warning(f"Skipping {subject_id}. NWB already exists.")
            write_file = False

        # Use standard DLC2NWB export
        if write_file and not use_element_session:
            output_path = convert_h5_to_nwb(config_file, h5file, subject_id)

        # Pass Element Session export items in export
        if write_file and use_element_session:
            from element_session.export.nwb import session_to_nwb

            session_nwb = session_to_nwb(key, **session_kwargs)  # call session export
            dlc_nwb = write_subject_to_nwb(session_nwb, h5file, subject_id, config_file)
            # warnings filter from DLC2NWB
            with warnings.catch_warnings(), NWBHDF5IO(output_path, mode="w") as io:
                warnings.filterwarnings("ignore", category=DtypeConversionWarning)
                io.write(dlc_nwb)

    return output_path
