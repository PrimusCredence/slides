# PrimusCredence — slide deck (three Services)

The current deck and the **source of truth for all copy**. It sells the
**three Services** only: access control (application entitlement proofs),
network-layer isolation (reachability & segmentation proofs), and data
residency (residency proofs). The brochure (`../brochures`) carries its copy,
and the website's `web/solutions/` is a copy of this folder's output
(`slides/`, `index.html`, `solutions-slides.pdf`) — re-sync it after each change.

20 slides, 16:10 (1187 × 742). Product tagline: "Provable Security for
Applications".

## Structure

| # | Slide |
|---|---|
| 1 | Title |
| 2 | Dr. Raghavendra Ramesh — founder bio |
| 3 | Where the Risk Actually Lives — the stack diagram (anchor) |
| 4 | OWASP 2025 — Access Control & Misconfiguration |
| 5 | Segmentation Is Asserted, Not Proven — network reachability & lateral movement |
| 6 | Residency Is Reviewed, Not Proven |
| 7 | AI Industrialises the Attacker |
| 8 | What Today's Security Stack Leaves Open |
| 9 | Proof — Now Feasible |
| 10 | Automated Reasoning |
| 11 | Services (overview, three) |
| 12–14 | Services 1–3 — each with an "In the demo" card of verdicts |
| 15 | Our Approach — partner with cybersecurity solutions providers |
| 16 | Why the Provider's Clients Will Ask |
| 17 | What a Provider Can Resell |
| 18 | One Result, Three Registers |
| 19 | Take Away |
| 20 | Thank You |

This deck is pitched **to** cybersecurity solutions providers, so the long-term
"assurance hub" vision slide and the investment ask are omitted (they live only in git history).

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/20.svg
# PDF: render each slide to its own PDF page with headless Chrome, then
# pdfunite them into solutions-slides.pdf (a single make-pdf.js call times out
# on the heavier slides)
```
