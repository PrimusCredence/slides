# PrimusCredence — slide deck

Twenty slides drawn from `Solutions-Confidential.md`: *Provable Security
for Apps & AI Agents*.

- `slides/01.svg` … `slides/20.svg` — one SVG per slide, each self-contained
  (it loads its own webfonts), sized 16:10 (1187 × 742 units), the MacBook /
  widescreen aspect, so the deck fills a laptop display edge to edge. Body copy
  sits at 23–26 units. Every slide is white, with soft tinted blooms behind
  frosted-glass panels.
- `index.html` — the deck: arrow keys, click zones, swipe, `o` for the
  overview grid, `f` for fullscreen (slide only, no chrome), deep links
  (`#7`), and a print stylesheet that emits one 16:10 page per slide.
- `solutions-slides.pdf` — the deck as one 16:10 PDF, a slide per page, for
  sending to people who would rather have a file than a link. Text stays
  selectable and searchable.
- `make-pdf.js` — rebuilds that PDF (`node make-pdf.js [out.pdf]`). It inlines
  the SVGs so their webfonts load, and needs puppeteer, which it takes from
  this folder or from the sibling reports repo.
- `build.py` — regenerates every SVG. Content lives in `SOLUTIONS` and the
  per-slide functions; the palette and type scale sit at the top.

## Hosting

Upload the folder as-is; `index.html` references `slides/NN.svg` relatively,
so any static host works. Share the URL, or `…/index.html#13` to open on a
particular slide.

## Structure

| # | Slide |
|---|---|
| 1 | Title |
| 2 | Dr. Raghavendra Ramesh |
| 3 | Why Now: The Attacker Industrialised |
| 4 | Automated Reasoning |
| 5 | We Add a Layer to Your Stack |
| 6 | Six Solutions, Two Families |
| 7 | § Cybersecurity Solutions |
| 8–11 | Solutions 1–4 |
| 12 | § AI Security Solutions |
| 13–14 | Solutions 5–6 |
| 15 | Why Your Clients Will Ask |
| 16 | What a Provider Can Resell |
| 17 | One Result, Three Registers |
| 18 | Investment |
| 19 | Take Away |
| 20 | Thank You |

Slides 5 and 15–17 address a security solutions provider reading the deck as
a partner rather than as an end client.

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/20.svg
node make-pdf.js      # writes solutions-slides.pdf
```

The slides are drawn at 16:10 (1187 × 742 units), the MacBook / widescreen
aspect, and the PDF page box is 320 × 200 mm (also 16:10) so each slide fills
the page.

Text is wrapped against measured average glyph advances, and every block has
a line budget, so copy that grows past its budget is clipped rather than
allowed to overflow the page. If a line disappears, shorten the string in
`build.py` — do not raise the budget without re-checking the slide.
