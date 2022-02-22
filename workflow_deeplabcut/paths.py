import datajoint as dj


def get_dlc_root_data_dir():
    dlc_root_dirs = dj.config.get('custom', {}).get('dlc_root_data_dir', None)
    return dlc_root_dirs if dlc_root_dirs else None


def get_session_directory(session_key: dict) -> str:
    from .pipeline import session
    session_dir = (session.SessionDirectory & session_key).fetch1('session_dir')
    return session_dir


def get_dlc_processed_data_dir(session_key: dict) -> str:
    """ Returns session_dir relative to custom 'dlc_output_dir' root """
    from pathlib import Path
    dlc_output_dir = dj.config.get('custom', {}).get('dlc_output_dir', None)
    if dlc_output_dir:
        return Path(dlc_output_dir, get_session_directory(session_key))
    else:
        return None
