from pydantic import BaseModel
from typing import List, Optional

class CustomMatchupRequest(BaseModel):
    team_home: str
    team_away: str
    kickoff_iso: str  # e.g., "2025-10-05T13:00:00"
    neutral: bool = False
    manual_injuries_home: Optional[List[str]] = None
    manual_injuries_away: Optional[List[str]] = None

class MatchupPrediction(BaseModel):
    team_home: str
    team_away: str
    kickoff_iso: str
    home_win_prob: float
    away_win_prob: float
    model_version: str
    features_used: dict
