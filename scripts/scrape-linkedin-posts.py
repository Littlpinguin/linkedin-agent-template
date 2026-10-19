#!/usr/bin/env python3
"""Récupère tes anciens posts LinkedIn via Apify et les écrit en CSV pour l'onboarding.

Lit APIFY_TOKEN (obligatoire) et APIFY_LINKEDIN_ACTOR (facultatif) dans .env.
Acteur par défaut : harvestapi/linkedin-profile-posts (sans cookie ni connexion,
payé au post, crédits offerts à l'inscription sur apify.com).

Usage :
    python3 scripts/scrape-linkedin-posts.py --profile https://www.linkedin.com/in/ton-profil/
    python3 scripts/scrape-linkedin-posts.py --profile <url> --max 150 --out outputs/onboarding/posts.csv

Colonnes du CSV : date, text, likes, comments, shares, url, type.
À n'utiliser que sur ton propre profil, dans le respect des conditions de LinkedIn.
"""
import argparse
import csv
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_ACTOR = "harvestapi/linkedin-profile-posts"
DEFAULT_OUT = ROOT / "outputs" / "onboarding" / "posts.csv"
FIELDS = ["date", "text", "likes", "comments", "shares", "url", "type"]

REPLI = (
    "Deux voies gratuites restent possibles :\n"
    "  1. l'export officiel LinkedIn (Préférences > Confidentialité des données >\n"
    "     Obtenir une copie de vos données > Publications), sans les chiffres d'engagement ;\n"
    "  2. coller une quinzaine de posts dans la conversation."
)


def load_env():
    """Charge .env (KEY=VALUE) sans dépendance externe ; l'environnement existant prime."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def pick(item, *paths, default=""):
    """Première valeur non vide parmi plusieurs chemins possibles ("a.b" = item["a"]["b"])."""
    for path in paths:
        value = item
        for key in path.split("."):
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break
        if value not in (None, ""):
            return value
    return default


def as_text(value):
    """Ramène une valeur imbriquée (dict, liste) à une chaîne lisible pour le CSV."""
    if isinstance(value, dict):
        return str(value.get("date") or value.get("timestamp") or "")
    if isinstance(value, list):
        return " | ".join(str(v) for v in value)
    return value


def to_row(item):
    """Normalise un élément du dataset Apify, quel que soit l'acteur, en ligne du CSV."""
    likes = pick(item, "engagement.likes", "numLikes", "likesCount", "reactionsCount",
                 "totalReactionCount", "stats.total_reactions", default=0)
    return {
        "date": as_text(pick(item, "postedAt.date", "postedAtISO", "posted_at.date", "date",
                             "postedAt.timestamp", "postedAt")),
        "text": pick(item, "content", "text", "postText", "commentary"),
        "likes": likes,
        "comments": pick(item, "engagement.comments", "numComments", "commentsCount",
                         "stats.comments", default=0),
        "shares": pick(item, "engagement.shares", "numShares", "repostsCount", "sharesCount",
                       "stats.reposts", default=0),
        "url": pick(item, "linkedinUrl", "url", "postUrl"),
        "type": pick(item, "type", "postType", default="post"),
    }


def fetch(token, actor, profile, max_posts):
    """Lance l'acteur en mode synchrone et renvoie la liste des éléments du dataset."""
    try:
        import requests
    except ImportError:
        sys.exit("Il manque la bibliothèque requests : lance `pip install requests` puis réessaie.")
    url = f"https://api.apify.com/v2/acts/{actor.replace('/', '~')}/run-sync-get-dataset-items"
    payload = {
        "targetUrls": [profile],
        "maxPosts": max_posts,
        "includeQuotePosts": True,
        "includeReposts": False,
        "scrapeReactions": False,
        "scrapeComments": False,
    }
    try:
        r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {token}"},
                          timeout=330)
    except requests.RequestException as e:
        sys.exit(f"Impossible de joindre Apify ({e}). Vérifie ta connexion internet.\n{REPLI}")
    if r.status_code in (401, 403):
        sys.exit("Apify refuse le jeton. Vérifie APIFY_TOKEN dans .env "
                 "(apify.com > Settings > API & Integrations).\n" + REPLI)
    if r.status_code == 402:
        sys.exit("Ton compte Apify n'a plus de crédits pour cet acteur.\n" + REPLI)
    if r.status_code == 408:
        sys.exit("Apify a mis trop de temps à répondre. Relance avec moins de posts (--max 50).\n" + REPLI)
    if r.status_code >= 400:
        sys.exit(f"Apify a répondu {r.status_code} : {r.text[:300]}\n{REPLI}")
    try:
        data = r.json()
    except ValueError:
        sys.exit(f"Apify a renvoyé une réponse illisible : {r.text[:300]}\n{REPLI}")
    if isinstance(data, dict):
        data = data.get("items", [])
    return [i for i in data if isinstance(i, dict)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--profile", required=True, help="URL de ton profil LinkedIn")
    ap.add_argument("--max", type=int, default=100, help="nombre de posts à récupérer (défaut 100)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="chemin du CSV de sortie")
    args = ap.parse_args()

    load_env()
    token = os.environ.get("APIFY_TOKEN", "").strip()
    if not token:
        sys.exit("APIFY_TOKEN est vide. Copie ton jeton Apify dans le fichier .env "
                 "(ligne APIFY_TOKEN=), enregistre, puis relance.\n" + REPLI)
    actor = os.environ.get("APIFY_LINKEDIN_ACTOR", "").strip() or DEFAULT_ACTOR
    if "linkedin.com/" not in args.profile:
        sys.exit("L'URL ne ressemble pas à un profil LinkedIn (attendu : https://www.linkedin.com/in/…).")

    print(f"Récupération de {args.max} posts max avec {actor} (une à trois minutes)…")
    items = fetch(token, actor, args.profile, args.max)
    rows = [to_row(i) for i in items]
    rows = [r for r in rows if str(r["text"]).strip()]
    if not rows:
        sys.exit("Apify n'a renvoyé aucun post avec du texte pour ce profil. "
                 "Vérifie l'URL et que tes posts sont publics.\n" + REPLI)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} posts enregistrés dans {out}")


if __name__ == "__main__":
    main()
