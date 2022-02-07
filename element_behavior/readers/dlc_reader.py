import re
import numpy as np
import pandas as pd
from datetime import datetime
import pathlib
import pickle
import ruamel.yaml as yaml


class DLCLoader:

    def __init__(self, dlc_dir=None, pkl_path=None, h5_path=None, yml_path=None, filename_prefix=''):
        if dlc_dir is None:
            assert (pkl_path is not None and h5_path is not None and yml_path is not None,
                    'If "dlc_dir" is not provided, then "pkl_path", "h5_path", and "yml_path" must be provided')
        else:
            self.dlc_dir = pathlib.Path(dlc_dir)
            assert self.dlc_dir.exists()

        # meta file: pkl - info about this particular DLC run (input video, configuration, etc.)
        if pkl_path is None:
            pkl_paths = list(self.dlc_dir.glob(f'{filename_prefix}*.pickle'))
            assert len(pkl_paths) != 1, f'Unable to find one unique .pickle file in: {dlc_dir} - Found: {len(pkl_paths)}'
            self.pkl_path = pkl_paths[0]
        else:
            self.pkl_path = pathlib.Path(pkl_path)
            assert self.pkl_path.exists()

        # data file: h5 - body part outputs from the DLC post estimation step
        if h5_path is None:
            h5_paths = list(self.dlc_dir.glob(f'{filename_prefix}*.h5'))
            assert len(h5_paths) != 1, f'Unable to find one unique .h5 file in: {dlc_dir} - Found: {len(h5_paths)}'
            self.h5_path = h5_paths[0]
        else:
            self.h5_path = pathlib.Path(h5_path)
            assert self.h5_path.exists()

        assert self.pkl_path.stem == self.h5_path.stem

        # config file: yaml - configuration for invoking the DLC post estimation step
        if yml_path is None:
            yml_paths = list(self.dlc_dir.glob(f'{filename_prefix}*.yaml'))
            assert len(yml_paths) != 1, f'Unable to find one unique .yaml file in: {dlc_dir} - Found: {len(yml_paths)}'
            self.yml_path = yml_paths[0]
        else:
            self.yml_path = pathlib.Path(yml_path)
            assert self.yml_path.exists()

        self._pkl = None
        self._rawdata = None
        self._yml = None
        self._data = None

        self.model = {'Scorer': self.pkl['data']['Scorer'],
                      'Task': self.yml['Task'],
                      'date': self.yml['date'],
                      'iteration': self.pkl['data']['iteration (active-learning)'],
                      'shuffle': int(re.search('shuffle(\d+)', self.pkl['data']['Scorer']).groups()[0]),
                      'snapshotindex': self.yml['snapshotindex'],
                      'trainingsetindex': np.where((np.array(self.yml['TrainingFraction']) * 100).astype(int)
                                                   == int(self.pkl['data']['training set fraction'] * 100))[0][0],
                      'training_iteration': int(self.pkl['data']['Scorer'].split('_')[-1])}

        self.fps = self.pkl['data']['fps']

        self.creation_time = self.h5_path.stat().st_mtime

    @property
    def pkl(self):
        if self._pkl is None:
            with open(self.pkl_path, 'rb') as f:
                self._pkl = pickle.load(f)
        return self._pkl

    @property
    def yml(self):
        if self._yml is None:
            with open(self.yml_path, 'rb') as f:
                self._yml = yaml.safe_load(f)
        return self._yml

    @property
    def rawdata(self):
        if self._rawdata is None:
            self._rawdata = pd.read_hdf(self.h5_path)
        return self._rawdata

    @property
    def data(self):
        if self._data is None:
            self._data = self.reformat_rawdata()
        return self._data

    def reformat_rawdata(self):
        assert (len(self.rawdata) == self.pkl['data']['nframes'],
                f'Total frames from .h5 file ({len(self.rawdata)}) differs from .pickle ({self.pkl["data"]["nframes"]})')

        top_level = self.rawdata.columns.levels[0][0]
        dlc_df = self.rawdata.get(top_level)
        body_parts = dlc_df.columns.levels[0]

        dlc_data = {}
        for body_part in body_parts:
            dlc_data[body_part] = {c: dlc_df.get(body_part).get(c).values for c in dlc_df.get(body_part).columns}

        return dlc_data
