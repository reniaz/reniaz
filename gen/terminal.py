"""Terminal intro in the look of the demo GIFs in my project READMEs:
Catppuccin Mocha, VHS-style window. It types a short session, holds it,
clears and starts over.

Every character and line is its own element that switches on at a moment of
the loop (opacity only), so nothing depends on clip-path support. The base
style is the finished session, which is what reduced motion shows.
"""
import random

from common import C, JP, MONO, cells, esc, svg

W = 836
FS, LH = 15, 26
CW = FS * 0.6
PAD_X, TITLE_H = 28, 44
LOOP = 17.0        # seconds per cycle
CLEAR = 97.0       # % of the loop at which the screen clears

# (kind, payload). Output segments: (text, colour, bold).
SCRIPT = [
    ("cmd", "whoami"),
    ("out", [("reniaz", "text", True), (" — c first, everything else when it's needed", "subtext1", False)]),
    ("cmd", "cat now.txt"),
    ("out", [("building  ", "pink", False), ("leise — private community chat over i2p", "text", False)]),
    ("out", [("solving   ", "pink", False), ("advent of code & everybody.codes in plain c", "text", False)]),
    ("out", [("learning  ", "pink", False), ("日本語 — 毎日少しずつ", "text", False)]),
    ("cmd", "cc -std=c11 -Wall -Wextra -O2 hello.c -o hello && ./hello"),
    ("out", [("hello, world", "green", False)]),
]
H = TITLE_H + 16 + (len(SCRIPT) + 1) * LH + 14


def _p(t: float) -> str:
    return f"{t / LOOP * 100:.3f}"


class _Css:
    def __init__(self):
        self.rules, self.n = [], 0

    def _name(self) -> str:
        self.n += 1
        return f"k{self.n}"

    def appear(self, t: float) -> str:
        """Class that is hidden until t, shown until the screen clears."""
        k, p = self._name(), float(_p(t))
        self.rules.append(
            f".{k} {{ animation: {k} {LOOP:g}s linear infinite; }}\n"
            f"@keyframes {k} {{ 0%, {p:.3f}% {{ opacity: 0; }} {p + .01:.3f}%, {CLEAR}% {{ opacity: 1; }} "
            f"{CLEAR + .01}%, 100% {{ opacity: 0; }} }}"
        )
        return k

    def caret(self, t_on: float, hops: list[float], t_off: float) -> str:
        """Typing cursor: shows at t_on, hops one cell right at each time in
        hops, hides at t_off. Hidden at rest, as in the finished session."""
        k = self._name()
        frames = [f"0%, {_p(t_on)}% {{ opacity: 0; transform: translateX(0); }}",
                  f"{float(_p(t_on)) + .01:.3f}% {{ opacity: 1; transform: translateX(0); }}"]
        for i, t in enumerate(hops):
            frames.append(f"{_p(t)}% {{ opacity: 1; transform: translateX({i * CW:g}px); }}")
            frames.append(f"{float(_p(t)) + .01:.3f}% {{ opacity: 1; transform: translateX({(i + 1) * CW:g}px); }}")
        end = len(hops) * CW
        frames.append(f"{_p(t_off)}% {{ opacity: 1; transform: translateX({end:g}px); }}")
        frames.append(f"{float(_p(t_off)) + .01:.3f}%, 100% {{ opacity: 0; transform: translateX({end:g}px); }}")
        self.rules.append(f".{k} {{ opacity: 0; animation: {k} {LOOP:g}s linear infinite; }}\n"
                          f"@keyframes {k} {{ {' '.join(frames)} }}")
        return k


def _seg(text: str, col: int, y: float, colour: str, bold: bool = False, cls: str = "") -> str:
    weight = ' font-weight="700"' if bold else ""
    klass = f' class="{cls}"' if cls else ""
    return (f'<text{klass} x="{PAD_X + col * CW:g}" y="{y:g}" textLength="{cells(text) * CW:g}" '
            f'lengthAdjust="spacingAndGlyphs" xml:space="preserve" fill="{C[colour]}"{weight}>{esc(text)}</text>')


def _caret_rect(col: int, y: float, cls: str) -> str:
    return (f'<rect class="{cls}" x="{PAD_X + col * CW:g}" y="{y - FS * .95:g}" width="{CW:g}" '
            f'height="{FS * 1.25:g}" fill="{C["rosewater"]}"/>')


def build() -> str:
    rng = random.Random(3)
    css = _Css()
    rows = []
    t, y = 0.6, TITLE_H + 16 + FS
    prev = None
    for kind, payload in SCRIPT:
        if kind == "cmd":
            if prev == "out":
                t += 0.5
            rows.append(_seg("❯", 0, y, "text", True, css.appear(t)))
            t_on = t
            t += 0.35
            first_word = payload.split(" ")[0]
            hops = []
            for i, ch in enumerate(payload):
                t += rng.uniform(.035, .085)
                hops.append(t)
                if ch != " ":
                    in_first = i < len(first_word)
                    rows.append(_seg(ch, 2 + i, y, "mauve" if in_first else "text", in_first, css.appear(t)))
            t += 0.45
            rows.append(_caret_rect(2, y, css.caret(t_on, hops, t)))
            t += 0.1
        else:
            col = 0
            k = css.appear(t)
            for text, colour, bold in payload:
                rows.append(_seg(text, col, y, colour, bold, k))
                col += cells(text)
            t += 0.09
        prev = kind
        y += LH
    t += 0.5
    rows.append(_seg("❯", 0, y, "text", True, css.appear(t)))
    final = (f'<g class="{css.appear(t)}"><rect class="blink" x="{PAD_X + 2 * CW:g}" y="{y - FS * .95:g}" '
             f'width="{CW:g}" height="{FS * 1.25:g}" fill="{C["rosewater"]}"/></g>')
    assert t / LOOP * 100 < CLEAR - 25, "loop too short to hold the finished session"

    dots = "".join(f'<circle cx="{22 + i * 20}" cy="22" r="6" fill="{C[c]}"/>'
                   for i, c in enumerate(("red", "yellow", "green")))
    body = f"""<g class="tm"><rect width="{W}" height="{H}" rx="12" fill="{C['base']}"/>
{dots}
<text x="{W / 2:g}" y="27" text-anchor="middle" style="font-size:14px" fill="{C['subtext0']}">reniaz — ~</text>
{chr(10).join(rows)}
{final}</g>"""
    style = (f".tm text {{ font-family: {MONO},{JP}; font-size: {FS}px; }}\n"
             ".blink { animation: blink 1.1s steps(1, end) infinite; }\n"
             "@keyframes blink { 50% { opacity: 0; } }\n" + "\n".join(css.rules) + "\n")
    alt = ("terminal: whoami → reniaz, c first; cat now.txt → building leise, solving advent of code "
           "and everybody.codes in plain c, learning japanese; cc hello.c → hello, world")
    return svg(W, H, alt, body, style)


ASSETS = {"terminal": build}
