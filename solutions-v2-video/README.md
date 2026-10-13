# PrimusCredence — video deck (minimal, animated)

A single-file, animated presentation built for **recording the voice-over**. It
carries the same three-Service story as `../solutions-v2/` (access control,
network isolation, data residency), but with **minimal
text** so the audience follows your voice, not the slide. Content reveals **one
element at a time**, so you narrate a point and bring it on screen as you say it.

`index.html` — open it in a browser. Nothing to build; it loads its own
webfonts.

## Controls
- **→ / Space / click right** — reveal the next element; at the end of a slide,
  advance to the next slide.
- **← / click left** — step back one element (or to the previous slide).
- **F** — fullscreen (record this).
- **A** — toggle **autoplay** (reveals one element every ~3.2 s, hands-free;
  press again to stop). Good for an unattended take; use manual advance to sync
  tightly to narration.
- **Home / End**, and `#n` in the URL — jump to a slide.

## The 18 slides
Title · founder · **the stack** (the anchor — layers reveal with proven/unproven
badges) · the risk (100%) · the cost · segmentation & lateral movement ·
residency is reviewed, not proven · AI industrialises the attacker · what
today's stack leaves open · proof in four steps · the three Services · one slide
each for Services 1–3 (with an "In the demo" strip) · we sit behind the
providers + their client base · why clients ask · take-away · thank-you.

Copy follows the main deck (`../solutions-v2/build.py`), which is the source of
truth; when the main deck changes a figure or a line, mirror it here.

This deck is pitched **to** cybersecurity solutions providers, so the long-term
"assurance hub" vision and the investment ask are omitted.

The **stack diagram is retained** and is now animated, built from the ground up —
the cloud base first, then the seam (access via APIs, network paths, data paths),
the app and the plugins are each set down on top in turn, with "proven" / "unproven" badges.

## Recording tips
- Press **F** for fullscreen at 1920×1080, then screen-record.
- Advance manually in time with the matching block of
  `../../video/speaker-script.md` (the beats line up slide-for-slide with the
  minimal content here).
- The deck scales to any window; record at 16:9 for a clean full-frame or a
  picture-in-picture with you in the corner (see `../../video/README.md`).
