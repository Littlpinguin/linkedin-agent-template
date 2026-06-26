#!/usr/bin/env python3
"""Génère une image via Gemini (Nano Banana Pro) selon l'identité visuelle du profil.

Usage:
    python3 scripts/gen-image.py --slug <slug> --prompt-file <path> [--ref img1.png img2.png] [--aspect 16:9]

La clé GOOGLE_AI_API_KEY et GOOGLE_AI_IMAGE_MODEL sont lues depuis .env.
Sortie : outputs/images/YYYY-MM-DD-<slug>.png (+ .json sidecar + ligne registry.csv).
"""
import argparse, base64, csv, datetime, json, mimetypes, os, pathlib, sys

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "outputs" / "images"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal  # journal unifié → outputs/registry.csv


def load_env():
    env = {}
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    # variables d'environnement réelles ont priorité si non vides
    for k in ("GOOGLE_AI_API_KEY", "GOOGLE_AI_IMAGE_MODEL"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--ref", nargs="*", default=[], help="images de référence (chemins relatifs au repo)")
    ap.add_argument("--aspect", default="16:9")
    args = ap.parse_args()

    env = load_env()
    api_key = env.get("GOOGLE_AI_API_KEY", "")
    model = env.get("GOOGLE_AI_IMAGE_MODEL", "gemini-3-pro-image-preview")
    if not api_key:
        sys.exit("ERREUR : GOOGLE_AI_API_KEY est vide dans .env. Ajoute une clé Google AI Studio avant de lancer.")

    prompt = pathlib.Path(args.prompt_file).read_text()

    parts = [{"text": prompt}]
    for ref in args.ref:
        p = (ROOT / ref).resolve()
        mime = mimetypes.guess_type(str(p))[0] or "image/png"
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(p.read_bytes()).decode()}})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": args.aspect},
        },
    }
    r = requests.post(url, params={"key": api_key}, json=payload, timeout=180)
    if r.status_code != 200:
        sys.exit(f"ERREUR API {r.status_code}: {r.text[:2000]}")
    data = r.json()
    img_b64 = None
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                img_b64 = inline["data"]
                break
        if img_b64:
            break
    if not img_b64:
        sys.exit(f"Pas d'image dans la réponse : {json.dumps(data)[:2000]}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    png_path = OUTDIR / f"{today}-{args.slug}.png"
    png_path.write_bytes(base64.b64decode(img_b64))
    sidecar = OUTDIR / f"{today}-{args.slug}.json"
    sidecar.write_text(json.dumps({
        "slug": args.slug,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "model": model,
        "aspect_ratio": args.aspect,
        "reference_images": args.ref,
        "full_prompt_sent": prompt,
        "brand_guidelines_version": "voice/identite-editoriale.md",  # rempli à l'onboarding
    }, ensure_ascii=False, indent=2))
    # journal unifié — toujours sous linkedin-agent/outputs/registry.csv
    reg = journal.log(
        kind="image",
        slug=args.slug,
        output=png_path,
        source=args.prompt_file,
        model=model,
        refs=" | ".join(args.ref),
        ai_disclosure="Généré par IA (Nano Banana Pro)",
        status="brut",
        notes=f"aspect {args.aspect}",
    )

    print(f"OK → {png_path}")
    print(f"     {sidecar}")
    print(f"     journalisé → {reg}")


if __name__ == "__main__":
    main()
