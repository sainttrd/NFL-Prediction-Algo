import pandas as pd
import requests
from io import StringIO

NFLVERSE_BASES = {
    "pbp": "https://raw.githubusercontent.com/nflverse/nflfastR-data/master/data/play_by_play_{season}.csv.gz",
    "schedule": "https://raw.githubusercontent.com/nflverse/nflverse-data/master/schedules/regular_{season}.csv",
    "teams": "https://raw.githubusercontent.com/nflverse/nflverse-data/master/teams.csv"
}

def fetch_csv(url: str) -> pd.DataFrame:
    if url.endswith('.gz'):
        return pd.read_csv(url, compression='gzip', low_memory=False)
    else:
        return pd.read_csv(url, low_memory=False)

def load_schedule(season: int) -> pd.DataFrame:
    return fetch_csv(NFLVERSE_BASES["schedule"].format(season=season))

def load_pbp(season: int) -> pd.DataFrame:
    return fetch_csv(NFLVERSE_BASES["pbp"].format(season=season))
