import warnings
import logging
from pynwb import NWBHDF5IO
from hdmf.build.warnings import DtypeConversionWarning
from pathlib import Path
from collections import abc
from .. import model

try:  # Not all users will want NWB export, so dependency not in requirements.
    from dlc2nwb.utils import convert_h5_to_nwb
except ImportError:
    raise ImportError(
        "The package `dlc2nwb` is missing. Please run `pip install dlc2nwb`."
    )

logger = logging.getLogger("datajoint")


def dlc_session_to_nwb(keys, use_element_session=True, session_kwargs=None):
    """Using keys from PoseEstimation table, save DLC's h5 output to NWB.

    Calls DLC2NWB to export NWB file using current h5 on disk. If use_element_session,
    calls NWB export function from element session, passing session_kwargs.

    Parameters
    ----------
    Keys - one or more keys from model.PoseEstimation
    use_element_session - Optional. If True, call NWB export from Element Session
    session_kwargs - Optiona. Additional keyword arguements for Element Session export
    """
    if not isinstance(keys, abc.Sequence):  # Ensure list for following loop
        keys = [keys]

    for key in keys:
        subject_id = key["subject"]
        output_dir = model.PoseEstimationTask.infer_output_dir(key)
        video_name = Path((model.VideoRecording.File & key).fetch1("file_path")).stem
        h5file = str(list(output_dir.glob(f"{video_name}*h5"))[0])
        output_path = convert_h5_to_nwb(  # Saves it's own NWB
            str(output_dir / "dj_dlc_config.yaml"), h5file, subject_id
        )

        if use_element_session:  # rewrites nwb saved above with session_to_nwb data
            # TODO: refactor after merge: https://github.com/DeepLabCut/DLC2NWB/pull/10
            from element_session.export.nwb import session_to_nwb

            with NWBHDF5IO(output_path[0], "r") as io:
                dlcnwb = io.read()  # read NWB file saved above
            session_nwb = session_to_nwb(key, **session_kwargs)  # call session export
            behavior_pm = session_nwb.create_processing_module(
                name="behavior", description="processed behavioral pose estimation"
            )
            behavior_pm.add(dlcnwb.processing)

            with warnings.catch_warnings(), NWBHDF5IO(output_path, mode="w") as io:
                warnings.filterwarnings("ignore", category=DtypeConversionWarning)
                io.write(session_nwb)

        logger.info(f"Saved NWB:\n\t{output_path}")
