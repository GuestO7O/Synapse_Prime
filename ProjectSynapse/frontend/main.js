// 1) Optional override from config.js
if (typeof window !== 'undefined' && window.SYNAPSE_API_BASE) {
  // @ts-ignore
  var API_BASE = window.SYNAPSE_API_BASE
} else {
  // 2) Default; auto-detect will override if needed
  var API_BASE = 'http://127.0.0.1:8002/api/v1'
}

let apiReady = false
let apiReadyPromise = null

async function pingRoot(base){
  try{
    const res = await fetch(base.replace(/\/?api\/v1\/?$/, '/'), { method: 'GET' })
    return res.ok
  }catch{
    return false
  }
}

async function detectApiBase(){
  // Prefer standard dev port first
  const candidates = [
    typeof window !== 'undefined' && window.SYNAPSE_API_BASE ? window.SYNAPSE_API_BASE : null,
    'http://127.0.0.1:8002/api/v1',
    'http://127.0.0.1:8003/api/v1',
    'http://127.0.0.1:8000/api/v1',
  ].filter(Boolean)
  for(const c of candidates){
    if(await pingRoot(c)){
      return c
    }
  }
  return API_BASE
}

async function getJson(url){
  try{
    const res = await fetch(url);
    if(!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)
    return await res.json()
  }catch(e){
    console.error('Fetch error:', e)
    return {__error: String(e)}
  }
}

async function postJson(url, data){
  try{
    const res = await fetch(url, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if(!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)
    return await res.json()
  }catch(e){
    console.error('Post error:', e)
    return {__error: String(e)}
  }
}

async function refresh(){
  // Wait until detection completes (first load)
  if (apiReadyPromise) {
    try { await apiReadyPromise } catch (_) { /* ignore */ }
  }
  console.log('🔄 Refresh functie aangeroepen');

  const statusEl = document.getElementById('status');
  if (!statusEl) {
    console.error('❌ Status element niet gevonden!');
    return;
  }

  statusEl.textContent = 'Status: fetching...';
  console.log('📡 Testing API connection...');

  try {
    const rootBase = API_BASE.replace(/\/?api\/v1\/?$/, '/');
    const root = await getJson(rootBase);
    console.log('✅ Root API response:', root);
    statusEl.textContent = `Status: ${root.status || 'OK'} - ${root.message || ''}`;
  } catch (e) {
    console.error('❌ Root API error:', e);
    statusEl.textContent = `Status: Error - ${e.message}`;
  }

  // Test andere endpoints
  const agentsEl = document.getElementById('agents');
  if (agentsEl) {
    const agents = await getJson(`${API_BASE}/agents`);
    agentsEl.textContent = agents.__error ? `Error: ${agents.__error}` : JSON.stringify(agents, null, 2);
  }

  const queueEl = document.getElementById('queue');
  if (queueEl) {
    const q = await getJson(`${API_BASE}/project-queue`);
    queueEl.textContent = q.__error ? `Error: ${q.__error}` : JSON.stringify(q, null, 2);
  }

  console.log('✅ Refresh compleet');
}

async function runCrewMission(){
  const description = document.getElementById('crewDescription').value
  const agentsCount = parseInt(document.getElementById('agentsCount').value) || 2

  if(!description.trim()){
    alert('Please enter a mission description')
    return
  }

  const resultEl = document.getElementById('crewResult')
  resultEl.textContent = 'Running crew mission...'

  const result = await postJson(`${API_BASE}/crew-mission`, {
    description: description,
    agents_count: agentsCount
  })

  resultEl.textContent = result.__error ? `Error: ${result.__error}` : JSON.stringify(result, null, 2)
}

async function submitFeedback(){
  const agentId = document.getElementById('feedbackAgentId').value
  const score = parseFloat(document.getElementById('feedbackScore').value)
  const traitUpdates = document.getElementById('traitUpdates').value

  if(!agentId.trim()){
    alert('Please enter agent ID')
    return
  }

  let traitUpdatesObj = null
  if(traitUpdates.trim()){
    try{
      traitUpdatesObj = JSON.parse(traitUpdates)
    }catch(e){
      alert('Invalid JSON for trait updates')
      return
    }
  }

  const resultEl = document.getElementById('feedbackResult')
  resultEl.textContent = 'Submitting feedback...'

  const result = await postJson(`${API_BASE}/evolution/feedback`, {
    agent_id: agentId,
    score: score,
    trait_updates: traitUpdatesObj
  })

  resultEl.textContent = result.__error ? `Error: ${result.__error}` : JSON.stringify(result, null, 2)
  refresh() // Refresh to show updated data
}

async function registerAgent(){
  const agentId = document.getElementById('registerAgentId').value

  if(!agentId.trim()){
    alert('Please enter agent ID')
    return
  }

  const resultEl = document.getElementById('registerResult')
  resultEl.textContent = 'Registering agent...'

  const result = await postJson(`${API_BASE}/evolution/register/${agentId}`)
  resultEl.textContent = result.__error ? `Error: ${result.__error}` : JSON.stringify(result, null, 2)
  refresh()
}

document.getElementById('btnRefresh').addEventListener('click', refresh)
document.getElementById('btnRunCrew').addEventListener('click', runCrewMission)
document.getElementById('btnSubmitFeedback').addEventListener('click', submitFeedback)
document.getElementById('btnRegisterAgent').addEventListener('click', registerAgent)

// Zorg ervoor dat refresh wordt aangeroepen wanneer de pagina laadt
window.addEventListener('load', async () => {
  console.log('📄 Pagina volledig geladen');
  try{
    apiReadyPromise = detectApiBase()
      .then((detected) => {
        API_BASE = detected
        console.log('🌐 API_BASE:', API_BASE)
        apiReady = true
        try {
          window.dispatchEvent(new CustomEvent('synapse-api-ready', { detail: { apiBase: API_BASE } }))
        } catch {}
        return detected
      })
      .catch((e) => {
        console.warn('Could not detect API base, using default:', API_BASE)
        apiReady = true
        return API_BASE
      })
    await apiReadyPromise
  }catch(e){
    // already warned above
  }
  setTimeout(refresh, 500);
});

// Als backup: probeer refresh direct aan te roepen
setTimeout(() => {
  console.log('⏰ Backup refresh call');
  refresh();
}, 2000);
