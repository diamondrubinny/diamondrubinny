// Captures the real extension at work (Chromium with the built extension loaded) into docs/screenshots/.
// Usage: npm run build && node scripts/screenshots.cjs      (needs Playwright; 1366x768 images)
const { chromium } = require('playwright');
const http = require('node:http');
const path = require('node:path');
const os = require('node:os');
const fs = require('node:fs');

const root = path.resolve(__dirname, '..');
const outDir = path.resolve(root, '../docs/screenshots');
const font = fs.readFileSync(path.resolve(root, '../marketing/assets/Heebo.ttf'));

const PAGE = (caption, dir) => `<!doctype html><meta charset=utf-8><title>Chat</title>
<style>
@font-face{font-family:Heebo;src:url(/Heebo.ttf);font-weight:100 900}
*{box-sizing:border-box;margin:0}
body{font-family:Heebo,sans-serif;background:#eef2f7;color:#0f172a;height:100vh;display:flex;flex-direction:column}
#cap{background:linear-gradient(90deg,#1d4ed8,#7c3aed);color:#fff;font-weight:800;font-size:34px;padding:22px 36px;letter-spacing:.2px}
#cap small{display:block;font-weight:500;font-size:20px;opacity:.9;margin-top:4px}
#app{flex:1;display:flex;flex-direction:column;max-width:980px;width:100%;margin:28px auto;background:#fff;border-radius:22px;box-shadow:0 20px 60px rgba(15,23,42,.18);overflow:hidden}
#top{padding:18px 26px;border-bottom:1px solid #e2e8f0;font-weight:700;font-size:22px}
#msgs{flex:1;padding:24px 26px;display:flex;flex-direction:column;gap:14px}
.m{max-width:62%;padding:12px 18px;border-radius:18px;font-size:22px}
.in{background:#e2e8f0;align-self:flex-start;direction:ltr}.out{background:#2563eb;color:#fff;align-self:flex-end}
#box{padding:18px 26px;border-top:1px solid #e2e8f0;background:#f8fafc}
textarea{width:100%;font:inherit;font-size:34px;font-weight:700;border:2px solid #94a3b8;border-radius:16px;padding:14px 20px;height:100px;resize:none;direction:${dir}}
textarea:focus{outline:3px solid #2563eb;border-color:#2563eb}
</style>
<div id=cap>${caption[0]}<small>${caption[1]}</small></div>
<div id=app><div id=top>Dana</div>
<div id=msgs><div class="m in">Hi! Are you coming tonight?</div><div class="m out">${dir === 'rtl' ? 'כן, אני מגיע' : 'Yes, I am on my way'}</div></div>
<div id=box><textarea id=t autofocus></textarea></div></div>`;

let current = PAGE(['', ''], 'rtl');
const server = http.createServer((req, res) => {
  if (req.url === '/Heebo.ttf') { res.setHeader('content-type', 'font/ttf'); return res.end(font); }
  res.setHeader('content-type', 'text/html'); res.end(current);
});

(async () => {
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}/`;
  const ext = path.resolve(root, 'dist');
  const ctx = await chromium.launchPersistentContext(fs.mkdtempSync(path.join(os.tmpdir(), 'kfshot-')), {
    headless: false, viewport: { width: 1366, height: 768 },
    args: ['--headless=new', `--disable-extensions-except=${ext}`, `--load-extension=${ext}`],
  });
  const worker = ctx.serviceWorkers()[0] ?? (await ctx.waitForEvent('serviceworker'));
  const extId = new URL(worker.url()).host;
  const page = await ctx.newPage();
  const type = async (text) => { await page.click('#t'); await page.keyboard.type(text, { delay: 55 }); await page.waitForTimeout(700); };
  const shot = (name) => page.screenshot({ path: path.join(outDir, name) });

  // 1) wrong layout, correction switched off for this host
  await worker.evaluate(() => chrome.storage.local.set({ disabledHosts: ['127.0.0.1'] }));
  current = PAGE(['1. You typed with the wrong keyboard layout', 'A Hebrew sentence typed on an English keyboard'], 'rtl');
  await page.goto(base); await page.waitForTimeout(600);
  await type('akuo nv akunl tck kt zv ');
  await shot('01-wrong-layout.png');

  // 2) the same typing with KeyFlip on
  await worker.evaluate(() => chrome.storage.local.set({ disabledHosts: [] }));
  current = PAGE(['2. KeyFlip fixes it automatically', 'Corrected at the end of each word, Ctrl+Z undoes it'], 'rtl');
  await page.goto(base); await page.click('#t'); await page.waitForTimeout(2500);
  await type('akuo nv akunl tck kt zv ');
  await shot('02-fixed-automatically.png');

  // 3) the other direction
  current = PAGE(['3. It works both ways', 'English typed on a Hebrew keyboard becomes English'], 'ltr');
  await page.goto(base); await page.click('#t'); await page.waitForTimeout(1500);
  await type('יקךךם אישמלד ');
  await shot('03-english-from-hebrew-layout.png');

  // 4) options page
  const opt = await ctx.newPage();
  await opt.setViewportSize({ width: 1366, height: 768 });
  await opt.goto(`chrome-extension://${extId}/options.html`); await opt.waitForTimeout(500);
  await opt.screenshot({ path: path.join(outDir, '05-settings.png') });

  // 5) popup, framed on a 1366x768 canvas
  const pop = await ctx.newPage();
  await pop.setViewportSize({ width: 340, height: 330 });
  // The popup normally sits above a web page; opened as a tab it would report "unsupported site", so show an ordinary site.
  await pop.addInitScript(() => { chrome.tabs.query = async () => [{ url: 'https://docs.example.com/page' }]; });
  await pop.goto(`chrome-extension://${extId}/popup.html`); await pop.waitForTimeout(500);
  const popPng = (await pop.screenshot()).toString('base64');
  const frame = await ctx.newPage();
  await frame.setViewportSize({ width: 1366, height: 768 });
  await frame.setContent(`<body style="margin:0;height:768px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:sans-serif;color:#fff">
    <div style="font-size:40px;font-weight:800;margin-bottom:28px">4. Switch it off per site, any time</div>
    <img src="data:image/png;base64,${popPng}" style="border-radius:16px;box-shadow:0 24px 70px rgba(0,0,0,.45);transform:scale(1.5);margin:70px 0"></body>`);
  await frame.screenshot({ path: path.join(outDir, '04-popup.png') });

  await ctx.close(); server.close();
  console.log('screenshots written to', outDir);
})();
