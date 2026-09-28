const { chromium } = require(process.env.PWPATH || 'playwright');
(async () => {
  const file = process.argv[2], outPrefix = process.argv[3] || '/tmp/shot', views = (process.argv[4] || 'tee,top,back').split(',');
  const q = process.argv[5] || 'std';
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 760 } });
  await page.route('https://cdn.jsdelivr.net/npm/three@0.160.0/**', r => {
    const p = r.request().url().split('three@0.160.0/')[1];
    r.fulfill({ path: '/tmp/cdn/' + p, contentType: 'application/javascript', headers: { 'access-control-allow-origin': '*' } });
  });
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('[console]', m.type(), m.text().slice(0, 300)); });
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  await page.goto('file://' + file);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 180000 });
  if (q !== 'std') await page.evaluate(q => { document.getElementById('quality').value = q; window.__views.setQuality(q); }, q);
  for (const v of views) {
    const t0 = Date.now();
    await page.evaluate(v => {
      const m = { tee: 'viewTee', top: 'viewTop', back: 'viewBack' };
      if (v.startsWith('fly')) { window.__views.viewFly(); } else window.__views[m[v]]();
    }, v);
    await page.waitForTimeout(v.startsWith('fly') ? parseInt(v.slice(3) || '7000') : parseInt(process.env.WAIT||'4000'));
    await page.screenshot({ path: `${outPrefix}_${v}.png`, timeout: 900000 });
    const fps = await page.evaluate(() => document.getElementById('fps').textContent);
    console.log('shot', v, fps, (Date.now() - t0) + 'ms');
  }
  await browser.close();
})();
