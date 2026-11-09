"""Banner: night sky over a small town, a sakura tree shedding petals, the
handle with a blinking cursor, and an MSE-6 droid scurrying along the ground."""
import random

import scene
from common import C, JP, MONO, esc, svg

W, H = 1200, 340
TITLE, TITLE_SIZE, TITLE_LEN = "reniaz", 104, 420
CURSOR_W, CURSOR_GAP = 40, 16
TITLE_Y = 172
JP_LINE = "Cで書く、たまに他も。"
EN_LINE = "systems tinkerer · c first · linux · a little hardware"
MOON = (1012, 86, 42)
DROID_X, DROID_Y = 300, 322


def _skyline(rng) -> str:
    """Distant buildings right of centre with a few lit, flickering windows."""
    out, x = [], 872
    tallest = None
    while x < W:
        w = rng.randint(22, 46)
        top = rng.randint(226, 268)
        out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{300 - top}" fill="#33284f"/>')
        if tallest is None or top < tallest[1]:
            tallest = (x + w / 2, top)
        for wy in range(top + 8, 292, 10):
            for wx in range(x + 5, x + w - 6, 8):
                if rng.random() < 0.3:
                    cls, style = "", ""
                    if rng.random() < 0.35:
                        cls = ' class="win"'
                        style = (f' style="animation-duration:{rng.uniform(5, 11):.1f}s;'
                                 f'animation-delay:-{rng.uniform(0, 11):.1f}s"')
                    out.append(f'<rect{cls} x="{wx}" y="{wy}" width="3" height="4" '
                               f'fill="{C["yellow"]}" opacity=".7"{style}/>')
        x += w + rng.randint(0, 4)
    ax, ay = tallest
    out.append(f'<path d="M{ax:g},{ay} L{ax:g},{ay - 22}" stroke="#33284f" stroke-width="2"/>')
    out.append(f'<circle class="beacon" cx="{ax:g}" cy="{ay - 23}" r="2.2" fill="{C["red"]}"/>')
    return "\n".join(out)


def _tree(rng) -> str:
    """Sakura on the left: rigid trunk, branches and blossoms sway together."""
    bark = "#1b1430"
    trunk = ("M118,322 C122,292 126,268 120,246 C116,232 122,214 134,204 C142,198 150,192 156,184 "
             "L162,188 C156,198 148,206 142,214 C134,226 132,240 136,256 C142,280 140,300 148,322 Z")
    branches = [
        ("M128,236 C106,222 86,214 58,204", 6), ("M134,214 C150,196 176,180 212,168", 5),
        ("M126,250 C104,252 84,260 64,262", 4), ("M150,196 C150,176 140,160 126,146", 4),
        ("M158,188 C186,190 214,198 242,214", 4),
    ]
    clusters = [(56, 198, 34), (124, 142, 36), (212, 162, 34), (244, 210, 26), (88, 238, 24),
                (170, 178, 28), (60, 258, 18)]
    # Per cluster: a shaded under-layer for volume, dense small blooms, and a
    # few pale highlights on the moonlit (upper right) side.
    shade, blooms, lights = [], [], []
    for cx, cy, r in clusters:
        for _ in range(4):
            shade.append(f'<circle cx="{cx + rng.gauss(0, r * .3):.0f}" cy="{cy + rng.gauss(0, r * .25) + 4:.0f}" '
                         f'r="{r * rng.uniform(.45, .6):.1f}" fill="#a8618f" opacity=".45"/>')
        for _ in range(int(r * 1.3)):
            dx, dy = rng.gauss(0, r * 0.42), rng.gauss(0, r * 0.34)
            blooms.append(f'<circle cx="{cx + dx:.0f}" cy="{cy + dy:.0f}" r="{rng.uniform(3.5, 7.5):.1f}" '
                          f'fill="{rng.choice(scene.PETAL_FILLS + ("#e8a6c8", "#e8a6c8"))}" '
                          f'opacity="{rng.uniform(.8, .95):.2f}"/>')
        for _ in range(int(r * .25)):
            lights.append(f'<circle cx="{cx + rng.uniform(0, r * .6):.0f}" cy="{cy - rng.uniform(0, r * .5):.0f}" '
                          f'r="{rng.uniform(1.8, 3):.1f}" fill="#fde4f0" opacity=".9"/>')
    blossoms = shade + blooms + lights
    sway = "".join(f'<path d="{d}" fill="none" stroke="{bark}" stroke-width="{w}" stroke-linecap="round"/>'
                   for d, w in branches)
    return (f'<path d="{trunk}" fill="{bark}"/>\n<g class="sway">{sway}\n' + "\n".join(blossoms) + "</g>")


def build() -> str:
    rng = random.Random(11)
    sky_defs, sky = scene.sky(W, H, 18)
    mx, my, mr = MOON
    defs = sky_defs + f"""
<linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{C['lavender']}"/><stop offset=".5" stop-color="{C['mauve']}"/><stop offset="1" stop-color="{C['pink']}"/>
</linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{C['rosewater']}" stop-opacity=".42"/><stop offset="1" stop-color="{C['rosewater']}" stop-opacity="0"/></radialGradient>
<linearGradient id="trail" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="-90" y2="-30">
  <stop offset="0" stop-color="{C['rosewater']}"/><stop offset="1" stop-color="{C['rosewater']}" stop-opacity="0"/>
</linearGradient>
<filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="{C['pink']}" flood-opacity=".45"/></filter>"""

    title_x = W / 2 - (TITLE_LEN + CURSOR_GAP + CURSOR_W) / 2
    cursor_x = title_x + TITLE_LEN + CURSOR_GAP
    craters = "".join(f'<circle cx="{mx + dx}" cy="{my + dy}" r="{r}" fill="#e3cdc9" opacity=".55"/>'
                      for dx, dy, r in ((-14, -8, 7), (12, 14, 5), (9, -15, 3.5), (-10, 17, 4), (20, -2, 2.5)))

    body = f"""{sky}
{scene.stars(rng, 52, W, 205)}
<circle cx="{mx}" cy="{my}" r="120" fill="url(#glow)"/>
<circle cx="{mx}" cy="{my}" r="{mr}" fill="{C['rosewater']}"/>{craters}
<g class="shoot" style="animation-delay:-9s"><g transform="translate(380,40)"><path d="M0,0 L-90,-30" stroke="url(#trail)" stroke-width="2" stroke-linecap="round"/></g></g>
{_skyline(rng)}
<path d="M0,292 C160,272 280,296 420,284 C560,272 700,300 840,288 C960,278 1080,296 1200,282 L1200,340 L0,340 Z" fill="{scene.HILL_BACK}"/>
{_tree(rng)}
<path d="M0,318 C200,312 400,321 600,316 C800,311 1000,320 1200,314 L1200,340 L0,340 Z" fill="{scene.HILL_FRONT}"/>
{scene.droid(DROID_X, DROID_Y, 1.3)}
<text x="{title_x:g}" y="{TITLE_Y}" font-family="{MONO}" font-size="{TITLE_SIZE}" font-weight="800" textLength="{TITLE_LEN}" lengthAdjust="spacing" fill="url(#title)" filter="url(#soft)">{TITLE}</text>
<rect class="cursor" x="{cursor_x:g}" y="{TITLE_Y - 76}" width="{CURSOR_W}" height="80" rx="3" fill="{C['pink']}" filter="url(#soft)"/>
<text x="{W / 2:g}" y="{TITLE_Y + 46}" text-anchor="middle" font-family="{JP}" font-size="26" letter-spacing="6" fill="{C['rosewater']}">{esc(JP_LINE)}</text>
<text x="{W / 2:g}" y="{TITLE_Y + 82}" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{C['subtext1']}">{esc(EN_LINE)}</text>
{scene.petals(rng, 12, 20, 320, 110, 300)}
{scene.petals(rng, 10, 320, 1180, 20, 320)}
{scene.close_frame()}"""

    css = (scene.STAR_CSS + scene.petal_css(120, 420) + scene.droid_css(DROID_X, W, 28) + f"""
.cursor {{ animation: blink 1.1s steps(1, end) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.sway {{ transform-box: view-box; transform-origin: 136px 300px; animation: sway 7s ease-in-out infinite alternate; }}
@keyframes sway {{ from {{ transform: rotate(-1.2deg); }} to {{ transform: rotate(1.2deg); }} }}
.win {{ animation: flicker ease-in-out infinite; }}
@keyframes flicker {{ 0%,40%,100% {{ opacity: .7; }} 55%,80% {{ opacity: .08; }} }}
.beacon {{ animation: beacon 2s ease-in-out infinite; }}
@keyframes beacon {{ 0%,100% {{ opacity: .2; }} 50% {{ opacity: 1; }} }}
.shoot {{ opacity: 0; animation: shoot 13s ease-out infinite; }}
@keyframes shoot {{
  0% {{ transform: translate(0,0); opacity: 0; }}
  1% {{ opacity: 1; }}
  6% {{ transform: translate(260px,88px); opacity: 0; }}
  100% {{ transform: translate(260px,88px); opacity: 0; }}
}}
""")
    return svg(W, H, f"reniaz — {JP_LINE} {EN_LINE}", body, css, defs)


ASSETS = {"banner": build}
