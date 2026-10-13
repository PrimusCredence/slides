# PrimusCredence — slide deck (v2, three solutions)

A variant of the main deck (`../`) with the **AI guardrail solution dropped** —
it sells the **three Services** only: access control
(application entitlement proofs), network-layer isolation (reachability &
segmentation proofs), and data residency (residency proofs, since 11 Oct 2026). The
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
- The anchor stack diagram (slide 3) is **retained**; its seam is APIs, network
  paths and data paths, numbered by the Service that proves each.

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
"assurance hub" vision slide and the investment ask are omitted (they are only
in the parent deck's history, not here).

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/20.svg
# PDF: render each slide to its own PDF page with headless Chrome, then
# pdfunite them into solutions-slides.pdf (a single make-pdf.js call times out
# on the heavier slides)
```
