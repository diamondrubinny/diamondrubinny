// Renders promo.html frame by frame (deterministic) and writes frames + sfx.json.
// Usage: node render.cjs <framesDir> <sfxJson> [fps]
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const [framesDir, sfxPath, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30);
  fs.mkdirSync(framesDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'promo.html'));
  await page.evaluate(() => document.fonts.ready);
  const duration = await page.evaluate(() => window.DURATION);
  fs.writeFileSync(sfxPath, JSON.stringify({ duration, sfx: await page.evaluate(() => window.SFX) }));
  const total = Math.round(duration * fps);
  for (let i = 0; i < total; i++) {
    await page.evaluate((t) => window.render(t), i / fps);
    await page.screenshot({ path: path.join(framesDir, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await browser.close();
  console.log('frames:', total);
})();
