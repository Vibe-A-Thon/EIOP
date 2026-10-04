/**
 * Phase 12.1 — Self-Contained Interactive HTML Export.
 * Generates a single HTML file containing graph data, Sigma.js renderer,
 * search/filter/inspect interaction — all inline, no server needed.
 */

function compressElements(nodes, edges) {
  return {
    n: nodes.map(n => ({
      i: n.id, l: n.label, d: n.domain,
      p: n.properties || {}, m: n.metrics || {},
    })),
    e: edges.map(e => ({
      i: e.id, t: e.type, s: e.from_id, r: e.to_id,
      cs: e.creation_status, p: e.properties || {},
    })),
  };
}

export function generateInteractiveHTML(nodes, edges, options = {}) {
  const {title = 'KGR Graph Export', darkMode = true, communityHulls = true} = options;
  const data = JSON.stringify(compressElements(nodes, edges));

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0f172a;--fg:#e2e8f0;--panel:#1e293b;--line:#334155;--accent:#7c5cff;--muted:#64748b}
@media(prefers-color-scheme:light){:root{--bg:#f8fafc;--fg:#1e293b;--panel:#fff;--line:#e2e8f0;--muted:#94a3b8}}
body{font-family:Inter,system-ui,sans-serif;background:var(--bg);color:var(--fg);height:100vh;display:flex;flex-direction:column}
#toolbar{display:flex;gap:8px;padding:8px 12px;background:var(--panel);border-bottom:1px solid var(--line);align-items:center;flex-wrap:wrap}
#toolbar input[type="text"]{flex:1;min-width:150px;padding:5px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font-size:12px}
#toolbar label{font-size:11px;display:flex;align-items:center;gap:4px;color:var(--muted)}
#toolbar input[type="checkbox"]{accent-color:var(--accent)}
#container{flex:1;position:relative}
#inspector{position:absolute;top:8px;right:8px;width:280px;max-height:calc(100vh - 80px);background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;overflow-y:auto;font-size:12px;display:none;z-index:5}
#inspector h3{margin:0 0 6px;font-size:14px}
#inspector .prop{display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid var(--line)}
#inspector .prop dt{color:var(--muted)}
#inspector .close{position:absolute;top:8px;right:10px;cursor:pointer;color:var(--muted);font-size:16px}
#info{position:absolute;bottom:8px;left:8px;font-size:11px;color:var(--muted);background:var(--panel);padding:4px 10px;border-radius:6px;border:1px solid var(--line)}
</style>
</head>
<body>
<div id="toolbar">
  <strong style="font-size:13px">${title}</strong>
  <input type="text" id="search" placeholder="Search nodes...">
  <div id="type-filters"></div>
</div>
<div id="container"></div>
<div id="inspector"><span class="close" onclick="this.parentElement.style.display='none'">&times;</span><h3 id="ins-title"></h3><div id="ins-props"></div></div>
<div id="info"></div>
<script>
const D=${data};
const palette={WorkItem:'#7c5cff',Project:'#9a7dff',Person:'#ef6e91',Repository:'#0ea5e9',Branch:'#38bdf8',Commit:'#2563eb',File:'#64748b',CodeSymbol:'#10b981',Dependency:'#f59e0b',MergeRequest:'#8b5cf6',PipelineRun:'#f97316',Document:'#14b8a6',Evidence:'#eab308',IngestionRun:'#94a3b8',ValidationRun:'#22c55e',ValidationFinding:'#ef4444'};
const types=new Set(D.n.map(n=>n.l));
const filtersEl=document.getElementById('type-filters');
const activeTypes=new Set(types);
types.forEach(t=>{
  const lbl=document.createElement('label');
  const cb=document.createElement('input');cb.type='checkbox';cb.checked=true;
  cb.onchange=()=>{cb.checked?activeTypes.add(t):activeTypes.delete(t);render()};
  lbl.append(cb,' '+t);filtersEl.append(lbl);
});
const nodes=new Map(),nodePositions={};
D.n.forEach((n,i)=>{
  nodes.set(n.i,n);
  const angle=2*Math.PI*i/D.n.length;
  nodePositions[n.i]={x:400+300*Math.cos(angle),y:300+300*Math.sin(angle)};
});
const canvas=document.createElement('canvas');
canvas.style.width='100%';canvas.style.height='100%';
document.getElementById('container').append(canvas);
let W,H,offX=0,offY=0,scale=1,dragging=false,dragX,dragY;
function resize(){W=canvas.clientWidth;H=canvas.clientHeight;canvas.width=W*2;canvas.height=H*2}
window.addEventListener('resize',resize);resize();
const ctx=canvas.getContext('2d');
let searchText='';
document.getElementById('search').oninput=e=>{searchText=e.target.value.toLowerCase();render()};
function render(){
  ctx.setTransform(2,0,0,2,0,0);ctx.clearRect(0,0,W,H);
  ctx.save();ctx.translate(W/2+offX,H/2+offY);ctx.scale(scale,scale);ctx.translate(-W/2,-H/2);
  D.e.forEach(e=>{
    if(!activeTypes.has(nodes.get(e.s)?.l)||!activeTypes.has(nodes.get(e.r)?.l))return;
    const s=nodePositions[e.s],t=nodePositions[e.r];if(!s||!t)return;
    ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(t.x,t.y);
    ctx.strokeStyle=e.cs==='INFERRED'?'#f59e0b44':'#64748b44';ctx.lineWidth=0.8;ctx.stroke();
  });
  D.n.forEach(n=>{
    if(!activeTypes.has(n.l))return;
    if(searchText&&!(n.p.name||n.i).toLowerCase().includes(searchText))return;
    const p=nodePositions[n.i];if(!p)return;
    const deg=n.m.degree||1;const r=Math.max(4,Math.min(14,3+deg*0.5));
    ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);
    ctx.fillStyle=palette[n.l]||'#64748b';ctx.fill();
    if(scale>0.6){ctx.fillStyle=getComputedStyle(document.body).color;ctx.font='9px Inter,sans-serif';
      ctx.fillText((n.p.name||n.i).slice(0,18),p.x+r+3,p.y+3);}
  });
  ctx.restore();
  document.getElementById('info').textContent=D.n.length+' nodes · '+D.e.length+' edges · zoom '+scale.toFixed(1)+'x';
}
canvas.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?1.1:0.9;scale=Math.max(0.1,Math.min(8,scale*f));render()});
canvas.addEventListener('mousedown',e=>{dragging=true;dragX=e.clientX;dragY=e.clientY});
canvas.addEventListener('mousemove',e=>{if(!dragging)return;offX+=e.clientX-dragX;offY+=e.clientY-dragY;dragX=e.clientX;dragY=e.clientY;render()});
canvas.addEventListener('mouseup',()=>dragging=false);
canvas.addEventListener('click',e=>{
  const rect=canvas.getBoundingClientRect();
  const mx=(e.clientX-rect.left-rect.width/2-offX)/scale+W/2;
  const my=(e.clientY-rect.top-rect.height/2-offY)/scale+H/2;
  let closest=null,minD=Infinity;
  D.n.forEach(n=>{
    const p=nodePositions[n.i];if(!p)return;
    const d=Math.hypot(p.x-mx,p.y-my);if(d<20&&d<minD){minD=d;closest=n}
  });
  if(closest){
    const ins=document.getElementById('inspector');ins.style.display='block';
    document.getElementById('ins-title').textContent=(closest.p.name||closest.i);
    const props=document.getElementById('ins-props');props.innerHTML='';
    Object.entries({type:closest.l,domain:closest.d,...closest.p,...closest.m}).forEach(([k,v])=>{
      if(v==null)return;const row=document.createElement('div');row.className='prop';
      row.innerHTML='<dt>'+k+'</dt><dd>'+String(v).slice(0,60)+'</dd>';props.append(row);
    });
  }
});
render();
<\/script>
</body>
</html>`;
}

export function estimateExportSize(nodeCount) {
  return Math.ceil(150 + nodeCount * 0.35);
}
