export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || ""; // set in Vercel env

export async function getWeek(season: number, week: number) {
  const r = await fetch(`${BACKEND_URL}/predict/week/${season}/${week}`, { cache: 'no-store' });
  if (!r.ok) throw new Error('Backend error');
  return r.json();
}

export async function postCustom(body: any) {
  const r = await fetch(`${BACKEND_URL}/predict/custom`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error('Backend error');
  return r.json();
}
