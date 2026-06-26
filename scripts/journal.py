#!/usr/bin/env python3
"""Journal unifié de toutes les productions visuelles du linkedin-agent.

Une seule ligne par production (image générée, carte composée, carrousel exporté),
toujours écrite dans linkedin-agent/outputs/registry.csv. Tout reste sous linkedin-agent.

Usage CLI :
    python3 scripts/journal.py --kind carte --slug mon-post \
        --output outputs/carte-mon-post/carte.png --source outputs/carte-mon-post/index.html

Usage import (depuis un autre script du dossier scripts/) :
    import journal
    journal.log(kind="image", slug="...", output=png_path, source=prompt_file, model="...")
"""
import argparse
import csv
import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "outputs" / "registry.csv"
FIELDS = [
    "logged_at", "date", "kind", "slug", "output", "source",
    "model", "refs", "ai_disclosure", "status", "notes",
]


def _rel(p):
    """Chemin relatif à la racine du projet si possible (sinon tel quel)."""
    try:
        return str(pathlib.Path(p).resolve().relative_to(ROOT))
    except (ValueError, TypeError):
        return str(p)


def log(kind, slug, output, source="", model="", refs="",
        ai_disclosure="", status="", notes=""):
    """Ajoute une ligne au registre unifié outputs/registry.csv."""
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    new_file = not REGISTRY.exists()
    with REGISTRY.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        w.writerow({
            "logged_at": datetime.datetime.utcnow().isoformat() + "Z",
            "date": datetime.date.today().isoformat(),
            "kind": kind,
            "slug": slug,
            "output": _rel(output),
            "source": _rel(source) if source else "",
            "model": model,
            "refs": refs,
            "ai_disclosure": ai_disclosure,
            "status": status,
            "notes": notes,
        })
    return REGISTRY


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, help="image | carte | carrousel")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--source", default="")
    ap.add_argument("--model", default="")
    ap.add_argument("--refs", default="")
    ap.add_argument("--ai-disclosure", default="")
    ap.add_argument("--status", default="")
    ap.add_argument("--notes", default="")
    a = ap.parse_args()
    reg = log(a.kind, a.slug, a.output, a.source, a.model, a.refs,
              a.ai_disclosure, a.status, a.notes)
    print(f"journalisé → {reg}")
