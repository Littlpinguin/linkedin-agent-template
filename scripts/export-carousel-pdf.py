#!/usr/bin/env python3
"""Exporte un carrousel HTML standalone vers un PDF multipage via Playwright.

Le HTML doit être structuré avec une section par slide + `page-break-after: always`
+ une règle `@page { size: <w>px <h>px; margin: 0 }` qui définit la taille de page.

Usage:
    python3 scripts/export-carousel-pdf.py <html_file> <out_pdf> [--width 1080] [--height 1350]

Exemple :
    python3 scripts/export-carousel-pdf.py \\
        06-graphic-design/outputs/carrousel-da-vs-ia-2026-05-13/index.html \\
        06-graphic-design/outputs/carrousel-da-vs-ia-2026-05-13/exports/carrousel-da-vs-ia.pdf
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
    ap.add_argument("pdf", type=pathlib.Path)
    ap.add_argument("--width", default="1080px")
    ap.add_argument("--height", default="1350px")
    ap.add_argument("--wait-ms", type=int, default=1200,
                    help="Délai après chargement réseau pour laisser les polices se rendre.")
    ap.add_argument("--slug", default="", help="slug pour le journal (défaut : nom du PDF)")
    ap.add_argument("--kind", default="carrousel", help="type journalisé")
    args = ap.parse_args()

    html_path = args.html.resolve()
    if not html_path.exists():
        sys.exit(f"ERREUR : {html_path} introuvable.")
    args.pdf.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={
            "width": int(args.width.rstrip("px")),
            "height": int(args.height.rstrip("px")),
        })
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(args.wait_ms)
        page.pdf(
            path=str(args.pdf),
            width=args.width,
            height=args.height,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        browser.close()

    journal.log(kind=args.kind, slug=args.slug or args.pdf.stem,
                output=args.pdf, source=args.html, status="exporté")
    print(f"OK → {args.pdf}")


if __name__ == "__main__":
    main()
