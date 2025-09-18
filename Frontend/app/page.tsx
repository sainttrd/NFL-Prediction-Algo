'use client'
import { useEffect, useState } from 'react'
import { getWeek, postCustom } from './api/backend'
import MatchupCard from './(components)/MatchupCard'
import TeamSelect from './(components)/TeamSelect'
import WeekPicker from './(components)/WeekPicker'

export default function Page(){
  const now = new Date()
  const [season] = useState(now.getFullYear())
  const [week, setWeek] = useState(1)
  const [games, setGames] = useState<any[]>([])
  const [home, setHome] = useState('NE')
  const [away, setAway] = useState('NYJ')
  const [kickoff, setKickoff] = useState(new Date().toISOString())
  const [pred, setPred] = useState<any | null>(null)

  useEffect(()=>{
    getWeek(season, week).then(setGames).catch(()=>setGames([]))
  }, [season, week])

  return (
    <div className="space-y-8">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">NFL Predictor</h1>
        <WeekPicker week={week} setWeek={setWeek} />
      </header>

      <section className="grid gap-4 sm:grid-cols-2">
        {games.map((g, i)=> <MatchupCard key={i} game={g} />)}
      </section>

      <section className="rounded-2xl p-4 bg-neutral-900 border border-neutral-800">
        <h2 className="text-xl font-semibold">Custom Matchup</h2>
        <div className="mt-3 grid sm:grid-cols-2 gap-4">
          <TeamSelect label="Home Team" value={home} onChange={setHome} />
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
