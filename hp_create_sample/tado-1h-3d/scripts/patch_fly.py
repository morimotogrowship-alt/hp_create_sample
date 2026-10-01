s = open('/tmp/template2.html', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, 1)

# ---- CSS ----
rep("  #fps{left:10px;bottom:6px;font-size:11px;padding:3px 6px;}", """  #fps{left:10px;bottom:6px;font-size:11px;padding:3px 6px;}
  #flyHud{left:50%;top:10px;transform:translateX(-50%);display:none;text-align:center;font-size:13px;min-width:300px;}
  #flyHud .help{font-size:11px;color:#c9d6c5;margin-top:4px;}
  #joy{position:absolute;left:24px;bottom:40px;width:130px;height:130px;border-radius:50%;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.45);display:none;touch-action:none;}
  #joyKnob{position:absolute;left:40px;top:40px;width:50px;height:50px;border-radius:50%;background:rgba(255,255,255,.55);}
  #flyBtns{position:absolute;right:24px;bottom:40px;display:none;flex-direction:column;gap:10px;}
  #flyBtns button{width:64px;height:52px;font-size:13px;text-align:center;touch-action:none;background:rgba(18,28,22,.75);}
  button.fly{background:#7a4d12;border-color:#d9973a;}""")

# ---- UI ----
rep('  <button id="vBack">④ グリーン奥から振り返り</button>', """  <button id="vBack">④ グリーン奥から振り返り</button>
  <button id="vFree" class="fly">⑤ 自由飛行モード：OFF</button>""")
rep('<div id="measure" class="panel"></div>', """<div id="measure" class="panel"></div>
<div id="flyHud" class="panel"><div id="flyInfo"></div>
  <div class="help">PC：W/S 前後・A/D 左右・Space/E 上昇・Shift+Space/Q 下降・ドラッグで向き・ホイールで速さ・Shiftで加速・Escで終了<br>スマホ：左の円で移動・画面ドラッグで向き・右のボタンで上下</div></div>
<div id="joy"><div id="joyKnob"></div></div>
<div id="flyBtns"><button id="flyUp">▲ 上昇</button><button id="flyDown">▼ 下降</button></div>""")

# ---- logic ----
rep("$('vTee').onclick=viewTee; $('vTop').onclick=viewTop; $('vBack').onclick=viewBack; $('vFly').onclick=viewFly;", r"""$('vTee').onclick=()=>{stopFree(); viewTee();}; $('vTop').onclick=()=>{stopFree(); viewTop();}; $('vBack').onclick=()=>{stopFree(); viewBack();}; $('vFly').onclick=()=>{stopFree(); viewFly();};

// ---------- free flight (drone-style) ----------
const free = { on:false, yaw:0, pitch:0, vel:new THREE.Vector3(), speed:15, keys:{}, joy:[0,0], up:0, drag:null };
const FREE_LIMIT = MID.ext - 300;      // stay inside the detailed terrain
function startFree(){
  fly=null; free.on=true; controls.enabled=false;
  const d=new THREE.Vector3(); camera.getWorldDirection(d);
  free.yaw=Math.atan2(d.x, -d.z); free.pitch=Math.asin(Math.max(-0.99, Math.min(0.99, d.y)));
  free.vel.set(0,0,0); camera.fov=60; camera.updateProjectionMatrix();
  $('vFree').classList.add('on'); $('vFree').textContent='⑤ 自由飛行モード：ON';
  $('flyHud').style.display='block';
  const touch = matchMedia('(pointer: coarse)').matches;
  $('joy').style.display = touch ? 'block' : 'none'; $('flyBtns').style.display = touch ? 'flex' : 'none';
}
function stopFree(){
  if (!free.on) return; free.on=false;
  const d=new THREE.Vector3(); camera.getWorldDirection(d);
  controls.target.copy(camera.position).addScaledVector(d, 40); controls.enabled=true; controls.update();
  $('vFree').classList.remove('on'); $('vFree').textContent='⑤ 自由飛行モード：OFF';
  $('flyHud').style.display='none'; $('joy').style.display='none'; $('flyBtns').style.display='none';
  free.keys={}; free.joy=[0,0]; free.up=0;
}
$('vFree').onclick=()=>{ if (free.on) stopFree(); else startFree(); };
const typing = e => ['INPUT','SELECT','TEXTAREA'].includes(document.activeElement && document.activeElement.tagName);
window.addEventListener('keydown', e=>{ if (!free.on || typing(e)) return;
  if (e.code==='Escape'){ stopFree(); return; }
  free.keys[e.code]=true; if (['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)) e.preventDefault(); });
window.addEventListener('keyup', e=>{ free.keys[e.code]=false; });
canvas.addEventListener('wheel', e=>{ if (!free.on) return; e.preventDefault();
  free.speed=Math.max(2, Math.min(120, free.speed*(e.deltaY<0?1.15:1/1.15))); }, {passive:false});
canvas.addEventListener('pointerdown', e=>{ if (!free.on) return; free.drag={id:e.pointerId, x:e.clientX, y:e.clientY}; canvas.setPointerCapture(e.pointerId); });
canvas.addEventListener('pointermove', e=>{ if (!free.on || !free.drag || free.drag.id!==e.pointerId) return;
  const k = e.pointerType==='touch' ? 0.005 : 0.0035;
  free.yaw += (e.clientX-free.drag.x)*k; free.pitch -= (e.clientY-free.drag.y)*k;
  free.pitch=Math.max(-1.45, Math.min(1.2, free.pitch)); free.drag.x=e.clientX; free.drag.y=e.clientY; });
canvas.addEventListener('pointerup', e=>{ if (free.drag && free.drag.id===e.pointerId) free.drag=null; });
// touch joystick
{ const joy=$('joy'), knob=$('joyKnob'); let jid=null;
  const setJ=(e)=>{ const r=joy.getBoundingClientRect(); let dx=(e.clientX-r.left-r.width/2)/(r.width/2), dy=(e.clientY-r.top-r.height/2)/(r.height/2);
    const l=Math.hypot(dx,dy); if (l>1){ dx/=l; dy/=l; } free.joy=[dx,-dy]; knob.style.left=(40+dx*40)+'px'; knob.style.top=(40+dy*40)+'px'; };
  joy.addEventListener('pointerdown', e=>{ jid=e.pointerId; joy.setPointerCapture(jid); setJ(e); e.stopPropagation(); });
  joy.addEventListener('pointermove', e=>{ if (e.pointerId===jid) setJ(e); });
  const end=e=>{ if (e.pointerId!==jid) return; jid=null; free.joy=[0,0]; knob.style.left='40px'; knob.style.top='40px'; };
  joy.addEventListener('pointerup', end); joy.addEventListener('pointercancel', end);
  for (const [id,v] of [['flyUp',1],['flyDown',-1]]){ const b=$(id);
    b.addEventListener('pointerdown', e=>{ free.up=v; e.preventDefault(); }); for (const ev of ['pointerup','pointerleave','pointercancel']) b.addEventListener(ev, ()=>{ free.up=0; }); }
}
function updateFree(dt){
  const K=free.keys;
  let f=(K.KeyW||K.ArrowUp?1:0)-(K.KeyS||K.ArrowDown?1:0)+free.joy[1];
  let r=(K.KeyD||K.ArrowRight?1:0)-(K.KeyA||K.ArrowLeft?1:0)+free.joy[0];
  const shift=K.ShiftLeft||K.ShiftRight;
  let u=((K.Space&&!shift)||K.KeyE?1:0)-((K.Space&&shift)||K.KeyQ?1:0)+free.up;
  const sp=free.speed*(shift&&!K.Space?2.5:1);
  const fwd=new THREE.Vector3(Math.sin(free.yaw)*Math.cos(free.pitch), Math.sin(free.pitch), -Math.cos(free.yaw)*Math.cos(free.pitch));
  const right=new THREE.Vector3(Math.cos(free.yaw), 0, Math.sin(free.yaw));
  const want=new THREE.Vector3().addScaledVector(fwd,f).addScaledVector(right,r).addScaledVector(new THREE.Vector3(0,1,0),u);
  if (want.lengthSq()>1) want.normalize(); want.multiplyScalar(sp);
  free.vel.lerp(want, 1-Math.exp(-dt*4));                 // smooth acceleration / braking like a drone
  camera.position.addScaledVector(free.vel, dt);
  camera.position.x=Math.max(-FREE_LIMIT, Math.min(FREE_LIMIT, camera.position.x));
  camera.position.z=Math.max(-FREE_LIMIT, Math.min(FREE_LIMIT, camera.position.z));
  const g=hAt(camera.position.x, camera.position.z);
  if (camera.position.y < g+1.5){ camera.position.y=g+1.5; if (free.vel.y<0) free.vel.y=0; }   // never go below the ground
  if (camera.position.y > g+600) camera.position.y=g+600;
  camera.lookAt(camera.position.clone().add(fwd));
  const dp=Math.hypot(pin.x-camera.position.x, pin.z-camera.position.z);
  $('flyInfo').innerHTML=`高度（地面から）<b>${(camera.position.y-g).toFixed(1)} m</b>　速さ <b>${(free.vel.length()*3.6).toFixed(0)} km/h</b>（設定 ${(free.speed*3.6).toFixed(0)}）　ピンまで <b>${Math.round(dp/YD)} Y</b>`;
}""")
rep("function animate(now){", "let lastFrame=performance.now();\nfunction animate(now){\n  const dtF=Math.min(0.1,(now-lastFrame)/1000); lastFrame=now;")
rep("  if (fly){", "  if (free.on){ updateFree(dtF); }\n  else if (fly){")
rep("window.__views = {viewTee,", "window.__views = {startFree, stopFree, viewTee,")
open('/tmp/template2.html', 'w', encoding='utf-8').write(s)
print('ok')
