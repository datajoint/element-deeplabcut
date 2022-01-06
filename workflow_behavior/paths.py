import datajoint as dj


def get_beh_root_data_dir():
    beh_root_dirs = dj.config.get('custom', {}).get('beh_root_data_dir', None)
    return beh_root_dirs if beh_root_dirs else None


def get_beh_root_output_dir():
    beh_output_dir = dj.config.get('custom', {}).get('beh_output_dir', None)
    return beh_output_dir if beh_output_dir else None


def get_session_directory(session_key: dict) -> str:
    from .pipeline import session
    session_dir = (session.SessionDirectory & session_key
                   ).fetch1('session_dir')
    return session_dir
