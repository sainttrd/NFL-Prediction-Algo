"use client";
import { useState } from "react";

export default function HomePage() {
  const [home, setHome] = useState("");
  const [away, setAway] = useState("");
  const [result, setResult] = useState<any>(null);

  async function handlePredict() {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/predict?home=${home}&away=${away}`
    );
    const data = await res.json();
    setResult(data);
  }

  return (
    <main style={{ padding: 20 }}>
      <h1>NFL Prediction App</h1>

      <input
        placeholder="Home Team"
        value={home}
        onChange={(e) => setHome(e.target.value)}
      />
      <input
        placeholder="Away Team"
        value={away}
        onChange={(e) => setAway(e.target.value)}
      />
      <button onClick={handlePredict}>Predict</button>

      {result && (
        <pre style={{ marginTop: 20 }}>{JSON.stringify(result, null, 2)}</pre>
      )}
    </main>
  );
  <TeamSelect label="Away Team" value={away} onChange={setAway} />
          <label className="block text-sm sm:col-span-2">
            <span className="text-neutral-400">Kickoff (ISO)</span>
            <input value={kickoff} onChange={e=>setKickoff(e.target.value)} className="mt-1 w-full bg-neutral-900 border border-neutral-800 rounded-xl p-2" />
          </label>
          <button className="sm:col-span-2 justify-self-start bg-white text-black rounded-xl px-4 py-2"
            onClick={async ()=>{ const r = await postCustom({ team_home:home, team_away:away, kickoff_iso:kickoff }); setPred(r); }}>
            Predict
          </button>
        </div>
        {pred && (
          <div className="mt-4">
            <MatchupCard game={pred} />
          </div>
        )}
      </section>
    </div>
  )
}
