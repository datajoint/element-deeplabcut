import datatajoint as dj

schema = dj.Schema()


@schema
class VideoRecording(dj.Manual):
    definition = """      
    -> Session
    -> Device
    recording_start_time: datetime
    """

    class File(dj.Part):
        definition = """
        -> master
        file_path: varchar(255)  # filepath of the video, relative to root data directory
        """


@schema
class ConfigParamSet(dj.Lookup):
    definition = """
    # Parameters to specify a DLC model training instance
    paramset_idx    : smallint
    ---
    shuffle         : int         # shuffle number to use (usually 1)
    train_fraction  : float       # training fraction
    filter_type=""  : varchar(16) # filter type, blank if none (e.g., median, arima)
    track_method="" : varchar(16) # tracking method, blank if none (e.g,. box, ellipse)
    scorer_legacy=0 : bool        # legacy naming for DLC < v2.1.0
    param_set_hash  : uuid        # hash identifying this parameterset
    unique index (param_set_hash)
    """


@schema
class TrainingTask(dj.Manual):
    definition = """                  # Info required to specify 1 model
    -> VideoRecording                 # labeled video for training
    -> ConfigParamSet
    training_id: int           
    """


@schema
class ModelTraining(dj.Computed):
    definition = """
    -> TrainingTask
    ---
    snapshot_index_exact  : int unsigned   # exact snapshot index (i.e., never -1)
    config_template : longblog       # stored full config file
    """

    """TODO: ingestion of config w/ understanding that
        config gets updated on snapshots"""

    def make(self, key):
        # command line to trigger a model training event
        # from jupyter notebook?
        raise NotImplementedError


@schema
class BodyPart(dj.Lookup):
    definition = """
    body_part: varchar(32)
    ---
    body_part_description='': varchar(1000)
    """


@schema
class Model(dj.Manual):
    definition = """
    model_name           : varchar(32) # user-friendly model name
    ---
    task                 : varchar(32)  # task in the config yaml
    date                 : varchar(16)  # date in the config yaml
    iteration            : int  # iteration/version of this model
    snapshotindex        : int  # which snapshot index used for prediction (if -1 then use the latest snapshot)
    shuffle              : int  # which shuffle of the training dataset used for training the network (typically 1)
    trainingsetindex     : int  # which training set fraction used to generate the model (typically 0)
    unique index (task, date, iteration, shuffle, trainingsetindex, snapshotindex)
    model                : varchar(64) # scorer/network name for a particular shuffle, training fraction etc. - DLC's GetScorerName()
    config_template      : longblob  # dictionary of the config yaml needed to run the deeplabcut.analyze_videos()
    model_description='' : varchar(1000)
    project_path         : varchar(255)  # relative path of the DLC project, appended to the root_dir to be used for the project_path var in the config.yaml
    -> [nullable] ModelTraining
    """

    class BodyPart(dj.Part):
        definition = """
        -> master
        -> BodyPart
        """


@schema
class PoseEstimation(dj.Computed):
    definition = """
    -> VideoRecording
    -> Model
    """

    class BodyPartPosition(dj.Part):
        definition = """ # uses DeepLabCut h5 output for body part position
        -> master
        -> Model.BodyPart
        ---
        frame_index : longblob     # frame index in model
        x_pos       : longblob
        y_pos       : longblob
        z_pos=null  : longblob
        likelihood  : longblob
        """

    def make(self, key):
        raise NotImplementedError
