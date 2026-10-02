#!/usr/bin/env python3
"""Builds the PrimusCredence slide deck.

One .svg per slide in slides/, stitched together by index.html.

Geometry is 16:10 (1187 x 742 units), the MacBook / widescreen aspect, so the
deck fills a laptop display edge to edge rather than letterboxing an A5 page.
Body copy sits at 23-26 units and nothing is smaller than 19 (~a comfortable
on-screen minimum); every text block has a line budget so nothing overflows.

Every slide is white, with soft tinted blooms behind frosted-glass panels.
Text is wrapped against measured average glyph advances (see W_SANS etc.),
and every block has a line budget, so the layout does not overflow.
"""

import os

W, H = 1187, 742            # 16:10 — a MacBook / widescreen display
M = 68                      # page margin
CW = W - 2 * M              # content width (1051)

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

BLOOM_IDS = {GOLD: "bl-gold", GOLDINK: "bl-goldink", INK: "bl-ink",
             FAM["cyb"]["c"]: "bl-cyb", FAM["ai"]["c"]: "bl-ai",
             FAM["cry"]["c"]: "bl-cry"}
BLOOM_GRADS = "".join(
    f'<radialGradient id="{i}"><stop offset="0" stop-color="{c}" '
    f'stop-opacity="1"/><stop offset="0.45" stop-color="{c}" stop-opacity="0.45"/>'
    f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
    for c, i in BLOOM_IDS.items())

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
{BLOOM_GRADS}</defs>'''


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
    """A soft wash of colour. Drawn as a radial gradient rather than a blurred
    circle: a Gaussian blur forces the renderer to rasterise the whole page,
    which made the print PDF enormous."""
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * 1.9:.0f}" '
            f'fill="url(#{BLOOM_IDS[color]})" opacity="{op}"/>')


def water(fam="gold"):
    """The background wash: soft blooms in brand gold and the family hue."""
    f = FAM[fam]
    return (bloom(W - 170, 110, 210, f["c"], 0.16) +
            bloom(130, 665, 230, GOLD, 0.13) +
            bloom(W / 2, 380, 260, f["c"], 0.05))


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
    b.append(t(M, 384, "Provable Security", 46, GOLDINK, SERIF, "600"))

    # No name or email here: the founder is introduced on slide 2 and the
    # contact details are on the closing slide.
    b.append(hline(M, 592, CW))
    b.append(t(M, 644, "primuscredence.com", 27, GOLDINK, MONO, "500"))
    b.append(t(W - M, 644, "UAE", 24, INK2, MONO, anchor="end"))
    return page("".join(b))


# ============================================================ about
def s02(num=2):
    b = [water("gold"), heading("Dr. Raghavendra Ramesh")]
    b.append(t(M, 176, "Founder & CEO, PrimusCredence", 26, GOLDINK, SANS, "500"))
    b.append(eyebrow(M, 232, "22+ years of experience in provable security",
                     INK2, 20, 2.4, maxw=510))

    steps = [("PhD, IISc Bangalore", "Model checking for information-flow security"),
             ("Oracle Labs · 2014–2019", "Java vulnerability detection"),
             ("ConsenSys R&D · 2019–2021", "Cross-chain protocols, consensus verification"),
             ("Supra · VP of R&D · 2021–ongoing", "BFT design & FV, bridges, DeFi & Crypto")]
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

    b.append(chrome(num))
    return page("".join(b))


# ============================================================ AI industrialises the attacker
def s03(num=7):
    b = [water("gold"), heading("AI Industrialises the Attacker")]
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
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ the method
def s04(num=11):
    b = [water("gold"), heading("Automated Reasoning")]
    b.append(t(M, 184, "Proof establishes that bad things cannot happen.",
               30, INK, SERIF, "600", style="italic"))

    steps = [("1", "Formalise", "Your existing artefact becomes a logical model"),
             ("2", "State", "The bad state you fear becomes a formula"),
             ("3", "Solve", "Z3, Batfish, IVy, TLA+ decide it; CBMC to a bound"),
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

    b.append(t(M, 648, "Not every property is decidable, and a proof holds only for the "
                       "property and model stated.", 20, MUTED, SANS))
    b.append(t(M, 676, "Industrial practice: AWS · Microsoft · Meta · Airbus.", 20, MUTED, SANS))
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ the map
def sol_card(x, y, w, h, fam, n, title, sub):
    """One solution as a framed card: a number badge, a title, a one-line gloss."""
    f = FAM[fam]
    out = [glass(x, y, w, h, 16, f["tint"], 0.4)]
    out.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{f["c"]}"/>')
    out.append(orb(x + 40, y + 42, 18, f["c"]))
    out.append(t(x + 40, y + 51, str(n), 22, WHITE, MONO, "500", anchor="middle"))
    ty = y + 40
    for i, ln in enumerate(wrap(title, w - 92, 24, W_SERIF)[:2]):
        out.append(t(x + 70, ty + i * 30, ln, 24, INK, SERIF, "600"))
    out.append(t(x + 24, y + h - 26, sub, fit(sub, w - 48, 20, W_SANS, 16), f["c"], SANS, "500"))
    return "".join(out)


def s05(num=12):
    b = [water("gold"), heading("Solutions")]
    b.append(t(M, 176, "One method — four solutions, across the application and its seams.",
               26, INK, SERIF, "600", style="italic"))

    # four cyber solutions, no family split — a 2×2 grid.
    sols = [(1, "App entitlement proofs", "Who can reach what?"),
            (2, "Network segmentation", "Any path across zones?"),
            (3, "App & API conformance", "SDKs used correctly?"),
            (4, "Post-quantum migration", "Bound on a PQC base?")]
    cw2 = (CW - 20) / 2
    for i, (n, title, sub) in enumerate(sols):
        x = M + (i % 2) * (cw2 + 20)
        y = 226 + (i // 2) * (210 + 20)
        b.append(sol_card(x, y, cw2, 210, "cyb", n, title, sub))

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
def s18(num=21):
    b = [water("gold"), heading("Take Away")]

    b.append(solid(M, 174, CW, 106, INK, 18, sheen=False, gloss=0, edge=0.16))
    b.append(t(W / 2, 222, "Mathematical rigour to security —", 33, WHITE, SERIF,
               "600", anchor="middle"))
    b.append(t(W / 2, 264, "proof alongside testing, across apps and AI.",
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


# --- QR code for primuscredence.com (25x25 modules, version 2, level M) -----
# Precomputed so the build has no QR dependency. Regenerate with:
#   python3 -c "import segno;[print(''.join('1' if c else '0' for c in r)) \
#     for r in segno.make('https://primuscredence.com', error='m').matrix]"
QR = [
    "1111111011011111101111111",
    "1000001001101100101000001",
    "1011101000111001001011101",
    "1011101011001111101011101",
    "1011101010100111101011101",
    "1000001011111100001000001",
    "1111111010101010101111111",
    "0000000011100010100000000",
    "1000101111101000111111001",
    "0010110110001011110011010",
    "1101101100110111010001100",
    "1011100000001000111000110",
    "0100011100101000011001111",
    "1111110000001111100010010",
    "0001011111011101011111100",
    "0000000100111010100110110",
    "1111101110011000111111100",
    "0000000011010111100010000",
    "1111111010011010101010000",
    "1000001001101010100011111",
    "1011101010111010111111100",
    "1011101000010011011100111",
    "1011101001111110111001010",
    "1000001001000000001111110",
    "1111111011001001011000111",
]


def qr(x, y, size, quiet=2):
    """A QR code for primuscredence.com drawn as one path, top-left at x, y.

    size is the side of the finished block including the quiet zone.
    """
    n = len(QR)
    u = size / (n + 2 * quiet)
    d = []
    for r, row in enumerate(QR):
        c = 0
        while c < n:
            if row[c] == "1":
                c2 = c
                while c2 + 1 < n and row[c2 + 1] == "1":
                    c2 += 1
                px = x + (quiet + c) * u
                py = y + (quiet + r) * u
                d.append(f"M{px:.2f} {py:.2f}h{(c2-c+1)*u:.2f}v{u:.2f}h{-(c2-c+1)*u:.2f}z")
                c = c2 + 1
            else:
                c += 1
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" '
            f'rx="6" fill="{WHITE}"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" '
            f'rx="6" fill="none" stroke="{LINE}"/>'
            f'<path d="{"".join(d)}" fill="{INK}"/>')


# ============================================================ 19 · thank you
def s19():
    b = [water("gold"), symbol_field(GOLD),
         f'<rect x="0" y="0" width="{W}" height="7" fill="url(#goldbar)"/>']
    b.append(t(M, 268, "Thank You", 84, INK, SERIF, "600"))
    b.append(f'<rect x="{M}" y="300" width="200" height="4" rx="2" fill="{GOLD}"/>')
    qx = W - M - 158
    b.append(qr(qx, 300, 158))
    b.append(t(qx + 79, 484, "primuscredence.com", 21, INK2, MONO, anchor="middle"))

    b.append(hline(M, 500, CW))
    b.append(t(M, 552, "Dr. Raghavendra Ramesh", 33, INK, SERIF, "600"))
    b.append(t(M, 588, "Founder & CEO, PrimusCredence", 24, INK2, SANS))
    b.append(t(M, 620, "PhD, IISc Bangalore", 24, INK2, SANS))
    b.append(t(W - M, 552, "raghavendra@primuscredence.com", 27, GOLDINK, MONO,
               "500", anchor="end"))
    b.append(t(W - M, 590, "+971 58 189 2803", 24, INK2, MONO, anchor="end"))
    b.append(t(W - M, 622, "UAE", 24, INK2, MONO, anchor="end"))
    b.append(t(M, 676, "Provable Security for Applications", 22, GOLDINK, MONO,
               "500", ls="1.8"))
    return page("".join(b))


# ==================================================================== content
SOLUTIONS = [
    dict(num=13, fam="cyb", n=1,
         title="Application Access-Policy & Entitlement Verification",
         question="What can each app role, API token and public user do inside the app — "
                  "and can any of them reach what they should not?",
         problem="An app's authorisation lives in its own database and admin panel — which "
                 "role reads which type, what the Public role exposes. No SAST, CSPM or "
                 "CNAPP reads it; DAST only samples.",
         build=["The app's roles, API tokens and public users, into Cedar",
                "SymCC decides over all requests — BOLA, BFLA, BOPLA",
                "CheckNoNewAccess gates every role change in CI"],
         output="Proof that no role, token or public user reaches what it must not — over all "
                "requests — or the exact request that breaks it.",
         precedent="Cedar + SymCC → Cedar Analysis",
         buyers="Platform & AppSec teams · ISVs",
         note="Portable: it reads the app's own config, so it holds on-prem, not only in cloud."),

    dict(num=14, fam="cyb", n=2,
         title="Network Reachability & Segmentation Proofs",
         question="Does any path exist from an untrusted zone to this subnet — and does "
                  "east-west segmentation actually hold?",
         problem="Probing tests the paths you thought of, when you ran it. Reachability is a "
                 "property of the configuration — routes, security groups, firewall rules — "
                 "not of the packets you send.",
         build=["Hybrid and on-prem estate modelled with Batfish",
                "Soufflé and Z3 over the cloud topology, statically",
                "Microsegmentation checked against the declared policy"],
         output="A proof that no path exists — or the path, hop by hop, with the rule that "
                "permits it and the owner of that rule.",
         precedent="AWS Tiros → VPC Reachability Analyzer",
         buyers="Regulated finance · OT & critical infra · sovereign cloud",
         note="No scanning window, no production traffic — it re-runs on every change."),

    dict(num=15, fam="cyb", n=3,
         title="Application and API-Usage Conformance",
         question="Does our own code use the APIs it is built on — cloud, credential and crypto "
                  "SDKs, and its own data-access calls — the way their contracts require?",
         problem="Cloud and app APIs are protocols, not calls. Undrained pagination, a logged "
                 "credential, an object fetched by request ID without an ownership check — all "
                 "compile and pass review. Same risk on-prem or in cloud.",
         build=["Object-ownership (BOLA/IDOR) and auth-routing patterns",
                "A conformance gate for library publishers",
                "PR-gate CI on Soot, CodeQL and Infer"],
         output="The call site, the taint trace, the pattern violated and the corrected call "
                "sequence — plus which patterns were checked.",
         precedent="AWS RAPID → CodeGuru · 76% accepted",
         buyers="Platform and AppSec teams · ISVs",
         note="A correct policy invoked through a misused SDK still leaks. Bounded by the library."),

    dict(num=16, fam="cyb", n=4,
         title="Post-Quantum Cryptography Migration",
         question="On an already quantum-safe cloud, does the app's integration still "
                  "authenticate the right party in every session?",
         problem="The cloud's PQC transport can be formally proven and the app on top still "
                 "relayed or downgraded. Hybrid migration adds identity-binding and combiner "
                 "failures that code review ships past.",
         build=["Discovery and a versioned CBOM, gaps listed",
                "The app-to-cloud integration protocol, transport proof discharged",
                "Identity, channel and downgrade binding, over all sessions"],
         output="The CBOM and a sequenced plan; then a proof the app's integration preserves "
                "authentication and secrecy on the verified base — or the relay that breaks it.",
         precedent="PQ-SSH counterexample, then proved (2024)",
         buyers="Gov ID · PKI · banks · healthcare · defence",
         note="Verified app crypto on an already-verified cloud — proof end to end."),

]

TITLES = [
    "PrimusCredence — Provable Security for Applications",
    "Dr. Raghavendra Ramesh",
    "Where the Risk Actually Lives",
    "OWASP 2025 — Access Control & Misconfiguration",
    "Apps Misuse the APIs They Run On",
    "The Base Went Post-Quantum. Are the Apps Ready?",
    "AI Industrialises the Attacker",
    "Segmentation Is Asserted, Not Proven",
    "Why Today's Security Stack Isn't Enough",
    "Proof — Now Feasible",
    "Automated Reasoning",
    "Solutions",
    "1. Application Access-Policy & Entitlement Verification",
    "2. Network Reachability & Segmentation Proofs",
    "3. Application & API-Usage Conformance",
    "4. Post-Quantum Cryptography Migration",
    "Our Approach",
    "Why the Provider's Clients Will Ask",
    "What a Provider Can Resell",
    "One Result, Three Registers",
    "Take Away",
    "Thank You",
]


def build():
    os.makedirs(OUT, exist_ok=True)
    pages = {
        1: s01(),
        2: s02(2),
        3: s_layers(3),
        4: s_owasp(4), 5: s_api(5), 6: s_pqc(6), 7: s03(7),
        8: s_network(8),
        9: s_landscape(9), 10: s_feasible(10), 11: s04(11), 12: s05(12),
        17: s_shortterm(17), 18: s_demand(18),
        19: s_resell(19), 20: s_registers(20),
        21: s18(21), 22: s19(),
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


def s_demand(num=18):
    """The demand signal: why a provider's existing clients will ask for this."""
    b = [water("gold"),
         heading("Why the Provider's Clients Will Ask")]
    b.append(t(M, 184, "Four things happened at once in the GCC — and their clients feel all "
                       "four.", 28, INK, SERIF, "600", style="italic"))

    tiles = [
        ("Mandatory replaced voluntary",
         "UAE cyber-resilience obligations now carry penalties of AED 100k–3m."),
        ("Assurance shifted to evidence",
         "Regulators increasingly ask for demonstrable control effectiveness, not attestation."),
        ("Third-party risk is now in scope",
         "Rules increasingly require evidence that integrations and components are controlled."),
        ("Sovereignty is a reachability question",
         "Localisation asks whether regulated data can leave — our reachability proofs settle it."),
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
    frames = [("DESC ISR", "1 2 3"), ("NESA / UAE IAS", "2"), ("UAE PDPL", "2 3"),
              ("SAMA CSF", "1 2 3"), ("NCA ECC", "1 2 3"), ("PCI DSS 4.0", "1 2 3"),
              ("ISO 27001", "1 2 3 4"), ("CIS Controls", "1 2 3"), ("NIST CSF 2.0", "1–4")]
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


def arrow_r(x1, x2, y, color=GOLD, sw=2.6):
    """A thin horizontal arrow pointing right, from x1 to x2."""
    return (f'<path d="M{x1:.0f},{y:.0f} L{x2-11:.0f},{y:.0f}" stroke="{color}" '
            f'stroke-width="{sw}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x2-13:.0f},{y-7:.0f} l13,7 -13,7" stroke="{color}" '
            f'stroke-width="{sw}" fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


def s_vision(num=16):
    """The long-term vision: PrimusCredence as the assurance hub — it takes the
    mandate from clients and awards the build to cybersecurity vendors."""
    b = [water("gold"), heading("The Long-Term Vision — the Assurance Hub")]
    b.append(t(M, 184, "PrimusCredence becomes the hub: it takes the mandate, and awards "
                       "the build.", 27, INK, SERIF, "600", style="italic"))

    # the three nodes, lifted up a little so the row is not crowded against the
    # bottom band; node titles are set at one uniform size across all nodes.
    ny, nh, nw = 276, 210, 290
    lx = M
    cx = M + nw + 90          # 448
    rx = M + 2 * (nw + 90)    # 828
    ts = 27                   # one shared title size for every node

    # left — the clients who bring the mandate
    b.append(glass(lx, ny, nw, nh, 18, FAM["gold"]["tint"], 0.42))
    b.append(eyebrow(lx + 26, ny + 44, "The mandate", GOLDINK, 20, 2.4, maxw=nw - 52))
    b.append(t(lx + 26, ny + 92, "Government", ts, INK, SERIF, "600"))
    b.append(t(lx + 26, ny + 126, "& enterprises", ts, INK, SERIF, "600"))
    b.append(t(lx + 26, ny + 166, "They bring the problem.",
               fit("They bring the problem.", nw - 52, 21, W_SANS, 17), INK2))

    # centre — the hub
    b.append(solid(cx, ny, nw, nh, INK, 18, sheen=False, gloss=0, edge=0.16))
    b.append(f'<text x="{cx+nw/2:.0f}" y="{ny+74}" font-family="{SERIF}" font-size="30" '
             f'font-weight="600" text-anchor="middle"><tspan fill="{WHITE}">Primus</tspan>'
             f'<tspan fill="{GOLD}">Credence</tspan></text>')
    b.append(f'<rect x="{cx+nw/2-54:.0f}" y="{ny+90}" width="108" height="3" rx="1.5" '
             f'fill="{GOLD}"/>')
    b.append(t(cx + nw / 2, ny + 122, "THE ASSURANCE HUB", 18, GOLD, MONO, "500",
               anchor="middle", ls="2.6"))
    for i, ln in enumerate(["Takes the mandate.", "Owns the proof.", "Awards the build."]):
        b.append(t(cx + nw / 2, ny + 152 + i * 22, ln, 20, WHITE, SANS, anchor="middle"))

    # right — the cybersecurity vendors who deliver
    b.append(glass(rx, ny, nw, nh, 18, FAM["cyb"]["tint"], 0.42))
    b.append(eyebrow(rx + 26, ny + 44, "The build", FAM["cyb"]["c"], 20, 2.4, maxw=nw - 52))
    b.append(t(rx + 26, ny + 92, "Cybersecurity", ts, INK, SERIF, "600"))
    b.append(t(rx + 26, ny + 126, "vendors", ts, INK, SERIF, "600"))
    b.append(t(rx + 26, ny + 166, "They deliver the build.",
               fit("They deliver the build.", nw - 52, 21, W_SANS, 17), INK2))

    # forward flow across the top of the nodes
    b.append(arrow_r(lx + nw + 6, cx - 6, ny + 46))
    b.append(t((lx + nw + cx) / 2, ny + 32, "orders", 19, GOLDINK, MONO, "500",
               anchor="middle", ls="1.5"))
    b.append(arrow_r(cx + nw + 6, rx - 6, ny + 46, FAM["cyb"]["c"]))
    b.append(t((cx + nw + rx) / 2, ny + 32, "contracts", 19, FAM["cyb"]["c"], MONO, "500",
               anchor="middle", ls="1.5"))

    b.append(t(W / 2, 514, "Proof, assurance and single-point accountability flow back to "
                           "the client.", 21, MUTED, SANS, "400", anchor="middle",
               style="italic"))

    b.append(glass(M, 548, CW, 128, 18, FAM["gold"]["tint"], 0.5))
    b.append(f'<rect x="{M+2}" y="562" width="5" height="100" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(M + 34, 588, "Where this goes", GOLDINK, 20, 2.4, maxw=CW - 80))
    b.append(t(M + 34, 624, "The client signs with PrimusCredence — we hold the mandate and "
                            "the proof,", 24, INK2))
    b.append(t(M + 34, 654, "and award the build to the cybersecurity vendors best placed to "
                            "deliver it.", 24, INK2))

    b.append(chrome(num))
    return page("".join(b))


def s_shortterm(num=17):
    """Our approach: we partner with cybersecurity solutions providers, adding
    provable control effectiveness to their bids and reaching their clients."""
    b = [water("gold"), heading("Our Approach")]
    b.append(t(M, 184, "We partner with cybersecurity solutions providers, adding provable "
                       "assurance.", 26, INK, SERIF, "600", style="italic"))

    # how we partner — no named firms
    b.append(glass(M, 220, CW, 146, 18, FAM["gold"]["tint"], 0.42))
    b.append(eyebrow(M + 30, 258, "How we partner — through the providers", GOLDINK, 20, 2.6,
                     maxw=CW - 60))
    pts = [
        "Provable control effectiveness inside their bids.",
        "They keep the client relationship and the contract.",
        "We don't certify — a channel, not a rival.",
    ]
    colw = (CW - 60 - 2 * 24) / 3
    for i, p in enumerate(pts):
        x = M + 30 + i * (colw + 24)
        b.append(f'<rect x="{x:.0f}" y="296" width="30" height="3" rx="1.5" fill="{GOLD}"/>')
        blk, _ = block(x, 326, p, colw, 21, 26, INK2, 2)
        b.append(blk)

    by = 392
    b.append(glass(M, by, CW, 288, 18))
    b.append(eyebrow(M + 30, by + 36, "Whom we reach through them — the GCC client base",
                     INK2, 20, 2.6, maxw=CW - 60))
    sectors = [
        ("Government & sovereign", ["UAE Digital Govt", "Smart Dubai", "Abu Dhabi Govt"]),
        ("Aviation & CNI", ["dans · air navigation", "DEWA", "Regional utilities"]),
        ("Energy, oil & gas", ["ADNOC", "Aramco", "OT operators"]),
        ("Banking & finance", ["Regional banks", "Sovereign wealth funds", "FinTechs"]),
        ("Telecom & cloud", ["e& · Etisalat", "Core42 · G42", "STC Cloud"]),
    ]
    ry = by + 78
    for label, names in sectors:
        b.append(t(M + 30, ry, label, 23, INK, SANS, "600"))
        ch, _ = chips(M + 320, ry - 27, names, CW - 320 - 30, 20, 12, 38,
                      textfill=INK2, edge=LINE)
        b.append(ch)
        ry += 42

    b.append(chrome(num))
    return page("".join(b))


def s_resell(num=19):
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


def s_registers(num=20):
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


def s_invest(num=21):
    """Early-stage raise: what the money buys — feasibility studies and pilots."""
    b = [water("gold"), heading("Investment")]
    b.append(t(M, 184, "Early-stage — we raise to prove the method, not to scale ahead "
                       "of proof.", 28, INK, SERIF, "600", style="italic"))

    tw = (CW - 24) / 2
    cards = [
        ("Feasibility studies",
         "Validate each solution on real client artefacts — a claim becomes a proof, "
         "or a counter-example, on systems that matter.",
         ["De-risk four solutions on live estates",
          "Turn research into productised checks",
          "Reference results to show the next buyer"]),
        ("Pilot projects",
         "Co-funded pilots with named design partners: one narrow, high-risk slice, "
         "delivered end to end.",
         ["Paid proofs-of-value with design partners",
          "Read-only and agentless — fast to deploy",
          "Each pilot becomes a reusable case study"]),
    ]
    for i, (head, intro, items) in enumerate(cards):
        x = M + i * (tw + 24)
        b.append(glass(x, 220, tw, 350, 18, FAM["gold"]["tint"], 0.4))
        b.append(f'<rect x="{x+26}" y="252" width="46" height="4" rx="2" fill="{GOLD}"/>')
        b.append(t(x + 26, 296, head, 30, INK, SERIF, "600"))
        blk, _ = block(x + 26, 332, intro, tw - 52, 22, 28, INK2, 3)
        b.append(blk)
        bl, _ = bullets(x + 26, 432, items, tw - 52, 22, 30, 12, INK2, GOLD, maxlines=1)
        b.append(bl)

    b.append(glass(M, 592, CW, 92, 16, FAM["gold"]["tint"], 0.5))
    b.append(f'<rect x="{M+2}" y="606" width="5" height="64" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(M + 34, 632, "The ask — investment in the order of", GOLDINK,
                     20, 2.4, maxw=640))
    b.append(t(M + 34, 666, "Toward feasibility studies and co-funded pilots — evidence "
                            "first. Milestones on request.", 23, INK2))
    b.append(t(W - M - 30, 644, "USD 50K", 46, GOLDINK, SERIF, "600", anchor="end"))

    b.append(chrome(num))
    return page("".join(b))


# ==========================================================================
# Motivation slides: why the problem is everywhere (access control and
# misconfiguration, apps and APIs, post-quantum, AI), why the current stack
# is not enough, why proof is now feasible, and why AI agents need it.
# ==========================================================================

def stat_tile(x, y, w, h, big, sub, tint="gold", accent=None):
    """A framed statistic: a large figure over a wrapped caption."""
    f = FAM[tint]
    accent = accent or f["c"]
    out = [glass(x, y, w, h, 16, f["tint"], 0.45)]
    out.append(t(x + 24, y + 58, big, fit(big, w - 48, 44, W_SERIF, 26), accent, SERIF, "600"))
    blk, _ = block(x + 24, y + 92, sub, w - 48, 20, 25, INK2, 3)
    out.append(blk)
    return "".join(out)


# ===================================================== anchor · the stack
def s_layers(num=3):
    """The anchor diagram for the whole talk: the application stack. Plugins run
    inside the app; the app sits on a proven cloud base; and between them lies the
    seam — APIs, third-party libraries, and the PQC app-to-cloud binding — where
    access control and misconfiguration actually fail. The cloud base (IAM,
    network, PQC transport) is already formally proven; the app and the seam are
    not, and that is the layer we prove."""
    b = [water("gold"), heading("Where the Risk Actually Lives")]
    b.append(t(M, 176, "The cloud base is proven. The app above it — and the seams between — "
                       "are not.", 25, INK, SERIF, "600", style="italic"))

    cyb, cry = FAM["cyb"], FAM["cry"]
    sx, sw = M, 716                 # stack column: 68 .. 784
    vx = 808
    vw = M + CW - vx                # verdict column: 808 .. 1119

    # ---- layer 1 — plugins / extensions (sit on top of the app) -------------
    y1, h1 = 206, 58
    b.append(glass(sx, y1, sw, h1, 14, FAM["gold"]["tint"], 0.45))
    b.append(t(sx + 26, y1 + 26, "Third-party plugins & extensions", 22, INK, SANS, "600"))
    b.append(t(sx + 26, y1 + 48, "Run inside the app — and inherit its privilege", 19, INK2))

    # ---- layer 2 — the application (the hero) --------------------------------
    y2, h2 = 274, 150
    b.append(glass(sx, y2, sw, h2, 16, cyb["tint"], 0.5))
    b.append(f'<rect x="{sx}" y="{y2}" width="6" height="{h2}" rx="3" fill="{cyb["c"]}"/>')
    b.append(t(sx + 30, y2 + 48, "APPLICATION", 30, INK, SERIF, "600"))
    b.append(t(sx + 30, y2 + 82, "Its own roles, API tokens and public users — the authorisation",
               22, INK2))
    b.append(t(sx + 30, y2 + 110, "logic and configuration in its database and admin panel",
               22, INK2))
    b.append(t(sx + 30, y2 + 138, "OWASP #1 Broken Access Control · #2 Misconfiguration — in "
                                  "100% of apps", fit("OWASP #1 Broken Access Control · #2 "
              "Misconfiguration — in 100% of apps", sw - 60, 20, W_SANS, 16), cyb["c"],
              SANS, "600"))

    # ---- the seam — where app meets cloud and third-party libraries ---------
    y3, h3 = 436, 96
    b.append(glass(sx, y3, sw, h3, 14, FAM["gold"]["tint"], 0.4))
    b.append(f'<rect x="{sx+2}" y="{y3+12}" width="5" height="{h3-24}" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(sx + 26, y3 + 30, "The app ↔ cloud & library seam", GOLDINK, 19, 2.2,
                     maxw=sw - 52))
    seam = [("Access control via APIs", cyb["c"]), ("SDK & library usage", cyb["c"]),
            ("PQC app↔cloud binding", cry["c"])]
    seamx = [sx + 28, sx + 272, sx + 480]
    for (lab, col), xx in zip(seam, seamx):
        b.append(f'<circle cx="{xx}" cy="{y3+66}" r="4.5" fill="{col}"/>')
        b.append(t(xx + 16, y3 + 72, lab, 19, INK2, SANS, "500"))

    # ---- layer 4 — the cloud / infrastructure base (proven) -----------------
    y4, h4 = 548, 128
    b.append(glass(sx, y4, sw, h4, 16, "#e6f2ea", 0.6))
    b.append(f'<rect x="{sx}" y="{y4}" width="6" height="{h4}" rx="3" fill="{GREEN}"/>')
    b.append(t(sx + 30, y4 + 44, "CLOUD & INFRASTRUCTURE", 26, INK, SERIF, "600"))
    b.append(t(sx + 30, y4 + 74, "VMs · containers · databases · queues · object storage · IAM "
                                 "· network", fit("VMs · containers · databases · queues · object "
              "storage · IAM · network", sw - 60, 20, W_SANS, 16), INK2))
    b.append(t(sx + 30, y4 + 106, "Access control, network & PQC transport — proven: Zelkova, "
                                  "Tiros, ML-KEM",
               fit("Access control, network & PQC transport — proven: Zelkova, Tiros, ML-KEM",
                   sw - 60, 20, W_SANS, 16), GREEN, SANS, "600"))

    # ---- braces tying each group to its verdict card ------------------------
    b.append(arrow_r(sx + sw + 4, vx - 4, 369, GOLDINK))
    b.append(arrow_r(sx + sw + 4, vx - 4, 612, GREEN))

    # ---- verdict card 1 — unproven (plugins + app + seam) -------------------
    b.append(glass(vx, 206, vw, 326, 16, FAM["gold"]["tint"], 0.5))
    b.append(f'<rect x="{vx+2}" y="220" width="5" height="298" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(vx + 26, 250, "Unproven today", GOLDINK, 19, 2.2, maxw=vw - 52))
    b.append(t(vx + 26, 290, "Where the", 27, INK, SERIF, "600"))
    b.append(t(vx + 26, 322, "breaches are", 27, INK, SERIF, "600"))
    blk, _ = block(vx + 26, 362, "The app's own access control, its plugins, and the API, "
                                 "library and PQC seams beneath it.", vw - 52, 21, 27, INK2, 5)
    b.append(blk)
    b.append(t(vx + 26, 510, "→ This is what we prove.", 21, GOLDINK, SANS, "600"))

    # ---- verdict card 2 — proven base (cloud) -------------------------------
    b.append(glass(vx, 548, vw, 128, 16, "#e6f2ea", 0.6))
    b.append(f'<rect x="{vx+2}" y="562" width="5" height="100" rx="2.5" fill="{GREEN}"/>')
    b.append(eyebrow(vx + 26, 582, "Proven base", GREEN, 19, 2.2, maxw=vw - 52))
    blk, _ = block(vx + 26, 614, "Cloud IAM, network & PQC transport — already formally "
                                 "verified.", vw - 52, 19, 24, INK2, 3)
    b.append(blk)

    b.append(chrome(num))
    return page("".join(b))


# ================================================= network reachability
def s_network(num=8):
    """Motivation: network reachability & segmentation. Once inside, lateral
    movement is fast, and segmentation is asserted far more than it is proven."""
    b = [water("gold"), heading("Segmentation Is Asserted, Not Proven")]
    b.append(t(M, 184, "Once inside, lateral movement is the phase that turns an incident "
                       "into a breach.", 27, INK, SERIF, "600", style="italic"))

    stats = [("29 min", "average breakout to the first lateral move (2025)"),
             ("27 sec", "the fastest breakout ever observed"),
             ("82%", "of intrusions were malware-free — valid access, not code")]
    tw = (CW - 2 * 20) / 3
    for i, (big, sub) in enumerate(stats):
        x = M + i * (tw + 20)
        b.append(glass(x, 216, tw, 158, 16, FAM["gold"]["tint"], 0.45))
        b.append(t(x + 24, 280, big, 48, GOLDINK, SERIF, "600"))
        blk, _ = block(x + 24, 312, sub, tw - 48, 20, 25, INK2, 3)
        b.append(blk)

    y, hw = 404, CW / 2 - 12
    b.append(glass(M, y, hw, 188, 16))
    b.append(eyebrow(M + 26, y + 40, "Why probing can't answer it", FAM["cyb"]["c"],
                     maxw=hw - 52))
    bl, _ = bullets(M + 26, y + 80, [
        "Tests only the paths you thought of",
        "Can't tell blocked from about-to-change",
        "East-west is claimed more than shown",
    ], hw - 52, 22, 30, 14, INK2, FAM["cyb"]["c"], maxlines=1)
    b.append(bl)

    b.append(glass(M + CW / 2 + 12, y, hw, 188, 16, FAM["gold"]["tint"], 0.45))
    b.append(eyebrow(M + CW / 2 + 38, y + 40, "Reachability is a config property", GOLDINK,
                     maxw=hw - 52))
    bl, _ = bullets(M + CW / 2 + 38, y + 80, [
        "Routes, SGs, NACLs, firewall rules",
        "Decided statically — no scanning window",
        "Precedent: AWS Tiros · Batfish",
    ], hw - 52, 22, 30, 14, INK2, GOLDINK, maxlines=1)
    b.append(bl)

    b.append(t(M, 654, "On an OT network probing is forbidden — the IT/OT boundary must be "
                       "proven, not tested.", 24, GOLDINK, SANS, "500"))
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 2 · OWASP top two
def s_owasp(num=4):
    b = [water("gold"), heading("OWASP 2025 — Access Control & Misconfiguration")]
    b.append(t(M, 176, "The two categories at the top are found in 100% of apps tested.",
               27, INK, SERIF, "600", style="italic"))

    hw = CW / 2 - 12
    cards = [
        ("cyb", "A01", "#1 — unchanged", "Broken Access Control",
         "40 CWEs · 1.84M occurrences · 32,654 CVEs",
         "SSRF now folded in — easy to exploit, widespread."),
        ("cry", "A02", "#2 — up from #5", "Security Misconfiguration",
         "16 CWEs · 719,084 occurrences",
         "Again, 100% of tested apps carried a form of it."),
    ]
    for i, (fam, code, rank, title, stat, note) in enumerate(cards):
        f = FAM[fam]
        x = M + i * (hw + 24)
        b.append(glass(x, 206, hw, 182, 16, f["tint"], 0.5))
        b.append(orb(x + 44, 250, 24, f["c"]))
        b.append(t(x + 44, 259, code, 21, WHITE, MONO, "500", anchor="middle"))
        b.append(t(x + 84, 244, title, fit(title, hw - 108, 28, W_SERIF, 22), INK, SERIF, "600"))
        b.append(t(x + 84, 274, rank, 20, f["c"], MONO, "500"))
        b.append(t(x + 30, 330, stat, fit(stat, hw - 60, 22, W_MONO, 15), INK2, MONO))
        b.append(t(x + 30, 364, note, fit(note, hw - 60, 21, W_SANS, 16), INK2))

    b.append(glass(M, 408, CW, 236, 16))
    b.append(eyebrow(M + 30, 446, "Broken access control in the wild", INK2, 20, 2.6))
    incidents = [
        ("Capital One", "106M", "WAF SSRF → over-privileged role; a tipster found it, ~4 months in"),
        ("Optus", "9.5M", "access-control bug on a dormant, internet-facing API — latent ~4 years"),
        ("T-Mobile", "37M", "API data retrieval without authorization — ~6 weeks to notice"),
        ("Dell", "49M", "auto-approved fake partner, then service-tag enumeration"),
        ("Trello", "15M", "unauthenticated email lookup through rotating proxies"),
        ("Twilio Authy", "33M", "unauthenticated endpoint enumerated for phone numbers"),
    ]
    cy = 486
    for name, recs, cause in incidents:
        b.append(t(M + 30, cy, name, 23, INK, SANS, "600"))
        b.append(t(M + 250, cy, recs, 23, GOLDINK, MONO, "500", anchor="end"))
        b.append(t(M + 274, cy, cause, fit(cause, CW - 274 - 30, 22, W_SANS, 17), INK2))
        cy += 27

    b.append(t(M, 680, "Every one was a well-formed, authenticated request a monitor read as "
                       "normal.", 24, GOLDINK, SANS, "500"))
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 3 · apps & APIs
def s_api(num=5):
    b = [water("gold"), heading("Apps Misuse the APIs They Run On")]
    b.append(t(M, 176, "Cloud and app APIs are protocols, not calls — misuse still "
                       "compiles.", 26, INK, SERIF, "600", style="italic"))

    lw, rx, rw = 500, M + 534, CW - 534
    b.append(glass(M, 206, lw, 270, 18))
    b.append(eyebrow(M + 26, 246, "The pattern", FAM["cyb"]["c"], maxw=lw - 52))
    bl, _ = bullets(M + 26, 288, [
        "An object fetched by request ID with no ownership check — BOLA / IDOR",
        "A credential written to a log; pagination left undrained",
        "Authorisation in middleware a scanner can't see",
    ], lw - 52, 23, 27, 16, INK2, FAM["cyb"]["c"])
    b.append(bl)

    b.append(glass(rx, 206, rw, 270, 18, FAM["cry"]["tint"], 0.42))
    b.append(eyebrow(rx + 26, 246, "The trend is not reversing", FAM["cry"]["c"], maxw=rw - 52))
    trends = [("+29%", "IDOR reports year on year (HackerOne 2025)"),
              ("+36%", "access-control criticals — now #1 (Bugcrowd 2025)"),
              ("~95%", "of API attacks carry a valid token — authentic, not authorised")]
    ty = 302
    for big, sub in trends:
        b.append(t(rx + 26, ty, big, 32, FAM["cry"]["c"], SERIF, "600"))
        blk, _ = block(rx + 132, ty - 20, sub, rw - 132 - 26, 20, 25, INK2, 2)
        b.append(blk)
        ty += 58

    tiles = [("$4.4M", "average cost of a data breach (IBM 2025)"),
             ("241 days", "mean time to identify and contain (IBM 2025)"),
             ("258 / day", "API attacks per enterprise — 2× 2024 (Akamai 2025)")]
    tw = (CW - 2 * 20) / 3
    for i, (big, sub) in enumerate(tiles):
        b.append(stat_tile(M + i * (tw + 20), 478, tw, 138, big, sub, "gold"))

    b.append(t(M, 668, "A correct policy invoked through a misused SDK still leaks.",
               24, GOLDINK, SANS, "500"))
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 4 · post-quantum
def s_pqc(num=6):
    b = [water("gold"), heading("The Base Went Post-Quantum. Are the Apps Ready?")]
    b.append(t(M, 176, "The internet and cloud layer are shifting to hybrid PQC — and it is "
                       "proven.", 26, INK, SERIF, "600", style="italic"))

    hw = CW / 2 - 12
    b.append(glass(M, 206, hw, 300, 18, "#e6f2ea", 0.6))
    b.append(eyebrow(M + 26, 246, "Already shifting, already proven", GREEN, maxw=hw - 52))
    bl, _ = bullets(M + 26, 296, [
        "NIST FIPS 203 / 204 / 205 (Aug 2024)",
        "Hybrid ML-KEM default in browsers",
        "Live at Cloudflare, AWS, Google, Apple",
        "ML-KEM itself machine-checked (2024)",
    ], hw - 52, 23, 28, 22, INK2, GREEN, maxlines=1)
    b.append(bl)

    b.append(glass(M + hw + 24, 206, hw, 300, 18, FAM["cry"]["tint"], 0.45))
    b.append(eyebrow(M + hw + 50, 246, "The app on top is not", FAM["cry"]["c"], maxw=hw - 52))
    bl, _ = bullets(M + hw + 50, 296, [
        "No identity binding → impersonation",
        "Downgrade to legacy → decrypt later",
        "KEM key reuse → forward secrecy lost",
        "Token not channel-bound → replayed",
    ], hw - 52, 23, 28, 22, INK2, FAM["cry"]["c"], maxlines=1)
    b.append(bl)

    b.append(glass(M, 526, CW, 118, 18, FAM["gold"]["tint"], 0.5))
    b.append(f'<rect x="{M+2}" y="540" width="5" height="90" rx="2.5" fill="{GOLD}"/>')
    b.append(eyebrow(M + 34, 566, "Long-secret verticals bite hardest", GOLDINK, 20, 2.4,
                     maxw=CW - 80))
    b.append(t(M + 34, 600, "Gov ID (10+ yr) · PKI · healthcare · defence (25–50 yr).",
               23, INK2))
    b.append(t(M + 34, 628, "A mis-bound 10-year credential is a decade-long liability.",
               23, INK2))

    b.append(t(M, 680, "A proof at the transport layer says nothing about the app on top of "
                       "it.", 24, GOLDINK, SANS, "500"))
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 6 · the landscape
def s_landscape(num=9):
    b = [water("gold"), heading("Why Today's Security Stack Isn't Enough")]
    b.append(t(M, 176, "The collective wisdom of years of breaches — yet each only samples.",
               26, INK, SERIF, "600", style="italic"))

    ch, cy = chip_rows(W / 2, 224,
                       [["SAST / DAST / IAST", "SCA / supply chain", "ASPM",
                         "WAF / API security"],
                        ["CSPM · CIEM · CNAPP", "Pen test & red team", "SOC · EDR · SIEM",
                         "Policy-as-code"]])
    b.append(ch)

    b.append(glass(M, 342, CW, 258, 18))
    rows = [
        ("SAST", "Knows code patterns, not intent. A check present but wrong still passes."),
        ("DAST", "Only crawled endpoints and seeded data; even multi-persona only samples."),
        ("IAST / RASP", "Same-code-path BOLA is invisible — was the call even permitted?"),
        ("SCA / ASPM", "Known CVEs and risk diffs; never whether a grant is actually correct."),
        ("CNAPP / CSPM", "Stops at the cloud IAM role; never reads the app's own roles."),
        ("WAF / API sec", "A permitted request and a legitimate one look identical on the wire."),
    ]
    ry = 384
    for name, lim in rows:
        b.append(f'<circle cx="{M+34}" cy="{ry-8}" r="4" fill="{GOLD}"/>')
        b.append(t(M + 56, ry, name, 23, INK, SANS, "600"))
        b.append(t(M + 262, ry, lim, fit(lim, CW - 262 - 30, 23, W_SANS, 18), INK2))
        ry += 36

    b.append(t(M, 648, "They all share one gap: no statement of what is allowed, decided over "
                       "every request.", 24, INK, SANS, "500"))
    b.append(t(M, 680, "Keep every one of them — and add the layer that closes that gap.",
               24, GOLDINK, SANS, "600"))
    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 7 · proof, feasible
def s_feasible(num=10):
    b = [water("gold"), heading("Proof — Now Feasible")]
    b.append(t(M, 176, "Formal verification used to take expert teams years. AI brings it "
                       "into range.", 26, INK, SERIF, "600", style="italic"))

    hw = CW / 2 - 12
    b.append(glass(M, 206, hw, 206, 18, "#eef1f7", 0.7))
    b.append(eyebrow(M + 26, 246, "Then", MUTED, 20, 3.0))
    bl, _ = bullets(M + 26, 292, [
        "Expert teams, bespoke specs, years",
        "Confined to avionics, silicon, protocols",
        "“End users won’t write a spec”",
    ], hw - 52, 22, 28, 20, INK2, MUTED, maxlines=1)
    b.append(bl)

    b.append(glass(M + hw + 24, 206, hw, 206, 18, FAM["gold"]["tint"], 0.5))
    b.append(eyebrow(M + hw + 50, 246, "Now — AI-assisted", GOLDINK, 20, 3.0))
    bl, _ = bullets(M + hw + 50, 292, [
        "AI assists modelling & proof search",
        "Expert owns & ratifies the spec",
        "AWS runs ~1B SMT queries a day",
    ], hw - 52, 22, 28, 20, INK2, GOLDINK, maxlines=1)
    b.append(bl)

    b.append(solid(M, 430, CW, 82, INK, 16, sheen=False, gloss=0, edge=0.16))
    b.append(t(M + 32, 462, "What we add", 20, GOLD, MONO, "500", ls="2.6"))
    b.append(t(M + 210, 462, "A preventive control with evidence behind it, beside your "
                             "testing and SOC.", 23, WHITE))
    b.append(t(M + 210, 492, "We add to your stack; we don’t replace it. Proof alone isn’t "
                             "enough.", 23, GOLD))

    b.append(eyebrow(M, 562, "What stays with you — all of it needed", INK2, 20, 2.4,
                     maxw=CW))
    keeps = ["Configuration drift, shadow assets and anything outside the model",
             "Insider misuse, and valid credentials used exactly as intended",
             "Detection, response and the rest of the programme you already run"]
    cw = (CW - 2 * 20) / 3
    for i, k in enumerate(keeps):
        x = M + i * (cw + 20)
        blk, _ = block(x, 586, k, cw, 21, 26, INK2, 3)
        b.append(blk)

    b.append(chrome(num))
    return page("".join(b))


# ============================================================ 15 · AI agents
def s_ai_motivation(num=16):
    fam = "ai"
    f = FAM[fam]
    b = [water(fam), heading("AI Agents Multiply Faster Than the Rules", fam)]
    b.append(t(M, 176, "An agent is a non-human identity with delegated privilege and a "
                       "writable channel.", 24, INK, SERIF, "600", style="italic"))

    hw = CW / 2 - 12
    b.append(glass(M, 210, hw, 328, 18, f["tint"], 0.4))
    b.append(eyebrow(M + 26, 250, "The rules are arriving", f["c"], maxw=hw - 52))
    bl, _ = bullets(M + 26, 294, [
        "EU AI Act — Art. 15 robustness & security",
        "ISO/IEC 42001 — AI management system",
        "ISO/IEC 24029-2 — formal methods for AI",
        "DIFC Reg 10 · Dubai AI Seal · SDAIA",
    ], hw - 52, 22, 26, 14, INK2, f["c"], maxlines=1)
    b.append(bl)
    b.append(hline(M + 26, 474, hw - 52))
    blk, _ = block(M + 26, 498, "The assurance market does not exist yet — anywhere. "
                                "You would be early, not late.", hw - 52, 20, 24, GOLDINK, 2,
                   style="italic")
    b.append(blk)

    b.append(glass(M + hw + 24, 210, hw, 328, 18))
    b.append(eyebrow(M + hw + 50, 250, "The challenge — guardrails escape", f["c"], maxw=hw - 52))
    blk, _ = block(M + hw + 50, 292, "A guard model judging a model is detective, not "
                                     "preventive. The question is not “how often does it "
                                     "fail?” but “can it do this at all?”",
                   hw - 52, 23, 29, INK2, 4)
    b.append(blk)
    b.append(hline(M + hw + 50, 412, hw - 52))
    modes = [("5", "What an agent may do", "tool calls, arguments, data access")]
    my = 452
    for n, head, sub in modes:
        b.append(orb(M + hw + 68, my - 8, 15, f["c"]))
        b.append(t(M + hw + 68, my - 2, n, 18, WHITE, MONO, "500", anchor="middle"))
        b.append(t(M + hw + 96, my, head, 23, INK, SANS, "600"))
        b.append(t(M + hw + 96, my + 26, sub, fit(sub, hw - 120, 20, W_SANS, 16), INK2))
        my += 58

    b.append(solid(M, 558, CW, 74, f["c"], 16, sheen=False, gloss=0.14, edge=0.22))
    b.append(t(W / 2, 603, "Our AI-agentic guardrail solution proves the mediation layer, not "
                           "the model  →", 26, WHITE, SERIF, "600", anchor="middle"))

    b.append(chrome(num))
    return page("".join(b))


if __name__ == "__main__":
    build()
    print(f"wrote {len(TITLES)} slides to {OUT}")
