const API_BASE = 'http://127.0.0.1:5001/api'

async function getJson(url){
  try{
    const res = await fetch(url);
    if(!res.ok) throw new Error(`HTTP ${res.status}`)
    return await res.json()
  }catch(e){
    return {__error: String(e)}
  }
}

async function refresh(){
  document.getElementById('status').textContent = 'Status: fetching...'
  const root = await getJson('http://127.0.0.1:5001/')
  document.getElementById('status').textContent = `Status: ${root.status || JSON.stringify(root)}`

  const agents = await getJson(`${API_BASE}/agents`)
  document.getElementById('agents').textContent = JSON.stringify(agents, null, 2)

  const q = await getJson(`${API_BASE}/project-queue`)
  document.getElementById('queue').textContent = JSON.stringify(q, null, 2)
}

document.getElementById('btnRefresh').addEventListener('click', refresh)
window.addEventListener('load', refresh)
