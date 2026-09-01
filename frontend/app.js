const $=id=>document.getElementById(id);
async function api(url,options){const r=await fetch(url,options);if(!r.ok)throw Error(await r.text());return r.json()}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const grade=n=>n>=80?'good':n>=55?'warn':'bad';
async function load(){
  const [d,a,s]=await Promise.all([api('/api/devices'),api('/api/alerts'),api('/api/stats')]);
  $('devices').textContent=s.devices;$('online').textContent=s.online;
  $('alerts').textContent=s.alerts;$('health').textContent=s.average_health+'%';
  $('refresh').textContent=new Date().toLocaleTimeString();
  $('fleet').innerHTML=d.length?d.map(x=>`
    <div class="device" onclick="selectDevice(${x.id},'${esc(x.name)}')">
      <div><span class="status ${x.status==='online'?'online':''}"></span>
      <span class="name">${esc(x.name)}</span>
      <div class="meta">${esc(x.location)} · ${x.status}</div></div>
      <b class="score ${grade(x.health_score||0)}">${x.health_score??'--'}%</b>
    </div>`).join(''):'<p>No devices registered yet.</p>';
  $('alertList').innerHTML=a.length?a.map(x=>`
    <div class="alert"><b class="${x.severity}">${x.severity.toUpperCase()}</b><br>
    <strong>${esc(x.device_name)}</strong> — ${esc(x.message)}<br>
    <small>${new Date(x.timestamp).toLocaleString()}</small></div>`).join(''):'<p>No alerts recorded.</p>';
}
async function selectDevice(id,name){
  $('title').textContent=name;$('subtitle').textContent='Recent telemetry readings';
  const rows=await api(`/api/devices/${id}/telemetry?limit=5`);
  $('telemetry').innerHTML=rows.length?rows.slice().reverse().map(x=>`
    <div class="reading"><span>${new Date(x.timestamp).toLocaleTimeString()}</span>
    <strong>${x.temperature.toFixed(1)} °C</strong><span>Temperature</span>
    <strong>${x.voltage.toFixed(2)} V</strong><span>Voltage</span>
    <strong>${x.current.toFixed(2)} A</strong><span>Current</span>
    <strong>${x.signal_strength} dBm</strong><span>Signal</span>
    <strong>${x.health_score}%</strong><span>Health</span></div>`).join(''):'<p>No telemetry received yet.</p>';
}
$('add').onclick=()=>$('modal').classList.remove('hidden');
$('close').onclick=()=>$('modal').classList.add('hidden');
$('export').onclick=()=>location.href='/api/export';
$('form').onsubmit=async e=>{e.preventDefault();await api('/api/devices',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:$('name').value,location:$('location').value||'Unassigned'})});e.target.reset();$('modal').classList.add('hidden');load()};
load();setInterval(load,5000);