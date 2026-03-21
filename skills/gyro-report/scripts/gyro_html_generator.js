#!/usr/bin/env node
/**
 * GYRO Systems — HTML Slide Deck Generator
 * 
 * Generates a single-file HTML presentation matching GYRO brand identity.
 * Architecture inspired by Claude Code HTML slide output format.
 * 
 * Brand extracted from: GYRO投影片SAMPLE.pptx
 *   Primary: #BD442C (brick red)   Dark: #B93A21
 *   Accent1: #4472C4 (blue)        Accent2: #ED7D31 (orange)
 *   Accent3: #FFC000 (gold)        Text: #333333 / #404040
 *   Fonts: Microsoft YaHei UI / Calibri
 * 
 * Usage:
 *   node gyro_html_generator.js content.json output.html
 */

const fs = require('fs');
const path = require('path');

// ── GYRO Brand Tokens ────────────────────────────────────────────────
const BRAND = {
  primary:      '#BD442C',
  primaryLight: '#D4563E',
  primaryDark:  '#B93A21',
  accent1:      '#4472C4',
  accent2:      '#ED7D31',
  accent3:      '#FFC000',
  bg:           '#1a1a1a',
  card:         '#ffffff',
  text:         '#333333',
  textLight:    '#44546A',
  textBody:     '#404040',
  success:      '#198038',
  danger:       '#C00000',
  lightBg:      '#F8F8F8',
  white:        '#FFFFFF',
  link:         '#0070C0',
  company:      'GYRO SYSTEMS, INC.',
  tagline:      '機器人 / 工業物聯網 實踐者',
};

// ── CSS Template ─────────────────────────────────────────────────────
function generateCSS() {
  return `
:root {
  --primary: ${BRAND.primary};
  --primary-light: ${BRAND.primaryLight};
  --primary-dark: ${BRAND.primaryDark};
  --accent1: ${BRAND.accent1};
  --accent2: ${BRAND.accent2};
  --accent3: ${BRAND.accent3};
  --bg: ${BRAND.bg};
  --card: ${BRAND.card};
  --text: ${BRAND.text};
  --text-light: ${BRAND.textLight};
  --text-body: ${BRAND.textBody};
  --success: ${BRAND.success};
  --danger: ${BRAND.danger};
  --light-bg: ${BRAND.lightBg};
  --white: ${BRAND.white};
  --link: ${BRAND.link};
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: var(--bg); font-family: "Microsoft YaHei UI", "Segoe UI", "Noto Sans TC", "Calibri", Arial, sans-serif; }

/* ── Slide Container ── */
.deck { position: relative; width: 100vw; height: 100vh; }
.slide {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  opacity: 0; pointer-events: none;
  transition: opacity 0.45s ease;
  background: var(--white);
}
.slide.active { opacity: 1; pointer-events: auto; z-index: 2; }

/* ── Slide Inner ── */
.slide-inner {
  flex: 1; display: flex; flex-direction: column;
  max-width: 1200px; width: 100%; margin: 0 auto;
  padding: 48px 64px 32px;
  overflow-y: auto;
}
.slide-inner::-webkit-scrollbar { width: 4px; }
.slide-inner::-webkit-scrollbar-thumb { background: #ccc; border-radius: 2px; }

/* ── Header Bar (GYRO red band) ── */
.slide-header-bar {
  position: absolute; top: 0; left: 0; right: 0;
  height: 56px;
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 60%, var(--primary-light) 100%);
  display: flex; align-items: center;
  padding: 0 64px;
  z-index: 5;
}
.slide-header-bar .section-label {
  font-size: 22px; font-weight: 700; color: var(--white);
  letter-spacing: 1px;
}

/* ── Title Slide ── */
.slide.title-slide {
  background: var(--white);
  justify-content: center; align-items: center; text-align: center;
}
.slide.title-slide .slide-inner { justify-content: center; align-items: center; padding-top: 0; }
.title-company { font-size: 15px; letter-spacing: 5px; text-transform: uppercase; color: var(--primary); font-weight: 700; margin-bottom: 16px; }
.title-main { font-size: 44px; font-weight: 700; line-height: 1.3; margin-bottom: 12px; color: var(--text); }
.title-sub { font-size: 18px; color: var(--text-light); margin-bottom: 32px; }
.title-meta { font-size: 13px; color: var(--text-light); line-height: 1.8; }
.title-bar-bottom {
  position: absolute; bottom: 0; left: 0; right: 0; height: 8px;
  background: linear-gradient(90deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
}

/* ── Section Divider Slide ── */
.slide.section-slide {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
  color: var(--white); justify-content: center; align-items: center; text-align: center;
}
.slide.section-slide .slide-inner { justify-content: center; align-items: center; }
.section-main-title { font-size: 44px; font-weight: 700; line-height: 1.3; margin-bottom: 12px; }
.section-subtitle { font-size: 18px; opacity: 0.85; }

/* ── Content Slide ── */
.slide-header {
  display: flex; align-items: center; gap: 16px;
  padding-bottom: 14px; margin-bottom: 20px;
  border-bottom: 3px solid var(--primary);
}
.slide-header .num {
  background: var(--primary); color: var(--white);
  font-size: 14px; font-weight: 700;
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.slide-header h2 { font-size: 24px; font-weight: 700; color: var(--text); }
.slide-header h3 { font-size: 13px; color: var(--text-light); margin-left: auto; }

/* ── Tables ── */
table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 10px 0; }
thead th { background: var(--primary); color: var(--white); padding: 8px 12px; text-align: left; font-weight: 600; white-space: nowrap; }
thead th:first-child { border-radius: 4px 0 0 0; }
thead th:last-child { border-radius: 0 4px 0 0; }
tbody td { padding: 7px 12px; border-bottom: 1px solid #e8eaed; }
tbody tr:nth-child(even) { background: var(--light-bg); }
tbody tr:hover { background: #f0f4f8; }
.small-table { font-size: 12px; }
.small-table td, .small-table th { padding: 5px 10px; }

/* ── Cards / Grid ── */
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 12px 0; }
.card {
  background: var(--light-bg); border: 1px solid #dde1e6; border-radius: 8px; padding: 18px 20px;
  border-left: 4px solid var(--primary);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.card.accent1 { border-left-color: var(--accent1); }
.card.accent2 { border-left-color: var(--accent2); }
.card.accent3 { border-left-color: var(--accent3); }
.card.success { border-left-color: var(--success); }
.card.danger  { border-left-color: var(--danger); }
.card .label { font-size: 11px; color: var(--text-light); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.card .value { font-size: 22px; font-weight: 700; color: var(--primary); }
.card .desc  { font-size: 12px; color: var(--text-light); margin-top: 4px; }

/* ── Feature Cards (grid with top accent) ── */
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; margin: 14px 0; }
.feature-card {
  background: var(--light-bg); border: 1px solid #e0e3e7; border-radius: 8px;
  padding: 20px; border-top: 4px solid var(--primary);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.feature-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(189,68,44,0.10); }
.feature-card h4 { font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 6px; }
.feature-card p  { font-size: 12px; color: var(--text-light); line-height: 1.5; }

/* ── Stats Cards ── */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px; margin: 18px 0; }
.stat-card {
  background: var(--light-bg); border: 1px solid #e0e3e7; border-radius: 8px;
  padding: 24px 20px; text-align: center;
  border-top: 4px solid var(--primary);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(189,68,44,0.10); }
.stat-card .stat-value { font-size: 36px; font-weight: 800; color: var(--primary); line-height: 1.2; }
.stat-card .stat-label { font-size: 13px; font-weight: 600; color: var(--text); margin-top: 6px; }
.stat-card .stat-desc  { font-size: 11px; color: var(--text-light); margin-top: 4px; }

/* ── Callout ── */
.callout { background: #fef4f2; border-left: 4px solid var(--primary); border-radius: 0 6px 6px 0; padding: 12px 16px; margin: 10px 0; font-size: 13px; color: var(--text-body); }
.callout.info  { background: #e8f4fd; border-left-color: var(--accent1); }
.callout.warn  { background: #fef7e0; border-left-color: var(--accent2); }
.callout.ok    { background: #e6f4ea; border-left-color: var(--success); }

/* ── Two-col ── */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.two-col.ratio-6-4 { grid-template-columns: 3fr 2fr; }
.two-col.ratio-4-6 { grid-template-columns: 2fr 3fr; }
.col-divider { position: relative; }
.col-divider::before {
  content: ''; position: absolute; left: -16px; top: 0; bottom: 0;
  width: 2px; background: linear-gradient(180deg, var(--primary) 0%, rgba(189,68,44,0.1) 100%);
}

/* ── Footer ── */
.slide-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 64px; font-size: 11px; color: #999;
  border-top: 1px solid #eee; flex-shrink: 0;
}
.slide-footer .brand { font-weight: 700; color: var(--primary); font-size: 12px; }

/* ── Closing Slide ── */
.slide.closing-slide {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
  color: var(--white); justify-content: center; align-items: center; text-align: center;
}
.slide.closing-slide .slide-inner { justify-content: center; align-items: center; }
.closing-title { font-size: 52px; font-weight: 800; margin-bottom: 16px; letter-spacing: 2px; }
.closing-sub   { font-size: 18px; opacity: 0.85; margin-bottom: 8px; }
.closing-company { font-size: 14px; opacity: 0.6; letter-spacing: 3px; text-transform: uppercase; margin-top: 24px; }

/* ── Nav ── */
.nav {
  position: fixed; bottom: 20px; right: 24px; z-index: 100;
  display: flex; gap: 8px; align-items: center;
}
.nav button {
  width: 40px; height: 40px; border-radius: 50%;
  border: none; background: rgba(189,68,44,0.85); color: var(--white);
  font-size: 18px; cursor: pointer; transition: background 0.2s;
  display: flex; align-items: center; justify-content: center;
}
.nav button:hover { background: var(--primary-dark); }
.nav .counter { color: var(--white); font-size: 13px; background: rgba(0,0,0,0.5); padding: 4px 12px; border-radius: 12px; }

/* ── Progress Bar ── */
.progress { position: fixed; top: 0; left: 0; height: 3px; background: var(--primary); z-index: 100; transition: width 0.35s ease; }

/* ── Images ── */
.slide-image { margin: 12px 0; text-align: center; }
.slide-image img { max-width: 100%; max-height: 420px; object-fit: contain; border: 1px solid #e0e3e7; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.slide-image.compact img { max-height: 280px; }
.slide-image.large img { max-height: 520px; }
.image-caption { font-size: 11px; color: var(--text-light); margin-top: 6px; text-align: center; }
.image-slide-layout { display: flex; gap: 24px; align-items: flex-start; flex: 1; min-height: 0; }
.image-slide-layout .image-side { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; min-width: 0; }
.image-slide-layout .image-side img { max-width: 100%; max-height: 380px; object-fit: contain; border: 1px solid #e0e3e7; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.image-slide-layout .text-side { flex: 1; min-width: 0; }

/* ── Misc ── */
h4 { font-size: 14px; font-weight: 600; color: var(--primary); margin: 14px 0 8px; }
ul { margin: 6px 0 10px 20px; font-size: 13px; color: var(--text-body); }
li { margin: 4px 0; line-height: 1.6; }
li::marker { color: var(--primary); }
strong { color: var(--primary); }
pre.diagram { font-size: 11px; line-height: 1.4; background: var(--light-bg); border: 1px solid #e0e3e7; border-radius: 6px; padding: 12px 16px; overflow-x: auto; font-family: "Consolas", "Courier New", monospace; color: var(--text-body); margin: 8px 0; white-space: pre; }
.mermaid-wrap { margin: 12px 0; display: flex; justify-content: center; }
.mermaid-wrap .mermaid { width: 100%; }
.mermaid-wrap .mermaid svg { max-width: 100%; max-height: 420px; }

/* ── Print ── */
@media print {
  .nav, .progress { display: none !important; }
  .slide { position: relative !important; opacity: 1 !important; pointer-events: auto !important;
    page-break-after: always; min-height: 100vh; }
  .deck { overflow: visible; height: auto; }
  body { background: #fff; overflow: visible; }
}

/* ── CONFIDENTIAL Watermark ── */
.slide::after {
  content: "GYRO SYSTEMS";
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(-35deg);
  font-size: 64px; font-weight: 900;
  color: rgba(189, 68, 44, 0.04);
  letter-spacing: 10px;
  pointer-events: none; user-select: none;
  z-index: 1; white-space: nowrap;
}
  `;
}

// ── JS Template ──────────────────────────────────────────────────────
function generateJS() {
  return `
(function() {
  const slides = document.querySelectorAll('.slide');
  const total  = slides.length;
  let cur = 0;

  function go(n) {
    if (n < 0 || n >= total) return;
    slides[cur].classList.remove('active');
    cur = n;
    slides[cur].classList.add('active');
    document.getElementById('counter').textContent = (cur + 1) + ' / ' + total;
    document.getElementById('progress').style.width = ((cur + 1) / total * 100) + '%';
  }

  document.getElementById('prev').onclick = function() { go(cur - 1); };
  document.getElementById('next').onclick = function() { go(cur + 1); };

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); go(cur + 1); }
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                    { e.preventDefault(); go(cur - 1); }
    if (e.key === 'Home') { e.preventDefault(); go(0); }
    if (e.key === 'End')  { e.preventDefault(); go(total - 1); }
  });

  // Touch swipe
  let startX = 0;
  document.addEventListener('touchstart', function(e) { startX = e.changedTouches[0].screenX; });
  document.addEventListener('touchend', function(e) {
    const dx = e.changedTouches[0].screenX - startX;
    if (dx < -50) go(cur + 1);
    if (dx >  50) go(cur - 1);
  });

  go(0);
})();
  `;
}

// ── Image Helper ────────────────────────────────────────────────────
let imageBasePath = '';

function resolveImagePath(imgPath) {
  if (!imgPath) return null;
  if (path.isAbsolute(imgPath)) return imgPath;
  return path.resolve(imageBasePath, imgPath);
}

function embedImage(imgPath) {
  const resolved = resolveImagePath(imgPath);
  if (!resolved) return null;
  try {
    const buf = fs.readFileSync(resolved);
    const ext = path.extname(resolved).toLowerCase();
    const mime = ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' : ext === '.png' ? 'image/png' : ext === '.gif' ? 'image/gif' : ext === '.svg' ? 'image/svg+xml' : 'image/png';
    return `data:${mime};base64,${buf.toString('base64')}`;
  } catch (e) {
    console.warn(`⚠ Image not found: ${resolved}`);
    return null;
  }
}

function renderImageHTML(imgPath, caption, cssClass) {
  const dataUri = embedImage(imgPath);
  if (!dataUri) return '';
  const cls = cssClass ? ` ${cssClass}` : '';
  let html = `<div class="slide-image${cls}"><img src="${dataUri}" alt="${esc(caption || '')}">`;
  if (caption) html += `<div class="image-caption">${esc(caption)}</div>`;
  html += '</div>';
  return html;
}

// ── Slide Renderers ──────────────────────────────────────────────────
function esc(s) {
  if (typeof s !== 'string') return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

let slideCounter = 0;

function renderCoverSlide(s) {
  return `
<!-- ===== COVER ===== -->
<div class="slide title-slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-inner">
    <div class="title-company">${esc(s.company || BRAND.company)}</div>
    <div class="title-main">${esc(s.title)}</div>
    <div class="title-sub">${esc(s.subtitle || '')}</div>
    <div class="title-meta">${esc(s.date || '')}</div>
  </div>
  <div class="title-bar-bottom"></div>
</div>`;
}

function renderSectionSlide(s) {
  return `
<!-- ===== SECTION ===== -->
<div class="slide section-slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-inner">
    <div class="section-main-title">${esc(s.title)}</div>
    <div class="section-subtitle">${esc(s.subtitle || '')}</div>
  </div>
</div>`;
}

function renderContentSlide(s, num, title) {
  const sectionLabel = s.section || '';
  let body = '';

  // Mermaid diagram
  if (s.mermaid) {
    body += `<div class="mermaid-wrap"><div class="mermaid">\n${s.mermaid}\n</div></div>`;
  }

  // Diagram (preformatted text)
  if (s.diagram) {
    body += `<pre class="diagram">${esc(s.diagram)}</pre>`;
  }

  // Image
  if (s.imagePath) {
    body += renderImageHTML(s.imagePath, s.imageCaption, s.imageClass || '');
  }

  // Bullets
  if (s.bullets && s.bullets.length) {
    body += '<ul>';
    for (const b of s.bullets) body += `<li>${esc(b)}</li>`;
    body += '</ul>';
  }

  // Text
  if (s.text) {
    body += `<p style="font-size:13px;color:var(--text-body);line-height:1.7;">${esc(s.text)}</p>`;
  }

  // Callout
  if (s.callout) {
    const cls = s.calloutType ? ` ${s.calloutType}` : '';
    body += `<div class="callout${cls}">${esc(s.callout)}</div>`;
  }

  return `
<!-- ===== CONTENT ===== -->
<div class="slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-header-bar"><span class="section-label">${esc(sectionLabel)}</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">${num}</div>
      <h2>${esc(s.title)}</h2>
    </div>
    ${body}
  </div>
  <div class="slide-footer"><span class="brand">${esc(BRAND.company)}</span><span>${esc(title)}</span></div>
</div>`;
}

function renderImageContentSlide(s, num, title) {
  const sectionLabel = s.section || '';
  let textBody = '';

  if (s.bullets && s.bullets.length) {
    textBody += '<ul>';
    for (const b of s.bullets) textBody += `<li>${esc(b)}</li>`;
    textBody += '</ul>';
  }
  if (s.text) {
    textBody += `<p style="font-size:13px;color:var(--text-body);line-height:1.7;">${esc(s.text)}</p>`;
  }
  if (s.callout) {
    const cls = s.calloutType ? ` ${s.calloutType}` : '';
    textBody += `<div class="callout${cls}">${esc(s.callout)}</div>`;
  }

  const imgDataUri = embedImage(s.imagePath);
  const imgHtml = imgDataUri ? `<img src="${imgDataUri}" alt="${esc(s.imageCaption || '')}">` : '';
  const capHtml = s.imageCaption ? `<div class="image-caption">${esc(s.imageCaption)}</div>` : '';

  return `
<!-- ===== IMAGE-CONTENT ===== -->
<div class="slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-header-bar"><span class="section-label">${esc(sectionLabel)}</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">${num}</div>
      <h2>${esc(s.title)}</h2>
    </div>
    <div class="image-slide-layout">
      <div class="image-side">${imgHtml}${capHtml}</div>
      <div class="text-side">${textBody}</div>
    </div>
  </div>
  <div class="slide-footer"><span class="brand">${esc(BRAND.company)}</span><span>${esc(title)}</span></div>
</div>`;
}

function renderTwoColumnSlide(s, num, title) {
  const sectionLabel = s.section || '';

  function renderCol(col) {
    let h = '';
    if (col.heading) h += `<h4>${esc(col.heading)}</h4>`;
    if (col.bullets && col.bullets.length) {
      h += '<ul>';
      for (const b of col.bullets) h += `<li>${esc(b)}</li>`;
      h += '</ul>';
    }
    if (col.text) h += `<p style="font-size:13px;color:var(--text-body);line-height:1.7;">${esc(col.text)}</p>`;
    return h;
  }

  return `
<!-- ===== TWO-COLUMN ===== -->
<div class="slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-header-bar"><span class="section-label">${esc(sectionLabel)}</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">${num}</div>
      <h2>${esc(s.title)}</h2>
    </div>
    <div class="two-col">
      <div>${renderCol(s.left || {})}</div>
      <div class="col-divider">${renderCol(s.right || {})}</div>
    </div>
  </div>
  <div class="slide-footer"><span class="brand">${esc(BRAND.company)}</span><span>${esc(title)}</span></div>
</div>`;
}

function renderFeatureGridSlide(s, num, title) {
  const sectionLabel = s.section || '';
  let cards = '';
  const features = s.features || [];
  for (const f of features) {
    cards += `<div class="feature-card"><h4>${esc(f.title)}</h4><p>${esc(f.desc)}</p></div>`;
  }

  return `
<!-- ===== FEATURE GRID ===== -->
<div class="slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-header-bar"><span class="section-label">${esc(sectionLabel)}</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">${num}</div>
      <h2>${esc(s.title)}</h2>
    </div>
    <div class="feature-grid">${cards}</div>
  </div>
  <div class="slide-footer"><span class="brand">${esc(BRAND.company)}</span><span>${esc(title)}</span></div>
</div>`;
}

function renderStatsSlide(s, num, title) {
  const sectionLabel = s.section || '';
  let cards = '';
  const stats = s.stats || [];
  for (const st of stats) {
    cards += `
    <div class="stat-card">
      <div class="stat-value">${esc(st.value)}</div>
      <div class="stat-label">${esc(st.label)}</div>
      <div class="stat-desc">${esc(st.desc || '')}</div>
    </div>`;
  }

  return `
<!-- ===== STATS ===== -->
<div class="slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-header-bar"><span class="section-label">${esc(sectionLabel)}</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">${num}</div>
      <h2>${esc(s.title)}</h2>
    </div>
    <div class="stats-grid">${cards}</div>
  </div>
  <div class="slide-footer"><span class="brand">${esc(BRAND.company)}</span><span>${esc(title)}</span></div>
</div>`;
}

function renderTableSlide(s, num, title) {
  const sectionLabel = s.section || '';
  const rows = s.table || [];

  let thead = '', tbody = '';
  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i];
    if (i === 0) {
      thead = '<thead><tr>' + cells.map(c => `<th>${esc(c)}</th>`).join('') + '</tr></thead>';
    } else {
      tbody += '<tr>' + cells.map(c => `<td>${esc(c)}</td>`).join('') + '</tr>';
    }
  }

  let extra = '';
  if (s.imagePath) extra += renderImageHTML(s.imagePath, s.imageCaption, s.imageClass || 'compact');
  if (s.callout) {
    const cls = s.calloutType ? ` ${s.calloutType}` : '';
    extra += `<div class="callout${cls}">${esc(s.callout)}</div>`;
  }

  return `
<!-- ===== TABLE ===== -->
<div class="slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-header-bar"><span class="section-label">${esc(sectionLabel)}</span></div>
  <div class="slide-inner" style="padding-top: 72px;">
    <div class="slide-header">
      <div class="num">${num}</div>
      <h2>${esc(s.title)}</h2>
    </div>
    <table>${thead}<tbody>${tbody}</tbody></table>
    ${extra}
  </div>
  <div class="slide-footer"><span class="brand">${esc(BRAND.company)}</span><span>${esc(title)}</span></div>
</div>`;
}

function renderClosingSlide(s) {
  return `
<!-- ===== CLOSING ===== -->
<div class="slide closing-slide${slideCounter === 0 ? ' active' : ''}">
  <div class="slide-inner">
    <div class="closing-title">${esc(s.title || 'Thank You')}</div>
    <div class="closing-sub">${esc(s.subtitle || BRAND.tagline)}</div>
    <div class="closing-company">${esc(s.company || BRAND.company)}</div>
  </div>
</div>`;
}

// ── Main Generator ───────────────────────────────────────────────────
function generate(content) {
  const meta = content.meta || {};
  const slides = content.slides || [];
  const deckTitle = meta.title || 'GYRO Systems Presentation';

  let slidesHTML = '';
  let contentNum = 0;

  for (const s of slides) {
    slideCounter++;
    switch (s.type) {
      case 'cover':
        slidesHTML += renderCoverSlide(s);
        break;
      case 'section':
        slidesHTML += renderSectionSlide(s);
        break;
      case 'content':
        contentNum++;
        slidesHTML += renderContentSlide(s, contentNum, deckTitle);
        break;
      case 'two-column':
        contentNum++;
        slidesHTML += renderTwoColumnSlide(s, contentNum, deckTitle);
        break;
      case 'feature-grid':
        contentNum++;
        slidesHTML += renderFeatureGridSlide(s, contentNum, deckTitle);
        break;
      case 'stats':
        contentNum++;
        slidesHTML += renderStatsSlide(s, contentNum, deckTitle);
        break;
      case 'table':
        contentNum++;
        slidesHTML += renderTableSlide(s, contentNum, deckTitle);
        break;
      case 'image-content':
        contentNum++;
        slidesHTML += renderImageContentSlide(s, contentNum, deckTitle);
        break;
      case 'closing':
        slidesHTML += renderClosingSlide(s);
        break;
      default:
        // Treat unknown types as content
        contentNum++;
        slidesHTML += renderContentSlide(s, contentNum, deckTitle);
    }
  }

  return `<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(deckTitle)}</title>
<style>${generateCSS()}</style>
</head>
<body>

<div class="progress" id="progress"></div>

<div class="deck" id="deck">
${slidesHTML}
</div>

<div class="nav">
  <button id="prev">&#9664;</button>
  <span class="counter" id="counter">1 / ${slides.length}</span>
  <button id="next">&#9654;</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#fef4f2',
    primaryBorderColor: '#BD442C',
    primaryTextColor: '#333333',
    lineColor: '#BD442C',
    secondaryColor: '#e8f4fd',
    tertiaryColor: '#F8F8F8',
    fontFamily: '"Microsoft YaHei UI","Segoe UI","Noto Sans TC",Calibri,Arial,sans-serif',
    fontSize: '13px'
  },
  flowchart: { curve: 'basis', padding: 12 },
  sequence: { mirrorActors: false }
});
async function renderMermaids() {
  const els = document.querySelectorAll('.mermaid');
  for (let i = 0; i < els.length; i++) {
    const el = els[i];
    const id = 'mermaid-' + i;
    try {
      const { svg } = await mermaid.render(id, el.textContent.trim());
      el.innerHTML = svg;
    } catch(e) { console.warn('Mermaid render error:', e); }
  }
}
renderMermaids();
</script>
<script>${generateJS()}</script>
</body>
</html>`;
}

// ── CLI Entry Point ──────────────────────────────────────────────────
function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('Usage: node gyro_html_generator.js <content.json> <output.html>');
    process.exit(1);
  }

  const contentPath = args[0];
  const outputPath  = args[1];

  const content = JSON.parse(fs.readFileSync(contentPath, 'utf-8'));
  imageBasePath = path.dirname(path.resolve(contentPath));
  const html = generate(content);
  fs.writeFileSync(outputPath, html, 'utf-8');
  console.log(`✅ Generated: ${outputPath} (${slides_count(content)} slides)`);
}

function slides_count(c) { return (c.slides || []).length; }

main();
