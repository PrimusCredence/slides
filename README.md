# PrimusCredence — slide deck

Twenty-three slides drawn from `Solutions-Confidential.md`: *Provable Security
Solutions to Cloud, AI and Crypto*.

- `slides/01.svg` … `slides/23.svg` — one SVG per slide, each self-contained
  (it loads its own webfonts), sized A5 landscape (210 × 148.5 mm at 5 units
  per mm). Nothing on a slide is smaller than ~11 pt in print. Every slide is
  white, with soft tinted blooms behind frosted-glass panels.
- `index.html` — the deck: arrow keys, click zones, swipe, `o` for the
  overview grid, `f` for fullscreen (slide only, no chrome), deep links
  (`#7`), and a print stylesheet that emits one A4 landscape page per slide.
- `solutions-slides.pdf` — the deck as one A4-landscape PDF, a slide
  per page, for printing and for sending to people who would rather have a
  file than a link. Text stays selectable and searchable.
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
| 6 | Nine Solutions, Three Families |
| 7 | § Cybersecurity Solutions |
| 8–12 | Solutions 1–5 |
| 13 | § AI Security Solutions |
| 14–15 | Solutions 6–7 |
| 16 | § Crypto Security Solutions |
| 17–18 | Solutions 8–9 |
| 19 | Why Your Clients Will Ask |
| 20 | What a Provider Can Resell |
| 21 | One Result, Three Registers |
| 22 | Take Away |
| 23 | Thank You |

Slides 5 and 19–21 address a security solutions provider reading the deck as
a partner rather than as an end client.

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/23.svg
node make-pdf.js      # writes solutions-slides.pdf
```

The slides are drawn at A5 landscape and scale up to A4 without cropping:
1050 × 742 is 1.4151:1, A4 landscape is 1.4143:1. Printed at A4 the body copy
lands near 20 pt, so the deck doubles as a leave-behind.

Text is wrapped against measured average glyph advances, and every block has
a line budget, so copy that grows past its budget is clipped rather than
allowed to overflow the page. If a line disappears, shorten the string in
`build.py` — do not raise the budget without re-checking the slide.
