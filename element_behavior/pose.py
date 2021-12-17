import datajoint as dj
import inspect
import importlib

schema = dj.schema()

def activate(schema_name, *, create_schema=True, create_tables=True, linking_module=None):
  """
  activate(schema_name, *, create_schema=True, create_tables=True, linking_module=None)
    :param schema_name: schema name on the database server to activate the `behavior` element
    :param create_schema: when True (default), create schema in the database if it does not yet exist.
    :param create_tables: when True (default), create tables in the database if they do not yet exist.
    :param linking_module: a module name or a module containing the required
     dependencies to activate the `session` element:
      Upstream tables:
        + Session: parent table to ProbeInsertion, typically identifying a recording session.
      Functions:
        + get_root_data_dir() -> list
          Retrieve the root data directory/directories containing behavioral recordings
          (e.g., video files) for all subject/sessions.
          :return: a string for full path to the root data directory
        + get_beh_sess_dir(session_key: dict) -> str
          Retrieve the session directory containing the recording(s) for a given Session
          :param session_key: a dictionary of one Session `key`
          :return: a string for full path to the session directory
  """
  if isinstance(linking_module, str):
    linking_module = importlib.import_module(linking_module)
  assert inspect.ismodule(linking_module), "The argument 'dependency' must be a module's name or a module"

  schema.activate(schema_name, create_schema=create_schema,
          create_tables=create_tables, add_objects=linking_module.__dict__)

# -------------- Functions required by the elements-ephys  ---------------

# CB: Ephys pulls from linking module, MAP defines internally - default to ephys style?

def get_root_data_dir() -> list:
  """
  All data paths, directories in DataJoint Elements are recommended to be stored as
  relative paths, with respect to some user-configured "root" directory,
   which varies from machine to machine (e.g. different mounted drive locations)

  get_root_data_dir() -> list
    This user-provided function retrieves the list of possible root data directories
     containing the behavioral data for all subjects/sessions (e.g., bpod files)
    :return: a string for full path to the behavioral root data directory,
     or list of strings for possible root data directories
  """
  try: return _linking_module.get_root_data_dir()
  except:
    root_data_dirs = dj.config.get('custom', {}).get('root_data_dir', None)
    return root_data_dirs if root_data_dirs else None

def get_session_directory(session_key: dict) -> str:
    from .pipeline import session
    session_dir = (session.SessionDirectory & session_key).fetch1('session_dir')
    return session_dir


def get_beh_sess_dir(session_key: dict) -> str:
  """
  get_beh_sess_dir(session_key: dict) -> str
    Retrieve the session directory containing the recordings for a given Session
    :param session_key: a dictionary of one Session `key`
    :return: a string for full path to the session directory
  """
  return _linking_module.get_beh_sess_dir(session_key)

# ----------------------------- Table declarations ----------------------

@schema
class RecordingType(dj.Lookup):
  definition = """
  recording_type: varchar(16)
  ---
  tracked_dimensions: tinyint # tracking in 1,2,3 dimensions
  number_of_markers: int
  recording_type_desc: varchar(256)
  """

  class MarkerInfo(dj.Part):
    definition = """
    marker_id = varchar(16)
    ---
    marker_location = varchar(32)
    marker_description = varchar(32)
    """

@schema
class BehTrackRecording(dj.Imported)
  definition = """
  -> session.SessionDirectory
  recording_id: varchar(16)
  ---
  recording_notes: varchar(256)
  """

  class BehFile(dj.Part):
    definition = """
    -> master
    filetype: varchar(16)
    """

  def make(self, key):
    root_data_dir = pathlib.Path(get_root_data_dir(key))
    beh_sess_dir = pathlib.Path(get_beh_sess_dir(key))
    beh_dir_full = find_full_path(root_data_dir,beh_sess_dir)

    for beh_pattern, beh_file_type in zip(['*mat','*XXX'],
                                          ['bpod','Kepecs Standard'])
      beh_filepaths = [fp for fp in beh_dir_full.rglob(beh_pattern)]
      if beh_filepaths:
        filetype = beh_file_type
        break
      else:
        raise FileNotFoundError(
          f'Neither bpod mat file nor csv file found in {beh_sess_dir}')

    if filetype == 'bpod':
      for filepath in beh_filepaths:
        bpod_data = bpod.BPod(filepath)
        '''
        key['property'] = bpod_data.property
        '''
    elif filetype == 'Kepecs Standard':
      for filepath in beh_filepaths:
        pass
        # Waiting on more info from Kepecs Lab
    # elif filetype == "other standard??" what others?
    else:
    raise NotImplementedError(f'Behavioral file of type {filetype}'
                              ' is not yet implemented')

@schema
class DLCModel(dj.Imported):
  definition = """
  dlc_model_id: varchar(16)
  """
