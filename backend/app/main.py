from fastapi import FastAPI
from .schemas import CustomMatchupRequest, MatchupPrediction
from .predict import model_version

app = FastAPI(title="NFL Predictor API", version=model_version())

# Don’t preload data at import time
_pbp = None
_roll = None

@app.on_event("startup")
async def startup_event():
    global _pbp, _roll
    try:
        from .data_sources import load_pbp
        from .features import rolling_team_features
        _pbp = load_pbp(2023)  # smaller / last finished season
        _roll = rolling_team_features(_pbp)
    except Exception as e:
        print("Startup warm-up failed:", e)

@app.get("/health")
def health():
    return {"ok": True, "model_version": model_version()}            'team_home': row['home_team'],
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
