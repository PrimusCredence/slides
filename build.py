#!/usr/bin/env python3
"""Builds the PrimusCredence slide deck.

One .svg per slide in slides/, stitched together by index.html.

Geometry is A5 landscape (210 x 148.5 mm) at 5 units per mm, so one unit is
0.2 mm and a 24-unit font prints at ~13.6 pt. Nothing in the deck is smaller
than 19 units (~10.8 pt) and body copy sits at 23-26.

Every slide is white, with soft tinted blooms behind frosted-glass panels.
Text is wrapped against measured average glyph advances (see W_SANS etc.),
and every block has a line budget, so the layout does not overflow.
"""

import os

W, H = 1050, 742
M = 68                      # page margin
CW = W - 2 * M              # content width (914)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slides")

# --- PrimusCredence Gold palette (carried from the report and the card) ------
INK      = "#14181f"
BLACK    = "#0b0d12"
INK2     = "#4a5260"
MUTED    = "#767e8c"
WHITE    = "#ffffff"
LINE     = "#e3e6ec"
GOLD     = "#c8940a"
GOLDINK  = "#a87c00"
GREEN    = "#2f7d4f"
AMBER    = "#b06a00"

FAM = {
    "cyb":  dict(c="#1d5fa8", tint="#e9eff9", name="Cybersecurity Solutions"),
    "ai":   dict(c="#0f766e", tint="#e3f1ef", name="AI Security Solutions"),
    "cry":  dict(c="#b81f63", tint="#fbe8f0", name="Crypto Security Solutions"),
    "gold": dict(c=GOLDINK, tint="#f6efdd", name=""),
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

DEFS = f'''<defs>
<filter id="lift" x="-30%" y="-30%" width="160%" height="180%">
  <feDropShadow dx="0" dy="10" stdDeviation="13" flood-color="#0b1a2e" flood-opacity="0.11"/>
  <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#0b1a2e" flood-opacity="0.07"/>
</filter>
<filter id="liftsm" x="-30%" y="-40%" width="160%" height="200%">
  <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0b1a2e" flood-opacity="0.09"/>
</filter>
<filter id="bloom" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="70"/>
</filter>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.99"/>
  <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.93"/>
  <stop offset="1" stop-color="#eef1f7" stop-opacity="0.92"/>
</linearGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0.3" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.50"/>
  <stop offset="0.46" stop-color="#ffffff" stop-opacity="0.14"/>
  <stop offset="0.47" stop-color="#ffffff" stop-opacity="0.03"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0.05"/>
</linearGradient>
<radialGradient id="orb" cx="0.32" cy="0.26" r="0.9">
  <stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/>
  <stop offset="0.45" stop-color="#ffffff" stop-opacity="0.08"/>
  <stop offset="1" stop-color="#000000" stop-opacity="0.13"/>
</radialGradient>
<linearGradient id="goldbar" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GOLD}"/>
  <stop offset="0.55" stop-color="#e0b64a"/>
  <stop offset="1" stop-color="{GOLD}"/>
</linearGradient>
</defs>'''


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
          family=SANS, adv=W_SANS, style="normal", weight="400", anchor="start"):
    lines = wrap(text, width, size, adv)
    if maxlines:
        lines = lines[:maxlines]
    return ("".join(t(x, y + i * lead, ln, size, fill, family, weight,
                      anchor=anchor, style=style) for i, ln in enumerate(lines)),
            y + len(lines) * lead)


def eyebrow(x, y, s, fill=GOLDINK, size=21, ls=3.2, maxw=None, anchor="start"):
    s = s.upper()
    if maxw:
        size = fit(s, maxw, size, W_MONO, 14, ls)
    return t(x, y, s, size, fill, MONO, "500", anchor=anchor, ls=str(ls))


# measured advance of the wordmark in Source Serif 4 semibold, per character
# per unit of font size — the rule under it is drawn to exactly this width
W_MARK = 0.4932


def mark_width(size):
    return len("PrimusCredence") * size * W_MARK


def wordmark(x, y, size, anchor="start"):
    """Primus in black, Credence in gold, set solid."""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{SERIF}" font-size="{size}" '
            f'font-weight="600"{a}><tspan fill="{BLACK}">Primus</tspan>'
            f'<tspan fill="{GOLDINK}">Credence</tspan></text>')


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


def rrect(x, y, w, h, fill, r=14, stroke=None, sw=1, opacity=None):
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
         f'rx="{r}" fill="{fill}"')
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if opacity:
        s += f' opacity="{opacity}"'
    return s + "/>"


def glass(x, y, w, h, r=16, tint=None, tint_op=0.55, edge=LINE):
    """A frosted panel with a little depth: a layered drop shadow, a vertical
    glass gradient, a diagonal gloss across the top-left, a lit top edge and a
    faint shaded bottom edge."""
    out = ['<g filter="url(#lift)">']
    if tint:
        out.append(rrect(x, y, w, h, tint, r, opacity=tint_op))
        out.append(rrect(x, y, w, h, "url(#glass)", r, opacity=0.45))
    else:
        out.append(rrect(x, y, w, h, "url(#glass)", r))
    out.append(rrect(x, y, w, h, "url(#gloss)", r, opacity=0.9 if tint else 1))
    out.append(rrect(x, y, w, h, "none", r, edge, 1))
    out.append("</g>")
    out.append(f'<rect x="{x+14:.0f}" y="{y+1:.0f}" width="{w-28:.0f}" height="1.4" '
               f'rx="0.7" fill="url(#sheen)"/>')
    out.append(f'<rect x="{x+16:.0f}" y="{y+h-2:.0f}" width="{w-32:.0f}" height="1.2" '
               f'rx="0.6" fill="#0b1a2e" opacity="0.05"/>')
    return "".join(out)


def solid(x, y, w, h, fill, r=16, sheen=True, gloss=0.55, edge=None):
    """A filled block with a lit edge. `gloss` is the face sheen, which dark or
    saturated blocks want low or off; `edge` adds a light inner border."""
    out = [f'<g filter="url(#lift)">', rrect(x, y, w, h, fill, r)]
    if gloss:
        out.append(rrect(x, y, w, h, "url(#gloss)", r, opacity=gloss))
    if edge:
        out.append(f'<rect x="{x+1:.0f}" y="{y+1:.0f}" width="{w-2:.0f}" '
                   f'height="{h-2:.0f}" rx="{r-1}" fill="none" stroke="#ffffff" '
                   f'stroke-width="1.2" opacity="{edge}"/>')
    out.append("</g>")
    if sheen:
        out.append(f'<rect x="{x+14:.0f}" y="{y+1:.0f}" width="{w-28:.0f}" height="1.4" '
                   f'rx="0.7" fill="#ffffff" opacity="0.3"/>')
    return "".join(out)


def orb(cx, cy, r, fill=GOLD):
    """A filled circle with a specular highlight, so badges read as buttons."""
    return (f'<g filter="url(#liftsm)"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" '
            f'fill="{fill}"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" '
            f'fill="url(#orb)"/></g>')


def bloom(cx, cy, r, color, op=0.16):
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{color}" '
            f'opacity="{op}" filter="url(#bloom)"/>')


def water(fam="gold"):
    """The background wash: soft blooms in brand gold and the family hue."""
    f = FAM[fam]
    return (bloom(880, 110, 210, f["c"], 0.16) +
            bloom(130, 665, 230, GOLD, 0.13) +
            bloom(560, 380, 260, f["c"], 0.05))


def hline(x, y, w, color=LINE, sw=1):
    return (f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+w:.0f}" y2="{y:.0f}" '
            f'stroke="{color}" stroke-width="{sw}"/>')


SYMBOLS = [("∀", 120, 216, 190, .05), ("∃", 878, 156, 150, .045),
           ("⊨", 250, 600, 170, .04), ("∧", 640, 250, 130, .035),
           ("◇", 928, 560, 150, .045), ("⊤", 470, 690, 120, .03),
           ("¬", 40, 470, 120, .03), ("⟹", 700, 660, 130, .03)]


def symbol_field(color=GOLD):
    return "".join(
        f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
        f'fill="{color}" opacity="{op}">{ch}</text>'
        for ch, x, y, size, op in SYMBOLS)


def chrome(num):
    """Footer: the wordmark left, the slide number right. Nothing else."""
    return (hline(M, 700, CW) + wordmark(M, 728, 21) +
            t(W - M, 728, str(num), 21, MUTED, MONO, "500", anchor="end", ls="1.4"))


def page(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" role="img">'
            f'<style>{FONTS}</style>{DEFS}'
            f'<rect width="{W}" height="{H}" fill="{WHITE}"/>{body}</svg>')


def heading(title, fam="gold", y=112):
    f = FAM[fam]
    return (t(M, y, title, fit(title, CW, 46, W_SERIF, 30), INK, SERIF, "600") +
            f'<rect x="{M}" y="{y+16:.0f}" width="112" height="4" rx="2" fill="{f["c"]}"/>')


# ============================================================ 1 · title
def s01():
    b = [water("gold"), symbol_field(GOLD),
         f'<rect x="0" y="0" width="{W}" height="7" fill="url(#goldbar)"/>']
    b.append(wordmark(M, 236, 88))
    b.append(f'<rect x="{M}" y="272" width="{mark_width(88):.0f}" height="4" rx="2" '
             f'fill="{GOLD}"/>')
    b.append(t(M, 356, "Provable Security Solutions", 46, GOLDINK, SERIF, "600"))
    b.append(t(M, 410, "to Cloud, AI & Crypto", 46, GOLDINK, SERIF, "600"))

    b.append(hline(M, 528, CW))
    b.append(t(M, 578, "Dr. Raghavendra Ramesh", 33, INK, SERIF, "600"))
    b.append(t(M, 612, "Founder & CEO", 24, INK2, SANS))
    b.append(t(M, 644, "PhD, IISc Bangalore", 24, INK2, SANS))
    b.append(t(W - M, 578, "primuscredence.com", 27, GOLDINK, MONO, "500", anchor="end"))
    b.append(t(W - M, 612, "raghavendra@primuscredence.com", 24, INK2, MONO, anchor="end"))
    b.append(t(W - M, 644, "UAE", 24, INK2, MONO, anchor="end"))
    return page("".join(b))


# ============================================================ 2 · about
def s02():
    b = [water("gold"), heading("Dr. Raghavendra Ramesh")]
    b.append(t(M, 176, "Founder & CEO, PrimusCredence", 26, GOLDINK, SANS, "500"))
    b.append(eyebrow(M, 232, "22+ years of experience in provable security",
                     INK2, 20, 2.4, maxw=510))

    steps = [("PhD, IISc Bangalore", "Model checking for information-flow security"),
             ("Oracle Labs · 2014–2019", "Java vulnerability detection"),
             ("ConsenSys R&D · 2019–2021", "Cross-chain protocols, consensus verification"),
             ("Supra · VP of R&D · 2021–ongoing", "BFT design & FV, bridges, DeFi")]
    cy = 292
    for head, sub in steps:
        b.append(f'<rect x="{M}" y="{cy-25}" width="4" height="54" rx="2" fill="{GOLD}"/>')
        b.append(t(M + 20, cy, head, fit(head, 490, 26, W_SANS, 21), INK, SANS, "600"))
        b.append(t(M + 20, cy + 30, sub, fit(sub, 490, 23, W_SANS, 19), INK2))
        cy += 82

    x2, w2 = M + 574, CW - 574
    b.append(glass(x2, 264, w2, 292, 18, FAM["gold"]["tint"], 0.5))
    b.append(eyebrow(x2 + 30, 308, "Techniques", GOLDINK, 20, 2.6))
    blk, _ = block(x2 + 30, 346, "Static analysis, theorem proving, model checking",
                   w2 - 60, 23, 29, INK2, 3)
    b.append(blk)
    b.append(hline(x2 + 30, 432, w2 - 60))
    b.append(eyebrow(x2 + 30, 470, "Tools", GOLDINK, 20, 2.6))
    blk, _ = block(x2 + 30, 508, "Dafny, TLA+, IVy, Lean, Isabelle", w2 - 60, 23, 29, INK2, 2)
    b.append(blk)

    b.append(chrome(2))
    return page("".join(b))


# ============================================================ 3 · why now
def s03():
    b = [water("gold"), heading("Why Now: The Attacker Industrialised")]
    b.append(t(M, 184, "A sampling defence cannot answer an enumerating attack.",
               30, INK, SERIF, "600", style="italic"))

    stats = [("4.5×", "revenue of AI-assisted scam operations versus non-AI equivalents"),
             ("$3.52", "average compute cost per LLM-agent exploit attempt on a real CVE"),
             ("87%", "of a 15-CVE sample exploited from the public description alone")]
    tw = (CW - 2 * 20) / 3
    for i, (big, sub) in enumerate(stats):
        x = M + i * (tw + 20)
        b.append(glass(x, 216, tw, 158, 16, FAM["gold"]["tint"], 0.45))
        b.append(t(x + 24, 280, big, 48, GOLDINK, SERIF, "600"))
        blk, _ = block(x + 24, 312, sub, tw - 48, 20, 25, INK2, 3)
        b.append(blk)

    y, hw = 404, CW / 2 - 12
    b.append(glass(M, y, hw, 188, 16))
    b.append(solid(M + CW / 2 + 12, y, hw, 188, FAM["cyb"]["c"], 16,
                   sheen=False, gloss=0.14, edge=0.22))
    b.append(eyebrow(M + 26, y + 44, "Traditional pen test", INK2, 20, 2.6))
    b.append(eyebrow(M + CW / 2 + 38, y + 44, "AI-driven adversary", "#cfe0f7", 20, 2.6))
    left = ["10²–10³ paths, human-selected", "2–4 week window, then closed",
            "High marginal cost per path", "“We found no way in”"]
    right = ["10⁵–10⁷ paths, machine-enumerated", "Continuous, no window",
             "Near-zero marginal cost", "Approaching exhaustive"]
    for i, (l, r) in enumerate(zip(left, right)):
        b.append(t(M + 26, y + 88 + i * 30, l, 23, INK2))
        b.append(t(M + CW / 2 + 38, y + 88 + i * 30, r, 23, WHITE))

    b.append(t(M, 654, "Proof is the one capability that answers exhaustive search in kind.",
               26, GOLDINK, SANS, "500"))
    b.append(chrome(3))
    return page("".join(b))


# ============================================================ 4 · the method
def s04():
    b = [water("gold"), heading("Automated Reasoning")]
    b.append(t(M, 184, "Proof establishes that bad things cannot happen.",
               30, INK, SERIF, "600", style="italic"))

    steps = [("1", "Formalise", "Your existing artefact becomes a logical model"),
             ("2", "State", "The security property becomes a formula"),
             ("3", "Solve", "Z3, CBMC, Batfish, IVy and TLA+ search it all"),
             ("4", "Report", "A proof, or a reproducible attack path")]
    tw = (CW - 3 * 18) / 4
    for i, (n, head, body) in enumerate(steps):
        x = M + i * (tw + 18)
        cx = x + tw / 2
        b.append(glass(x, 208, tw, 192, 16))
        b.append(orb(cx, 248, 19))
        b.append(t(cx, 257, n, 23, WHITE, MONO, "500", anchor="middle"))
        b.append(t(cx, 296, head, 27, INK, SERIF, "600", anchor="middle"))
        blk, _ = block(cx, 330, body, tw - 40, 21, 27, INK2, 3, anchor="middle")
        b.append(blk)
        b.append(f'<line x1="{cx:.0f}" y1="400" x2="{cx:.0f}" y2="408" '
                 f'stroke="{GOLD}" stroke-width="2" opacity="0.5"/>')

    # every step above is AI-assisted
    b.append(solid(M, 408, CW, 46, "url(#goldbar)", 23))
    b.append(t(W / 2, 439, "✦  AI-POWERED  ✦", 22, WHITE, MONO, "500",
               anchor="middle", ls="4"))

    hw = CW / 2 - 12
    b.append(glass(M, 476, hw, 146, 16, "#e6f2ea", 0.7))
    b.append(glass(M + CW / 2 + 12, 476, hw, 146, 16, "#fbeee6", 0.7))
    b.append(t(M + 26, 520, "UNSAT", 29, GREEN, MONO, "500"))
    blk, _ = block(M + 26, 558, "No violating state exists — over the entire space, "
                                "under a stated model.", hw - 52, 22, 28, INK2, 2)
    b.append(blk)
    b.append(t(M + 26, 614, "Not “none was found”.", 22, GREEN, SANS, "500"))
    b.append(t(M + CW / 2 + 38, 520, "SAT + witness", 29, AMBER, MONO, "500"))
    blk, _ = block(M + CW / 2 + 38, 558, "The exact request, path or call ordering that "
                                         "breaks it — reproducible on your estate.",
                   hw - 52, 22, 28, INK2, 3)
    b.append(blk)

    b.append(t(M, 664, "Industrial practice: AWS (Zelkova, Tiros, Nitro) · Microsoft (Z3) · "
                       "Meta (Infer) · Airbus (Astrée)", 21, MUTED, SANS))
    b.append(chrome(4))
    return page("".join(b))


# ============================================================ 5 · the map
def s05(num=6):
    b = [water("gold"), heading("Nine Solutions, Three Families")]

    bands = [
        ("cyb", "Cybersecurity", "CISO · cloud security · AppSec", 196, 176,
         [(1, "Cloud entitlement proofs"), (2, "Network segmentation proofs"),
          (3, "API-usage conformance"), (4, "Firmware & CVE reachability"),
          (5, "Post-quantum migration")]),
        ("ai", "AI Security", "Head of AI · model risk", 392, 124,
         [(6, "LLM guardrail verification"), (7, "Neurosymbolic assurance")]),
        ("cry", "Crypto Security", "Protocol lead · CTO · VARA", 536, 124,
         [(8, "Smart-contract verification"), (9, "Protocol & consensus proofs")]),
    ]
    for fam, name, buyer, y, h, items in bands:
        f = FAM[fam]
        b.append(glass(M, y, CW, h, 18, f["tint"], 0.38))
        blockpath = (f'M{M},{y+16} a16,16 0 0 1 16,-16 l220,0 l0,{h} l-220,0 '
                     f'a16,16 0 0 1 -16,-16 z')
        b.append(f'<path d="{blockpath}" fill="{f["c"]}"/>')
        b.append(f'<path d="{blockpath}" fill="url(#gloss)" opacity="0.55"/>')
        b.append(f'<rect x="{M+14}" y="{y+1}" width="208" height="1.4" rx="0.7" '
                 f'fill="#ffffff" opacity="0.3"/>')
        b.append(t(M + 26, y + 54, name, fit(name, 196, 29, W_SERIF, 22), WHITE, SERIF, "600"))
        blk, _ = block(M + 26, y + 86, buyer, 200, 19, 24, "#eaf1f8", 2)
        b.append(blk)

        colx = [M + 256, M + 596]
        colmax = [596 - 256 - 48, CW - 596 - 30]
        cols = [items[:3], items[3:]] if len(items) > 3 else [items[:1], items[1:]]
        top = y + 54 if len(items) > 3 else y + 74
        for ci, col in enumerate(cols):
            for ri, (n, label) in enumerate(col):
                cy = top + ri * 40
                b.append(t(colx[ci], cy, str(n), 24, f["c"], MONO, "500"))
                b.append(t(colx[ci] + 32, cy, label,
                           fit(label, colmax[ci], 24, W_SANS, 19), INK2))

    b.append(chrome(num))
    return page("".join(b))


# ====================================================== section divider slides
def section(num, fam, title, items):
    f = FAM[fam]
    b = [water(fam), symbol_field(f["c"]),
         f'<rect x="0" y="0" width="{W}" height="7" fill="{f["c"]}"/>']
    b.append(t(M, 258, title, fit(title, CW, 66, W_SERIF, 46), INK, SERIF, "600"))
    b.append(f'<rect x="{M}" y="286" width="160" height="4" rx="2" fill="{f["c"]}"/>')
    cy = 376
    for n, name in items:
        b.append(f'<circle cx="{M+13}" cy="{cy-9}" r="14" fill="{f["c"]}" opacity="0.13"/>'
                 f'<circle cx="{M+13}" cy="{cy-9}" r="14" fill="url(#gloss)" opacity="0.7"/>')
        b.append(t(M + 13, cy, str(n), 23, f["c"], MONO, "500", anchor="middle"))
        b.append(t(M + 50, cy, name, fit(name, CW - 62, 29, W_SANS, 22), INK2))
        cy += 48
    b.append(chrome(num))
    return page("".join(b))


# ========================================================== solution template
def solution(num, fam, n, title, question, problem, build, output, precedent,
             buyers, note=None):
    f = FAM[fam]
    b = [water(fam), heading(f"{n}. {title}", fam, y=110)]

    # the question it settles
    b.append(glass(M, 152, CW, 86, 16, f["tint"], 0.55))
    b.append(f'<rect x="{M+2}" y="164" width="5" height="62" rx="2.5" fill="{f["c"]}"/>')
    one_line = fit(question, CW - 80, 28, 0.50, 20)
    if one_line >= 24:
        b.append(t(M + 34, 204, question, one_line, INK, SERIF, "600", style="italic"))
    else:
        for i, ln in enumerate(wrap(question, CW - 80, 28, W_SERIF)[:2]):
            b.append(t(M + 34, 192 + i * 34, ln, 28, INK, SERIF, "600", style="italic"))

    lw, rx, rw = 500, M + 534, CW - 534

    # left — the problem, the line worth repeating, then precedent and buyers
    b.append(eyebrow(M, 292, "The problem", f["c"], maxw=lw))
    blk, _ = block(M, 330, problem, lw, 25, 32, INK2, 5)
    b.append(blk)
    if note:
        b.append(hline(M, 472, lw))
        blk, _ = block(M, 500, note, lw, 24, 30, GOLDINK, 2, style="italic")
        b.append(blk)
        ly = 566
    else:
        b.append(hline(M, 492, lw))
        ly = 532
    b.append(t(M, ly, "PRECEDENT", 19, MUTED, MONO, "500", ls="2.4"))
    b.append(t(M + 140, ly, precedent, fit(precedent, lw - 140, 21, W_SANS, 16), INK2))
    b.append(t(M, ly + 30, "BUYERS", 19, MUTED, MONO, "500", ls="2.4"))
    b.append(t(M + 140, ly + 30, buyers, fit(buyers, lw - 140, 21, W_SANS, 16), INK2))

    # right — what we build
    b.append(glass(rx, 262, rw, 314, 18))
    b.append(eyebrow(rx + 26, 304, "What we build", f["c"], maxw=rw - 52))
    bl, _ = bullets(rx + 26, 348, build, rw - 52, 24, 30, 18, INK2, f["c"])
    b.append(bl)

    # bottom — the output
    b.append(glass(M, 612, CW, 74, 16, f["tint"], 0.55))
    b.append(t(M + 32, 658, "OUTPUT", 20, f["c"], MONO, "500", ls="2.6"))
    blk, _ = block(M + 168, 644, output, CW - 200, 22, 28, INK2, 2)
    b.append(blk)

    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 18 · take away
def s18(num=22):
    b = [water("gold"), heading("Take Away")]

    b.append(solid(M, 174, CW, 106, INK, 18, sheen=False, gloss=0, edge=0.16))
    b.append(t(W / 2, 222, "Mathematical rigour to security —", 33, WHITE, SERIF,
               "600", anchor="middle"))
    b.append(t(W / 2, 264, "proof alongside testing, across cloud, AI and crypto.",
               33, GOLD, SERIF, "600", anchor="middle"))

    cols = [("The shift", "Attack path discovery is automated, parallel and cheap. "
                          "A defence that only samples cannot answer one that enumerates."),
            ("The addition", "We do not replace testing, monitoring or the SOC. "
                             "We make one class of controls machine checkable."),
            ("The honesty", "A proof is relative to a model and a specification — both stated. "
                            "We produce the evidence; we do not certify.")]
    cw = (CW - 2 * 24) / 3
    for i, (head, body) in enumerate(cols):
        x = M + i * (cw + 24)
        b.append(f'<rect x="{x:.0f}" y="320" width="{cw-10:.0f}" height="3" rx="1.5" '
                 f'fill="{GOLD}"/>')
        b.append(t(x, 364, head, 29, INK, SERIF, "600"))
        blk, _ = block(x, 404, body, cw - 10, 23, 29, INK2, 6)
        b.append(blk)

    b.append(glass(M, 566, CW, 112, 18, FAM["gold"]["tint"], 0.5))
    b.append(f'<rect x="{M+2}" y="580" width="5" height="84" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(M + 34, 606, "Start here — Micro Assessment of Solution 1",
                     GOLDINK, 20, 2.4, maxw=CW - 80))
    b.append(t(M + 34, 640, "One narrow, high-risk slice. Read-only access, no agent deployed,",
               23, INK2))
    b.append(t(M + 34, 668,
               "weeks not months — and a counter-example on your own systems, or a proof.",
               23, INK2))

    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 19 · thank you
def s19():
    b = [water("gold"), symbol_field(GOLD),
         f'<rect x="0" y="0" width="{W}" height="7" fill="url(#goldbar)"/>']
    b.append(t(M, 268, "Thank You", 84, INK, SERIF, "600"))
    b.append(f'<rect x="{M}" y="300" width="200" height="4" rx="2" fill="{GOLD}"/>')
    b.append(t(M, 378, "Let us prove one property on your estate —", 31, INK2,
               SERIF, "400", style="italic"))
    b.append(t(M, 420, "then judge the method on the result.", 31, INK2,
               SERIF, "400", style="italic"))

    b.append(hline(M, 500, CW))
    b.append(t(M, 552, "Dr. Raghavendra Ramesh", 33, INK, SERIF, "600"))
    b.append(t(M, 588, "Founder & CEO, PrimusCredence", 24, INK2, SANS))
    b.append(t(M, 620, "PhD, IISc Bangalore", 24, INK2, SANS))
    b.append(t(W - M, 552, "raghavendra@primuscredence.com", 27, GOLDINK, MONO,
               "500", anchor="end"))
    b.append(t(W - M, 590, "+971 58 189 2803", 24, INK2, MONO, anchor="end"))
    b.append(t(W - M, 622, "UAE", 24, INK2, MONO, anchor="end"))
    b.append(t(M, 676, "Cloud  |  AI  |  Crypto", 23, GOLDINK, MONO, "500", ls="3.2"))
    return page("".join(b))


# ==================================================================== content
SOLUTIONS = [
    dict(num=8, fam="cyb", n=1,
         title="Cloud Access-Policy & Entitlement Verification",
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
         buyers="Regional CSPs · sovereign hosts"),

    dict(num=9, fam="cyb", n=2,
         title="Network Reachability & Segmentation Proofs",
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

    dict(num=10, fam="cyb", n=3,
         title="API-Usage Conformance",
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
         buyers="Platform and AppSec teams · ISVs",
         note="A correct policy invoked through a misused SDK still leaks. Bounded by the library."),

    dict(num=11, fam="cyb", n=4,
         title="Hypervisor, Firmware & CVE Reachability",
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

    dict(num=12, fam="cyb", n=5,
         title="Post-Quantum Cryptography Migration",
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

    dict(num=14, fam="ai", n=6,
         title="AI and LLM Guardrail Verification",
         question="Not “how often does the agent fail?” but “can it do this at all?”",
         problem="An agent is a non-human identity with delegated privilege and an instruction "
                 "channel the adversary can write to. A guard model judging a model is "
                 "detective, not preventive.",
         build=["Tool-call constraints over identity and arguments",
                "Data-access boundaries in the Solution 1 logic",
                "Composition safety across call sequences"],
         output="A result about the mediation layer, not the model: nothing permitted escapes "
                "the envelope, and no path bypasses it.",
         precedent="Bedrock Automated Reasoning",
         buyers="Banks · sovereign AI · OT · healthcare",
         note="Provable: no rows outside the caller's ACL. Not provable: no PII ever reaches the user."),

    dict(num=15, fam="ai", n=7,
         title="Neurosymbolic Assurance",
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
         buyers="Banks and insurers · government",
         note="LLM autoformalization drafts the theory; the domain expert ratifies it."),

    dict(num=17, fam="cry", n=8,
         title="Formal Verification of Smart Contracts",
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

    dict(num=18, fam="cry", n=9,
         title="Formal Verification of Distributed Protocols",
         question="Does this protocol admit an execution that breaks safety under Byzantine "
                  "faults, asynchrony or partition?",
         problem="These are design defects: no CVE, no patch, no signature, present from the "
                 "first commit. One AWS TLA+ finding needed a 35-step sequence.",
         build=["IVy in decidable EPR: proof or counterexample",
                "Dafny and IronFleet; TLA+ with TLC and TLAPS",
                "Coq/Rocq for consensus and replication safety"],
         output="Machine-checked inductive invariants with the fault, adversary and network "
                "assumptions stated — or the breaking execution.",
         precedent="Pipelined Moonshot in IVy · FMBC 2024",
         buyers="L1/L2 teams · settlement infrastructure"),
]

TITLES = [
    "PrimusCredence — Provable security solutions",
    "Dr. Raghavendra Ramesh",
    "Why Now: The Attacker Industrialised",
    "Automated Reasoning",
    "We Add a Layer to Your Stack",
    "Nine Solutions, Three Families",
    "Cybersecurity Solutions",
    "1. Cloud Access-Policy & Entitlement Verification",
    "2. Network Reachability & Segmentation Proofs",
    "3. API-Usage Conformance",
    "4. Hypervisor, Firmware & CVE Reachability",
    "5. Post-Quantum Cryptography Migration",
    "AI Security Solutions",
    "6. AI and LLM Guardrail Verification",
    "7. Neurosymbolic Assurance",
    "Crypto Security Solutions",
    "8. Formal Verification of Smart Contracts",
    "9. Formal Verification of Distributed Protocols",
    "Why Your Clients Will Ask",
    "What a Provider Can Resell",
    "One Result, Three Registers",
    "Take Away",
    "Thank You",
]


def build():
    os.makedirs(OUT, exist_ok=True)
    pages = {
        1: s01(), 2: s02(), 3: s03(), 4: s04(),
        5: s_stack(5), 6: s05(6),
        7: section(7, "cyb", "Cybersecurity Solutions",
                   [(1, "Cloud access-policy and entitlement verification"),
                    (2, "Network reachability and segmentation proofs"),
                    (3, "API-usage conformance"),
                    (4, "Hypervisor, firmware and CVE reachability"),
                    (5, "Post-quantum cryptography migration")]),
        13: section(13, "ai", "AI Security Solutions",
                    [(6, "Guardrail verification — what an agent may do"),
                     (7, "Neurosymbolic assurance — what an agent may say")]),
        16: section(16, "cry", "Crypto Security Solutions",
                    [(8, "Formal verification of smart contracts"),
                     (9, "Formal verification of distributed protocols")]),
        19: s_demand(19), 20: s_resell(20), 21: s_registers(21),
        22: s18(22), 23: s19(),
    }
    for sol in SOLUTIONS:
        pages[sol["num"]] = solution(**sol)
    for i in range(1, len(TITLES) + 1):
        with open(os.path.join(OUT, f"{i:02d}.svg"), "w") as fh:
            fh.write(pages[i])


# ==========================================================================
# Slides written for a security solutions provider reading the deck as a
# partner: where this sits beside what they already sell, why their clients
# will ask, what they can resell, and what one result is worth.
# ==========================================================================

def chips(x, y, items, maxw, size=21, gap=12, h=40, fill="#ffffff",
          textfill=INK2, edge=LINE, rows_lead=52):
    """Pills laid out left to right, wrapping within maxw."""
    out, cx, cy = [], x, y
    for it in items:
        w = len(it) * size * W_SANS + 36
        if cx + w > x + maxw and cx > x:
            cx, cy = x, cy + rows_lead
        out.append(f'<g filter="url(#liftsm)">{rrect(cx, cy, w, h, fill, h / 2)}'
                   f'{rrect(cx, cy, w, h, "url(#gloss)", h / 2, opacity=0.8)}'
                   f'{rrect(cx, cy, w, h, "none", h / 2, edge, 1)}</g>')
        out.append(t(cx + 18, cy + h / 2 + 7, it, size, textfill))
        cx += w + gap
    return "".join(out), cy + h


def chip_rows(cx, y, rows, size=21, gap=12, h=40, lead=52, fill="#ffffff",
              textfill=INK2, edge=LINE):
    """Rows of pills, each row centred on cx."""
    out = []
    for ri, row in enumerate(rows):
        widths = [len(it) * size * W_SANS + 36 for it in row]
        total = sum(widths) + gap * (len(row) - 1)
        x, ry = cx - total / 2, y + ri * lead
        for it, w in zip(row, widths):
            out.append(f'<g filter="url(#liftsm)">{rrect(x, ry, w, h, fill, h / 2)}'
                       f'{rrect(x, ry, w, h, "url(#gloss)", h / 2, opacity=0.8)}'
                       f'{rrect(x, ry, w, h, "none", h / 2, edge, 1)}</g>')
            out.append(t(x + 18, ry + h / 2 + 7, it, size, textfill))
            x += w + gap
    return "".join(out), y + len(rows) * lead


def s_stack(num=5):
    """Where this sits in a provider's existing stack."""
    b = [water("gold"),
         heading("We Add a Layer to Your Stack, NOT Replace It")]

    b.append(glass(M, 176, CW, 194, 18))
    b.append(eyebrow(M + 30, 214, "What your stack answers today", INK2, 20, 2.6))
    ch, _ = chip_rows(W / 2, 234,
                      [["Pen test & red team", "CSPM / CIEM", "ASPM / SAST"],
                       ["Vulnerability management", "SOC · EDR · SIEM"]])
    b.append(ch)
    b.append(t(M + 30, 352,
               "“We looked, and within the time available we did not find a way in.”",
               23, MUTED, SANS, "400", style="italic"))

    b.append(glass(M, 392, CW, 132, 18, FAM["gold"]["tint"], 0.55))
    b.append(f'<rect x="{M+2}" y="406" width="5" height="104" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(M + 34, 430, "What we add", GOLDINK, 20, 2.6))
    b.append(t(M + 34, 470,
               "“No way it exists — over the whole modelled space.”",
               30, INK, SERIF, "600"))
    b.append(t(M + 34, 502,
               "A preventive control with evidence behind it, re-run on every change.",
               22, INK2))

    b.append(eyebrow(M, 572, "What stays with you", INK2, 20, 2.6))
    keeps = ["Configuration drift, shadow assets and anything outside the model",
             "Insider misuse, and valid credentials used exactly as intended",
             "Detection, response and the rest of the programme you already run"]
    cw = (CW - 2 * 20) / 3
    for i, k in enumerate(keeps):
        x = M + i * (cw + 20)
        blk, _ = block(x, 606, k, cw, 21, 26, INK2, 3)
        b.append(blk)

    b.append(chrome(num))
    return page("".join(b))


def s_demand(num=19):
    """The demand signal: why a provider's clients will ask for this."""
    b = [water("gold"), heading("Why Your Clients Will Ask")]
    b.append(t(M, 184, "Four things happened at once in the GCC.",
               30, INK, SERIF, "600", style="italic"))

    tiles = [
        ("Mandatory replaced voluntary",
         "UAE cyber-resilience obligations now carry penalties of AED 100k–3m."),
        ("A regulator named the technique",
         "VARA expects formal verification where applicable for smart contracts."),
        ("AI rules arrived before AI assurance",
         "Risk-tiered obligations demand evidence the market cannot yet produce."),
        ("Sovereignty is a reachability question",
         "Localisation asks whether regulated data can leave. Solution 2 settles it."),
    ]
    tw, th = (CW - 20) / 2, 106
    for i, (head, body) in enumerate(tiles):
        x = M + (i % 2) * (tw + 20)
        y = 214 + (i // 2) * (th + 16)
        b.append(glass(x, y, tw, th, 16, FAM["gold"]["tint"], 0.42))
        b.append(t(x + 26, y + 42, head, fit(head, tw - 52, 25, W_SANS, 20), INK, SANS, "600"))
        blk, _ = block(x + 26, y + 76, body, tw - 52, 21, 26, INK2, 2)
        b.append(blk)

    b.append(glass(M, 470, CW, 172, 18))
    b.append(eyebrow(M + 30, 508, "Where a finding also lands", INK2, 20, 2.6))
    frames = [("DESC ISR", "1 2 3"), ("NESA / UAE IAS", "2 4"), ("UAE PDPL", "2 3 6"),
              ("SAMA CSF", "1 2 3 6"), ("NCA ECC", "1 2 3 4"), ("VARA", "8"),
              ("UAE AI Act", "6 7"), ("ISO 27001", "1 2 3 5"), ("NIST CSF 2.0", "1–5")]
    colw = (CW - 60) / 3
    for i, (name, nums) in enumerate(frames):
        x = M + 30 + (i % 3) * colw
        y = 550 + (i // 3) * 34
        b.append(t(x, y, name, fit(name, colw - 110, 21, W_SANS, 18), INK2))
        b.append(t(x + colw - 44, y, nums, 20, GOLDINK, MONO, "500", anchor="end"))

    b.append(t(M, 680, "Regulation routes the finding to a second reader. It is not the "
                       "reason to commission it.", 22, MUTED, SANS, "400", style="italic"))
    b.append(chrome(num))
    return page("".join(b))


def s_resell(num=20):
    """The channel case: what a provider can sell, and why it deploys easily."""
    b = [water("gold"), heading("What a Provider Can Resell")]
    b.append(t(M, 184, "We do not certify — so an audit firm or an MSSP is a channel, "
                       "not a rival.", 27, INK, SERIF, "600", style="italic"))

    b.append(glass(M, 214, CW, 82, 16))
    left_txt = "Scanning · posture reporting · monitoring"
    right_txt = "Provable control effectiveness"
    b.append(t(M + 30, 262, left_txt, fit(left_txt, 420, 25, W_SANS, 20), MUTED, SANS))
    b.append(f'<path d="M{M+476},254 l34,0 M{M+502},246 l8,8 -8,8" stroke="{GOLD}" '
             f'stroke-width="2.5" fill="none"/>')
    b.append(t(M + CW - 30, 262, right_txt,
               fit(right_txt, CW - 30 - 546, 25, W_SANS, 19), GOLDINK, SANS, "600",
               anchor="end"))

    lw, rx, rw = 470, M + 504, CW - 504
    b.append(eyebrow(M, 356, "The commercial move", GOLDINK, maxw=lw))
    bl, _ = bullets(M, 406, [
        "Specialist capability inside bids you already win",
        "You keep the client relationship and the contract",
    ], lw, 25, 33, 26, INK2, GOLD)
    b.append(bl)

    b.append(glass(rx, 330, rw, 214, 18, FAM["gold"]["tint"], 0.4))
    b.append(eyebrow(rx + 26, 374, "Why it deploys easily", GOLDINK, maxw=rw - 52))
    bl, _ = bullets(rx + 26, 416, [
        "Read-only access, no agent on any host",
        "No scanning window, no production traffic",
    ], rw - 52, 24, 31, 26, INK2, GOLD)
    b.append(bl)

    b.append(t(M, 622, "Read-only and agentless, so it clears change advisory in one pass.",
               22, GOLDINK, SANS, "500"))
    b.append(t(M, 656, "We produce the technical evidence. Your assessor keeps the opinion.",
               22, GOLDINK, SANS, "500"))
    b.append(chrome(num))
    return page("".join(b))


def s_registers(num=21):
    """One analysis, three deliverables — the evidence multiplier."""
    b = [water("gold"), heading("One Result, Three Registers")]

    cols = [("First line", "Engineering and security operations",
             "The property, its model and assumptions, and either the proof or a "
             "reproducible attack path."),
            ("Second line", "Risk",
             "Likelihood moved off a qualitative guess, with residual risk and the "
             "model's limits stated."),
            ("Third line", "Internal audit and compliance",
             "A clause-mapped control assertion: objective, status, owner and "
             "re-verification date.")]
    cw = (CW - 2 * 20) / 3
    for i, (head, sub, body) in enumerate(cols):
        x = M + i * (cw + 20)
        b.append(glass(x, 186, cw, 324, 18))
        b.append(f'<rect x="{x+26}" y="218" width="46" height="4" rx="2" fill="{GOLD}"/>')
        b.append(t(x + 26, 264, head, 29, INK, SERIF, "600"))
        blk, _ = block(x + 26, 296, sub, cw - 52, 20, 25, GOLDINK, 2)
        b.append(blk)
        blk, _ = block(x + 26, 360, body, cw - 52, 22, 28, INK2, 5)
        b.append(blk)

    b.append(glass(M, 546, CW, 88, 16, FAM["gold"]["tint"], 0.5))
    b.append(f'<path d="M{M+34},590 l9,9 15,-19" stroke="{GOLD}" stroke-width="2.8" '
             f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(t(M + 74, 598, "Design → operating effectiveness · attaches to your "
                            "GRC records · assessors probe less", 21, INK2))

    b.append(t(M, 674, "The first register is the product. The second and third make it "
                       "worth more than it cost.", 22, MUTED, SANS, "400", style="italic"))
    b.append(chrome(num))
    return page("".join(b))


if __name__ == "__main__":
    build()
    print(f"wrote {len(TITLES)} slides to {OUT}")
