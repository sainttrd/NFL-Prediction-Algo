import pandas as pd
import numpy as np
from .data_sources import load_pbp, load_schedule
from .features import rolling_team_features, elo_like, assemble_features
from .model_io import save_model
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

TARGET_COL = 'home_win'

FEATURES = [
    'off_epa_home_3','def_epa_home_3','off_epa_away_3','def_epa_away_3',
    'elo_delta','home','roof_dome','surface_turf','temp','wind','precip'
]

def build_training_frame(seasons):
    frames = []
    for s in seasons:
        pbp = load_pbp(s)
        sched = load_schedule(s)
        sched = sched.rename(columns={'home_team':'home_team','away_team':'away_team'})
        sched['gameday_iso'] = pd.to_datetime(sched['gameday']).astype(str)
        roll = rolling_team_features(pbp)
        elo = elo_like(sched)
        sched = sched.merge(elo, on=['gameday','home_team','away_team'], how='left')
        rows = []
        for _, r in sched.iterrows():
            feats = assemble_features(r, roll)
            y = 1 if (isinstance(r.get('result'), (int,float)) and r['result']>0) else (0 if isinstance(r.get('result'), (int,float)) else np.nan)
            rows.append({**feats, TARGET_COL: y, 'season': s})
        df = pd.DataFrame(rows)
        frames.append(df)
    all_df = pd.concat(frames, ignore_index=True)
    all_df = all_df.dropna(subset=[TARGET_COL])
    return all_df

def train_and_save():
    seasons = list(range(2015, 2025))
    df = build_training_frame(seasons)
    X = df[FEATURES]
    y = df[TARGET_COL].astype(int)

    pipe = Pipeline([
        ('imp', SimpleImputer(strategy='median')),
        ('sc', StandardScaler()),
        ('clf', LogisticRegression(max_iter=200))
    ])
    pipe.fit(X, y)

    save_model(pipe, version='v1-logreg-epa-elo-weather')
    print('Saved model with', len(y), 'examples')

if __name__ == '__main__':
    train_and_save()
