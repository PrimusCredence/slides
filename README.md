# PrimusCredence — slide deck

Twenty-four slides drawn from `Solutions-Confidential.md`, `HelpAG/appsec.md`
and `reports/fv-pqc.md`: *Provable Security for Apps & AI Agents*.

- `slides/01.svg` … `slides/24.svg` — one SVG per slide, each self-contained
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
| 3 | OWASP 2025 — Access Control & Misconfiguration (+ incidents) |
| 4 | Apps Misuse the APIs They Run On (exploits + cost) |
| 5 | The Base Went Post-Quantum. Are the Apps Ready? |
| 6 | AI Industrialises the Attacker |
| 7 | Why Today's Security Stack Isn't Enough |
| 8 | Proof — Now Feasible |
| 9 | Automated Reasoning |
| 10 | Solutions (overview) |
| 11 | Solution 1 — Application Access-Policy & Entitlement Verification |
| 12 | Solution 2 — App-to-Cloud Escalation-Path Proofs |
| 13–14 | Solutions 3–4 |
| 15 | AI Agents Are Multiplying Faster Than the Rules |
| 16 | Solution 5 — Agentic AI Guardrail Verification |
| 17 | The Long-Term Vision — the Assurance Hub |
| 18 | Short Term — We Sit Behind the Providers (clientele) |
| 19 | Why the Provider's Clients Will Ask |
| 20 | What a Provider Can Resell |
| 21 | One Result, Three Registers |
| 22 | Investment |
| 23 | Take Away |
| 24 | Thank You |

Slides 3–8 are the motivation arc (access control & misconfiguration, apps &
APIs, post-quantum, AI, the stack's gap, and why proof is now feasible).
Slides 17–21 set out the business model — the long-term assurance-hub vision,
the short-term channel through established providers (with the GCC clientele
they reach), and what one result is worth to a partner reselling it.

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/24.svg
node make-pdf.js      # writes solutions-slides.pdf
```

The slides are drawn at 16:10 (1187 × 742 units), the MacBook / widescreen
aspect, and the PDF page box is 320 × 200 mm (also 16:10) so each slide fills
the page.

Text is wrapped against measured average glyph advances, and every block has
a line budget, so copy that grows past its budget is clipped rather than
allowed to overflow the page. If a line disappears, shorten the string in
`build.py` — do not raise the budget without re-checking the slide.
