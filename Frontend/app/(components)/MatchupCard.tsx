import ProbabilityBar from './ProbabilityBar'

type Game = {
  team_home: string;
  team_away: string;
  kickoff_iso: string;
  home_win_prob: number;
  away_win_prob: number;
  model_version: string;
  features_used: Record<string, number | string | boolean>;
}

export default function MatchupCard({ game }: { game: Game }) {
  return (
    <div className="rounded-2xl p-4 bg-neutral-900 shadow-lg border border-neutral-800">
      <div className="flex items-center justify-between">
        <div className="text-lg font-semibold">{game.team_away} @ {game.team_home}</div>
        <div className="text-xs text-neutral-400">{new Date(game.kickoff_iso).toLocaleString()}</div>
      </div>
      <div className="mt-3"><ProbabilityBar homeProb={game.home_win_prob} /></div>
      <details className="mt-3 text-sm text-neutral-300">
        <summary className="cursor-pointer text-neutral-400">Features</summary>
        <pre className="mt-2 text-xs whitespace-pre-wrap">{JSON.stringify(game.features_used, null, 2)}</pre>
      </details>
    </div>
  );
}
