"""Night-sky pieces shared by the banner and the footer: sky, twinkling stars,
falling sakura petals and a scurrying MSE-6 mouse droid.

Animations start with negative delays, so the scene is already mid-motion on
the first frame, and every piece's base (unanimated) state is a sensible still.
"""
from common import C

PETAL = "M0,10 C-8,4 -8,-6 -2,-10 L0,-7 L2,-10 C8,-6 8,4 0,10 Z"
PETAL_FILLS = ("#f2a7c6", "#f5c2e7", "#fbd5e8")
HILL_BACK, HILL_FRONT = "#2b2142", "#1a1530"


def sky(width: int, height: int, rx: int) -> tuple[str, str]:
    """(defs, markup) for the gradient sky; markup also opens the rounded frame
    clip, which close_frame() ends."""
    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{C["crust"]}"/><stop offset=".55" stop-color="#2a1f4a"/>'
        '<stop offset="1" stop-color="#5e3a6e"/></linearGradient>'
        f'<clipPath id="frame"><rect width="{width}" height="{height}" rx="{rx}"/></clipPath>'
    )
    return defs, f'<g clip-path="url(#frame)">\n<rect width="{width}" height="{height}" fill="url(#sky)"/>'


def close_frame() -> str:
    return "</g>"


STAR_CSS = """.star { animation: tw ease-in-out infinite; }
@keyframes tw { 0%,100% { opacity: .2; } 50% { opacity: 1; } }
"""


def stars(rng, n: int, width: int, ymax: float) -> str:
    out = []
    for _ in range(n):
        x, y = rng.uniform(8, width - 8), rng.uniform(8, ymax)
        r = rng.choice((0.8, 0.8, 1, 1.2, 1.6))
        out.append(
            f'<circle class="star" cx="{x:.0f}" cy="{y:.0f}" r="{r:g}" fill="{C["rosewater"]}" '
            f'style="animation-duration:{rng.uniform(2.5, 5):.1f}s;animation-delay:-{rng.uniform(0, 5):.1f}s"/>'
        )
    return "\n".join(out)


def petal_css(drift: int, fall: int) -> str:
    """Petals ride the wind to the right while they fall."""
    return (
        ".petal { animation: fall linear infinite; transform-box: fill-box; transform-origin: center; }\n"
        f"@keyframes fall {{ from {{ transform: translate({-drift}px,{-fall}px) rotate(0deg); }} "
        f"to {{ transform: translate({drift}px,{fall}px) rotate(640deg); }} }}\n"
    )


def petals(rng, n: int, x0: float, x1: float, y0: float, y1: float, durations=(9, 16)) -> str:
    out = []
    for _ in range(n):
        x, y, s = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(0.7, 1.4)
        dur = rng.uniform(*durations)
        out.append(
            f'<g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})"><path class="petal" d="{PETAL}" '
            f'fill="{rng.choice(PETAL_FILLS)}" opacity=".85" '
            f'style="animation-duration:{dur:.1f}s;animation-delay:-{rng.uniform(0, dur):.1f}s"/></g>'
        )
    return "\n".join(out)


# MSE-6 "mouse droid": a low black box with a chamfered nose, a raised top
# panel, a red sensor eye and three wheels. Local origin = ground under its tail.
BODY = "#0c0a14"
DROID = f"""<g class="droid-bob">
  <rect x="11" y="-30" width="22" height="5" rx="1.5" fill="{BODY}" stroke="{C['surface1']}" stroke-width="1"/>
  <path d="M2,-8 L2,-23 Q2,-26 5,-26 L43,-26 L54,-17 L54,-8 Z" fill="{BODY}" stroke="{C['surface1']}" stroke-width="1" stroke-linejoin="round"/>
  <path d="M19,-23 L19,-11 M36,-23 L36,-11" stroke="#2c2640" stroke-width="1.2"/>
  <path d="M44,-21 L51,-15" stroke="#2c2640" stroke-width="1.2"/>
  <circle class="droid-eye" cx="49" cy="-12" r="1.9" fill="{C['red']}"/>
  <g fill="{BODY}" stroke="{C['surface1']}" stroke-width="1">
    <circle cx="11" cy="-4.5" r="4.5"/><circle cx="28" cy="-4.5" r="4.5"/><circle cx="45" cy="-4.5" r="4.5"/>
  </g>
  <g stroke="{C['overlay0']}" stroke-width="1.2" stroke-linecap="round">
    <path class="droid-wheel" d="M8,-4.5 L14,-4.5"/><path class="droid-wheel" d="M25,-4.5 L31,-4.5"/><path class="droid-wheel" d="M42,-4.5 L48,-4.5"/>
  </g>
</g>"""

# Fraction of the trip done at each keyframe: it scurries, stops to look
# around, scurries again, then waits off-stage before the next lap.
RUN_STOPS = ((0, 0), (20, .28), (28, .28), (48, .56), (55, .56), (84, 1), (100, 1))


def droid(x0: float, y0: float, scale: float = 1, delay: float = -6) -> str:
    return (f'<g class="droid-run" style="animation-delay:{delay:g}s">'
            f'<g transform="translate({x0:g},{y0:g}) scale({scale:g})">{DROID}</g></g>')


def droid_css(x0: float, width: int, duration: float) -> str:
    """The droid is drawn at x0 (its still position); the run moves it from
    just off the left edge to just off the right edge."""
    start, end = -80 - x0, width + 20 - x0
    frames = " ".join(
        f"{pct}% {{ transform: translateX({start + f * (end - start):.0f}px); }}" for pct, f in RUN_STOPS
    )
    return f""".droid-run {{ animation: run {duration:g}s cubic-bezier(.45,0,.3,1) infinite; }}
@keyframes run {{ {frames} }}
.droid-bob {{ animation: bob .32s ease-in-out infinite alternate; }}
@keyframes bob {{ to {{ transform: translateY(-.8px); }} }}
.droid-wheel {{ transform-box: fill-box; transform-origin: center; animation: spin .5s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.droid-eye {{ animation: eye 2.6s ease-in-out infinite; }}
@keyframes eye {{ 0%,60%,100% {{ opacity: 1; }} 75% {{ opacity: .25; }} }}
"""
