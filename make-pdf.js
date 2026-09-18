#!/usr/bin/env node
/**
 * Renders the deck to a single A4-landscape PDF, one slide per page.
 *
 *   node make-pdf.js  [output.pdf]
 *
 * The slides are drawn at A5 landscape (1050 x 742 units, 1.4151:1). A4
 * landscape is 1.4143:1, so each slide fills the page with a hairline of
 * white at the foot rather than being cropped or stretched.
 *
 * The SVGs are inlined rather than linked, so their webfonts load before the
 * PDF is written. Puppeteer is taken from this folder if present, otherwise
 * from the sibling reports repo, which already has it.
 */

const fs = require('fs');
const path = require('path');

function loadPuppeteer() {
  for (const p of ['puppeteer',
                   path.resolve(__dirname, '../reports/node_modules/puppeteer')]) {
    try { return require(p); } catch (e) { /* try the next one */ }
  }
  console.error('puppeteer not found — run `npm i puppeteer` in this folder.');
  process.exit(1);
}

const SLIDES = path.join(__dirname, 'slides');
const OUT = path.resolve(process.argv[2] || path.join(__dirname, 'PrimusCredence-Deck-A4.pdf'));

function slideFiles() {
  return fs.readdirSync(SLIDES)
    .filter(f => /^\d{2}\.svg$/.test(f))
    .sort();
}

function inline(file) {
  // fill the page box; the viewBox keeps the artwork proportional
  return fs.readFileSync(path.join(SLIDES, file), 'utf8')
    .replace(/<svg([^>]*?)width="\d+"\s+height="\d+"/,
             '<svg$1width="100%" height="100%" preserveAspectRatio="xMidYMid meet"');
}

(async () => {
  const files = slideFiles();
  if (!files.length) {
    console.error('no slides found in ' + SLIDES);
    process.exit(1);
  }

  const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400;1,8..60,600&display=swap">
<style>
  @page { size: A4 landscape; margin: 0; }
  *{ margin:0; padding:0; }
  html,body{ background:#fff; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  /* a hair under the page box: an element exactly 210mm tall rounds up and
     spills a blank page after every slide */
  .page{
    width:297mm; height:209.4mm; overflow:hidden; background:#fff;
    display:flex; align-items:center; justify-content:center;
    break-after:page; page-break-after:always;
  }
  .page:last-child{ break-after:auto; page-break-after:auto; }
  .page svg{ display:block; }
</style></head><body>
${files.map(f => `<div class="page">${inline(f)}</div>`).join('\n')}
</body></html>`;

  const puppeteer = loadPuppeteer();
  // the blurred blooms and layered shadows make each page expensive to
  // rasterise, so both the protocol and the print call get a long leash
  const browser = await puppeteer.launch({ protocolTimeout: 600000 });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 1200));   // let the last webfont settle
  await page.pdf({
    path: OUT,
    format: 'A4',
    landscape: true,
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    timeout: 600000,
  });
  await browser.close();

  const kb = (fs.statSync(OUT).size / 1024).toFixed(0);
  console.log(`wrote ${OUT} — ${files.length} pages, ${kb} KB`);
})();
