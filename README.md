# PrimusCredence — slide deck

Twenty-three slides drawn from `Solutions-Confidential.md`, `HelpAG/appsec.md`
and `reports/fv-pqc.md`: *Provable Security for Apps & AI Agents*.

- `slides/01.svg` … `slides/23.svg` — one SVG per slide, each self-contained
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
| 2 | Dr. Raghavendra Ramesh — founder bio (up front) |
| 3 | Where the Risk Actually Lives — the layered stack diagram (the anchor) |
| 4 | OWASP 2025 — Access Control & Misconfiguration (+ incidents) |
| 5 | Apps Misuse the APIs They Run On (exploits + cost) |
| 6 | The Base Went Post-Quantum. Are the Apps Ready? |
| 7 | AI Industrialises the Attacker |
| 8 | Why Today's Security Stack Isn't Enough |
| 9 | Proof — Now Feasible |
| 10 | Automated Reasoning |
| 11 | Solutions (overview) |
| 12 | Solution 1 — Application Access-Policy & Entitlement Verification |
| 13 | Solution 2 — App-to-Cloud Escalation-Path Proofs |
| 14–15 | Solutions 3–4 |
| 16 | AI Agents Are Multiplying Faster Than the Rules |
| 17 | Solution 5 — Agentic AI Guardrail Verification |
| 18 | We Sit Behind the Providers (clientele) |
| 19 | Why the Provider's Clients Will Ask |
| 20 | What a Provider Can Resell |
| 21 | One Result, Three Registers |
| 22 | Take Away |
| 23 | Thank You |

Slide 3 is the anchor diagram — plugins on top of the app, the app on a proven
cloud base, and the API / library / PQC seam between them — the mental model the
rest of the talk returns to. Slides 4–9 are the motivation arc (access control &
misconfiguration, apps & APIs, post-quantum, AI, the stack's gap, and why proof
is now feasible). Slides 18–21 set out the channel model for a cybersecurity
solutions provider — how this sits behind them, why their clients will ask, what
they can resell, and what one result is worth. (This deck is pitched to the
providers, so the long-term "assurance hub" vision and the investment ask are
deliberately omitted.)

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/23.svg
node make-pdf.js      # writes solutions-slides.pdf
```

The slides are drawn at 16:10 (1187 × 742 units), the MacBook / widescreen
aspect, and the PDF page box is 320 × 200 mm (also 16:10) so each slide fills
the page.

Text is wrapped against measured average glyph advances, and every block has
a line budget, so copy that grows past its budget is clipped rather than
allowed to overflow the page. If a line disappears, shorten the string in
`build.py` — do not raise the budget without re-checking the slide.
