const titles = ['SOC Analyst','Junior SOC Analyst','L1 SOC Analyst','Cybersecurity Analyst','SIEM Analyst','Blue Team Analyst','Information Security Analyst','IT Security Analyst'];
async function jobs(request, env) {
  const url = new URL(request.url);
  const location = url.searchParams.get('location') || 'UAE';
  if (!env.SERPAPI_KEY) return Response.json({jobs: []});
  const query = encodeURIComponent(`(${titles.slice(0,4).join(' OR ')}) cybersecurity ${location} UAE`);
  const api = `https://serpapi.com/search.json?engine=google_jobs&q=${query}&location=${encodeURIComponent(location+' UAE')}&hl=en&api_key=${env.SERPAPI_KEY}`;
  const r = await fetch(api);
  if (!r.ok) return Response.json({jobs: []}, {status: 502});
  const data = await r.json();
  const out = (data.jobs_results || []).map((j,i) => ({id:`serp-${i}`,title:j.title||'Cybersecurity role',company:j.company_name||'Company',location:j.location||location,source:'Google Jobs / SerpAPI',url:(j.apply_options?.[0]?.link)||j.share_link||'#',match:70,matched:['cybersecurity'],missing:['Review full requirements'],status:'Saved'}));
  return Response.json({jobs:out});
}
export default { async fetch(request, env) { const u=new URL(request.url); if (u.pathname==='/api/jobs') return jobs(request,env); if (env.ASSETS) return env.ASSETS.fetch(request); return new Response('GulfSignal Worker'); } };
