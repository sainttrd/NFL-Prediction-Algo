import pandas as pd
import numpy as np
from datetime import datetime
import json, os, requests

with open(os.path.join(os.path.dirname(__file__), 'stadiums.json')) as f:
    STADIUMS = {s['team']: s for s in json.load(f)}

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

def rolling_team_features(pbp: pd.DataFrame) -> pd.DataFrame:
    # Compute simple rolling EPA/Success metrics per team
    df = pbp[(pbp['season_type']=="REG") & (~pbp['posteam'].isna())].copy()
    df['epa'] = df['epa'].fillna(0)
    g = df.groupby(['season','week','posteam'], as_index=False)['epa'].mean()
    g = g.sort_values(['posteam','season','week'])
    g['off_epa_3'] = g.groupby('posteam')['epa'].transform(lambda s: s.shift().rolling(3, min_periods=1).mean())
    g = g.rename(columns={'posteam':'team'})[['season','week','team','off_epa_3']]

    # Defensive EPA allowed by opponent
    d = df.copy()
    d = d.groupby(['season','week','defteam'], as_index=False)['epa'].mean()
    d = d.sort_values(['defteam','season','week'])
    d['def_epa_3'] = d.groupby('defteam')['epa'].transform(lambda s: s.shift().rolling(3, min_periods=1).mean())
    d = d.rename(columns={'defteam':'team'})[['season','week','team','def_epa_3']]

    out = g.merge(d, on=['season','week','team'], how='outer')
    return out

def elo_like(schedule: pd.DataFrame, k=20, hfa=55):
    # Minimal ELO through schedule
    teams = pd.unique(schedule[['home_team','away_team']].values.ravel('K'))
    elo = {t: 1500 for t in teams}
    rows = []
    for _, r in schedule.sort_values(['gameday']).iterrows():
        h, a = r['home_team'], r['away_team']
        ra = elo[a]
        rh = elo[h] + hfa
        ea = 1/(1+10**((rh-ra)/400))
        eh = 1-ea
        # outcome
        if r.get('result') is not None:
            # nflverse schedules have 'result' as home margin; positive means home won
            outcome_h = 1.0 if r['result']>0 else (0.5 if r['result']==0 else 0.0)
        else:
            outcome_h = 0.5
        elo[h] = elo[h] + k*(outcome_h - eh)
        elo[a] = elo[a] + k*((1-outcome_h) - ea)
        rows.append({'gameday': r['gameday'], 'home_team':h, 'away_team':a, 'elo_home':elo[h], 'elo_away':elo[a]})
    return pd.DataFrame(rows)

def fetch_weather(lat, lon, kickoff_iso):
    # Hourly weather around kickoff
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m,precipitation,wind_speed_10m',
        'start_hour': kickoff_iso,
        'end_hour': kickoff_iso
    }
    try:
        r = requests.get(OPEN_METEO, params=params, timeout=10)
        j = r.json()
        return {
            'temp': j['hourly']['temperature_2m'][0],
            'wind': j['hourly']['wind_speed_10m'][0],
            'precip': j['hourly']['precipitation'][0]
        }
    except Exception:
        return {'temp': np.nan, 'wind': np.nan, 'precip': np.nan}

def assemble_features(row, rolling_feats):
    # Join rolling EPA and ELO deltas + weather + stadium
    h, a = row['home_team'], row['away_team']
    season, week = int(row['season']), int(row['week'])

    rh = rolling_feats.query('season==@season and week==@week and team==@h').tail(1)
    ra = rolling_feats.query('season==@season and week==@week and team==@a').tail(1)

    off_h = float(rh['off_epa_3'].values[0]) if len(rh) else 0.0
    def_h = float(rh['def_epa_3'].values[0]) if len(rh) else 0.0
    off_a = float(ra['off_epa_3'].values[0]) if len(ra) else 0.0
    def_a = float(ra['def_epa_3'].values[0]) if len(ra) else 0.0

    elo_h = row.get('elo_home', 1500)
    elo_a = row.get('elo_away', 1500)

    st = STADIUMS.get(h, {})
    lat, lon, roof, surface = st.get('lat'), st.get('lon'), st.get('roof','outdoor'), st.get('surface','turf')
    wx = fetch_weather(lat, lon, row['gameday_iso']) if (lat and lon and roof!='dome') else {'temp':np.nan,'wind':np.nan,'precip':np.nan}

    return {
        'off_epa_home_3': off_h,
        'def_epa_home_3': def_h,
        'off_epa_away_3': off_a,
        'def_epa_away_3': def_a,
        'elo_delta': elo_h - elo_a,
        'home': 0 if row.get('neutral_site', False) else 1,
        'roof_dome': 1 if roof=='dome' else 0,
        'surface_turf': 1 if 'turf' in surface.lower() else 0,
        'temp': wx['temp'],
        'wind': wx['wind'],
        'precip': wx['precip']
    }
