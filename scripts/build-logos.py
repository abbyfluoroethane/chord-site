"""Build the Chord logo pack: SVG (text as outlines) and PNG for every logo setup.

Run from the repo root: python3 <this file> <path to bricolage-grotesque-latin-700-normal.woff>
Writes to public/brand/.
"""
import sys, zipfile, asyncio, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1]
OUT = pathlib.Path("public/brand")
OUT.mkdir(parents=True, exist_ok=True)

# ---- colors (from src/styles/chord.css) ----
THEMES = {
    "":          {"ring": "#1A1C20", "chord": "#C47B0C", "text": "#1A1C20"},   # for light backgrounds
    "-reversed": {"ring": "#ECE8E1", "chord": "#F2A93B", "text": "#ECE8E1"},   # for dark backgrounds
    "-mono-black": {"ring": "#1A1C20", "chord": "#1A1C20", "text": "#1A1C20"},
    "-mono-white": {"ring": "#FFFFFF", "chord": "#FFFFFF", "text": "#FFFFFF"},
}

# ---- the mark, in a 64 x 64 box ----
def mark(c, dx=0, dy=0, s=1.0):
    g = f'<g transform="translate({dx} {dy}) scale({s})">'
    g += f'<circle cx="32" cy="32" r="22" fill="none" stroke="{c["ring"]}" stroke-width="4"/>'
    g += f'<line x1="11.3" y1="39.5" x2="39.5" y2="11.3" stroke="{c["chord"]}" stroke-width="4" stroke-linecap="round"/>'
    g += f'<circle cx="11.3" cy="39.5" r="5" fill="{c["chord"]}"/><circle cx="39.5" cy="11.3" r="5" fill="{c["chord"]}"/>'
    return g + "</g>"

# ---- the wordmark "chord" as outlines ----
font = TTFont(FONT)
upm = font["head"].unitsPerEm
cmap = font.getBestCmap()
gs = font.getGlyphSet()
hmtx = font["hmtx"]
TRACK = -0.02 * upm  # letter-spacing -0.02em

def word_paths(text):
    """Return (list of (path_d, x_offset)), advance width, y extents in font units."""
    x = 0
    parts = []
    ymin, ymax = 0, 0
    for i, ch in enumerate(text):
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[name].draw(pen)
        bp = BoundsPen(gs); gs[name].draw(bp)
        if bp.bounds:
            ymin = min(ymin, bp.bounds[1]); ymax = max(ymax, bp.bounds[3])
        parts.append((pen.getCommands(), x))
        x += hmtx[name][0] + (TRACK if i < len(text) - 1 else 0)
    return parts, x, ymin, ymax

parts, adv, ymin, ymax = word_paths("chord")
# Ascender of "h" sets the size: it matches the ring's outer diameter (48 of 64).
bp = BoundsPen(gs); gs[cmap[ord("h")]].draw(bp)
asc = bp.bounds[3]

def wordmark(color, height_px, dx=0, baseline=0):
    s = height_px / asc
    g = f'<g fill="{color}" transform="translate({dx} {baseline}) scale({s} {-s})">'
    for d, x in parts:
        g += f'<path transform="translate({x} 0)" d="{d}"/>'
    return g + "</g>", adv * s

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}">{body}</svg>\n'

files = {}

# Marks
for suf, c in THEMES.items():
    files[f"chord-mark{suf}.svg"] = svg(64, 64, mark(c))

# App icon
files["chord-app-icon.svg"] = svg(64, 64, '<rect width="64" height="64" rx="14" fill="#111316"/>' + mark(THEMES["-reversed"]))

# Wordmark alone: ascender 48, padded to the glyph bounds
for suf, c in THEMES.items():
    s = 48 / asc
    top = (ymax - asc) * s  # room above the ascender, usually 0
    h = (ymax - ymin) * s
    body, w = wordmark(c["text"], 48, dx=0, baseline=ymax * s)
    files[f"chord-wordmark{suf}.svg"] = svg(w, h, body)

# Lockup: mark + wordmark. Text baseline sits on the ring's outer bottom (y = 56),
# ascender reaches the ring's outer top (y = 8). Gap = a quarter of the mark (16).
for suf, c in THEMES.items():
    s = 48 / asc
    body_w, w = wordmark(c["text"], 48, dx=64 + 16, baseline=56)
    below = -ymin * s  # descender room (none for "chord", but kept for safety)
    h = max(64, 56 + below)
    files[f"chord-lockup{suf}.svg"] = svg(64 + 16 + w, h, mark(c) + body_w)

for name, text in files.items():
    (OUT / name).write_text(text)
print("wrote", len(files), "SVGs")

# ---- PNGs, rendered by Chromium ----
from playwright.async_api import async_playwright

async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for name in sorted(files):
            src = (OUT / name).read_text()
            vb = [float(v) for v in src.split('viewBox="')[1].split('"')[0].split()]
            vw, vh = vb[2], vb[3]
            tall = 1024 if vh == 64 and vw == 64 else 512
            scale = tall / vh
            W, H = round(vw * scale), round(vh * scale)
            body = src.replace(f'width="{vw:.0f}" height="{vh:.0f}"', f'width="{W}" height="{H}"', 1)
            await pg.set_viewport_size({"width": W, "height": H})
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{body}</body></html>')
            await pg.screenshot(path=str(OUT / name.replace(".svg", ".png")), omit_background=True, clip={"x": 0, "y": 0, "width": W, "height": H})
        await b.close()

asyncio.run(render())
print("wrote", len(files), "PNGs")

# ---- one zip with everything ----
with zipfile.ZipFile(OUT / "chord-brand.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):
        if f.suffix in (".svg", ".png"):
            z.write(f, f"chord-brand/{f.name}")
print("wrote chord-brand.zip")
