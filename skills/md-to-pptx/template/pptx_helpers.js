// pptx_helpers.js — GYRO branded PptxGenJS helpers (16:9, A4).
// Factory pattern: pass in pres instance, get back {C, addFooter, addHeaderBar, ...}.
// Extracted from create_pptx_v21.js (錼創 V2.1) lines 1-108, plus cardsGrid extracted as reusable.

const C = {
  red: "BD442C", redDark: "A63B26", orange: "E8833A",
  white: "FFFFFF", black: "1A1A1A", darkText: "333333",
  gray: "888888", lightGray: "EEEEEE",
  tableHead: "BD442C", tableHeadText: "FFFFFF", tableAlt: "F9F9F9",
  infoBg: "F0F6FF", warnBg: "FFF8E7", footerLine: "CCCCCC",
};

function build(pres, meta = {}) {
  const company = meta.company || "GYRO SYSTEMS, INC.";
  const docLabel = meta.docLabel || "";

  function addFooter(slide) {
    slide.addShape(pres.shapes.LINE, { x: 0.3, y: 5.15, w: 9.4, h: 0, line: { color: C.footerLine, width: 0.5 } });
    slide.addText(company, { x: 0.3, y: 5.18, w: 3, h: 0.35, fontSize: 8, fontFace: "Arial", color: C.red, bold: true, margin: 0 });
    if (docLabel) slide.addText(docLabel, { x: 6.5, y: 5.18, w: 3.2, h: 0.35, fontSize: 8, fontFace: "Arial", color: C.gray, align: "right", margin: 0 });
  }

  function addHeaderBar(slide, sectionName) {
    slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.55, fill: { color: C.red } });
    slide.addText(sectionName || "", { x: 0.4, y: 0, w: 9, h: 0.55, fontSize: 14, fontFace: "Arial", color: C.white, bold: true, valign: "middle", margin: 0 });
  }

  function addSlideTitle(slide, num, title) {
    if (num !== "" && num !== null && num !== undefined) {
      slide.addShape(pres.shapes.OVAL, { x: 0.4, y: 0.75, w: 0.4, h: 0.4, fill: { color: C.orange } });
      slide.addText(String(num), { x: 0.4, y: 0.75, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: C.white, bold: true, align: "center", valign: "middle", margin: 0 });
      slide.addText(title, { x: 0.95, y: 0.72, w: 8.5, h: 0.5, fontSize: 20, fontFace: "Arial", color: C.darkText, bold: true, margin: 0 });
    } else {
      slide.addText(title, { x: 0.4, y: 0.72, w: 9, h: 0.5, fontSize: 20, fontFace: "Arial", color: C.darkText, bold: true, margin: 0 });
    }
    slide.addShape(pres.shapes.LINE, { x: 0.4, y: 1.2, w: 9.2, h: 0, line: { color: C.red, width: 1.5 } });
  }

  function contentSlide(section, num, title) {
    const s = pres.addSlide();
    s.background = { color: C.white };
    addHeaderBar(s, section);
    addSlideTitle(s, num, title);
    addFooter(s);
    return s;
  }

  function sectionSlide(title, subtitle) {
    const s = pres.addSlide();
    s.background = { color: C.red };
    s.addText(title, { x: 0, y: 1.8, w: 10, h: 1.2, fontSize: 40, fontFace: "Arial", color: C.white, bold: true, align: "center", valign: "middle" });
    if (subtitle) s.addText(subtitle, { x: 0, y: 3.0, w: 10, h: 0.5, fontSize: 14, fontFace: "Arial", color: "F5D0C5", align: "center" });
    return s;
  }

  function titleSlide({ org = "G Y R O  S Y S T E M S ,  I N C .", title, subtitle, confidential = "Confidential", date, tagline }) {
    const s = pres.addSlide();
    s.background = { color: C.white };
    s.addShape(pres.shapes.LINE, { x: 0, y: 5.55, w: 10, h: 0, line: { color: C.red, width: 3 } });
    s.addText(org, { x: 0, y: 2.0, w: 10, h: 0.4, fontSize: 14, fontFace: "Arial", color: C.red, bold: true, align: "center", charSpacing: 2 });
    s.addText(title || "", { x: 0, y: 2.5, w: 10, h: 0.9, fontSize: 36, fontFace: "Arial", color: C.darkText, bold: true, align: "center" });
    if (subtitle) s.addText(subtitle, { x: 0, y: 3.4, w: 10, h: 0.4, fontSize: 16, fontFace: "Arial", color: C.gray, align: "center" });
    if (confidential) s.addText(`${company} — ${confidential}`, { x: 0, y: 4.0, w: 10, h: 0.3, fontSize: 11, fontFace: "Arial", color: C.gray, align: "center" });
    if (date) s.addText(date, { x: 0, y: 4.3, w: 10, h: 0.3, fontSize: 11, fontFace: "Arial", color: C.gray, align: "center" });
    if (tagline) s.addText(tagline, { x: 1, y: 4.7, w: 8, h: 0.3, fontSize: 10, fontFace: "Arial", color: C.darkText, align: "center" });
    return s;
  }

  function makeTable(slide, headers, rows, opts = {}) {
    const x = opts.x ?? 0.4;
    const y = opts.y ?? 1.5;
    const w = opts.w ?? 9.2;
    const colW = opts.colW;
    const fs = opts.fontSize || 10;

    const headerRow = headers.map(h => ({
      text: h, options: { bold: true, color: C.tableHeadText, fill: { color: C.tableHead }, fontSize: fs, fontFace: "Arial", valign: "middle" }
    }));
    const dataRows = rows.map((row, i) =>
      row.map(cell => {
        const isStr = typeof cell === "string";
        const text = isStr ? cell : cell.text;
        const cellOpts = {
          fontSize: fs, fontFace: "Arial", color: C.darkText,
          fill: { color: i % 2 === 0 ? C.white : C.tableAlt }, valign: "middle",
        };
        if (!isStr && cell.color) cellOpts.color = cell.color;
        if (!isStr && cell.bold) cellOpts.bold = true;
        return { text, options: cellOpts };
      })
    );
    const tableOpts = { x, y, w, border: { pt: 0.5, color: C.lightGray }, margin: [3, 6, 3, 6] };
    if (colW) tableOpts.colW = colW;
    slide.addTable([headerRow, ...dataRows], tableOpts);
  }

  function addInfoBox(slide, text, opts = {}) {
    const x = opts.x ?? 0.4;
    const y = opts.y ?? 4.7;
    const w = opts.w ?? 9.2;
    const h = opts.h ?? 0.35;
    const bg = opts.bg || C.infoBg;
    const textColor = opts.textColor || (bg === C.warnBg ? "8B6914" : "1E40AF");
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: bg }, line: { color: bg === C.infoBg ? "BFD4F2" : "F5DEB3", width: 0.5 } });
    slide.addText(text, { x: x + 0.15, y, w: w - 0.3, h, fontSize: 9, fontFace: "Arial", color: textColor, valign: "middle", margin: 0 });
  }

  function cardsGrid(slide, items, opts = {}) {
    const x0 = opts.x ?? 0.4;
    const y0 = opts.y ?? 1.5;
    const cols = opts.cols || 3;
    const cardW = opts.cardW || 2.9;
    const cardH = opts.cardH || 1.35;
    const gapX = opts.gapX ?? 0.2;
    const gapY = opts.gapY ?? 0.2;
    const accentByRow = opts.accentByRow || [C.red, C.orange];
    items.forEach((c, i) => {
      const col = i % cols;
      const row = Math.floor(i / cols);
      const bx = x0 + col * (cardW + gapX);
      const by = y0 + row * (cardH + gapY);
      const accent = accentByRow[row % accentByRow.length];
      slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: cardW, h: cardH, fill: { color: C.white }, line: { color: C.lightGray, width: 1 } });
      slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: by, w: cardW, h: 0.04, fill: { color: accent } });
      slide.addText(c.title || "", { x: bx + 0.15, y: by + 0.12, w: cardW - 0.3, h: 0.3, fontSize: 11, fontFace: "Arial", color: C.darkText, bold: true, margin: 0 });
      slide.addText(c.desc || "", { x: bx + 0.15, y: by + 0.45, w: cardW - 0.3, h: cardH - 0.55, fontSize: 8, fontFace: "Arial", color: C.gray, margin: 0 });
    });
  }

  function bulletList(slide, items, opts = {}) {
    const x = opts.x ?? 0.4;
    const y = opts.y ?? 1.5;
    const w = opts.w ?? 9.2;
    const h = opts.h ?? 3.4;
    const fs = opts.fontSize || 11;
    const lines = items.map(it => ({
      text: typeof it === "string" ? it : (it.text || ""),
      options: { bullet: { code: "25A0" }, color: C.darkText, fontSize: fs, fontFace: "Arial", paraSpaceAfter: 6 }
    }));
    slide.addText(lines, { x, y, w, h, valign: "top", margin: 0 });
  }

  function flowChain(slide, blocks, opts = {}) {
    const x0 = opts.x ?? 0.4;
    const y0 = opts.y ?? 2.0;
    const totalW = opts.w ?? 9.2;
    const gap = opts.gap ?? 0.4;
    const blockH = opts.blockH ?? 0.7;
    const fs = opts.fontSize ?? 8;
    const n = blocks.length;
    const blockW = (totalW - gap * (n - 1)) / n;
    const arrows = opts.arrows || [];
    blocks.forEach((b, i) => {
      const bx = x0 + i * (blockW + gap);
      slide.addShape(pres.shapes.RECTANGLE, { x: bx, y: y0, w: blockW, h: blockH,
        fill: { color: b.color || "BFDBFE" }, line: { color: b.border || "3B82F6", width: 1 } });
      slide.addText(b.label, { x: bx, y: y0, w: blockW, h: blockH,
        fontSize: fs, fontFace: "Arial", color: C.darkText, align: "center", valign: "middle", margin: 0 });
      if (i < n - 1) {
        const ax = bx + blockW;
        slide.addText("→", { x: ax, y: y0, w: gap, h: blockH,
          fontSize: 14, fontFace: "Arial", color: C.gray, align: "center", valign: "middle", margin: 0 });
        if (arrows[i]) {
          slide.addText(arrows[i], { x: ax - 0.1, y: y0 + blockH + 0.02, w: gap + 0.2, h: 0.32,
            fontSize: 7, fontFace: "Arial", color: C.gray, align: "center", margin: 0 });
        }
      }
    });
  }

  function imageWithCaption(slide, imgPath, caption, opts = {}) {
    const x = opts.x ?? 1.5;
    const y = opts.y ?? 1.4;
    const w = opts.w ?? 7;
    const h = opts.h ?? 3.2;
    slide.addImage({ path: imgPath, x, y, w, h });
    if (caption) {
      slide.addText(caption, { x: 0.4, y: y + h + 0.1, w: 9.2, h: 0.3, fontSize: 9, fontFace: "Arial", color: C.gray, align: "center" });
    }
  }

  return { C, addFooter, addHeaderBar, addSlideTitle, contentSlide, sectionSlide, titleSlide, makeTable, addInfoBox, cardsGrid, bulletList, imageWithCaption, flowChain };
}

module.exports = { C, build };
