import datajoint as dj
from .pipeline import session
from pathlib import Path


def get_beh_root_dir():
    beh_root_dirs = dj.config.get('custom', {}).get('root_data_dir', None)
    return beh_root_dirs if beh_root_dirs else None


def get_session_dir(session_key: dict) -> str:
    session_dir = (session.SessionDirectory & session_key
                   ).fetch1('session_dir')
    return session_dir


def get_beh_output_dir(session_key: dict) -> str:
    """ Returns session_dir relative to custom 'beh_output_dir' root """
    beh_output_dir = dj.config.get('custom', {}
                                   ).get('beh_output_dir', None)
    if beh_output_dir is not None:
        return Path(beh_output_dir, get_session_dir(session_key))
    else:
        return None
