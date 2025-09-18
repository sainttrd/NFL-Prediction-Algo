"use client";
import { useState } from "react";

export default function HomePage() {
  const [home, setHome] = useState("");
  const [away, setAway] = useState("");
  const [kickoff, setKickoff] = useState("");
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

      <label>
        <span>Kickoff (ISO)</span>
        <input
          value={kickoff}
          onChange={(e) => setKickoff(e.target.value)}
        />
      </label>

      <button onClick={handlePredict}>Predict</button>

      {result && (
        <pre style={{ marginTop: 20 }}>{JSON.stringify(result, null, 2)}</pre>
      )}
    </main>
  );
}
