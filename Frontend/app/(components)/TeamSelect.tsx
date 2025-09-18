const TEAMS = [
  'ARI','ATL','BAL','BUF','CAR','CHI','CIN','CLE','DAL','DEN','DET','GB','HOU','IND','JAX','KC','LV','LAC','LAR','MIA','MIN','NE','NO','NYG','NYJ','PHI','PIT','SEA','SF','TB','TEN','WAS'
]
export default function TeamSelect(props: { label: string, value: string, onChange: (v:string)=>void }){
  return (
    <label className="block text-sm">
      <span className="text-neutral-400">{props.label}</span>
      <select value={props.value} onChange={e=>props.onChange(e.target.value)} className="mt-1 w-full bg-neutral-900 border border-neutral-800 rounded-xl p-2">
        {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
      </select>
    </label>
  )
}
