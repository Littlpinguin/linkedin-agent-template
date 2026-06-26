#!/usr/bin/env python3
"""HTML standalone -> PNG @2x via Playwright.

Pour les cartes / infographies LinkedIn single-image (skill carte-linkedin).
Le HTML doit contenir un conteneur dimensionné 1080x1350 (4:5 portrait).

Usage:
    python3 scripts/screenshot.py <html_file> <out_png> [--width 1080] [--height 1350] [--scale 2]
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal  # journal unifié → outputs/registry.csv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("png", type=pathlib.Path)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--scale", type=int, default=2, help="device_scale_factor (2 -> sortie 2160x2700)")
    ap.add_argument("--wait-ms", type=int, default=1200,
                    help="Delai apres networkidle pour laisser les polices se rendre.")
    ap.add_argument("--slug", default="", help="slug pour le journal (défaut : nom du PNG)")
    ap.add_argument("--kind", default="carte", help="type journalisé")
    args = ap.parse_args()

    html_path = args.html.resolve()
    if not html_path.exists():
        sys.exit(f"ERREUR : {html_path} introuvable.")
    args.png.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(args.wait_ms)
        page.screenshot(
            path=str(args.png),
            clip={"x": 0, "y": 0, "width": args.width, "height": args.height},
        )
        browser.close()

    journal.log(kind=args.kind, slug=args.slug or args.png.stem,
                output=args.png, source=args.html, status="composé")
    print(f"OK -> {args.png}  ({args.width * args.scale}x{args.height * args.scale})")


if __name__ == "__main__":
    main()
