const { chromium } = require(process.env.PWPATH);
(async () => {
  const file = process.argv[2], out = process.argv[3], views = process.argv[4].split(',');
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => r.fulfill({ path: '/tmp/cdn/' + r.request().url().split('three@0.160.0/')[1], contentType: 'application/javascript' }));
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  await page.goto('file://' + file);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 300000 });
  await page.evaluate(() => {
    document.querySelectorAll('.panel').forEach(p => { if (p.id !== 'credit') p.style.display = 'none'; });
    for (const id of ['tTees', 'tYards']) { const e = document.getElementById(id); e.checked = false; e.dispatchEvent(new Event('change')); }
  });
  for (const v of views) {
    const t0 = Date.now();
    await page.evaluate(v => {
      const d = window.__dbg, V = window.__views, F = JSON.parse(document.getElementById('data').textContent).feat;
      const T = d.THREE;
      if (v === 'tee') V.viewTee();
      else if (v === 'back') V.viewBack();
      else if (v === 'top') V.viewTop();
      else if (v === 'aerial') {   // drone-style: behind & above the tee, looking down the hole
        const a = F.tees.FULL, b = F.pin; const dx = b.x - a.x, dz = b.z - a.z, l = Math.hypot(dx, dz);
        const ux = dx / l, uz = dz / l;
        d.controls.enabled = true;
        d.camera.position.set(a.x - ux * 60, 88 + 55, a.z - uz * 60);
        d.controls.target.set(a.x + ux * 260, 80, a.z + uz * 260); d.controls.update();
      } else if (v === 'green') {  // approach to the green, like the official 3rd-shot photo
        const a = F.centerline[F.centerline.length - 3], b = F.pin;
        d.camera.position.set(a[0], 83 + 9, a[1]); d.controls.target.set(b.x, 82, b.z); d.controls.update();
      }
    }, v);
    await page.waitForTimeout(parseInt(process.env.WAIT || '30000'));
    await page.screenshot({ path: `${out}_${v}.png`, timeout: 900000 });
    console.log('shot', v, (Date.now() - t0) + 'ms');
  }
  await browser.close();
})();
