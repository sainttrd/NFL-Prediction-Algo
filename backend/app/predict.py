import numpy as np
import pandas as pd
from .model_io import load_model
from .features import assemble_features

FEATURES = [
    'off_epa_home_3','def_epa_home_3','off_epa_away_3','def_epa_away_3',
    'elo_delta','home','roof_dome','surface_turf','temp','wind','precip'
]

_model, _version = load_model()

def predict_matchup(row, rolling_feats):
    feats = assemble_features(row, rolling_feats)
    X = np.array([[feats[k] for k in FEATURES]])
    prob_home = float(_model.predict_proba(X)[0,1])
    return prob_home, feats

def model_version():
    return _version
