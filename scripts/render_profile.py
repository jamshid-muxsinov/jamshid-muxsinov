"""Render the committed GitHub snapshot as self-contained profile images."""

import base64
import calendar
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

TEXT = "#f5f5fa"
MUTED = "#bdc0d4"
LAVENDER = "#bbb5ff"
SURFACE = "#090a12"
BORDER = "#57596e"
LEVELS = ("#191b2d", "#343353", "#55538c", "#827bd8", "#b2a6ff")
TEXTURE = Path(__file__).resolve().parents[1] / "assets" / "stats" / "nebula.jpg"

# Stroke pictograms use a single 24-unit coordinate system.
ICONS = {
    "star": '<path fill="currentColor" stroke="none" d="m12 2 3.1 6.3 7 .9-5.1 5 1.2 7-6.2-3.3-6.2 3.3 1.2-7-5.1-5 7-.9Z"/>',
    "commit": '<circle cx="12" cy="12" r="5"/><path d="M2 12h5m10 0h5"/>',
    "pr": '<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/><path d="M6 7v10m12 0v-5a7 7 0 0 0-7-7m3-3-3 3 3 3"/>',
    "issue": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>',
    "repo": '<path d="M5 3h14v17H6a2.5 2.5 0 0 1-2.5-2.5V5A2 2 0 0 1 5 3Zm-.5 13H19M8 7h7"/>',
    "layers": '<path d="m2 7 10-5 10 5-10 5ZM2 12l10 5 10-5M2 17l10 5 10-5"/>',
    "flame": '<path d="M13 2c0 4-2 6-3 8-1-1-2-3-2-4-3 3-5 6-5 9a9 9 0 0 0 18 0c0-3-2-6-4-8 0 2-1 4-2 5 0-4 0-7-2-10Z"/>',
    "trophy": '<path d="M7 3h10v6a5 5 0 0 1-10 0Zm0 2H2v3a5 5 0 0 0 6 5m9-8h5v3a5 5 0 0 1-6 5m-4 1v5m-4 2h8m-7-2h6"/>',
}

GITHUB_MARK = (
    "M48.854 0C21.839 0 0 22 0 49.217c0 21.756 13.993 40.172 33.405 46.69 "
    "2.427.49 3.316-1.059 3.316-2.362 0-1.141-.08-5.052-.08-9.127-13.59 "
    "2.934-16.42-5.867-16.42-5.867-2.184-5.704-5.42-7.17-5.42-7.17-4.448-3.015"
    ".324-3.015.324-3.015 4.934.326 7.523 5.052 7.523 5.052 4.367 7.496 11.404 "
    "5.378 14.235 4.074.404-3.178 1.699-5.378 3.074-6.6-10.839-1.141-22.243-5.378"
    "-22.243-24.283 0-5.378 1.94-9.778 5.014-13.2-.485-1.222-2.184-6.275.486-13.038 "
    "0 0 4.125-1.304 13.426 5.052a46.97 46.97 0 0 1 12.214-1.63c4.125 0 8.33.571 "
    "12.213 1.63 9.302-6.356 13.427-5.052 13.427-5.052 2.67 6.763.97 11.816.485 "
    "13.038 3.155 3.422 5.015 7.822 5.015 13.2 0 18.905-11.404 23.06-22.324 "
    "24.283 1.78 1.548 3.316 4.481 3.316 9.126 0 6.6-.08 11.897-.08 13.526 "
    "0 1.304.89 2.853 3.316 2.364 19.412-6.52 33.405-24.935 33.405-46.691"
    "C97.707 22 75.788 0 48.854 0z"
)


def svg(width, height, title, description, body):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        'role="img" aria-labelledby="title description" '
        'font-family="system-ui, -apple-system, Segoe UI, sans-serif">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="description">{escape(description)}</desc>\n'
        f'{body}\n</svg>\n'
    )


def label(x, y, value, size, color=TEXT, weight=400, anchor="start"):
    return (
        f'<text x="{x:g}" y="{y:g}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'
    )


def icon(name, x, y, size, color=LAVENDER):
    return (
        f'<g transform="translate({x:g} {y:g}) scale({size / 24:.4f})" '
        f'fill="none" color="{color}" stroke="currentColor" stroke-width="1.9" '
        f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>'
    )


def stat_defs():
    texture = base64.b64encode(TEXTURE.read_bytes()).decode("ascii")
    return f'''<defs>
  <image id="nebula" width="167" height="165" xlink:href="data:image/jpeg;base64,{texture}"/>
  <linearGradient id="main-veil">
    <stop stop-color="#08090f" stop-opacity=".99"/><stop offset=".52" stop-color="#08090f" stop-opacity=".98"/>
    <stop offset=".65" stop-color="#0b0a19" stop-opacity=".14"/><stop offset="1" stop-color="#0b0a19" stop-opacity=".04"/>
  </linearGradient>
  <linearGradient id="small-veil" x1="0" y1="0" x2=".8" y2="1">
    <stop stop-color="#21182d" stop-opacity=".04"/><stop offset=".28" stop-color="#0b0c14" stop-opacity=".93"/>
    <stop offset=".70" stop-color="#0b0c14" stop-opacity=".97"/><stop offset="1" stop-color="#181327" stop-opacity=".08"/>
  </linearGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="#8b99fb"/><stop offset=".42" stop-color="#7a7bdc"/>
    <stop offset=".72" stop-color="#d8c2ff"/><stop offset="1" stop-color="#a193fa"/>
  </linearGradient>
  <radialGradient id="halo"><stop offset=".55" stop-color="#090b17" stop-opacity="0"/>
    <stop offset=".70" stop-color="#6864cf" stop-opacity=".45"/>
    <stop offset=".83" stop-color="#7c6dce" stop-opacity=".15"/><stop offset="1" stop-color="#6c62bb" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="core"><stop stop-color="#151628"/><stop offset=".70" stop-color="#11111f"/>
    <stop offset="1" stop-color="#27263f"/></radialGradient>
  <filter id="bloom" x="-.2" y="-.2" width="1.4" height="1.4"><feGaussianBlur stdDeviation="3"/></filter>
</defs>'''


def surface(x, y, w, h, name, content, main=False):
    veil = "main-veil" if main else "small-veil"
    texture_x = w * .49 if main else 0
    return f'''<g transform="translate({x} {y})">
  <clipPath id="clip-{name}"><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13"/></clipPath>
  <g clip-path="url(#clip-{name})">
    <rect width="{w}" height="{h}" fill="{SURFACE}"/>
    <use xlink:href="#nebula" transform="translate({texture_x:g} 0) scale({(w - texture_x) / 167:.4f} {h / 165:.4f})"/>
    <rect width="{w}" height="{h}" fill="url(#{veil})"/>
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13" fill="none" stroke="{BORDER}"/>
  {content}
</g>'''


def medallion(x, y, motion):
    glint = '''
  <style>
    @media (prefers-reduced-motion: no-preference) {
      .rim-glint { animation: sweep 9s linear infinite; }
      @keyframes sweep {
        from { opacity: 1; stroke-dashoffset: 0; }
        to { opacity: 1; stroke-dashoffset: -100; }
      }
    }
  </style>
  <g class="rim-glint" opacity="0" fill="none" stroke-linecap="round">
    <circle r="43" pathLength="100" stroke="#d1c5ff" stroke-width="3.1"
            stroke-dasharray="8 92" opacity=".54"/>
    <circle r="43" pathLength="100" stroke="#f5efff" stroke-width="2.5"
            stroke-dasharray="4 96" transform="rotate(7.2)"/>
  </g>''' if motion else ""
    return f'''<g transform="translate({x:g} {y:g})">
  <circle r="66" fill="url(#halo)"/>
  <circle r="43" fill="none" stroke="url(#rim)" stroke-width="7" opacity=".5" filter="url(#bloom)"/>
  <circle r="43" fill="url(#core)" stroke="#5d5caa" stroke-width="1.3"/>
  <circle r="43" fill="none" stroke="url(#rim)" stroke-width="3.2"
          stroke-dasharray="201 70" transform="rotate(-89)"/>{glint}
  <circle r="47" fill="none" stroke="#9394e4" stroke-opacity=".78"
          stroke-width="1.2" stroke-dasharray="64 232" transform="rotate(186)"/>
  <path transform="translate(-17 -17) scale(.35)" d="{GITHUB_MARK}" fill="#f6f5fa"/>
</g>'''


def number(value):
    return "—" if value is None else f"{value:,}"


def short_date(value):
    day = date.fromisoformat(value)
    return f"{calendar.month_abbr[day.month]} {day.day}"


def main_card(snapshot, width, mobile=False, motion=False):
    metrics = snapshot["metrics"]
    year = snapshot["as_of"][:4]
    rows = [
        ("star", "Total stars earned", metrics["stars"]),
        ("commit", f"Public commits ({year})", metrics["commits"]),
        ("pr", "Total pull requests", metrics["pull_requests"]),
        ("issue", "Total issues", metrics["issues"]),
        ("repo", "Contributed repos · recent", metrics["repositories"]),
    ]
    left = 15 if mobile else 22
    value_x = width - (18 if mobile else 140)
    parts = [label(left, 29 if mobile else 28, "Jamshid’s GitHub Stats",
                   16.5 if mobile else 15, weight=650)]
    for i, (symbol, caption, value) in enumerate(rows):
        baseline = 61 + i * 27 if mobile else 56 + i * 25
        parts.extend([
            icon(symbol, left, baseline - 11.8, 15 if mobile else 14),
            label(left + 26, baseline, caption, 14.4 if mobile else 12.1),
            label(value_x, baseline, number(value), 15.5 if mobile else 12.8, weight=650, anchor="end"),
        ])
    if mobile:
        parts.append(f'<g transform="translate({width - 27} 25) scale(.36)">{medallion(0, 0, motion)}</g>')
    else:
        parts.append(medallion(width - 68, 88, motion))
    return surface(0, 0, width, 185 if mobile else 177, "main", "\n".join(parts), main=True)


def small_card(x, y, w, h, name, value, caption, foot, mobile):
    accent = {"layers": "#9ca7ff", "flame": "#99a5ff", "trophy": "#c19aff"}[name]
    if mobile:
        detail = " ".join(foot)
        if name == "layers":
            detail = ", ".join(foot)
        parts = [
            icon(name, 15, 12, 21, accent),
            label(46, 28, " ".join(caption), 15.2, weight=550),
            label(w - 16, 29, number(value), 22, weight=650, anchor="end"),
            label(46, 47, detail, 13.3, MUTED),
        ]
        return surface(x, y, w, h, name, "\n".join(parts))
    cx = w / 2
    parts = [
        icon(name, cx - 12, 20, 24, accent),
        label(cx, 83, number(value), 27, weight=650, anchor="middle"),
    ]
    for i, line in enumerate(caption):
        parts.append(label(cx, 110 + 16 * i, line, 12.1, anchor="middle"))
    for i, line in enumerate(foot):
        parts.append(label(cx, h - 13 - (len(foot) - 1 - i) * 13, line, 10.1, MUTED, anchor="middle"))
    return surface(x, y, w, h, name, "\n".join(parts))


def statistics(snapshot, mobile=False, motion=False):
    year = snapshot["as_of"][:4]
    current = snapshot["streaks"]["current"]
    longest = snapshot["streaks"]["longest"]
    w, h, main_width = (280, 386, 280) if mobile else (775, 177, 390)
    best_dates = ["Consecutive days"]
    if longest["start"]:
        start = date.fromisoformat(longest["start"])
        end = date.fromisoformat(longest["end"])
        first = short_date(longest["start"])
        if start.year != end.year:
            first += f", {start.year}"
        best_dates = [first + " –", short_date(longest["end"]) + f", {end.year}"]
    specifications = [
        ("layers", snapshot["metrics"]["contributions"], ["Total", "Contributions"],
         [f"Jan 1 – {short_date(snapshot['as_of'])}", year]),
        ("flame", current["days"], ["Current Streak"], ["Consecutive days"]),
        ("trophy", longest["days"], ["Longest Streak"], best_dates),
    ]
    parts = [stat_defs(), main_card(snapshot, main_width, mobile, motion)]
    for i, (name, value, caption, foot) in enumerate(specifications):
        x, y, cw, ch = (0, 192 + 67 * i, 280, 60) if mobile else (402 + 128 * i, 0, 117, 177)
        parts.append(small_card(x, y, cw, ch, name, value, caption, foot, mobile))
    description = (
        f"Public GitHub statistics for {snapshot['login']} through {snapshot['as_of']}. "
        f"Stars on owned public repositories, public indexed commits in {year}, "
        "public authored pull requests and issues, and recent contributed repositories. "
        "Contribution totals are year to date. Streaks use the account’s contribution calendar. "
        "A dash denotes an unavailable count."
    )
    return svg(w, h, "Jamshid’s GitHub statistics", description, "\n".join(parts))


def calendar_band(days, start, end, x, y, width, height, mobile=False):
    """Lay out real dates on a Sunday-first grid. Leave dates outside the snapshot blank."""
    sunday = start - timedelta(days=(start.weekday() + 1) % 7)
    n_weeks = (end - sunday).days // 7 + 1
    step_x, step_y = width / n_weeks, height / 7
    gap_x, gap_y = step_x * .18, step_y * .18
    fragments = []
    for i, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        fragments.append(label(x - 8, y + step_y * (i + .68), name, 13 if mobile else 10.7, MUTED, anchor="end"))
    for month in range(start.month, end.month + 1):
        first = date(start.year, month, 1)
        col = (first - sunday).days // 7
        fragments.append(label(x + step_x * col, y - 12, calendar.month_abbr[month], 13.5 if mobile else 11.3))
    for day in days:
        dt = date.fromisoformat(day["date"])
        if not start <= dt <= end:
            continue
        col, row = divmod((dt - sunday).days, 7)
        color = LEVELS[day["level"]]
        fragments.append(
            f'<rect x="{x + col * step_x:.2f}" y="{y + row * step_y:.2f}" '
            f'width="{step_x - gap_x:.2f}" height="{step_y - gap_y:.2f}" '
            f'rx="2" fill="{color}"><title>{dt}: {day["count"]}</title></rect>'
        )
    return "\n".join(fragments)


def contributions(snapshot, mobile=False):
    start = date.fromisoformat(snapshot["start"])
    end = date.fromisoformat(snapshot["as_of"])
    count = number(snapshot["metrics"]["contributions"])
    w, h = (280, 285) if mobile else (775, 210)
    parts = [f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{SURFACE}" stroke="{BORDER}"/>']
    if mobile:
        intervals = [(start, date(start.year, 6, 30), 39),
                     (date(start.year, 7, 1), date(start.year, 12, 31), 140)]
        for first, last, y in intervals:
            parts.append(calendar_band(snapshot["days"], first, last, 44, y, 225, 68, mobile=True))
    else:
        parts.append(calendar_band(snapshot["days"], start, date(start.year, 12, 31), 55, 47, 703, 107))
    baseline = h - 20
    if mobile:
        parts.append(label(w / 2, 238, f"{count} contributions in {end.year}", 15, weight=550, anchor="middle"))
    else:
        parts.append(label(23, baseline, f"{count} contributions in {end.year}", 12.3, weight=550))
    key_x = 103 if mobile else w - 127
    cell = 10 if mobile else 11
    gap = 3 if mobile else 4
    parts.append(label(key_x - 8, baseline, "Less", 13 if mobile else 12, MUTED, anchor="end"))
    for i, color in enumerate(LEVELS):
        parts.append(f'<rect x="{key_x + i * (cell + gap)}" y="{baseline - cell + 1}" width="{cell}" height="{cell}" rx="2" fill="{color}"/>')
    parts.append(label(key_x + 5 * (cell + gap) + 3, baseline, "More", 13 if mobile else 12, MUTED))
    description = (
        f"{snapshot['login']} made {count} GitHub contributions from {start} through {end}. "
        "Each square represents a day. Brighter violet indicates a higher GitHub contribution level."
    )
    return svg(w, h, "Contribution Graph", description, "\n".join(parts))


def render_assets(snapshot):
    """Return image contents by basename, without modifying the output directory."""
    return {
        "statistics.svg": statistics(snapshot),
        "statistics-mobile.svg": statistics(snapshot, mobile=True),
        "statistics-motion.svg": statistics(snapshot, motion=True),
        "statistics-mobile-motion.svg": statistics(snapshot, mobile=True, motion=True),
        "contributions.svg": contributions(snapshot),
        "contributions-mobile.svg": contributions(snapshot, mobile=True),
    }
