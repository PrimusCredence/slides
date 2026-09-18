# PrimusCredence — slide deck

Nineteen slides drawn from `Solutions-Confidential.md`: *Provable Security
Solutions to Cloud, AI and Crypto*.

- `slides/01.svg` … `slides/19.svg` — one SVG per slide, each self-contained
  (it loads its own webfonts), sized A5 landscape (210 × 148.5 mm at 5 units
  per mm). Nothing on a slide is smaller than ~11 pt in print. Every slide is
  white, with soft tinted blooms behind frosted-glass panels.
- `index.html` — the deck: arrow keys, click zones, swipe, `o` for the
  overview grid, `f` for fullscreen (slide only, no chrome), deep links
  (`#7`), and a print stylesheet that emits one A5 landscape page per slide.
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
| 2 | About — Dr. Raghavendra Ramesh |
| 3 | Why Now: The Attacker Industrialised |
| 4 | Automated Reasoning |
| 5 | Nine Solutions, Three Families |
| 6 | § Cybersecurity Solutions |
| 7–11 | Solutions 1–5 |
| 12 | § AI Security Solutions |
| 13–14 | Solutions 6–7 |
| 15 | § Crypto Security Solutions |
| 16–17 | Solutions 8–9 |
| 18 | Take Away |
| 19 | Thank You |

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/19.svg
```

Text is wrapped against measured average glyph advances, and every block has
a line budget, so copy that grows past its budget is clipped rather than
allowed to overflow the page. If a line disappears, shorten the string in
`build.py` — do not raise the budget without re-checking the slide.
