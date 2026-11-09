"""Shared palette, type and helpers for the profile README art (assets/*.svg).

Same family as the anilist README art: Catppuccin Mocha, a night sky,
JetBrains-style mono for Latin text and Noto Sans JP for Japanese. Every image
is a filled panel, so one file works on GitHub's light and dark themes alike.
"""
from html import escape
from pathlib import Path
from unicodedata import east_asian_width

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# Catppuccin Mocha
C = {
    "crust": "#11111b", "mantle": "#181825", "base": "#1e1e2e",
    "surface0": "#313244", "surface1": "#45475a", "overlay0": "#6c7086",
    "subtext0": "#a6adc8", "subtext1": "#bac2de", "text": "#cdd6f4",
    "rosewater": "#f5e0dc", "pink": "#f5c2e7", "mauve": "#cba6f7",
    "red": "#f38ba8", "peach": "#fab387", "yellow": "#f9e2af",
    "green": "#a6e3a1", "blue": "#89b4fa", "lavender": "#b4befe",
}

MONO = ("'JetBrains Mono','Fira Code','Cascadia Code',ui-monospace,SFMono-Regular,"
        "Menlo,Consolas,'Liberation Mono',monospace")
JP = "'Noto Sans JP','Noto Sans CJK JP','Hiragino Kaku Gothic ProN','Yu Gothic',Meiryo,sans-serif"
CELL = 0.6  # advance of one monospace cell, in em

# Motion is decoration: with reduced motion every element rests at its base
# style, so base styles always describe a complete, good-looking frame.
BASE_CSS = "@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; } }\n"


def esc(text: str) -> str:
    return escape(text, quote=True)


def cells(text: str) -> int:
    """Terminal cells a string occupies: wide (CJK) characters take two."""
    return sum(2 if east_asian_width(ch) in "WF" else 1 for ch in text)


def svg(width: int, height: int, title: str, body: str, css: str = "", defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n<defs>{defs}</defs>\n"
        f"<style>\n{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def write(name: str, build) -> Path:
    ASSETS.mkdir(exist_ok=True)
    path = ASSETS / f"{name}.svg"
    path.write_text(build(), encoding="utf-8")
    return path
