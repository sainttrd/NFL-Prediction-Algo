from fastapi import FastAPI
from .schemas import CustomMatchupRequest, MatchupPrediction
from .data_sources import load_schedule, load_pbp
from .features import rolling_team_features
from .predict import predict_matchup, model_version
from datetime import datetime

app = FastAPI(title="NFL Predictor API", version=model_version())

# Cache rolling feats by latest season on startup
_pbp = load_pbp(2024)
_roll = rolling_team_features(_pbp)

@app.get("/health")
def health():
    return {"ok": True, "model_version": model_version()}

@app.get("/predict/week/{season}/{week}")
def predict_week(season: int, week: int):
    sched = load_schedule(season)
    games = sched.query('week==@week and season_type=="REG"')
    out = []
    for _, g in games.iterrows():
        row = {
            'home_team': g['home_team'],
            'away_team': g['away_team'],
            'season': season,
            'week': week,
            'gameday_iso': str(g['gameday']),
            'result': g.get('result', None),
            'neutral_site': bool(g.get('neutral_site', False)),
            'elo_home': None,
            'elo_away': None
        }
        p_home, feats = predict_matchup(row, _roll)
        out.append({
            'team_home': row['home_team'],
            'team_away': row['away_team'],
            'kickoff_iso': row['gameday_iso'],
            'home_win_prob': p_home,
            'away_win_prob': 1-p_home,
            'model_version': model_version(),
            'features_used': feats
        })
    return out

@app.post("/predict/custom", response_model=MatchupPrediction)
def predict_custom(req: CustomMatchupRequest):
    row = {
        'home_team': req.team_home,
        'away_team': req.team_away,
        'season': datetime.fromisoformat(req.kickoff_iso).year,
        'week': 1,
        'gameday_iso': req.kickoff_iso,
        'result': None,
        'neutral_site': req.neutral,
        'elo_home': None,
        'elo_away': None
    }
    p_home, feats = predict_matchup(row, _roll)
    return MatchupPrediction(
        team_home=req.team_home,
        team_away=req.team_away,
        kickoff_iso=req.kickoff_iso,
        home_win_prob=p_home,
        away_win_prob=1-p_home,
        model_version=model_version(),
        features_used=feats
    )
