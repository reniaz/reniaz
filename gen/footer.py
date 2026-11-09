"""Footer: a thin strip of the banner's night, a goodbye, and the droid again."""
import random

import scene
from common import C, JP, MONO, svg

W, H = 1200, 120
DROID_X, DROID_Y = 760, 112


def build() -> str:
    rng = random.Random(5)
    sky_defs, sky = scene.sky(W, H, 18)
    body = f"""{sky}
{scene.stars(rng, 40, W, 80)}
<path d="M0,96 C200,84 400,100 600,92 C800,84 1000,100 1200,90 L1200,120 L0,120 Z" fill="{scene.HILL_BACK}"/>
<path d="M0,110 C300,106 600,112 900,108 C1000,107 1100,110 1200,106 L1200,120 L0,120 Z" fill="{scene.HILL_FRONT}"/>
{scene.droid(DROID_X, DROID_Y, 0.8, -3)}
<text x="{W / 2:g}" y="62" text-anchor="middle" font-family="{MONO}" font-size="20" fill="{C['pink']}">thanks for stopping by ♡ <tspan font-family="{JP}">またね</tspan></text>
{scene.petals(rng, 14, 0, W, 0, H, (7, 12))}
{scene.close_frame()}"""
    css = scene.STAR_CSS + scene.petal_css(70, 170) + scene.droid_css(DROID_X, W, 24)
    return svg(W, H, "thanks for stopping by ♡ またね", body, css, sky_defs)


ASSETS = {"footer": build}
