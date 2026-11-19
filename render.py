#!/usr/bin/env python3
"""Fieldnotes - World Desk: deterministic news-poster generator.

Draws entry.png (1024x1024, RGB) next to this file using Pillow.
No randomness, no timestamps, no external assets: the same code always
produces byte-identical output.

Editorial basis: SOURCES.md (19 Nov 2026, early edition, reporting
through 14:00 UTC). The lead illustration is a symbolic conference
table with labeled country seats, not depictions of real leaders.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
BG = "#F4F0E8"
INK = "#14233D"
MUTED = "#58677C"
BLUE = "#2454E8"
CYAN = "#75E0D0"
ORANGE = "#F06A45"
WHITE = "#FFFFFF"

PANEL_DEEP = "#203757"      # inner table ellipse fill
PANEL_RIM = "#60718D"       # outer table ellipse outline
DATE_GREY = "#C6D1E0"       # date text inside lead panel
KICKER_PALE = "#DCE6F7"     # kicker text on blue / orange cards
CARD2_FILL = "#DDEBE6"
CN_RED = "#E44B4B"
RU_BLUE = "#7B9CF4"
FOOTER_LINE = "#B7C0CA"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def bold(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", size)


def sans(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", size)


def mono(size):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSansMono.ttf", size)


# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, font, max_width):
    """Greedy word wrap measured with the real font metrics."""
    lines = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered_text(draw, center_x, center_y, text, font, fill):
    draw.text((center_x, center_y), text, font=font, fill=fill, anchor="mm")


# ---------------------------------------------------------------- drawing
def draw_header(draw):
    draw.rectangle((0, 0, 1024, 12), fill=BLUE)
    draw.text((54, 38), "FIELDNOTES   /   WORLD DESK", font=bold(17), fill=BLUE)
    draw.text((54, 72), "THURSDAY  ·  19 NOV 2026", font=mono(18), fill=MUTED)
    # GLOBAL BRIEF pill
    draw.rounded_rectangle((750, 37, 970, 77), radius=18, fill=INK)
    draw.ellipse((768, 51, 780, 63), fill=ORANGE)
    draw.text((791, 48), "GLOBAL BRIEF", font=bold(15), fill=WHITE)


def draw_headline(draw):
    draw.text((52, 115), "POWER SHIFTS.", font=bold(52), fill=INK)
    draw.text((52, 172), "PRESSURE BUILDS.", font=bold(52), fill=INK)
    draw.text(
        (55, 238),
        "EARLY EDITION  /  Reporting through 14:00 UTC",
        font=sans(19),
        fill=MUTED,
    )


def draw_table(draw):
    """Symbolic conference table: two ellipses, APEC badge, three seats."""
    draw.text((681, 326), "19 NOV  ·  SHENZHEN", font=mono(13), fill=DATE_GREY)
    draw.ellipse((660, 366, 916, 510), outline=PANEL_RIM, width=3)
    draw.ellipse((690, 390, 886, 490), fill=PANEL_DEEP, outline=CYAN, width=2)
    draw.rounded_rectangle((747, 421, 829, 459), radius=17, fill=BLUE)
    draw.text((764, 430), "APEC", font=bold(17), fill=WHITE)

    seats = [
        # (top-left x, top-left y, fill, label)
        (649, 366, ORANGE, "US"),
        (857, 366, CN_RED, "CN"),
        (753, 502, RU_BLUE, "RU"),
    ]
    for x, y, color, label in seats:
        # thick arc hugging the underside of the seat, in the seat color
        draw.arc((x - 7, y - 7, x + 57, y + 57), start=15, end=165,
                 fill=color, width=5)
        draw.ellipse((x, y, x + 50, y + 50), fill=color, outline=BG, width=3)
        centered_text(draw, x + 25, y + 25, label, bold(14), WHITE)


def draw_lead_panel(draw):
    draw.rounded_rectangle((48, 282, 976, 570), radius=28, fill=INK)
    # tag
    draw.rounded_rectangle((72, 305, 238, 340), radius=16, fill=ORANGE)
    draw.text((88, 313), "TALKS BEGIN", font=bold(14), fill=INK)
    # kicker + headline
    draw.text((73, 362), "SHENZHEN  /  APEC", font=mono(17), fill=CYAN)
    draw.text((73, 397), "THREE POWERS,", font=bold(38), fill=WHITE)
    draw.text((73, 440), "ONE TABLE.", font=bold(38), fill=WHITE)
    # names + body
    draw.text((75, 499), "Trump · Xi · Putin", font=bold(21), fill=CYAN)
    draw.text((75, 527), "US, Chinese and Russian leaders begin",
              font=sans(16), fill=WHITE)
    draw.text((75, 548), "trilateral talks at the APEC summit.",
              font=sans(16), fill=WHITE)
    draw_table(draw)


def draw_card(draw, x, y, fill, kicker, kicker_color, title, title_color,
              icon_color, body, body_color, tag_fill, tag_text, tag_color):
    draw.rounded_rectangle((x, y, x + 296, y + 300), radius=22, fill=fill)
    draw.text((x + 20, y + 20), kicker, font=mono(13), fill=kicker_color)
    draw.text((x + 20, y + 55), title, font=bold(31), fill=title_color)
    # icon: horizontal line + filled dot under the title
    draw.line((x + 20, y + 108, x + 68, y + 108), fill=icon_color, width=3)
    draw.ellipse((x + 73, y + 103, x + 83, y + 113), fill=icon_color)
    # body, word-wrapped to the card's inner width
    body_font = sans(16)
    lines = wrap_text(draw, body, body_font, 296 - 40)
    for i, line in enumerate(lines):
        draw.text((x + 20, y + 137 + i * 24), line, font=body_font,
                  fill=body_color)
    # tag pill with centered label
    draw.rounded_rectangle((x + 18, y + 252, x + 278, y + 283), radius=14,
                           fill=tag_fill)
    centered_text(draw, x + 148, y + 267, tag_text, bold(11), tag_color)


def draw_cards(draw):
    y = 594
    draw_card(
        draw, 48, y,
        fill=BLUE,
        kicker="01  /  BERLIN", kicker_color=KICKER_PALE,
        title="UKRAINE", title_color=WHITE,
        icon_color=CYAN,
        body=("European allies plan Berlin talks with US envoys, backing "
              "Kyiv and seeking post-war security guarantees."),
        body_color=WHITE,
        tag_fill=WHITE, tag_text="DIPLOMACY", tag_color=INK,
    )
    draw_card(
        draw, 362, y,
        fill=CARD2_FILL,
        kicker="02  /  ANTALYA", kicker_color=INK,
        title="COP31", title_color=INK,
        icon_color=BLUE,
        body=("A report published today details divisions over fossil "
              "fuels, climate finance and IPCC report timing."),
        body_color=INK,
        tag_fill=INK, tag_text="19 NOV REPORT", tag_color=WHITE,
    )
    draw_card(
        draw, 676, y,
        fill=ORANGE,
        kicker="03  /  RIYADH", kicker_color=KICKER_PALE,
        title="YEMEN", title_color=WHITE,
        icon_color=INK,
        body=("Saudi coalition says it dealt with a Houthi missile threat; "
              "debris damage is being assessed."),
        body_color=WHITE,
        tag_fill=WHITE, tag_text="DEVELOPING", tag_color=INK,
    )


def draw_footer(draw):
    draw.line((52, 922, 972, 922), fill=FOOTER_LINE, width=2)
    draw.text((54, 940), "DIPLOMACY  ·  CLIMATE  ·  REGIONAL SECURITY",
              font=bold(13), fill=INK)
    draw.text(
        (54, 965),
        "Sources: ABC News · Reuters · AFP  /  19 Nov 2026  /  "
        "Original illustration",
        font=sans(12),
        fill=MUTED,
    )
    draw.text((812, 940), "WORLD DESK", font=mono(12), fill=BLUE)


def render():
    img = Image.new("RGB", (1024, 1024), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_headline(draw)
    draw_lead_panel(draw)
    draw_cards(draw)
    draw_footer(draw)
    return img


def main():
    out = Path(__file__).resolve().parent / "entry.png"
    render().save(out, format="PNG")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
