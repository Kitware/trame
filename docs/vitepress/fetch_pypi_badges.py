#!/usr/bin/env python3
"""
Render "downloads/month" SVG badges for each trame package.

Historically these badges were downloaded straight from shields.io's dynamic
`/pypi/dm/<package>` endpoint. That endpoint proxies a call to
pypistats.org/PyPI's BigQuery dataset on shields.io's own servers, and when
that upstream call is rate limited shields.io still answers HTTP 200 but
silently serves a generic placeholder badge instead of an error - so a
successful HTTP response doesn't mean the data is real.

To get real data reliably we fetch the monthly download count ourselves from
pypistats.org and render the SVG locally, removing shields.io from the loop
entirely. pypistats.org applies its own IP-based rate limiting, so a package
whose fetch fails after a couple of retries is simply skipped and its
existing badge file (if any) is left untouched rather than being blanked out
or replaced with bad data.
"""

import time
import warnings
from pathlib import Path

import requests

PACKAGES = [
    "trame",
    "trame-client",
    "trame-code",
    "trame-colormaps",
    "trame-common",
    "trame-components",
    "trame-dataclass",
    "trame-datagrid",
    "trame-deckgl",
    "trame-dockview",
    "trame-iframe",
    "trame-image-tools",
    "trame-leaflet",
    "trame-markdown",
    "trame-matplotlib",
    "trame-plotly",
    "trame-quasar",
    "trame-radial-menu",
    "trame-rca",
    "trame-router",
    "trame-server",
    "trame-simput",
    "trame-slicer",
    "trame-tauri",
    "trame-vega",
    "trame-vtk",
    "trame-vtklocal",
    "trame-vuetify",
    "trame-xterm",
]

OUTPUT_DIR = Path(__file__).with_name(".vitepress") / "dist" / "downloads"
LIVE_SITE_URL = "https://kitware.github.io/trame/downloads"

LABEL = "downloads"
LABEL_COLOR = "#555"
MESSAGE_COLOR = "#4b0"
REQUEST_DELAY_SECONDS = 1
MAX_ATTEMPTS_PER_PACKAGE = 2
RETRY_BACKOFF_SECONDS = 5

# Approximate Verdana-11 advance widths (px). Close enough for a badge: the
# SVG pins each text run to an explicit textLength, so glyphs are stretched
# to fit rather than needing pixel-perfect metrics.
CHAR_WIDTHS = {
    " ": 4,
    "!": 4,
    '"': 5,
    "#": 8,
    "$": 8,
    "%": 11,
    "&": 10,
    "'": 3,
    "(": 5,
    ")": 5,
    "*": 6,
    "+": 8,
    ",": 4,
    "-": 5,
    ".": 4,
    "/": 4,
    "0": 8,
    "1": 8,
    "2": 8,
    "3": 8,
    "4": 8,
    "5": 8,
    "6": 8,
    "7": 8,
    "8": 8,
    "9": 8,
    ":": 4,
    ";": 4,
    "<": 8,
    "=": 8,
    ">": 8,
    "?": 7,
    "@": 13,
    "A": 9,
    "B": 8,
    "C": 8,
    "D": 9,
    "E": 7,
    "F": 7,
    "G": 9,
    "H": 9,
    "I": 4,
    "J": 4,
    "K": 8,
    "L": 7,
    "M": 10,
    "N": 9,
    "O": 10,
    "P": 8,
    "Q": 10,
    "R": 8,
    "S": 8,
    "T": 7,
    "U": 9,
    "V": 9,
    "W": 13,
    "X": 8,
    "Y": 8,
    "Z": 8,
    "a": 7,
    "b": 8,
    "c": 6,
    "d": 8,
    "e": 7,
    "f": 4,
    "g": 8,
    "h": 8,
    "i": 3,
    "j": 3,
    "k": 7,
    "l": 3,
    "m": 12,
    "n": 8,
    "o": 8,
    "p": 8,
    "q": 8,
    "r": 5,
    "s": 6,
    "t": 4,
    "u": 8,
    "v": 7,
    "w": 10,
    "x": 7,
    "y": 7,
    "z": 6,
}


def github_action_formatwarning(message, category, filename, lineno, line=None):
    safe_message = str(message).replace(":", "%3A").replace(",", "%2C")
    return f"::warning file={filename},line={lineno},title={category.__name__}::{safe_message}\n"


warnings.formatwarning = github_action_formatwarning


def text_width(text: str) -> float:
    return sum(CHAR_WIDTHS.get(ch, 8) for ch in text)


def humanize(n: int) -> str:
    if n < 1000:
        return str(n)
    for unit, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "k")):
        value = n / unit
        if round(value, 1) < 1:
            continue
        if value < 10:
            text = f"{value:.1f}".rstrip("0").rstrip(".")
        else:
            text = str(round(value))
        return f"{text}{suffix}"
    return str(n)


def render_badge(message: str) -> str:
    label_w = round(text_width(LABEL) + 10)
    msg_w = round(text_width(message) + 10)
    total_w = label_w + msg_w
    label_x = label_w * 5
    label_len = round(text_width(LABEL) * 10)
    msg_x = round((label_w + msg_w / 2) * 10)
    msg_len = round(text_width(message) * 10)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20" '
        f'role="img" aria-label="{LABEL}: {message}">'
        f"<title>{LABEL}: {message}</title>"
        f'<linearGradient id="s" x2="0" y2="100%">'
        f'<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>'
        f'<stop offset="1" stop-opacity=".1"/></linearGradient>'
        f'<clipPath id="r"><rect width="{total_w}" height="20" rx="3"/></clipPath>'
        f'<g clip-path="url(#r)">'
        f'<rect width="{label_w}" height="20" fill="{LABEL_COLOR}"/>'
        f'<rect x="{label_w}" width="{msg_w}" height="20" fill="{MESSAGE_COLOR}"/>'
        f'<rect width="{total_w}" height="20" fill="url(#s)"/>'
        f"</g>"
        f'<g fill="#fff" text-anchor="middle" '
        f'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="110" '
        f'text-rendering="geometricPrecision">'
        f'<g transform="scale(.1)">'
        f'<text x="{label_x}" y="140" textLength="{label_len}">{LABEL}</text>'
        f"</g>"
        f'<g transform="scale(.1)">'
        f'<text x="{msg_x}" y="140" textLength="{msg_len}">{message}</text>'
        f"</g></g></svg>"
    )


def seed_from_live_site(package: str, dest: Path) -> None:
    """Best-effort pre-fill so a fresh checkout (no previous badge on disk)
    still has a real "last known good" badge to fall back on, sourced from
    what's already deployed rather than a generic placeholder."""
    try:
        response = requests.get(f"{LIVE_SITE_URL}/{package}.svg", timeout=10)
        if response.status_code == 200:
            dest.write_bytes(response.content)
    except requests.RequestException:
        pass


class RateLimited(Exception):
    pass


def fetch_monthly_downloads(package: str) -> int | None:
    url = f"https://pypistats.org/api/packages/{package}/recent"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        warnings.warn(f"Error fetching stats for {package}: {e}")
        return None

    if response.status_code == 200:
        return response.json()["data"]["last_month"]

    if response.status_code == 429:
        raise RateLimited(package)

    warnings.warn(
        f"Failed to fetch stats for {package}, status code: {response.status_code}"
    )
    return None


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    fetch_list = list(PACKAGES)
    update_count = 1
    max_attempts = 5

    while fetch_list and update_count + max_attempts > 0:
        max_attempts -= 1
        print(f"\nFetching {len(fetch_list)} packages stats")
        update_count = 0
        current_fetch_list = list(fetch_list)
        fetch_list.clear()
        for package in current_fetch_list:
            dest = OUTPUT_DIR / f"{package}.svg"

            if not dest.exists():
                seed_from_live_site(package, dest)

            try:
                print(".", end="", flush=True)
                downloads = fetch_monthly_downloads(package)
                results[package] = downloads
                update_count += 1
            except RateLimited:
                fetch_list.append(package)
            finally:
                time.sleep(REQUEST_DELAY_SECONDS)

    print("\n----------------------")
    for fail_package in fetch_list:
        print(f"    {fail_package}: FAILED")

    for package, downloads in results.items():
        dest = OUTPUT_DIR / f"{package}.svg"
        message = f"{humanize(downloads)}/month"
        dest.write_text(render_badge(message))
        print(f"    {package}: {message}")
    print("----------------------")
