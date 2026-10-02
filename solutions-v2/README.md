# PrimusCredence — slide deck (v2, three solutions)

A variant of the main deck (`../`) with the **AI guardrail solution dropped** —
it sells the **three cybersecurity solutions** only: access control
(application entitlement proofs), network-layer isolation (reachability &
segmentation proofs), and API protocols (app & API-usage conformance). The
"AI Industrialises the Attacker" slide is **kept**, because it argues *why* proof
is needed (attacks are now exhaustive), which still motivates the three
solutions. Post-quantum migration has been dropped as a solution, along with its
motivation slide.

20 slides, 16:10 (1187 × 742), same house style as the parent deck.

## What differs from `../`
- No "AI Agents Multiply…" motivation slide and no "Agentic Guardrail
  Verification" solution slide.
- Solutions overview is a row of three cards; "one method — three solutions".
- The regulatory grid and the "why clients ask" tiles drop the AI-governance
  rows (UAE AI Act, ISO 42001) in favour of cyber frameworks (PCI DSS 4.0, CIS
  Controls) and a third-party-risk shift.
- Product tagline is "Provable Security for Applications" (not "… for Apps & AI
  Agents").
- The anchor stack diagram (slide 3) is **retained**; its seam is now APIs,
  SDK/library usage and network paths (no PQC binding).

## Structure

| # | Slide |
|---|---|
| 1 | Title |
| 2 | Dr. Raghavendra Ramesh — founder bio |
| 3 | Where the Risk Actually Lives — the stack diagram (anchor) |
| 4 | OWASP 2025 — Access Control & Misconfiguration |
| 5 | Segmentation Is Asserted, Not Proven — network reachability & lateral movement |
| 6 | Apps Misuse the APIs They Run On |
| 7 | AI Industrialises the Attacker |
| 8 | Why Today's Security Stack Isn't Enough |
| 9 | Proof — Now Feasible |
| 10 | Automated Reasoning |
| 11 | Solutions (overview, three) |
| 12–14 | Solutions 1–3 |
| 15 | Our Approach — partner with cybersecurity solutions providers |
| 16 | Why the Provider's Clients Will Ask |
| 17 | What a Provider Can Resell |
| 18 | One Result, Three Registers |
| 19 | Take Away |
| 20 | Thank You |

This deck is pitched **to** cybersecurity solutions providers, so the long-term
"assurance hub" vision slide and the investment ask are omitted (they are only
in the parent deck's history, not here).

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/20.svg
node make-pdf.js      # writes solutions-slides.pdf (puppeteer from ../node_modules)
```
