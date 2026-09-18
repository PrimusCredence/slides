#!/usr/bin/env python3
"""Builds the PrimusCredence slide deck.

One .svg per slide in slides/, stitched together by index.html.

Geometry is A5 landscape (210 x 148.5 mm) at 5 units per mm, so one unit is
0.2 mm and a 24-unit font prints at ~13.6 pt. Nothing in the deck is smaller
than 20 units (~11.3 pt) and body copy sits at 24-26.

Text is wrapped against measured average glyph advances (see W_SANS etc.),
and every block has a stated line budget, so the layout does not overflow.
"""

import os

W, H = 1050, 742
M = 68                      # page margin
CW = W - 2 * M              # content width (914)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slides")

# --- PrimusCredence Gold palette (carried from the report and the card) ------
INK      = "#14181f"
INK2     = "#4a5260"
MUTED    = "#767e8c"
PAPER    = "#faf8f3"
PANEL    = "#f2efe6"
LINE     = "#ddd7c9"
GOLD     = "#c8940a"
GOLDINK  = "#a87c00"
WHITE    = "#ffffff"
GREEN    = "#2f7d4f"
AMBER    = "#b06a00"

FAM = {
    "cyb":  dict(c="#1d5fa8", tint="#e9eff9", name="Cybersecurity Solutions"),
    "ai":   dict(c="#0f766e", tint="#e3f1ef", name="AI Security Solutions"),
    "cry":  dict(c="#b81f63", tint="#fbe8f0", name="Crypto Security Solutions"),
    "gold": dict(c=GOLDINK, tint=PANEL, name=""),
}

SERIF = "'Source Serif 4','Iowan Old Style',Georgia,serif"
SANS  = "'IBM Plex Sans','Helvetica Neue',Arial,sans-serif"
MONO  = "'IBM Plex Mono','SF Mono',Menlo,monospace"

# average advance per character, as a fraction of font size (measured off
# rendered output, with a little headroom)
W_SANS, W_SERIF, W_MONO = 0.48, 0.46, 0.605

FONTS = ("@import url('https://fonts.googleapis.com/css2?"
         "family=IBM+Plex+Mono:wght@400;500&amp;"
         "family=IBM+Plex+Sans:wght@300;400;500;600&amp;"
         "family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;"
         "1,8..60,400;1,8..60,600&amp;display=swap');")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, width, size, adv=W_SANS):
    maxchars = max(6, int(width / (size * adv)))
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if len(trial) <= maxchars or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(text, width, size, adv=W_SANS, minsize=18, ls=0.0):
    """Largest size <= `size` at which `text` stays on one line."""
    s = size
    while s > minsize and len(text) * (s * adv + ls) > width:
        s -= 1
    return s


def t(x, y, s, size=26, fill=INK, family=SANS, weight="400", anchor="start",
      style="normal", ls=None, opacity=None):
    a = [f'x="{x:.0f}"', f'y="{y:.0f}"', f'font-family="{family}"',
         f'font-size="{size}"', f'font-weight="{weight}"', f'fill="{fill}"']
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if style != "normal":
        a.append(f'font-style="{style}"')
    if ls:
        a.append(f'letter-spacing="{ls}"')
    if opacity:
        a.append(f'opacity="{opacity}"')
    return f'<text {" ".join(a)}>{esc(s)}</text>'


def block(x, y, text, width, size=26, lead=33, fill=INK2, maxlines=None,
          family=SANS, adv=W_SANS, style="normal", weight="400"):
    lines = wrap(text, width, size, adv)
    if maxlines:
        lines = lines[:maxlines]
    return ("".join(t(x, y + i * lead, ln, size, fill, family, weight,
                      style=style) for i, ln in enumerate(lines)),
            y + len(lines) * lead)


def eyebrow(x, y, s, fill=GOLDINK, size=21, ls=3.2, maxw=None, anchor="start"):
    s = s.upper()
    if maxw:
        size = fit(s, maxw, size, W_MONO, 14, ls)
    return t(x, y, s, size, fill, MONO, "500", anchor=anchor, ls=str(ls))


def bullets(x, y, items, width, size=24, lead=30, gap=14, fill=INK2,
            dot=GOLDINK, maxlines=2):
    out, cy = [], y
    for it in items:
        lines = wrap(it, width - 28, size, W_SANS)[:maxlines]
        out.append(f'<circle cx="{x+5}" cy="{cy-8}" r="3.6" fill="{dot}"/>')
        for i, ln in enumerate(lines):
            out.append(t(x + 26, cy + i * lead, ln, size, fill))
        cy += len(lines) * lead + gap
    return "".join(out), cy


def rrect(x, y, w, h, fill, r=12, stroke=None, sw=1):
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
         f'rx="{r}" fill="{fill}"')
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + "/>"


def hline(x, y, w, color=LINE, sw=1):
    return (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+w:.0f}" y2="{y:.0f}" '
            f'stroke="{color}" stroke-width="{sw}"/>')


SYMBOLS = [("∀", 120, 210, 190, .07), ("∃", 880, 150, 150, .06),
           ("⊨", 250, 600, 170, .05), ("∧", 640, 250, 130, .05),
           ("◇", 930, 560, 150, .06), ("⊤", 470, 690, 120, .04),
           ("¬", 40, 470, 120, .04), ("⟹", 700, 660, 130, .04)]


def symbol_field(color=GOLD):
    return "".join(
        f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
        f'fill="{color}" opacity="{op}">{ch}</text>'
        for ch, x, y, size, op in SYMBOLS)


def chrome(num, centre="", fam="gold", dark=False, left="PrimusCredence"):
    f = FAM[fam]
    ink = "#8d97a6" if dark else MUTED
    out = [f'<rect x="0" y="0" width="{W}" height="6" fill="{GOLD}"/>']
    if fam != "gold":
        out.append(f'<rect x="0" y="0" width="{W*0.42:.0f}" height="6" fill="{f["c"]}"/>')
    out.append(hline(M, 706, CW, "#2a3140" if dark else LINE))
    if left:
        out.append(t(M, 730, left, fit(left, 640, 20, W_MONO, 16, 1.4), ink, MONO,
                     "400", ls="1.4"))
    if centre:
        size = fit(centre, 600, 20, W_MONO, 16, 1.4)
        out.append(t(W / 2, 730, centre, size, GOLD if dark else ink, MONO, "400",
                     anchor="middle", ls="1.4"))
    out.append(t(W - M, 730, f"{num:02d}", 20, ink, MONO, "500", anchor="end", ls="1.4"))
    return "".join(out)


def page(body, bg=PAPER):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img">'
            f'<style>{FONTS}</style>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def heading(title, kicker="", fam="gold", right=""):
    f = FAM[fam]
    out = []
    if kicker:
        out.append(eyebrow(M, 84, kicker, f["c"], maxw=560))
    if right:
        out.append(eyebrow(W - M, 84, right, MUTED, 20, 2.2, maxw=600, anchor="end"))
    out.append(t(M, 132, title, fit(title, CW, 46, W_SERIF, 32), INK, SERIF, "600"))
    out.append(hline(M, 154, 110, f["c"], 3))
    return "".join(out)


# ============================================================ 1 · title
def s01():
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', symbol_field(GOLD),
         f'<rect x="0" y="0" width="{W}" height="6" fill="{GOLD}"/>']
    b.append(t(M, 208, "PrimusCredence", 84, WHITE, SERIF, "600"))
    b.append(hline(M, 250, 300, GOLD, 3))
    b.append(t(M, 330, "Provable Security Solutions", 46, GOLD, SERIF, "600"))
    b.append(t(M, 384, "to Cloud, AI & Crypto", 46, GOLD, SERIF, "600"))
    b.append(t(M, 448, "Mathematical rigour to security — proof alongside testing.",
               26, "#b8c0cc", SANS, "300", style="italic"))

    b.append(hline(M, 528, CW, "#2a3140"))
    b.append(t(M, 578, "Dr. Raghavendra Ramesh", 33, WHITE, SERIF, "600"))
    b.append(t(M, 612, "PhD, IISc Bangalore", 24, "#98a2b1", SANS))
    b.append(t(M, 644, "Founder & CEO", 24, "#98a2b1", SANS))
    b.append(t(W - M, 578, "primuscredence.com", 27, GOLD, MONO, "500", anchor="end"))
    b.append(t(W - M, 612, "raghavendra@primuscredence.com", 24, "#98a2b1", MONO, anchor="end"))
    b.append(t(W - M, 644, "Dubai, UAE", 24, "#98a2b1", MONO, anchor="end"))
    return page("".join(b), INK)


# ============================================================ 2 · about
def s02():
    b = [heading("Dr. Raghavendra Ramesh", "About")]
    b.append(t(M, 196, "Founder & CEO, PrimusCredence  ·  VP of R&D, Supra  ·  Dubai",
               26, GOLDINK, SANS, "500"))

    b.append(eyebrow(M, 262, "Twenty years on the same problem", INK2, 20, 2.6))
    steps = [("PhD, IISc Bangalore", "Model checking for information-flow security"),
             ("Oracle Labs · 2014–2019", "Java vulnerability detection; static analysis"),
             ("ConsenSys R&D · 2019–2021", "Cross-chain atomic protocols; Besu prototype"),
             ("Supra · VP of R&D", "BFT consensus and protocol design, Dubai")]
    cy = 316
    for head, sub in steps:
        b.append(f'<rect x="{M}" y="{cy-25}" width="4" height="54" fill="{GOLD}"/>')
        b.append(t(M + 20, cy, head, 26, INK, SANS, "600"))
        b.append(t(M + 20, cy + 30, sub, 23, INK2))
        cy += 80

    x2, w2 = M + 574, CW - 574
    b.append(rrect(x2, 282, w2, 330, PANEL, 14, LINE))
    b.append(eyebrow(x2 + 30, 330, "Track record", GOLDINK, 20, 2.6))
    bl, _ = bullets(x2 + 30, 372, [
        "Moonshot safety proved in IVy, FMBC 2024",
        "DSN 2024 · VLDB 2025 · FMBC 2024",
        "Formal methods · program analysis",
    ], w2 - 60, 23, 28, 16)
    b.append(bl)
    b.append(hline(x2 + 30, 566, w2 - 60))
    b.append(t(x2 + 30, 596, "raghavendra80.github.io", 22, GOLDINK, MONO, "500"))

    b.append(chrome(2, "About"))
    return page("".join(b))


# ============================================================ 3 · why now
def s03():
    b = [heading("Why now: the attacker industrialised", "Chapter 2")]
    b.append(t(M, 198, "A sampling defence cannot answer an enumerating attack.",
               30, INK, SERIF, "600", style="italic"))

    stats = [("4.5×", "revenue of AI-assisted scam operations vs. non-AI"),
             ("USD 3.52", "compute cost per LLM-agent exploit attempt"),
             ("87%", "of a 15-CVE sample exploited from the description")]
    tw = (CW - 2 * 20) / 3
    for i, (big, sub) in enumerate(stats):
        x = M + i * (tw + 20)
        b.append(rrect(x, 234, tw, 134, PANEL, 12, LINE))
        b.append(t(x + 24, 298, big, 50, GOLDINK, SERIF, "600"))
        blk, _ = block(x + 24, 328, sub, tw - 48, 21, 25, INK2, 2)
        b.append(blk)

    y, hw = 408, CW / 2 - 12
    b.append(rrect(M, y, hw, 186, WHITE, 12, LINE))
    b.append(rrect(M + CW / 2 + 12, y, hw, 186, FAM["cyb"]["c"], 12))
    b.append(eyebrow(M + 24, y + 42, "Traditional pen test", INK2, 20, 2.6))
    b.append(eyebrow(M + CW / 2 + 36, y + 42, "AI-driven adversary", "#cfe0f7", 20, 2.6))
    left = ["10²–10³ paths, human-selected", "2–4 week window, then closed",
            "High marginal cost per path", "“We found no way in”"]
    right = ["10⁵–10⁷ paths, machine-enumerated", "Continuous, no window",
             "Near-zero marginal cost", "Approaching exhaustive"]
    for i, (l, r) in enumerate(zip(left, right)):
        b.append(t(M + 24, y + 86 + i * 30, l, 23, INK2))
        b.append(t(M + CW / 2 + 36, y + 86 + i * 30, r, 23, WHITE))

    b.append(t(M, 654, "Proof is the one capability that answers exhaustive search in kind.",
               26, GOLDINK, SANS, "500"))
    b.append(chrome(3, "Why now"))
    return page("".join(b))


# ============================================================ 4 · the method
def s04():
    b = [heading("The method: automated reasoning", "Chapter 3")]
    b.append(t(M, 198, "Testing shows what your system does. Proof shows what it cannot do.",
               29, INK, SERIF, "600", style="italic"))

    steps = [("1", "Formalise", "Your existing artefact becomes a logical model"),
             ("2", "State", "The security property becomes a formula"),
             ("3", "Solve", "Z3, CBMC, Batfish, IVy and TLA+ search it all"),
             ("4", "Report", "A proof, or a reproducible attack path")]
    tw = (CW - 3 * 18) / 4
    for i, (n, head, body) in enumerate(steps):
        x = M + i * (tw + 18)
        b.append(rrect(x, 236, tw, 190, WHITE, 12, LINE))
        b.append(f'<circle cx="{x+42:.0f}" cy="274" r="19" fill="{GOLD}"/>')
        b.append(t(x + 42, 283, n, 23, WHITE, MONO, "500", anchor="middle"))
        b.append(t(x + 72, 283, head, 27, INK, SERIF, "600"))
        blk, _ = block(x + 24, 334, body, tw - 48, 22, 28, INK2, 4)
        b.append(blk)
        if i < 3:
            b.append(f'<path d="M{x+tw+3:.0f},330 l11,0 M{x+tw+9:.0f},325 l5,5 -5,5" '
                     f'stroke="{GOLD}" stroke-width="2" fill="none"/>')

    hw = CW / 2 - 12
    b.append(rrect(M, 456, hw, 156, "#eaf4ee", 12, "#bcd8c7"))
    b.append(rrect(M + CW / 2 + 12, 456, hw, 156, "#fbeee6", 12, "#e8cdb6"))
    b.append(t(M + 24, 502, "UNSAT", 30, GREEN, MONO, "500"))
    blk, _ = block(M + 24, 542, "No violating state exists — over the entire space, "
                                "under a stated model.", hw - 48, 23, 29, INK2, 2)
    b.append(blk)
    b.append(t(M + 24, 600, "Not “none was found”.", 23, GREEN, SANS, "500"))
    b.append(t(M + CW / 2 + 36, 502, "SAT + witness", 30, AMBER, MONO, "500"))
    blk, _ = block(M + CW / 2 + 36, 542, "The exact request, path or call ordering that "
                                         "breaks it — reproducible on your estate.",
                   hw - 48, 23, 29, INK2, 3)
    b.append(blk)

    b.append(t(M, 664, "Industrial practice: AWS (Zelkova, Tiros, Nitro) · Microsoft (Z3) · "
                       "Meta (Infer) · Airbus (Astrée)", 22, MUTED, SANS))
    b.append(chrome(4, "The method"))
    return page("".join(b))


# ============================================================ 5 · the map
def s05():
    b = [heading("Nine solutions, three families", "Solutions")]
    b.append(t(M, 198, "One method, one evidence layer — three buyers, three regulatory hooks.",
               26, INK2, SANS))

    bands = [
        ("cyb", "Cybersecurity", "CISO · cloud security · AppSec", 228, 172,
         [(1, "Cloud entitlement proofs"), (2, "Network segmentation proofs"),
          (3, "API-usage conformance"), (4, "Firmware & CVE reachability"),
          (5, "Post-quantum migration")]),
        ("ai", "AI Security", "Head of AI · model risk", 416, 122,
         [(6, "LLM guardrail verification"), (7, "Neurosymbolic assurance")]),
        ("cry", "Crypto Security", "Protocol lead · CTO · VARA", 554, 122,
         [(8, "Smart-contract verification"), (9, "Protocol & consensus proofs")]),
    ]
    for fam, name, buyer, y, h, items in bands:
        f = FAM[fam]
        b.append(rrect(M, y, CW, h, WHITE, 12, LINE))
        b.append(f'<path d="M{M},{y+12} a12,12 0 0 1 12,-12 l224,0 l0,{h} l-224,0 '
                 f'a12,12 0 0 1 -12,-12 z" fill="{f["c"]}"/>')
        b.append(t(M + 26, y + 52, name, fit(name, 196, 29, W_SERIF, 22), WHITE, SERIF, "600"))
        blk, _ = block(M + 26, y + 84, buyer, 200, 19, 24, "#e4ecf6", 2)
        b.append(blk)

        colx = [M + 256, M + 596]
        colmax = [596 - 256 - 48, CW - 596 - 30]
        cols = [items[:3], items[3:]] if len(items) > 3 else [items[:1], items[1:]]
        top = y + 52 if len(items) > 3 else y + 72
        for ci, col in enumerate(cols):
            for ri, (n, label) in enumerate(col):
                cy = top + ri * 40
                b.append(t(colx[ci], cy, f"{n}", 24, f["c"], MONO, "500"))
                b.append(t(colx[ci] + 32, cy, label,
                           fit(label, colmax[ci], 24, W_SANS, 19), INK2))

    b.append(chrome(5, "Solutions"))
    return page("".join(b))


# ====================================================== section divider slides
def section(num, fam, title, kicker, items):
    f = FAM[fam]
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', symbol_field(f["c"]),
         f'<rect x="0" y="0" width="{W}" height="6" fill="{f["c"]}"/>']
    b.append(eyebrow(M, 202, kicker, f["c"], 22, 3.2))
    b.append(t(M, 292, title, fit(title, CW, 66, W_SERIF, 46), WHITE, SERIF, "600"))
    b.append(hline(M, 328, 160, f["c"], 3))
    cy = 404
    for n, name in items:
        b.append(t(M, cy, f"{n:02d}", 27, f["c"], MONO, "500"))
        b.append(t(M + 62, cy, name, fit(name, CW - 70, 29, W_SANS, 22), "#e7eaef", SANS))
        cy += 46
    b.append(chrome(num, f["name"], fam, dark=True))
    return page("".join(b), INK)


# ========================================================== solution template
def solution(num, fam, n, title, question, problem, build, output, precedent,
             buyers, note):
    f = FAM[fam]
    b = [heading(title, f"Solution {n}  ·  {f['name']}", fam)]

    # the question it settles
    b.append(rrect(M, 172, CW, 84, f["tint"], 12))
    b.append(f'<rect x="{M}" y="172" width="5" height="84" rx="2.5" fill="{f["c"]}"/>')
    qlines = wrap(question, CW - 76, 28, W_SERIF)[:2]
    y0 = 212 if len(qlines) == 2 else 224
    for i, ln in enumerate(qlines):
        b.append(t(M + 32, y0 + i * 34, ln, 28, INK, SERIF, "600", style="italic"))

    lw, rx, rw = 500, M + 534, CW - 534

    # left — the problem, the line worth repeating, the precedent
    b.append(eyebrow(M, 308, "The problem", f["c"], maxw=lw))
    blk, _ = block(M, 346, problem, lw, 25, 32, INK2, 5)
    b.append(blk)
    b.append(hline(M, 492, lw))
    blk, _ = block(M, 524, note, lw, 24, 30, GOLDINK, 2, style="italic")
    b.append(blk)
    b.append(t(M, 592, "PRECEDENT", 19, MUTED, MONO, "500", ls="2.4"))
    b.append(t(M + 140, 592, precedent, fit(precedent, lw - 140, 21, W_SANS, 16), INK2))

    # right — what we build
    b.append(rrect(rx, 282, rw, 304, WHITE, 12, LINE))
    b.append(eyebrow(rx + 26, 322, "What we build", f["c"], maxw=rw - 52))
    bl, _ = bullets(rx + 26, 366, build, rw - 52, 24, 30, 18, INK2, f["c"])
    b.append(bl)

    # bottom — the output
    b.append(rrect(M, 606, CW, 88, f["tint"], 12))
    b.append(f'<rect x="{M}" y="606" width="5" height="88" rx="2.5" fill="{f["c"]}"/>')
    b.append(eyebrow(M + 32, 640, "Output", f["c"], 20, 2.6))
    blk, _ = block(M + 168, 640, output, CW - 200, 23, 29, INK2, 2)
    b.append(blk)

    b.append(chrome(num, "", fam, left=f"Buyers: {buyers}"))
    return page("".join(b))


# ============================================================ 18 · take away
def s18():
    b = [heading("What to take away", "Take away")]

    b.append(rrect(M, 182, CW, 106, INK, 14))
    b.append(t(W / 2, 230, "Mathematical rigour to security —", 33, WHITE, SERIF,
               "600", anchor="middle"))
    b.append(t(W / 2, 272, "proof alongside testing, across cloud, AI and crypto.",
               33, GOLD, SERIF, "600", anchor="middle"))

    cols = [("The shift", "Attack path discovery is automated, parallel and cheap. "
                          "A defence that only samples cannot answer one that enumerates."),
            ("The addition", "We do not replace testing, monitoring or the SOC. "
                             "We make one class of control statement decidable, not sampled."),
            ("The honesty", "A proof is relative to a model and a specification — both stated. "
                            "We produce the evidence; we do not certify.")]
    cw = (CW - 2 * 24) / 3
    for i, (head, body) in enumerate(cols):
        x = M + i * (cw + 24)
        b.append(hline(x, 330, cw - 10, GOLD, 2))
        b.append(t(x, 372, head, 29, INK, SERIF, "600"))
        blk, _ = block(x, 412, body, cw - 10, 23, 29, INK2, 6)
        b.append(blk)

    b.append(rrect(M, 578, CW, 112, PANEL, 14, LINE))
    b.append(f'<rect x="{M}" y="578" width="5" height="112" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(M + 30, 614, "Start here — Milestone 1: the Micro-Proof Assessment",
                     GOLDINK, 20, 2.4, maxw=CW - 70))
    b.append(t(M + 30, 650, "One narrow, high-risk slice. Read-only access, no agent deployed,",
               23, INK2))
    b.append(t(M + 30, 678, "weeks not months — and a counter-example on your own systems, or a proof.",
               23, INK2))

    b.append(chrome(18, "Take away"))
    return page("".join(b))


# ============================================================ 19 · thank you
def s19():
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', symbol_field(GOLD),
         f'<rect x="0" y="0" width="{W}" height="6" fill="{GOLD}"/>']
    b.append(t(M, 264, "Thank you", 84, WHITE, SERIF, "600"))
    b.append(hline(M, 306, 200, GOLD, 3))
    b.append(t(M, 378, "Let us prove one property on your estate —", 31, "#b8c0cc",
               SERIF, "400", style="italic"))
    b.append(t(M, 420, "then judge the method on the result.", 31, "#b8c0cc",
               SERIF, "400", style="italic"))

    b.append(hline(M, 500, CW, "#2a3140"))
    b.append(t(M, 552, "Dr. Raghavendra Ramesh", 33, WHITE, SERIF, "600"))
    b.append(t(M, 588, "Founder & CEO, PrimusCredence · PhD, IISc", 24, "#98a2b1", SANS))
    b.append(t(W - M, 552, "raghavendra@primuscredence.com", 27, GOLD, MONO, "500", anchor="end"))
    b.append(t(W - M, 590, "primuscredence.com", 27, GOLD, MONO, "500", anchor="end"))
    b.append(t(W - M, 628, "+971 58 189 2803 · Dubai, UAE", 23, "#98a2b1", MONO, anchor="end"))
    b.append(t(M, 672, "Cloud  |  AI  |  Crypto", 23, GOLDINK, MONO, "500", ls="3.2"))
    return page("".join(b), INK)


# ==================================================================== content
SOLUTIONS = [
    dict(num=7, fam="cyb", n=1,
         title="Cloud access-policy & entitlement verification",
         question="Can any principal, in any request context, reach this resource from "
                  "outside the trust boundary?",
         problem="IAM is combinatorial: the effective permission composes policies, "
                 "boundaries, SCPs and request context. CIEM scores the paths it enumerated.",
         build=["Multi-cloud policies into one logical model",
                "Privilege-escalation paths across the graph",
                "Cedar symbolic checks as a CI/CD gate"],
         output="Proof of safety over all requests — or the violating request, the escalation "
                "path it opens, and its blast radius.",
         precedent="AWS Zelkova → IAM Access Analyzer",
         buyers="Regional CSPs · sovereign hosts · enterprises",
         note="Principal \"*\" with a NotIpAddress condition permits the whole internet "
              "except one /24."),

    dict(num=8, fam="cyb", n=2,
         title="Network reachability & segmentation proofs",
         question="Does any path exist from an untrusted zone to this subnet — and does "
                  "east-west segmentation hold?",
         problem="Probing tests the paths you thought of, at the moment you ran it. "
                 "Reachability is a property of the configuration, not of the packets sent.",
         build=["Batfish models of the hybrid and on-prem estate",
                "Soufflé and Z3 engines for cloud topologies",
                "Microsegmentation vs. the declared policy"],
         output="A proof that no path exists — or the path, hop by hop, with the rule that "
                "permits it and the owner of that rule.",
         precedent="AWS Tiros → VPC Reachability Analyzer",
         buyers="Sovereign cloud · banks · OT · telcos",
         note="Static: no scanning window, no production traffic — it re-runs on every change."),

    dict(num=9, fam="cyb", n=3,
         title="API-usage conformance",
         question="Does our own code use the platform, credential and crypto SDKs the way "
                  "their contracts require?",
         problem="Cloud APIs are protocols, not function calls. Undrained pagination, a logged "
                 "credential, an unsanitised response — all compile and pass review.",
         build=["Pattern libraries per SDK, versioned per release",
                "A conformance gate for library publishers",
                "PR-gate CI on Soot, CodeQL and Infer"],
         output="The call site, the taint trace, the pattern violated and the corrected call "
                "sequence — plus which patterns were checked.",
         precedent="AWS RAPID → CodeGuru · 76% accepted",
         buyers="Platform and AppSec teams · ISVs · banks",
         note="A correct policy invoked through a misused SDK still leaks. Bounded by the library."),

    dict(num=10, fam="cyb", n=4,
         title="Hypervisor, firmware & CVE reachability",
         question="Can tenant isolation break below the guest — and is this week's hypervisor "
                  "CVE reachable on our build?",
         problem="Below the application, security is a memory-safety question, and a flaw "
                 "there invalidates every control above it. Flashed firmware has no patch path.",
         build=["Firmware and bootloader kits: CBMC and Kani",
                "Enclave app and attestation-protocol proofs",
                "CVE triage against your exact build"],
         output="Bounded proof of memory safety and isolation, with the bound stated — or the "
                "failing trace; per-CVE verdicts ready for VEX.",
         precedent="AWS Nitro · ~330k lines of Isabelle/HOL",
         buyers="Sovereign cloud · chip vendors · defence",
         note="Three of four CVEs unreachable turns a fleet emergency into one scheduled patch."),

    dict(num=11, fam="cyb", n=5,
         title="Post-quantum cryptography migration",
         question="Where is every cryptographic asset, in what order does it move, and does "
                  "security hold at each stage?",
         problem="Harvest-now-decrypt-later opened the window years ago, so detection "
                 "contributes nothing. NIST settled the algorithms — which is why the work "
                 "gets mis-scoped.",
         build=["Discovery and a versioned CBOM, gaps listed",
                "Risk-based sequencing by confidentiality horizon",
                "Proof of combiner and downgrade states"],
         output="The CBOM and a sequenced migration plan; then, at each stage, a proof the "
                "transition preserves the property.",
         precedent="FREAK and Logjam: negotiation failures",
         buyers="CSPs · sovereign AI · banks · utilities",
         note="A programme over quarters with verification as its assurance layer."),

    dict(num=13, fam="ai", n=6,
         title="AI and LLM guardrail verification",
         question="Not “how often does the agent fail?” but “can it do this at all?”",
         problem="An agent is a non-human identity with delegated privilege and an instruction "
                 "channel the adversary can write to. A guard model judging a model is "
                 "detective, not preventive.",
         build=["Tool-call constraints over identity and arguments",
                "Data-access boundaries in the Solution 1 logic",
                "Composition safety across call sequences"],
         output="A result about the mediation layer, not the model: nothing permitted escapes "
                "the envelope, and no path bypasses it.",
         precedent="Bedrock Automated Reasoning · detect mode",
         buyers="Banks · sovereign AI · OT · healthcare",
         note="Provable: no rows outside the caller's ACL. Not provable: no PII ever reaches the user."),

    dict(num=14, fam="ai", n=7,
         title="Neurosymbolic assurance",
         question="Does this answer follow from the policy we operate under — and if not, what "
                  "assumption was silently supplied?",
         problem="Solution 6 bounds what an agent may do; nothing bounds what it may say. "
                 "Where the output is the product, the failure is entailment: no boundary "
                 "crossed, liability all the same.",
         build=["Policy theory development, scope stated",
                "Entailed / contradicted / unsupported verdicts",
                "An evaluation harness on the client's corpus"],
         output="Per answer: the verdict, the derivation or the contradicting rule, and the "
                "missing assumption named — an audit trail.",
         precedent="Bedrock Automated Reasoning checks",
         buyers="Banks and insurers · government · ISO 42001",
         note="LLM autoformalization drafts the theory; the domain expert ratifies it."),

    dict(num=16, fam="cry", n=8,
         title="Formal verification of smart contracts",
         question="Does this contract admit a reachable state that breaks its invariants, "
                  "access control or solvency?",
         problem="The code is public, the surface permissionless, exploitation atomic and "
                 "irreversible. Of 2025 DeFi protocol losses, roughly 89% were protocol logic.",
         build=["Tier 1 fuzzing: Echidna, Medusa, Foundry",
                "Tier 2 bounded: Certora, Halmos, hevm",
                "Tier 3 deductive: K/KEVM, Move Prover, Lean"],
         output="Machine-checked invariants — value, solvency, access control, reentrancy, "
                "upgrades — or the transaction that breaks them.",
         precedent="Certora in CI at Aave, Uniswap, Lido",
         buyers="VASPs · DeFi protocols · custody",
         note="“Formally verified” means three different things. The tier decides your risk."),

    dict(num=17, fam="cry", n=9,
         title="Formal verification of distributed protocols",
         question="Does this protocol admit an execution that breaks safety under Byzantine "
                  "faults, asynchrony or partition?",
         problem="These are design defects: no CVE, no patch, no signature, present from the "
                 "first commit. One AWS TLA+ finding needed a 35-step sequence.",
         build=["IVy in decidable EPR: proof or counterexample",
                "Dafny and IronFleet; TLA+ with TLC and TLAPS",
                "Cross-chain bridges — a genuine white space"],
         output="Machine-checked inductive invariants with the fault, adversary and network "
                "assumptions stated — or the breaking execution.",
         precedent="Pipelined Moonshot in IVy · FMBC 2024",
         buyers="L1/L2 teams · bridges · settlement",
         note="Bridges: USD 2.8bn lost, ~40% of all Web3 losses — and verification is thin."),
]

TITLES = [
    "PrimusCredence — Provable security solutions",
    "About — Dr. Raghavendra Ramesh",
    "Why now: the attacker industrialised",
    "The method: automated reasoning",
    "Nine solutions, three families",
    "Section — Cybersecurity Solutions",
    "Solution 1 — Cloud access-policy & entitlement verification",
    "Solution 2 — Network reachability & segmentation proofs",
    "Solution 3 — API-usage conformance",
    "Solution 4 — Hypervisor, firmware & CVE reachability",
    "Solution 5 — Post-quantum cryptography migration",
    "Section — AI Security Solutions",
    "Solution 6 — AI and LLM guardrail verification",
    "Solution 7 — Neurosymbolic assurance",
    "Section — Crypto Security Solutions",
    "Solution 8 — Formal verification of smart contracts",
    "Solution 9 — Formal verification of distributed protocols",
    "What to take away",
    "Thank you",
]


def build():
    os.makedirs(OUT, exist_ok=True)
    pages = {
        1: s01(), 2: s02(), 3: s03(), 4: s04(), 5: s05(),
        6: section(6, "cyb", "Cybersecurity Solutions", "Chapter 4 · Solutions 1–5",
                   [(1, "Cloud access-policy and entitlement verification"),
                    (2, "Network reachability and segmentation proofs"),
                    (3, "API-usage conformance"),
                    (4, "Hypervisor, firmware and CVE reachability"),
                    (5, "Post-quantum cryptography migration")]),
        12: section(12, "ai", "AI Security Solutions", "Chapter 5 · Solutions 6–7",
                    [(6, "Guardrail verification — what an agent may do"),
                     (7, "Neurosymbolic assurance — what an agent may say")]),
        15: section(15, "cry", "Crypto Security Solutions", "Chapter 6 · Solutions 8–9",
                    [(8, "Formal verification of smart contracts"),
                     (9, "Formal verification of distributed protocols")]),
        18: s18(), 19: s19(),
    }
    for s in SOLUTIONS:
        pages[s["num"]] = solution(**s)
    for i in range(1, 20):
        with open(os.path.join(OUT, f"{i:02d}.svg"), "w") as fh:
            fh.write(pages[i])


if __name__ == "__main__":
    build()
    print(f"wrote {len(TITLES)} slides to {OUT}")
