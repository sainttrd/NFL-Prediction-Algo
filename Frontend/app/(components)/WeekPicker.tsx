export default function WeekPicker({ week, setWeek }: { week: number, setWeek: (w:number)=>void }){
  return (
    <div className="flex items-center gap-2">
      <button className="px-3 py-1 rounded-xl bg-neutral-800" onClick={()=>setWeek(Math.max(1, week-1))}>-</button>
      <div>Week {week}</div>
      <button className="px-3 py-1 rounded-xl bg-neutral-800" onClick={()=>setWeek(Math.min(18, week+1))}>+</button>
    </div>
  )
}
