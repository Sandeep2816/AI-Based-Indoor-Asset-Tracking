const socket=io();
const assets=new Map();
let updates=0;
let alerts=0;

const $=id=>document.getElementById(id);
function setConnection(online){
  $("statusDot").className="dot "+(online?"online":"offline");
  $("statusText").textContent=online?"Live":"Offline";
}
function mapPoint(x,y){
  return {left:Math.max(1,Math.min(99,x/10*100)),top:Math.max(1,Math.min(99,100-y/8*100))};
}
function renderMap(){
  const map=$("floorMap");
  document.querySelectorAll(".asset-marker").forEach(el=>el.remove());
  for(const asset of assets.values()){
    const marker=document.createElement("div");
    marker.className="asset-marker";
    marker.dataset.label=asset.tag_id;
    const p=mapPoint(asset.position.x,asset.position.y);
    marker.style.left=p.left+"%";
    marker.style.top=p.top+"%";
    map.appendChild(marker);
  }
}
function lastRssi(asset){
  const values=Object.values(asset.anchors||{});
  return values.length?Math.max(...values):"—";
}
function renderAssets(){
  $("assetCount").textContent=assets.size;
  const anchorSet=new Set();
  const list=$("assetList");
  list.innerHTML="";
  if(!assets.size){
    list.innerHTML='<div class="empty">No assets detected yet.</div>';
    $("anchorCount").textContent="0";
    return;
  }
  for(const asset of assets.values()){
    Object.keys(asset.anchors||{}).forEach(a=>anchorSet.add(a));
    const restricted=(asset.geofences||[]).some(z=>z.zone==='restricted_zone'&&z.inside);
    const card=document.createElement("div");
    card.className="asset-card";
    card.innerHTML='<div class="asset-row"><span class="asset-id">' + asset.tag_id + '</span><span class="status-pill ' + (restricted?"danger-pill":"") + '">' + (restricted?"RESTRICTED":"TRACKING") + '</span></div>' +
'<div class="details"><span>Position <b>' + asset.position.x.toFixed(2) + ', ' + asset.position.y.toFixed(2) + ' m</b></span><span>Anchors <b>' + Object.keys(asset.anchors||{}).length + '</b></span><span>Last RSSI <b>' + lastRssi(asset) + ' dBm</b></span><span>Zone <b>' + (restricted?"Restricted":"Normal") + '</b></span></div>';
    list.appendChild(card);
  }
  $("anchorCount").textContent=anchorSet.size;
}
function renderAlerts(){
  const list=$("alertList");
  list.innerHTML="";
  let count=0;
  for(const asset of assets.values()){
    for(const zone of asset.geofences||[]){
      const card=document.createElement("div");
      card.className="alert-card "+(zone.inside?"":"ok");
      card.innerHTML='<div class="alert-title">' + (zone.inside?'⚠ ':'✓ ') + asset.tag_id + ' · ' + zone.zone + '</div><div class="alert-meta">' + (zone.inside?'Asset is inside this zone':'Asset is outside this zone') + '</div>';
      list.appendChild(card);
      if(zone.inside)count++;
    }
  }
  alerts=count;
  $("alertCount").textContent=alerts;
  if(!list.children.length)list.innerHTML='<div class="empty">No alerts.</div>';
}
function renderAll(){
  renderMap();renderAssets();renderAlerts();
  $("updateCount").textContent=updates;
  $("lastUpdate").textContent=new Date().toLocaleTimeString();
}
function upsert(asset){assets.set(asset.tag_id,asset);updates++;renderAll();}
async function loadAssets(){
  try{const response=await fetch('/api/assets');const data=await response.json();data.forEach(upsert);}
  catch(e){setConnection(false);}
}
async function loadHistory(){
  try{
    const response=await fetch('/api/history');
    const rows=await response.json();
    const body=$("historyBody");
    if(!rows.length)return;
    body.innerHTML=rows.slice(0,30).map(row=>
      '<tr><td>'+new Date(row.timestamp*1000).toLocaleTimeString()+'</td><td>'+row.tag_id+'</td><td>'+Number(row.x).toFixed(2)+'</td><td>'+Number(row.y).toFixed(2)+'</td><td>'+row.method+'</td></tr>').join("");
  }catch(e){}
}
socket.on('connect',()=>setConnection(true));
socket.on('disconnect',()=>setConnection(false));
socket.on('asset_update',upsert);
loadAssets();loadHistory();
setInterval(loadHistory,5000);