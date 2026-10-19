#!/usr/bin/env python3
"""Récupère tes anciens posts LinkedIn via Apify et les écrit en CSV pour l'onboarding.

Lit APIFY_TOKEN (obligatoire) et APIFY_LINKEDIN_ACTOR (facultatif) dans .env.
Acteur par défaut : harvestapi/linkedin-profile-posts (sans cookie ni connexion,
payé au post, crédits offerts à l'inscription sur apify.com).

Usage :
    python3 scripts/scrape-linkedin-posts.py --profile https://www.linkedin.com/in/ton-profil/
    python3 scripts/scrape-linkedin-posts.py --profile <url> --max 150 --visuels
    python3 scripts/scrape-linkedin-posts.py --dernier-lancement --visuels

--visuels télécharge les images, les pages des carrousels et les miniatures de vidéos
dans outputs/onboarding/visuels/ (gratuit : ils viennent du CDN de LinkedIn, pas d'Apify).
Les liens LinkedIn expirent : lance-le dans les jours qui suivent la récupération.
--dernier-lancement relit le résultat du dernier lancement sans relancer l'acteur (gratuit).

Colonnes du CSV, du plus récent au plus ancien :
date, text, likes, comments, shares, url, type, format, nb_visuels, visuels.
format : texte | image | images | carrousel | video | lien | citation.
Le JSON complet renvoyé par Apify est gardé à côté du CSV (posts-brut.json).
À n'utiliser que sur ton propre profil, dans le respect des conditions de LinkedIn.
"""
import argparse
import csv
import json
import os
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_ACTOR = "harvestapi/linkedin-profile-posts"
DEFAULT_OUT = ROOT / "outputs" / "onboarding" / "posts.csv"
FIELDS = ["date", "text", "likes", "comments", "shares", "url", "type",
          "format", "nb_visuels", "visuels"]
EXTENSIONS = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
              "image/webp": ".webp", "application/pdf": ".pdf"}

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


def media(item):
    """Format du post et visuels à récupérer : [(nom de fichier sans extension, URL)]."""
    images = [i.get("url") for i in item.get("postImages") or [] if isinstance(i, dict) and i.get("url")]
    doc = item.get("document") or {}
    video = item.get("postVideo") or {}
    article = item.get("article") or {}
    if doc:
        # Le PDF (transcribedDocumentUrl) est souvent tronqué : on prend les pages en images.
        # Le manifeste de la plus haute résolution liste toutes les pages ; coverPages, les 3 premières.
        covers = [u for p in doc.get("coverPages") or [] for u in p.get("imageUrls") or []]
        sizes = (doc.get("manifest") or {}).get("perResolutions") or []
        best = max(sizes, key=lambda p: p.get("width") or 0) if sizes else {}
        files = [("manifeste", best["imageManifestUrl"])] if best.get("imageManifestUrl") else []
        files += [(f"page-{n:02d}", u) for n, u in enumerate(covers, 1)]
        return "carrousel", int(doc.get("totalPageCount") or len(covers) or 1), files
    if video:
        thumb = video.get("thumbnailUrl")
        return "video", 1, [("miniature-video", thumb)] if thumb else []
    if images:
        files = [(f"image-{n}", u) for n, u in enumerate(images, 1)]
        return ("images" if len(images) > 1 else "image"), len(images), files
    if article:
        img = (article.get("image") or {}).get("url")
        return "lien", 1 if img else 0, [("apercu-lien", img)] if img else []
    if item.get("repost"):
        return "citation", 0, []
    return "texte", 0, []


def to_row(item):
    """Normalise un élément du dataset Apify, quel que soit l'acteur, en ligne du CSV."""
    likes = pick(item, "engagement.likes", "numLikes", "likesCount", "reactionsCount",
                 "totalReactionCount", "stats.total_reactions", default=0)
    fmt, count, _ = media(item)
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
        "format": fmt,
        "nb_visuels": count,
        "visuels": "",
    }


def slug(text, size=40):
    """Nom de dossier lisible à partir du début du post."""
    ascii_text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()[:size]).strip("-")
    return s or "post"


def download_visuals(requests, item, row, folder):
    """Télécharge les visuels d'un post ; renvoie les chemins relatifs au dossier de l'agent."""
    _, _, files = media(item)
    if not files:
        return []
    post_id = str(item.get("id") or "")[-6:]
    target = folder / "-".join(p for p in (str(row["date"])[:10], slug(row["text"]), post_id) if p)
    target.mkdir(parents=True, exist_ok=True)

    def get(url):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        except requests.RequestException as e:
            print(f"  visuel non récupéré : {e}")
            return None
        if r.status_code != 200:
            print(f"  visuel non récupéré : LinkedIn a répondu {r.status_code} (lien expiré : "
                  "relance avec --dernier-lancement --visuels dans les jours qui suivent le lancement).")
            return None
        return r

    if files[0][0] == "manifeste":
        r = get(files[0][1])
        try:
            pages = r.json().get("pages") if r is not None else None
        except ValueError:
            pages = None
        files = files[1:]
        if pages:
            files = [(f"page-{n:02d}", u) for n, u in enumerate(pages, 1) if isinstance(u, str)]
    saved = []
    for name, url in files:
        r = get(url)
        if r is None:
            continue
        ext = EXTENSIONS.get(r.headers.get("content-type", "").split(";")[0], ".bin")
        path = target / f"{name}{ext}"
        path.write_bytes(r.content)
        try:
            saved.append(str(path.relative_to(ROOT)))
        except ValueError:
            saved.append(str(path))
    return saved


def call_apify(requests, method, url, token, **kwargs):
    """Appel à l'API Apify avec des messages d'erreur en clair."""
    try:
        r = requests.request(method, url, headers={"Authorization": f"Bearer {token}"}, **kwargs)
    except requests.RequestException as e:
        sys.exit(f"Impossible de joindre Apify ({e}). Vérifie ta connexion internet.\n{REPLI}")
    if r.status_code in (401, 403):
        sys.exit("Apify refuse le jeton. Vérifie APIFY_TOKEN dans .env "
                 "(apify.com > Settings > API & Integrations).\n" + REPLI)
    if r.status_code == 402:
        sys.exit("Ton compte Apify n'a plus de crédits pour cet acteur.\n" + REPLI)
    if r.status_code == 404 and method == "GET":
        sys.exit("Aucun lancement précédent trouvé pour cet acteur : relance avec --profile.")
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


def fetch(requests, token, actor, profile, max_posts):
    """Lance l'acteur en mode synchrone et renvoie la liste des éléments du dataset."""
    url = f"https://api.apify.com/v2/acts/{actor.replace('/', '~')}/run-sync-get-dataset-items"
    payload = {
        "targetUrls": [profile],
        "maxPosts": max_posts,
        "includeQuotePosts": True,
        "includeReposts": False,
        "scrapeReactions": False,
        "scrapeComments": False,
    }
    return call_apify(requests, "POST", url, token, json=payload, timeout=330)


def fetch_last(requests, token, actor):
    """Relit le dataset du dernier lancement de l'acteur, sans relancer (rien de facturé au post)."""
    url = f"https://api.apify.com/v2/acts/{actor.replace('/', '~')}/runs/last/dataset/items"
    return call_apify(requests, "GET", url, token, params={"clean": "true"}, timeout=60)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--profile", help="URL de ton profil LinkedIn")
    ap.add_argument("--max", type=int, default=100, help="nombre de posts à récupérer (défaut 100)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="chemin du CSV de sortie")
    ap.add_argument("--visuels", action="store_true",
                    help="télécharger aussi les visuels des posts dans outputs/onboarding/visuels/")
    ap.add_argument("--dernier-lancement", action="store_true",
                    help="relire le dernier lancement au lieu de relancer l'acteur (gratuit)")
    args = ap.parse_args()

    load_env()
    token = os.environ.get("APIFY_TOKEN", "").strip()
    actor = os.environ.get("APIFY_LINKEDIN_ACTOR", "").strip() or DEFAULT_ACTOR
    if actor.startswith("apify_api_"):
        sys.exit("Ton jeton est sur la ligne APIFY_LINKEDIN_ACTOR du fichier .env. Déplace-le sur "
                 "la ligne APIFY_TOKEN=, laisse APIFY_LINKEDIN_ACTOR vide, enregistre, puis relance.")
    if not token:
        sys.exit("APIFY_TOKEN est vide. Copie ton jeton Apify dans le fichier .env "
                 "(ligne APIFY_TOKEN=), enregistre, puis relance.\n" + REPLI)
    if not args.dernier_lancement:
        if not args.profile:
            sys.exit("Donne l'URL de ton profil : --profile https://www.linkedin.com/in/…")
        if "linkedin.com/" not in args.profile:
            sys.exit("L'URL ne ressemble pas à un profil LinkedIn (attendu : https://www.linkedin.com/in/…).")
    try:
        import requests
    except ImportError:
        sys.exit("Il manque la bibliothèque requests : lance `python3 -m pip install requests` puis réessaie.")

    if args.dernier_lancement:
        print(f"Relecture du dernier lancement de {actor} (aucun nouveau lancement)…")
        items = fetch_last(requests, token, actor)
    else:
        print(f"Récupération de {args.max} posts max avec {actor} (une à trois minutes)…")
        items = fetch(requests, token, actor, args.profile, args.max)
    pairs = [(i, to_row(i)) for i in items]
    pairs = [(i, r) for i, r in pairs if str(r["text"]).strip()]
    if not pairs:
        sys.exit("Apify n'a renvoyé aucun post avec du texte pour ce profil. "
                 "Vérifie l'URL et que tes posts sont publics.\n" + REPLI)
    pairs.sort(key=lambda p: str(p[1]["date"]), reverse=True)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_name(out.stem + "-brut.json")
    raw.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")

    if args.visuels:
        folder = out.parent / "visuels"
        print(f"Téléchargement des visuels dans {folder}…")
        for item, row in pairs:
            row["visuels"] = " | ".join(download_visuals(requests, item, row, folder))

    rows = [r for _, r in pairs]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    formats = {}
    for r in rows:
        formats[r["format"]] = formats.get(r["format"], 0) + 1
    print(f"{len(rows)} posts enregistrés dans {out} (JSON complet : {raw.name})")
    print("Formats : " + ", ".join(f"{k} {v}" for k, v in sorted(formats.items(), key=lambda x: -x[1])))
    headline = pick(items[0], "author.info")
    if headline:
        print(f"Titre du profil LinkedIn : {headline}")


if __name__ == "__main__":
    main()
