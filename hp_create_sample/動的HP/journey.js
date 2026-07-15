(function(){
  const section=document.querySelector('.journey');
  if(!section)return;
  const q=s=>section.querySelector(s);
  const cloudsBack=q('.journey-clouds-back'),cloudsFront=q('.journey-clouds-front');
  const depthLeft=q('.journey-depth-left'),depthRight=q('.journey-depth-right'),city=q('.journey-city-gate');
  const sun=q('.journey-sun'),lane=q('.journey-lane'),mist=q('.journey-mist');
  const cityLeft=q('.future-city-left'),cityRight=q('.future-city-right'),skyway=q('.future-skyway'),streaks=q('.flight-streaks');
  const futureHero=q('.future-hero');
  const aboutScene=q('.corporate-about-scene'),businessScene=q('.corporate-business-scene');
  const motionToggle=q('.motion-toggle'),vignette=q('.motion-vignette');
  const ship=q('.journey-ship-position'),shipFloat=q('.journey-ship-float'),wake=q('.journey-wake'),foreground=q('.journey-foreground');
  const copy=[...section.querySelectorAll('[data-start]')],endmark=q('.journey-endmark'),bar=q('.journey-progress span');
  let target=0,current=0,velocity=0,ticking=false,active=true,motionEnabled=!matchMedia('(prefers-reduced-motion: reduce)').matches,clock=0;
  const clamp=n=>Math.min(1,Math.max(0,n));
  const smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a));return t*t*(3-2*t)};
  function measure(){const r=section.getBoundingClientRect();target=clamp(-r.top/(section.offsetHeight-innerHeight));active=r.top<=0&&r.bottom>=innerHeight;document.body.classList.toggle('journey-active',active)}
  function visible(p,a,b){return smooth(a,a+.045,p)*(1-smooth(b-.045,b,p))}
  function render(){
    clock+=.016;
    if(motionEnabled){velocity+=(target-current)*.045;velocity*=.79;current=clamp(current+velocity)}else{current=target;velocity=0}
    const depart=smooth(0,.17,current),channel=smooth(.16,.34,current),urban=smooth(.48,.72,current),read=smooth(.66,.84,current),open=smooth(.88,1,current);
    const ambient=motionEnabled?clock:0,speed=Math.min(1,Math.abs(velocity)*28),islandAvoid=smooth(.14,.25,current)*(1-smooth(.38,.48,current)),cityAvoid=smooth(.62,.7,current)*(1-smooth(.82,.9,current)),route=-islandAvoid*115+cityAvoid*125,sway=Math.sin(current*18)*8*(1-open)+Math.sin(ambient*.7)*4;
    cloudsBack.style.transform=`translate3d(${-current*190+ambient*-2}px,${Math.sin(ambient*.38)*8}px,0) scale(${1+current*.13})`;
    cloudsFront.style.transform=`translate3d(${current*250+ambient*3.5}px,${Math.cos(ambient*.45)*11}px,0) scale(${1+current*.28})`;
    depthLeft.style.transform=`translate3d(${-channel*95}px,${channel*8}px,${channel*150}px) scale(${1+channel*.38})`;
    depthRight.style.transform=`translate3d(${channel*105}px,${channel*5}px,${channel*170}px) scale(${1+channel*.42})`;
    depthLeft.style.opacity=1-urban;depthRight.style.opacity=1-urban;
    city.style.opacity=urban*(1-read);city.style.transform=`translateX(-50%) scale(${.18+urban*1.48}) translateY(${urban*35}px)`;
    const cityOpacity=smooth(.46,.57,current)*(1-smooth(.9,.98,current));
    cityLeft.style.opacity=cityOpacity;cityRight.style.opacity=cityOpacity;
    cityLeft.style.transform=`translate3d(${-read*220-open*600}px,${urban*16}px,${urban*230}px) rotateY(${8+urban*5}deg) scale(${.62+urban*.58})`;
    cityRight.style.transform=`translate3d(${read*235+open*620}px,${urban*9}px,${urban*250}px) rotateY(${-8-urban*5}deg) scale(${.62+urban*.62})`;
    skyway.style.opacity=cityOpacity*(1-read*.35);skyway.style.transform=`translateX(-50%) perspective(500px) rotateX(58deg) scale(${.3+urban*1.05}) translateY(${read*80}px)`;
    streaks.style.opacity=0;
    vignette.style.opacity=speed*.72;vignette.style.transform=`scale(${1+speed*.06})`;
    const heroOut=smooth(.12,.28,current);futureHero.style.opacity=1-heroOut;futureHero.style.transform=`translate3d(${heroOut*-35}px,${-50-heroOut*4}%,0)`;
    const aboutIn=smooth(.22,.29,current),aboutOut=smooth(.40,.47,current),aboutOp=aboutIn*(1-aboutOut);
    aboutScene.style.opacity=aboutOp;aboutScene.style.transform=`translate3d(0,${-50+(1-aboutOp)*5}%,0) scale(${.94+aboutOp*.06})`;aboutScene.classList.toggle('is-visible',aboutOp>.7);
    const businessIn=smooth(.69,.75,current),businessOut=smooth(.84,.91,current),businessOp=businessIn*(1-businessOut);
    businessScene.style.opacity=businessOp;businessScene.style.transform=`translate3d(0,${-50+(1-businessOp)*5}%,0) scale(${.94+businessOp*.06})`;businessScene.classList.toggle('is-visible',businessOp>.7);
    [[aboutScene,aboutOp],[businessScene,businessOp]].forEach(([card,op])=>{[...card.querySelectorAll('.journey-kicker,h2,p,a,li')].forEach((el,i)=>{const r=clamp((op-i*.055)*1.8);el.style.opacity=r;el.style.transform=`translate3d(0,${(1-r)*18}px,0)`})});
    sun.style.transform=`translate(-50%,-50%) scale(${1+open*.32})`;sun.style.opacity=.72+open*.28;
    lane.style.transform=`translateX(-50%) scaleX(${.72+depart*.45})`;lane.style.opacity=.35+depart*.65;
    mist.style.transform=`translate3d(${Math.sin(current*13)*35}px,${channel*12}px,0) scale(${1+channel*.18})`;mist.style.opacity=.58-open*.38;
    foreground.style.transform=`translate3d(${sway*-1.6}px,${Math.sin(current*32)*5}px,0) scale(${1+depart*.12})`;
    const shipScale=1-depart*.08+urban*.15-open*.32;
    ship.style.transform=`translate3d(${route+sway}px,${Math.sin(current*18)*3-open*5}px,0) translate(-50%,-50%) scale(${shipScale})`;
    shipFloat.style.transform=`rotate(${Math.sin(current*15)*1.3}deg)`;
    wake.style.transform=`scaleY(${.32+depart*.95}) scaleX(${.55+depart*.45})`;wake.style.opacity=.35+depart*.65;
    copy.forEach(el=>{const op=visible(current,+el.dataset.start,+el.dataset.end);el.style.opacity=op;el.style.transform=`translate3d(${(1-op)*44}px,${-45+(1-op)*3}%,0)`});
    const end=smooth(.94,.985,current);endmark.style.opacity=end;endmark.style.transform=`scale(${.96+end*.04})`;bar.style.height=`${current*100}%`;
    if(active&&(motionEnabled||Math.abs(target-current)>.0002||Math.abs(velocity)>.0001))requestAnimationFrame(render);else ticking=false;
  }
  function update(){measure();if(!ticking){ticking=true;requestAnimationFrame(render)}}
  motionToggle.setAttribute('aria-pressed',String(motionEnabled));section.classList.toggle('motion-off',!motionEnabled);
  motionToggle.addEventListener('click',()=>{motionEnabled=!motionEnabled;motionToggle.setAttribute('aria-pressed',String(motionEnabled));section.classList.toggle('motion-off',!motionEnabled);update()});
  addEventListener('scroll',update,{passive:true});addEventListener('resize',update);update();
})();
