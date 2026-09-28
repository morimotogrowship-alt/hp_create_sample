s = open('/tmp/template2.html', encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, count)

# ---- stripes + finer grass detail in the near terrain shader ----
rep("const nearMat = new THREE.MeshStandardMaterial({roughness:0.93, metalness:0});",
"""const HD = (()=>{ const a=D.feat.tees.FULL, b=D.feat.pin; const dx=b.x-a.x, dz=b.z-a.z, l=Math.hypot(dx,dz); return [dx/l, dz/l]; })();
const nearMat = new THREE.MeshStandardMaterial({roughness:0.93, metalness:0});""")
rep("    vec3 col = rough2;",
"""    vec2 hd = vec2(${HD[0].toFixed(5)}, ${HD[1].toFixed(5)}); vec2 pd = vec2(-hd.y, hd.x);
    float sF = smoothstep(0.46, 0.54, abs(fract(dot(vWP.xz, pd)/13.0)*2.0-1.0));
    float sG = smoothstep(0.44, 0.56, abs(fract(dot(vWP.xz, hd)/3.2)*2.0-1.0));
    float micro = vnoise(vWP.xz*22.0)*0.5 + vnoise(vWP.xz*55.0)*0.5;
    fair *= mix(0.86, 1.10, sF) * (0.95+0.08*micro);
    grn  *= mix(0.93, 1.06, sG) * (0.98+0.04*micro);
    teeC *= mix(0.94, 1.05, sG);
    rough2 *= 0.9+0.2*micro; rough1 *= 0.93+0.14*micro;
    vec3 col = rough2;""")
# summer colours
rep("vec3 rough2 = lin(vec3(0.30,0.42,0.16))", "vec3 rough2 = lin(vec3(0.27,0.44,0.13))")
rep("vec3 rough1 = lin(vec3(0.33,0.50,0.18))", "vec3 rough1 = lin(vec3(0.32,0.54,0.15))")
rep("vec3 fair   = lin(vec3(0.34,0.58,0.20))", "vec3 fair   = lin(vec3(0.38,0.66,0.19))")
rep("vec3 grn    = lin(vec3(0.27,0.62,0.24))", "vec3 grn    = lin(vec3(0.33,0.68,0.22))")
rep("vec3 forest = lin(vec3(0.13,0.20,0.08))", "vec3 forest = lin(vec3(0.16,0.22,0.09))")
rep("renderer.toneMappingExposure = 0.55;", "renderer.toneMappingExposure = 0.62;")

# ---- trees + clouds ----
rep("// ---------- info panel ----------", r"""// ---------- trees (procedural, instanced) ----------
function mulberry(a){ return ()=>{ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function leafTexture(seed, hueA, hueB, needle){
  const cv=document.createElement('canvas'); cv.width=cv.height=256; const c=cv.getContext('2d'); const r=mulberry(seed);
  for (let i=0;i<(needle?260:85);i++){
    const x=20+r()*216, y=20+r()*216, a=r()*Math.PI*2, l=needle? 10+r()*14 : 12+r()*14, w=needle? 1.2 : 5+r()*4;
    const h=hueA+(hueB-hueA)*r(), s=40+r()*25, v=20+r()*22;
    c.save(); c.translate(x,y); c.rotate(a); c.fillStyle=`hsl(${h},${s}%,${v}%)`;
    c.beginPath(); c.ellipse(0,0,l,w,0,0,Math.PI*2); c.fill();
    if (!needle){ c.strokeStyle=`hsla(${h},${s}%,${v+12}%,0.6)`; c.lineWidth=0.8; c.beginPath(); c.moveTo(-l,0); c.lineTo(l,0); c.stroke(); }
    c.restore();
  }
  const t=new THREE.CanvasTexture(cv); t.colorSpace=THREE.SRGBColorSpace; t.anisotropy=4; return t;
}
function makeTree(kind, seed){
  const r=mulberry(seed); const P=[],N=[],U=[],I=[]; const TP=[],TN=[],TI=[];
  function card(cx,cy,cz,size,ox,oy,oz,flat){
    const a=r()*Math.PI*2, b=(flat? (r()-0.5)*0.6 : (r()-0.5)*Math.PI);
    const ux=Math.cos(a), uz=Math.sin(a); const vx=-Math.sin(a)*Math.sin(b), vy=Math.cos(b), vz=Math.cos(a)*Math.sin(b);
    const tx=flat?ux:ux, ty=flat?0:0, tz=flat?uz:uz;
    const ax= flat? -uz : vx, ay= flat? 0.25 : vy, az= flat? ux : vz;
    const base=P.length/3;
    for (const [s,t] of [[-1,-1],[1,-1],[1,1],[-1,1]]){
      P.push(cx+(tx*s+ax*t)*size/2, cy+(ty*s+ay*t)*size/2, cz+(tz*s+az*t)*size/2);
      let nx=cx-ox, ny=(cy-oy)*0.8+0.35, nz=cz-oz; const l=Math.hypot(nx,ny,nz)||1; N.push(nx/l,ny/l,nz/l);
      U.push((s+1)/2,(t+1)/2);
    }
    I.push(base,base+1,base+2,base,base+2,base+3);
  }
  function cyl(x0,y0,z0,x1,y1,z1,r0,r1,seg=6){
    const base=TP.length/3; const d=new THREE.Vector3(x1-x0,y1-y0,z1-z0); const up=Math.abs(d.y/d.length())>0.9?new THREE.Vector3(1,0,0):new THREE.Vector3(0,1,0);
    const e1=new THREE.Vector3().crossVectors(d,up).normalize(), e2=new THREE.Vector3().crossVectors(d,e1).normalize();
    for (let k=0;k<=1;k++) for (let i=0;i<seg;i++){ const a=i/seg*Math.PI*2, rr=k?r1:r0; const n=e1.clone().multiplyScalar(Math.cos(a)).addScaledVector(e2,Math.sin(a));
      TP.push((k?x1:x0)+n.x*rr,(k?y1:y0)+n.y*rr,(k?z1:z0)+n.z*rr); TN.push(n.x,n.y,n.z); }
    for (let i=0;i<seg;i++){ const a=base+i, b=base+(i+1)%seg, c=a+seg, dd=b+seg; TI.push(a,b,c,b,dd,c); }
  }
  if (kind===0){ // broadleaf (konara / sakura type): spreading crown of leaf clumps
    const ch=0.66, cw=0.30+r()*0.06;
    cyl(0,0,0, 0,0.42,0, 0.03,0.02, 8);
    const nClump=15;
    for (let k=0;k<nClump;k++){
      const a=r()*Math.PI*2, e=r()*1.2-0.35; const cx=Math.cos(a)*Math.cos(e)*cw, cz=Math.sin(a)*Math.cos(e)*cw, cy=ch+Math.sin(e)*0.22;
      cyl(0,0.38+r()*0.06,0, cx*0.85,cy-0.04,cz*0.85, 0.012,0.005, 5);
      for (let j=0;j<8;j++) card(cx+(r()-0.5)*0.12, cy+(r()-0.5)*0.10, cz+(r()-0.5)*0.12, 0.13+r()*0.05, 0,ch,0, false);
    }
  } else if (kind===1){ // hinoki / sugi: narrow cone
    cyl(0,0,0, 0,0.97,0, 0.022,0.004, 7);
    for (let k=0;k<17;k++){ const t=0.18+k/17*0.8, rad=0.17*Math.pow(1-t,0.9)+0.02, cy=t;
      for (let j=0;j<7;j++){ const a=r()*Math.PI*2, rr=rad*(0.5+0.5*r()); card(Math.cos(a)*rr, cy+(r()-0.5)*0.04, Math.sin(a)*rr, 0.07+0.08*(1-t), 0,cy,0, true); } }
  } else { // akamatsu: tall slightly leaning trunk, flat clumps near the top
    const lx=(r()-0.5)*0.12, lz=(r()-0.5)*0.12;
    cyl(0,0,0, lx*0.5,0.45,lz*0.5, 0.028,0.022, 7); cyl(lx*0.5,0.45,lz*0.5, lx,0.82,lz, 0.022,0.01, 7);
    for (let k=0;k<7;k++){ const a=r()*Math.PI*2, d=0.08+r()*0.16, cy=0.62+r()*0.28; const cx=lx+Math.cos(a)*d, cz=lz+Math.sin(a)*d;
      cyl(lx*0.8,cy-0.06,lz*0.8, cx,cy,cz, 0.01,0.005, 5);
      for (let j=0;j<9;j++) card(cx+(r()-0.5)*0.14, cy+(r()-0.5)*0.03, cz+(r()-0.5)*0.14, 0.09+r()*0.04, lx,0.8,lz, true); }
  }
  const lg=new THREE.BufferGeometry(); lg.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); lg.setAttribute('normal',new THREE.Float32BufferAttribute(N,3)); lg.setAttribute('uv',new THREE.Float32BufferAttribute(U,2)); lg.setIndex(I);
  const tg=new THREE.BufferGeometry(); tg.setAttribute('position',new THREE.Float32BufferAttribute(TP,3)); tg.setAttribute('normal',new THREE.Float32BufferAttribute(TN,3)); tg.setIndex(TI);
  return {lg, tg};
}
const treeData = D.trees || [];
const treeMeshes = [];
{
  const leafTex=[leafTexture(11,85,110,false), leafTexture(12,95,125,true), leafTexture(13,80,105,true)];
  const barkCol=[0x5a4a3b, 0x6b4a36, 0x8d5a3a];
  const leafTint=[0xffffff, 0xd8e6d2, 0xe6f0d8];
  const bySp=[[],[],[]]; for (const t of treeData) bySp[t[2]].push(t);
  const m4=new THREE.Matrix4(), q=new THREE.Quaternion(), v=new THREE.Vector3(), sc3=new THREE.Vector3(), col=new THREE.Color();
  for (let sp=0; sp<3; sp++){
    const list=bySp[sp]; if (!list.length) continue;
    const {lg,tg}=makeTree(sp, 100+sp);
    const lm=new THREE.MeshStandardMaterial({map:leafTex[sp], alphaTest:0.5, side:THREE.DoubleSide, roughness:0.85, color:leafTint[sp]});
    const tm=new THREE.MeshStandardMaterial({color:barkCol[sp], roughness:1});
    const L=new THREE.InstancedMesh(lg, lm, list.length), T=new THREE.InstancedMesh(tg, tm, list.length);
    const rr=mulberry(500+sp);
    list.forEach((t,i)=>{ const [x,z,,h,rot]=t; q.setFromAxisAngle(new THREE.Vector3(0,1,0), rot); v.set(x, hNear(x,z)-0.15, z); sc3.set(h*(0.9+0.2*rr()), h, h*(0.9+0.2*rr()));
      m4.compose(v,q,sc3); L.setMatrixAt(i,m4); T.setMatrixAt(i,m4);
      col.setHSL(0.24+ (rr()-0.5)*0.05, 0.35+rr()*0.2, 0.42+rr()*0.16); L.setColorAt(i,col); });
    L.castShadow=true; L.receiveShadow=true; T.castShadow=true; T.receiveShadow=true;
    scene.add(L); scene.add(T); treeMeshes.push(L,T);
  }
}
function setTreeDensity(f){ for (const m of treeMeshes){ m.count=Math.floor(m.instanceMatrix.count*f); } }

// ---------- cumulus clouds (procedural dome following the camera) ----------
const cloudMat=new THREE.ShaderMaterial({ transparent:true, depthWrite:false, side:THREE.BackSide, fog:false,
  uniforms:{ uSun:{value:sunDir} },
  vertexShader:`varying vec3 vDir; void main(){ vDir=normalize(position); vec4 p=projectionMatrix*modelViewMatrix*vec4(position,1.0); gl_Position=p; gl_Position.z=p.w*0.99999; }`,
  fragmentShader:`varying vec3 vDir; uniform vec3 uSun;
    float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
    float n(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.0-2.0*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
    float fbm(vec2 p){ float s=0.0,a=0.5; for(int i=0;i<6;i++){ s+=a*n(p); p=p*2.03+vec2(1.7,9.2); a*=0.5; } return s; }
    void main(){ if (vDir.y<0.0) discard;
      vec2 uv=vDir.xz/(vDir.y+0.12)*1.3 + vec2(3.0,1.0);
      float d=fbm(uv); float c=smoothstep(0.55,0.78,d);
      float top=smoothstep(0.55,0.95,fbm(uv+vec2(0.03,0.05)));
      float sunF=pow(max(dot(normalize(vDir),normalize(uSun)),0.0),6.0);
      vec3 col=mix(vec3(0.62,0.66,0.72), vec3(1.0), 0.45+0.55*top) * (1.25+0.5*sunF);
      float a=c*smoothstep(0.02,0.22,vDir.y)*0.95;
      gl_FragColor=vec4(col*1.6,a);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }` });
const clouds=new THREE.Mesh(new THREE.SphereGeometry(8000,48,24), cloudMat); clouds.renderOrder=1; scene.add(clouds);

// ---------- info panel ----------""")
rep("  scaleMarkers();\n", "  scaleMarkers();\n  clouds.position.copy(camera.position);\n")
# quality: tree density
rep("function setQuality(q){ const c=Q[q]; buildNear(c.step);", "function setQuality(q){ const c=Q[q]; buildNear(c.step); setTreeDensity(c.trees);")
rep("const Q={ high:{step:1, shadow:4096, pr:2}, std:{step:2, shadow:2048, pr:1.5}, low:{step:4, shadow:1024, pr:1} };",
    "const Q={ high:{step:1, shadow:4096, pr:2, trees:1}, std:{step:2, shadow:2048, pr:1.5, trees:1}, low:{step:4, shadow:1024, pr:1, trees:0.4} };")
open('/tmp/template2.html', 'w', encoding='utf-8').write(s)
print('ok')
