#!/usr/bin/env python3
"""Rebuild the archived light/dark animated research header.

The current static README does not use this artwork.

Uses Pillow and fonts already present on the host. No network resources are needed.
The finished first frame also serves as the static fallback/thumbnail.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "profile-v6"
SIZE = (760, 314)
SCALE = 2
PIXELS = tuple(value * SCALE for value in SIZE)
CARD = (389, 56, 344, 218)


@dataclass(frozen=True)
class Palette:
    page: str
    body: str
    chrome: str
    card: str
    border: str
    divider: str
    text: str
    muted: str
    faint: str
    violet: str
    teal: str
    amber: str
    violet_soft: str
    teal_soft: str
    amber_soft: str


THEMES = {
    "light": Palette(
        page="#FFFFFF", body="#F7F9FD", chrome="#EEF2F8", card="#FFFFFF",
        border="#CFD9E8", divider="#DFE6F0", text="#172641",
        muted="#50637D", faint="#71829A", violet="#7455C9",
        teal="#168A96", amber="#A96B23", violet_soft="#EEE9FB",
        teal_soft="#E5F4F5", amber_soft="#F9EFDE",
    ),
    "dark": Palette(
        page="#0D1117", body="#0E1727", chrome="#172235", card="#152339",
        border="#34455F", divider="#2D3D56", text="#EDF3FF",
        muted="#B4C2D7", faint="#8295AE", violet="#AE97F5",
        teal="#65CAD2", amber="#E4B16D", violet_soft="#302B50",
        teal_soft="#1C3C48", amber_soft="#483A30",
    ),
}


AVENIR = Path("/System/Library/Fonts/Avenir Next.ttc")
MENLO = Path("/System/Library/Fonts/Menlo.ttc")
FALLBACK_SANS = Path("/System/Library/Fonts/HelveticaNeue.ttc")
FALLBACK_MONO = Path("/System/Library/Fonts/Monaco.ttf")
DEJAVU_SANS = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
DEJAVU_BOLD = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
DEJAVU_MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def font(size: float, weight: str = "regular") -> ImageFont.FreeTypeFont:
    """Use the same local fonts across both themes without bundling font files."""
    if weight == "mono":
        path = next((p for p in (MENLO, FALLBACK_MONO, DEJAVU_MONO) if p.exists()), None)
        index = 0
    else:
        path = next((p for p in (AVENIR, FALLBACK_SANS, DEJAVU_SANS) if p.exists()), None)
        if path == AVENIR:
            index = {"regular": 7, "medium": 5, "demi": 2, "bold": 0}[weight]
        elif path == FALLBACK_SANS:
            index = {"regular": 0, "medium": 10, "demi": 1, "bold": 1}[weight]
        elif weight in {"demi", "bold"} and DEJAVU_BOLD.exists():
            path, index = DEJAVU_BOLD, 0
        else:
            index = 0
    if path is None:
        raise FileNotFoundError("Install Avenir Next, Helvetica Neue, or DejaVu fonts")
    return ImageFont.truetype(str(path), round(size * SCALE), index=index)


def xy(point: tuple[float, float]) -> tuple[int, int]:
    return round(point[0] * SCALE), round(point[1] * SCALE)


def box(bounds: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(round(value * SCALE) for value in bounds)  # type: ignore[return-value]


def line(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: str,
         width: float = 1, joint: str = "curve") -> None:
    draw.line([xy(point) for point in points], fill=fill,
              width=max(1, round(width * SCALE)), joint=joint)


def text(draw: ImageDraw.ImageDraw, point: tuple[float, float], value: str,
         size: float, fill: str, weight: str = "regular") -> None:
    draw.text(xy(point), value, font=font(size, weight), fill=fill, anchor="lt")


def roundrect(draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float],
              radius: float, fill: str, outline: str | None = None,
              width: float = 1) -> None:
    draw.rounded_rectangle(box(bounds), radius=round(radius * SCALE), fill=fill,
                           outline=outline, width=max(1, round(width * SCALE)))


def circle(draw: ImageDraw.ImageDraw, cx: float, cy: float, radius: float,
           fill: str, outline: str | None = None, width: float = 1) -> None:
    draw.ellipse(box((cx-radius, cy-radius, cx+radius, cy+radius)), fill=fill,
                 outline=outline, width=max(1, round(width * SCALE)))


def base(p: Palette) -> Image.Image:
    im = Image.new("RGB", PIXELS, p.page)
    d = ImageDraw.Draw(im)
    roundrect(d, (1, 1, 759, 313), 18, p.body, p.border)
    # A restrained terminal title bar, clipped to the outer rounded shell.
    roundrect(d, (2, 2, 758, 52), 17, p.chrome)
    d.rectangle(box((2, 29, 758, 52)), fill=p.chrome)
    line(d, [(2, 52), (758, 52)], p.border)
    for x, color in ((22, "#E88A91"), (36, "#E3B95F"), (50, "#66C2A5")):
        circle(d, x, 26, 3.4, color)
    text(d, (68, 21), "mdrkabir / methods", 10, p.muted, "mono")
    text(d, (612, 21), "BLOOMINGTON, IN", 9, p.faint, "mono")

    roundrect(d, (27, 76, 31, 245), 2, p.violet)
    text(d, (48, 72), "PHD RESEARCHER / COMPUTER SCIENCE", 9.6, p.violet, "mono")
    text(d, (47, 99), "Md Rysul", 43, p.text, "bold")
    text(d, (47, 144), "Kabir", 43, p.text, "bold")
    text(d, (49, 208), "Computer Science Ph.D. student", 13.1, p.muted, "medium")
    text(d, (49, 228), "Indiana University Bloomington", 12.8, p.muted)
    line(d, [(49, 274), (349, 274)], p.divider)
    circle(d, 54, 292, 2.6, p.violet)
    circle(d, 66, 292, 2.6, p.teal)
    circle(d, 78, 292, 2.6, p.amber)
    text(d, (94, 286), "MODELS  ·  MEMORY  ·  INFERENCE", 8.8, p.faint, "mono")

    x, y, w, h = CARD
    roundrect(d, (x, y, x+w, y+h), 13, p.card, p.border)
    return im


def arrow(d: ImageDraw.ImageDraw, start: tuple[float, float],
          end: tuple[float, float], color: str, width: float = 1.5) -> None:
    line(d, [start, end], color, width)
    # All arrows in these compact diagrams point horizontally right.
    ex, ey = end
    line(d, [(ex-5, ey-4), end, (ex-5, ey+4)], color, width)


def llm_diagram(d: ImageDraw.ImageDraw, p: Palette) -> None:
    # A small conceptual flow from training through observed behavior to analysis.
    line(d, [(22, 180), (322, 180)], p.divider)
    for x, label, sub in ((47, "TUNE", "post-training"),
                          (172, "TEST", "behavior"),
                          (297, "TRACE", "mechanisms")):
        circle(d, x, 157, 21, p.violet_soft, p.violet, 1.25)
        circle(d, x, 157, 5.5, p.violet)
        text(d, (x-22, 194), label, 9.1, p.violet, "mono")
        text(d, (x-35, 209), sub, 8.5, p.muted)
    arrow(d, (73, 157), (139, 157), p.violet)
    arrow(d, (198, 157), (264, 157), p.violet)


def rl_diagram(d: ImageDraw.ImageDraw, p: Palette) -> None:
    # Multiple decays encode short and long memory traces on the same time axis.
    line(d, [(25, 220), (319, 220)], p.divider, 1.25)
    for x in (45, 95, 145, 195, 245, 295):
        line(d, [(x, 217), (x, 223)], p.faint)
    text(d, (24, 228), "NOW", 8.2, p.faint, "mono")
    text(d, (282, 228), "LATER", 8.2, p.faint, "mono")
    line(d, [(27, 202), (46, 153), (64, 188), (82, 199), (112, 207),
             (160, 215), (319, 219)], p.teal, 2)
    line(d, [(27, 202), (47, 168), (70, 175), (96, 182), (130, 190),
             (182, 201), (245, 211), (319, 216)], p.violet, 2)
    line(d, [(27, 202), (48, 183), (85, 185), (140, 187), (203, 190),
             (261, 194), (319, 197)], p.amber, 2)
    circle(d, 47, 168, 4, p.violet_soft, p.violet)
    circle(d, 47, 153, 4, p.teal_soft, p.teal)
    circle(d, 48, 183, 4, p.amber_soft, p.amber)


def bayes_diagram(d: ImageDraw.ImageDraw, p: Palette) -> None:
    # A hierarchical model pools individual estimates through one group level.
    top = (172, 155)
    lower = ((58, 195), (172, 195), (286, 195))
    for point in lower:
        line(d, [top, point], p.amber, 1.5)
    circle(d, *top, 17, p.amber_soft, p.amber, 1.4)
    text(d, (159, 149), "GROUP", 8.4, p.amber, "mono")
    for i, point in enumerate(lower, 1):
        circle(d, *point, 15, p.teal_soft, p.teal, 1.25)
        text(d, (point[0]-4.5, point[1]-6), str(i), 10, p.teal, "mono")
    line(d, [(27, 216), (317, 216)], p.divider)
    text(d, (23, 225), "SHARED PRIOR", 8.2, p.amber, "mono")
    text(d, (219, 225), "INDIVIDUALS", 8.2, p.teal, "mono")


TOPICS = (
    ("LLM POST-TRAINING", "Fine-tuning · safety evaluation", "violet", llm_diagram),
    ("RL & TEMPORAL MEMORY", "Agents · long-horizon decisions", "teal", rl_diagram),
    ("BAYESIAN MODELING", "Hierarchical inference · cognition", "amber", bayes_diagram),
)


def topic_layer(p: Palette, index: int) -> Image.Image:
    _, _, width, height = CARD
    im = Image.new("RGBA", (width*SCALE, height*SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    title, subtitle, color_key, diagram = TOPICS[index]
    accent = getattr(p, color_key)
    soft = getattr(p, f"{color_key}_soft")
    text(d, (21, 17), f"0{index+1} / 03", 9.4, accent, "mono")
    roundrect(d, (235, 15, 323, 35), 9, soft)
    text(d, (243, 21), "EXPERTISE", 8.2, accent, "mono")
    text(d, (21, 53), title, 19.5, p.text, "demi")
    text(d, (22, 83), subtitle, 10.4, p.muted)
    line(d, [(21, 109), (323, 109)], p.divider)
    # Draw diagrams on their own canvas so their labels remain inside the card.
    diagram_im = Image.new("RGBA", (im.width, (height+40)*SCALE),
                           (0, 0, 0, 0))
    diagram(ImageDraw.Draw(diagram_im), p)
    im.alpha_composite(diagram_im.crop((0, 20*SCALE, im.width,
                                        (height+20)*SCALE)))
    return im


def opacity(im: Image.Image, fraction: float) -> Image.Image:
    result = im.copy()
    result.putalpha(result.getchannel("A").point(lambda a: round(a*fraction)))
    return result


def frame(background: Image.Image, old: Image.Image, new: Image.Image | None = None,
          amount: float = 0) -> Image.Image:
    im = background.copy().convert("RGBA")
    x, y, _, _ = CARD
    if new is None:
        im.alpha_composite(old, xy((x, y)))
    else:
        # Fade through the card background rather than layering two sets of
        # small type and diagrams over each other during a transition.
        if amount < .5:
            im.alpha_composite(opacity(old, 1-2*amount),
                               xy((x-round(10*amount), y)))
        else:
            im.alpha_composite(opacity(new, 2*amount-1),
                               xy((x+round(10*(1-amount)), y)))
    return im.convert("RGB")


def build(theme: str) -> None:
    p = THEMES[theme]
    bg = base(p)
    layers = [topic_layer(p, i) for i in range(3)]
    frames: list[Image.Image] = []
    durations: list[int] = []
    for i, current in enumerate(layers):
        complete = frame(bg, current)
        frames.append(complete)
        durations.append(2600)
        if i == 0:
            complete.save(OUTPUT / f"hero-{theme}-still.png", optimize=True)
        following = layers[(i+1) % len(layers)]
        for amount in (.2, .4, .6, .8):
            frames.append(frame(bg, current, following, amount))
            durations.append(100)

    # One common palette prevents colors changing when the GIF advances.
    atlas = Image.new("RGB", (PIXELS[0]*3, PIXELS[1]), p.page)
    for i, layer in enumerate(layers):
        atlas.paste(frame(bg, layer), (PIXELS[0]*i, 0))
    palette = atlas.quantize(colors=96, method=Image.Quantize.MEDIANCUT,
                             dither=Image.Dither.NONE)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE)
               for im in frames]
    indexed[0].save(OUTPUT / f"hero-{theme}.gif", save_all=True,
                    append_images=indexed[1:], duration=durations,
                    loop=0, optimize=True, disposal=1)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        build(theme)
        print(f"Built {theme}: {OUTPUT / f'hero-{theme}.gif'}")


if __name__ == "__main__":
    main()
