// Renders the MSIX tile/logo PNGs from an inline SVG with the preinstalled Playwright. Run: node make-assets.cjs
const { chromium } = require('playwright');
const path = require('node:path');
const svg = (s) => `<svg xmlns="http://www.w3.org/2000/svg" width="${s}" height="${s}" viewBox="0 0 128 128">
<rect width="128" height="128" rx="24" fill="#1d4ed8"/>
<text x="64" y="58" font-family="Arial" font-weight="700" font-size="44" text-anchor="middle" fill="#fff">A</text>
<text x="64" y="106" font-family="Arial" font-weight="700" font-size="44" text-anchor="middle" fill="#fde68a">א</text>
<path d="M98 36 L110 48 L98 60" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const files = { 'StoreLogo.png': 50, 'Square44x44Logo.png': 44, 'Square150x150Logo.png': 150, 'Square44x44Logo.scale-200.png': 88, 'Square150x150Logo.scale-200.png': 300 };
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [name, s] of Object.entries(files)) {
    await p.setViewportSize({ width: s, height: s });
    await p.setContent(`<body style="margin:0;background:transparent">${svg(s)}</body>`);
    await p.screenshot({ path: path.join(__dirname, 'Assets', name), omitBackground: true });
  }
  await b.close();
})();
