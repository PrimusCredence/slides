# PrimusCredence — slide deck (v2, four solutions)

A variant of the main deck (`../`) with the **AI guardrail solution dropped** —
it sells the **four cybersecurity solutions** only: application entitlement
proofs, app-to-cloud escalation, app & API-usage conformance, and post-quantum
migration. The "AI Industrialises the Attacker" slide is **kept**, because it
argues *why* proof is needed (attacks are now exhaustive), which still motivates
the four solutions.

23 slides, 16:10 (1187 × 742), same house style as the parent deck.

## What differs from `../`
- No "AI Agents Multiply…" motivation slide and no "Agentic Guardrail
  Verification" solution slide.
- Solutions overview is a 2×2 of four cards; "one method — four solutions".
- The regulatory grid and the "why clients ask" tiles drop the AI-governance
  rows (UAE AI Act, ISO 42001) in favour of cyber frameworks (PCI DSS 4.0, CIS
  Controls) and a third-party-risk shift.
- Product tagline is "Provable Security for Applications" (not "… for Apps & AI
  Agents").
- The anchor stack diagram (slide 3) is **retained** unchanged.

## Structure

| # | Slide |
|---|---|
| 1 | Title |
| 2 | Dr. Raghavendra Ramesh — founder bio |
| 3 | Where the Risk Actually Lives — the stack diagram (anchor) |
| 4 | OWASP 2025 — Access Control & Misconfiguration |
| 5 | Apps Misuse the APIs They Run On |
| 6 | The Base Went Post-Quantum. Are the Apps Ready? |
| 7 | AI Industrialises the Attacker |
| 8 | Why Today's Security Stack Isn't Enough |
| 9 | Proof — Now Feasible |
| 10 | Automated Reasoning |
| 11 | Solutions (overview, four) |
| 12–15 | Solutions 1–4 |
| 16 | We Sit Behind the Providers |
| 17 | Why the Provider's Clients Will Ask |
| 18 | What a Provider Can Resell |
| 19 | One Result, Three Registers |
| 20 | Take Away |
| 21 | Thank You |

This deck is pitched **to** cybersecurity solutions providers, so the long-term
"assurance hub" vision slide and the investment ask are omitted (they are only
in the parent deck's history, not here).

## Rebuilding

```sh
python3 build.py      # writes slides/01.svg … slides/21.svg
node make-pdf.js      # writes solutions-slides.pdf (puppeteer from ../node_modules)
```
