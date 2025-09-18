export default function ProbabilityBar({ homeProb }: { homeProb: number }) {
  const hp = Math.round(homeProb * 100);
  return (
    <div className="w-full bg-neutral-800 rounded-xl overflow-hidden">
      <div className="h-3 bg-white/80" style={{ width: `${hp}%` }} />
      <div className="flex justify-between text-xs mt-1 text-neutral-400">
        <span>Home {hp}%</span>
        <span>Away {100-hp}%</span>
      </div>
    </div>
  );
}
