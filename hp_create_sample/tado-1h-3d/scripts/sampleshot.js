const { chromium } = require(process.env.PWPATH);
(async () => {
  const file = process.argv[2], out = process.argv[3], views = process.argv[4].split(',');
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: parseInt(process.env.VW||'1280'), height: parseInt(process.env.VH||'720') } });
  await page.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => r.fulfill({ path: '/tmp/cdn/' + r.request().url().split('three@0.160.0/')[1], contentType: 'application/javascript' }));
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  await page.goto('file://' + file);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 300000 });
  if (process.env.NOCREDIT) await page.evaluate(() => { window.__nocredit = true; });
  await page.evaluate(() => {
    document.querySelectorAll('.panel').forEach(p => { if (p.id !== 'credit' || window.__nocredit) p.style.display = 'none'; });
    for (const id of ['tTees', 'tYards']) { const e = document.getElementById(id); e.checked = false; e.dispatchEvent(new Event('change')); }
  });
  for (const v of views) {
    const t0 = Date.now();
    await page.evaluate(v => {
      const d = window.__dbg, V = window.__views, F = JSON.parse(document.getElementById('data').textContent).feat;
      const T = d.THREE;
      if (v === 'tee') V.viewTee();
      else if (v === 'teeREG') { document.getElementById('teeSel').value='REG'; V.viewTee(); }
      else if (v === 'teeup') {   // above the tee complex looking down-hole
        const a = F.tees.REG, b = F.tees.LADIES; d.controls.enabled = true;
        d.camera.position.set(a.x - 45, 87 + 32, a.z - 30); d.controls.target.set(b.x + 10, 84, b.z + 5); d.controls.update();
      }
      else if (v.startsWith('cam')) {   // cam_<dist along centreline m>_<alt m>_<look-ahead m>_<lateral m>
        const [, dd, alt, ahead, lat] = v.split('_').map(Number);
        const cl = F.centerline; const seg = []; let tot = 0;
        for (let i = 1; i < cl.length; i++) { const l = Math.hypot(cl[i][0]-cl[i-1][0], cl[i][1]-cl[i-1][1]); seg.push([cl[i-1], cl[i], tot, l]); tot += l; }
        const at = (s) => { s = Math.max(0, Math.min(tot, s)); for (const [a, b, t0, l] of seg) if (s <= t0 + l) { const u = (s - t0) / l; return [a[0] + (b[0]-a[0])*u, a[1] + (b[1]-a[1])*u, (b[0]-a[0])/l, (b[1]-a[1])/l]; } const q = seg[seg.length-1]; return [q[1][0], q[1][1], 0, 1]; };
        const p = at(dd), q = at(dd + ahead);
        const px = p[0] - p[3]*lat, pz = p[1] + p[2]*lat;
        const hA = window.__hAt(px, pz), hB = window.__hAt(q[0], q[1]);
        d.camera.fov = 48; d.camera.updateProjectionMatrix(); d.controls.enabled = true;
        d.camera.position.set(px, hA + alt, pz); d.controls.target.set(q[0], hB + Math.max(0, alt*0.15), q[1]); d.controls.update();
      }
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
