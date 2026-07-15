(function(){
  function start(){
    if(!window.THREE||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    const section=document.querySelector('.journey'),canvas=section&&section.querySelector('.journey-webgl');
    if(!section||!canvas)return;
    let renderer;
    try{renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,powerPreference:'high-performance'});}catch(e){return;}
    renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.7));renderer.outputEncoding=THREE.sRGBEncoding;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
    const scene=new THREE.Scene();scene.background=new THREE.Color(0x10283b);scene.fog=new THREE.FogExp2(0x7992a0,.012);
    const camera=new THREE.PerspectiveCamera(52,1,.1,500);camera.position.set(0,5,18);
    scene.add(new THREE.HemisphereLight(0xddefff,0x153245,1.35));
    const sun=new THREE.DirectionalLight(0xffe5b8,2.2);sun.position.set(-12,22,-35);scene.add(sun);
    const rim=new THREE.PointLight(0x75d9ff,1.4,70);rim.position.set(0,8,-62);scene.add(rim);

    const waterMat=new THREE.ShaderMaterial({transparent:false,uniforms:{uTime:{value:0},uNear:{value:new THREE.Color(0x285d72)},uFar:{value:new THREE.Color(0x0a2940)}},vertexShader:'uniform float uTime; varying float vWave; void main(){vec3 p=position; float w=sin(p.x*.34+uTime*.7)*.18+sin(p.y*.22-uTime*.52)*.14+sin((p.x+p.y)*.13+uTime*.35)*.1; p.z=w; vWave=w; gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.0);}',fragmentShader:'uniform vec3 uNear; uniform vec3 uFar; varying float vWave; void main(){float h=smoothstep(-.35,.36,vWave); vec3 c=mix(uFar,uNear,h); float glint=pow(max(h,.0),6.0)*.28; gl_FragColor=vec4(c+glint,1.0);}'});
    const water=new THREE.Mesh(new THREE.PlaneGeometry(260,260,110,110),waterMat);water.rotation.x=-Math.PI/2;water.position.set(0,0,-70);scene.add(water);
    const horizon=new THREE.Mesh(new THREE.CircleGeometry(8,64),new THREE.MeshBasicMaterial({color:0xffdeb0,transparent:true,opacity:.58}));horizon.position.set(0,16,-190);scene.add(horizon);

    function labelTexture(title,sub){const c=document.createElement('canvas');c.width=1024;c.height=512;const x=c.getContext('2d');x.fillStyle='#f2f0e9';x.fillRect(0,0,c.width,c.height);x.fillStyle='#0a2034';x.textAlign='center';x.font='700 112px Arial';x.fillText(title,512,220);x.font='400 30px Arial';x.fillText(sub,512,300);x.strokeStyle='#55788b';x.lineWidth=2;x.strokeRect(38,38,948,436);const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;return t;}
    const glass=new THREE.MeshStandardMaterial({color:0x17364a,metalness:.62,roughness:.26});
    const stone=new THREE.MeshStandardMaterial({color:0xbcc2c0,metalness:.18,roughness:.62});
    const dark=new THREE.MeshStandardMaterial({color:0x0c2639,metalness:.72,roughness:.3});
    const city=new THREE.Group();scene.add(city);
    const island=new THREE.Group();island.position.set(3.8,0,-35);scene.add(island);
    const rockMat=new THREE.MeshStandardMaterial({color:0x43564f,roughness:.88,metalness:.03});
    const greenMat=new THREE.MeshStandardMaterial({color:0x365847,roughness:.95});
    const islandBase=new THREE.Mesh(new THREE.SphereGeometry(4.4,22,12),rockMat);islandBase.scale.set(1,.38,1.25);islandBase.position.y=-.35;island.add(islandBase);
    [[-1.7,1.8,2.5],[.3,3.2,3.1],[2,2.2,2.3],[-.2,1.4,2]].forEach((v,i)=>{const peak=new THREE.Mesh(new THREE.ConeGeometry(v[2],v[1],7),i===1?rockMat:greenMat);peak.position.set(v[0],v[1]/2-.05,(i-1.5)*.75);peak.rotation.y=i*.8;island.add(peak);});
    function tower(x,z,w,h,d,mat,sign){const g=new THREE.Group();const box=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);box.position.y=h/2;g.add(box);const cap=new THREE.Mesh(new THREE.BoxGeometry(w*.9,.12,d*1.02),new THREE.MeshBasicMaterial({color:0x80c7d7}));cap.position.y=h*.76;g.add(cap);if(sign){const tex=labelTexture(sign.title,sign.sub);const face=new THREE.Mesh(new THREE.PlaneGeometry(w*.86,w*.43),new THREE.MeshBasicMaterial({map:tex}));face.position.set(x<0?w/2+.02:-w/2-.02,h*.58,0);face.rotation.y=x<0?Math.PI/2:-Math.PI/2;g.add(face);}g.position.set(x,0,z);city.add(g);return g;}
    tower(-5,-116,8,23,10,stone,{title:'BUSINESS',sub:'IT SERVICE / AI・DX / MODEL'});
    const specs=[[-12,-106,6,16,7],[-1,-108,7,28,8],[-13,-123,9,34,9],[-3,-132,7,22,8],[-14,-145,8,27,9],[-5,-153,6,18,7]];
    specs.forEach((v,i)=>tower(v[0],v[1],v[2],v[3],v[4],i%2?glass:dark));
    const cityMaterials=[];city.traverse(o=>{if(o.material&&!cityMaterials.includes(o.material)){o.material.transparent=true;o.material.opacity=0;cityMaterials.push(o.material);}});
    for(let z=-18;z>-140;z-=11){for(const x of[-7.8,7.8]){const lamp=new THREE.PointLight(0x7edcf2,.32,10);lamp.position.set(x,2.3,z);scene.add(lamp);}}

    const ship=new THREE.Group();scene.add(ship);
    const hullMat=new THREE.MeshStandardMaterial({color:0xe8e9e4,metalness:.68,roughness:.28});
    const hull=new THREE.Mesh(new THREE.SphereGeometry(1.28,32,18),hullMat);hull.scale.set(1,.5,3.45);hull.position.y=.05;ship.add(hull);
    const keel=new THREE.Mesh(new THREE.SphereGeometry(1.12,28,14),new THREE.MeshStandardMaterial({color:0x17394c,metalness:.55,roughness:.3}));keel.scale.set(1,.31,3.18);keel.position.y=-.34;ship.add(keel);
    const deck=new THREE.Mesh(new THREE.BoxGeometry(2.02,.16,3.75),hullMat);deck.position.set(0,.53,-.2);ship.add(deck);
    const cabinMat=new THREE.MeshStandardMaterial({color:0xf1f0e9,metalness:.42,roughness:.24});
    const cabin=new THREE.Mesh(new THREE.BoxGeometry(1.55,.72,1.7),cabinMat);cabin.position.set(0,.94,.15);ship.add(cabin);
    const bridge=new THREE.Mesh(new THREE.BoxGeometry(1.62,.38,.72),new THREE.MeshStandardMaterial({color:0x163b50,metalness:.48,roughness:.1}));bridge.position.set(0,1.05,-.47);ship.add(bridge);
    const upperDeck=new THREE.Mesh(new THREE.BoxGeometry(1.22,.12,1.2),cabinMat);upperDeck.position.set(0,1.37,.14);ship.add(upperDeck);
    const mast=new THREE.Mesh(new THREE.CylinderGeometry(.035,.05,1.55,10),new THREE.MeshStandardMaterial({color:0xcdd1cd,metalness:.8,roughness:.2}));mast.position.set(0,2.16,.05);ship.add(mast);
    const radar=new THREE.Mesh(new THREE.BoxGeometry(.72,.055,.08),new THREE.MeshBasicMaterial({color:0xbfe9ef}));radar.position.set(0,2.78,.05);ship.add(radar);
    const railMat=new THREE.MeshBasicMaterial({color:0xd7e1df});
    for(const x of[-1.03,1.03]){const rail=new THREE.Mesh(new THREE.BoxGeometry(.025,.18,3.1),railMat);rail.position.set(x,.73,.08);ship.add(rail);}
    const sternLight=new THREE.Mesh(new THREE.BoxGeometry(1.45,.07,.08),new THREE.MeshBasicMaterial({color:0x7be2f1,transparent:true,opacity:.9}));sternLight.position.set(0,.05,3.25);ship.add(sternLight);
    const hoverGlow=new THREE.PointLight(0x75dbff,2.1,13);hoverGlow.position.set(0,-.65,.35);ship.add(hoverGlow);
    const wake=new THREE.Mesh(new THREE.PlaneGeometry(3.2,15),new THREE.MeshBasicMaterial({color:0xb9efff,transparent:true,opacity:.23,side:THREE.DoubleSide,blending:THREE.AdditiveBlending}));wake.rotation.x=-Math.PI/2;wake.position.set(0,-.55,9.2);ship.add(wake);

    let target=0,progress=0,velocity=0,last=performance.now(),visible=true;
    const io=new IntersectionObserver(e=>{visible=e[0].isIntersecting;if(visible)requestAnimationFrame(loop)},{threshold:0});io.observe(section);
    function measure(){const r=section.getBoundingClientRect();target=Math.min(1,Math.max(0,-r.top/(section.offsetHeight-innerHeight)));}
    function resize(){const r=canvas.getBoundingClientRect();renderer.setSize(Math.max(1,r.width),Math.max(1,r.height),false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();}
    function ss(a,b,x){const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)}
    function path(p){const cityReveal=ss(.37,.5,p),cityP=ss(.58,.85,p),exit=ss(.91,1,p),islandAvoid=ss(.12,.24,p)*(1-ss(.38,.48,p)),cityAvoid=ss(.61,.71,p)*(1-ss(.84,.92,p)),route=-6.2*islandAvoid+6.6*cityAvoid,z=16-p*158;cityMaterials.forEach(m=>m.opacity=cityReveal);camera.position.set(route*.74+Math.sin(p*8)*.38*(1-exit),3.55+cityP*.75-exit*.3,z);camera.lookAt(route*.9,1.25+cityP*.25,z-18);ship.position.set(route,.72+Math.sin(p*28)*.045,z-13);ship.rotation.set(Math.sin(p*15)*.015,(-islandAvoid+cityAvoid)*.12,Math.sin(p*13)*-.03+islandAvoid*.08-cityAvoid*.08);ship.scale.setScalar(.84+cityP*.07-exit*.2);wake.material.opacity=.34+cityP*.1;}
    function loop(now){if(!visible)return;const motionOff=section.classList.contains('motion-off');const dt=Math.min(.04,(now-last)/1000);last=now;if(motionOff){progress=target;velocity=0}else{velocity+=(target-progress)*.038;velocity*=.8;progress=Math.min(1,Math.max(0,progress+velocity))}waterMat.uniforms.uTime.value=motionOff?0:now*.001;city.children.forEach((t,i)=>{t.position.y=motionOff?0:Math.sin(now*.00032+i)*.025});path(progress);renderer.render(scene,camera);requestAnimationFrame(loop);}
    addEventListener('scroll',measure,{passive:true});addEventListener('resize',resize);measure();resize();path(0);renderer.render(scene,camera);section.classList.add('webgl-ready');requestAnimationFrame(loop);
  }
  if(document.readyState==='complete')start();else addEventListener('load',start,{once:true});
})();
