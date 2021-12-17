import datajoint as dj
import pathlib

def get_beh_root_dir():
    beh_root_dirs = dj.config.get('custom', {}).get('beh_root_dir', None)
    return beh_root_dirs if beh_root_dirs else None

def get_session_directory(session_key: dict) -> str:
    from .pipeline import session
    session_dir = (session.SessionDirectory & session_key).fetch1('session_dir')
    return session_dir