#!/usr/bin/env python3
"""Programme tes posts LinkedIn et lit leurs résultats via Zernio (zernio.com).

Lit ZERNIO_API_KEY dans .env (zernio.com > Settings > API keys). Les 2 premiers comptes
connectés sont gratuits ; un profil ou une page entreprise compte pour un compte.

Ce script ne publie jamais tout de suite : un post est soit programmé à une date
future, soit enregistré en brouillon. Rien ne part sans --quand ou --brouillon.

Statistiques : sur un profil personnel, LinkedIn ne les donne que pour les posts publiés
via Zernio, et pour ceux importés un par un avec leur URL (commande `importer`).
Sur une page entreprise, tous les posts sont couverts.

Usage :
    python3 scripts/zernio.py comptes
    python3 scripts/zernio.py programmer --compte <id> --texte outputs/post-x/post.txt \
        --media outputs/carte-x/carte.png --quand 2026-10-27T08:00
    python3 scripts/zernio.py programmer --compte <id> --texte post.txt \
        --media outputs/carrousel-x/exports/x.pdf --titre-document "Mon carrousel" --brouillon
    python3 scripts/zernio.py statut <post_id>
    python3 scripts/zernio.py annuler <post_id> --confirme
    python3 scripts/zernio.py importer --compte <id> --url https://www.linkedin.com/posts/...
    python3 scripts/zernio.py resultats --compte <id> --out bilans/performances.csv
    python3 scripts/zernio.py creneaux --compte <id>
"""
import argparse
import csv
import datetime
import hashlib
import mimetypes
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://zernio.com/api/v1"
DEFAULT_TZ = "Europe/Paris"
MEDIA_TYPES = {"image/jpeg": "image", "image/png": "image", "image/webp": "image",
               "image/gif": "gif", "application/pdf": "document", "video/mp4": "video",
               "video/quicktime": "video", "video/webm": "video"}
DAYS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
METRICS = ["impressions", "reach", "likes", "comments", "shares", "saves", "sends",
           "clicks", "views", "engagementRate"]
MARGIN = datetime.timedelta(minutes=10)


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


def zone(name):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except (ValueError, KeyError, ImportError) as e:
        sys.exit(f"Fuseau inconnu : {name} ({e}). Exemple de fuseau valide : Europe/Paris.")


def session():
    load_env()
    key = os.environ.get("ZERNIO_API_KEY", "").strip()
    if not key:
        sys.exit("ZERNIO_API_KEY est vide. Crée une clé sur zernio.com (Settings > API keys), "
                 "colle-la dans .env sur la ligne ZERNIO_API_KEY=, enregistre, puis relance.")
    try:
        import requests
    except ImportError:
        sys.exit("Il manque la bibliothèque requests : lance `python3 -m pip install requests` puis réessaie.")
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {key}"
    return requests, s


def error_code(r):
    try:
        body = r.json()
    except ValueError:
        return ""
    return str(body.get("code") or (body.get("error") or {}).get("code") or "") if isinstance(body, dict) else ""


def call(requests, s, method, path, creating=False, **kwargs):
    """Appel à l'API Zernio avec des messages d'erreur en clair ; renvoie (code HTTP, JSON)."""
    try:
        r = s.request(method, API + path, timeout=120, **kwargs)
    except requests.RequestException as e:
        if creating:
            sys.exit(f"La réponse de Zernio n'est pas arrivée ({e}). Le post a peut-être été créé : "
                     "vérifie sur zernio.com (ou relance la même commande à l'identique, qui ne "
                     "créera pas de doublon) avant toute autre tentative.")
        sys.exit(f"Impossible de joindre Zernio ({e}). Vérifie ta connexion internet.")
    code = error_code(r) if r.status_code >= 400 else ""
    if r.status_code == 401:
        sys.exit(f"Zernio refuse l'accès ({code or r.status_code}) : clé ZERNIO_API_KEY invalide, ou "
                 "compte LinkedIn à reconnecter sur zernio.com.")
    if r.status_code == 402:
        sys.exit("Zernio demande un paiement pour cette action (compte au-delà des 2 gratuits, "
                 "ou statistiques non incluses). Regarde ton offre sur zernio.com avant de continuer.")
    if r.status_code == 403:
        reasons = {"ACCOUNT_DISCONNECTED": "le compte LinkedIn est déconnecté : reconnecte-le sur zernio.com",
                   "ACCOUNT_NOT_ENABLED_FOR_POSTING": "le compte n'est pas activé pour publier dans Zernio",
                   "PROFILE_OVER_LIMIT": "tu dépasses le nombre de comptes de ton offre"}
        sys.exit(f"Zernio refuse : {reasons.get(code, 'accès refusé à ce compte ou à cette fonction')}. "
                 f"Détail : {r.text[:300]}")
    if r.status_code == 409:
        if code == "idempotency_conflict":
            sys.exit("La même demande est déjà en cours de traitement chez Zernio. Attends une minute, "
                     "puis vérifie avec `statut` ou sur zernio.com.")
        sys.exit("Zernio a déjà ce post (même texte et mêmes médias sur ce compte depuis moins de "
                 f"24 h) : il n'a rien créé en double. Détail : {r.text[:300]}")
    if r.status_code == 429:
        sys.exit("Trop de requêtes vers Zernio : attends une minute et relance.")
    if r.status_code >= 400:
        sys.exit(f"Zernio a répondu {r.status_code} ({code}) : {r.text[:400]}")
    if not r.content:
        return r.status_code, {}
    try:
        return r.status_code, r.json()
    except ValueError:
        sys.exit(f"Zernio a renvoyé une réponse illisible : {r.text[:300]}")


def upload(requests, s, path):
    """Envoie un fichier local sur le stockage de Zernio et renvoie (url publique, type)."""
    p = pathlib.Path(path)
    ctype = mimetypes.guess_type(p.name)[0] or ""
    size = p.stat().st_size
    _, info = call(requests, s, "POST", "/media/presign",
                   json={"filename": p.name, "contentType": ctype, "size": size})
    try:
        with p.open("rb") as f:
            r = requests.put(info["uploadUrl"], data=f, headers={"Content-Type": ctype}, timeout=600)
    except requests.RequestException as e:
        sys.exit(f"Envoi de {p.name} impossible ({e}). Rien n'a été programmé.")
    if r.status_code >= 300:
        sys.exit(f"Envoi de {p.name} refusé par le stockage ({r.status_code}). Rien n'a été programmé.")
    return info["publicUrl"], MEDIA_TYPES[ctype]


def local_time(value, tz_name):
    """Date ISO renvoyée par Zernio (UTC) affichée en heure locale."""
    try:
        dt = datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return str(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(zone(tz_name or DEFAULT_TZ)).strftime("%d/%m/%Y à %H:%M")


def show_post(post):
    when = ""
    if post.get("scheduledFor"):
        tz_name = post.get("timezone") if post.get("timezone") not in (None, "", "UTC") else DEFAULT_TZ
        when = f", prévu le {local_time(post['scheduledFor'], tz_name)} ({tz_name})"
    print(f"Post {post.get('_id')} : statut {post.get('status')}{when}")
    for pl in post.get("platforms") or []:
        line = f"  {pl.get('platform')} : {pl.get('status')}"
        if pl.get("platformPostUrl"):
            line += f" · {pl['platformPostUrl']}"
        if pl.get("errorMessage"):
            line += f" · erreur : {pl['errorMessage']}"
        print(line)


def cmd_comptes(a):
    requests, s = session()
    _, data = call(requests, s, "GET", "/accounts", params={"platform": "linkedin"})
    accounts = data.get("accounts") or []
    if not accounts:
        print("Aucun compte LinkedIn connecté. Connecte ton profil (ou ta page) sur zernio.com, puis relance.")
        return
    for acc in accounts:
        name = acc.get("displayName") or acc.get("username") or ""
        state = "à reconnecter" if acc.get("needsReconnection") or not acc.get("isActive") else "actif"
        print(f"{acc.get('_id')}  {name}  {state}")


def parse_when(value, tz_name):
    """Heure locale stricte AAAA-MM-JJTHH:MM, sans Z ni décalage."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", value or ""):
        sys.exit("Date attendue au format AAAA-MM-JJTHH:MM, en heure locale, sans Z ni décalage "
                 "(ex. 2026-10-27T08:00). Le fuseau se règle avec --fuseau.")
    try:
        return datetime.datetime.fromisoformat(value).replace(tzinfo=zone(tz_name))
    except ValueError as e:
        sys.exit(f"Date impossible : {value} ({e}).")


def too_soon(when):
    return when <= datetime.datetime.now(datetime.timezone.utc) + MARGIN


def cmd_programmer(a):
    if a.brouillon and a.quand:
        sys.exit("Choisis : --quand pour programmer, ou --brouillon pour enregistrer sans date, pas les deux.")
    if not a.brouillon and not a.quand:
        sys.exit("Indique --quand AAAA-MM-JJTHH:MM (heure locale) pour programmer, ou --brouillon. "
                 "Ce script ne publie jamais tout de suite.")
    when = parse_when(a.quand, a.fuseau) if a.quand else None
    if when and too_soon(when):
        sys.exit("La date est passée ou dans moins de 10 minutes : choisis un créneau plus tard.")
    texte = pathlib.Path(a.texte)
    if not texte.is_file():
        sys.exit(f"Fichier du texte introuvable : {a.texte}")
    try:
        text = texte.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        sys.exit(f"{a.texte} n'est pas un fichier texte UTF-8.")
    if not text:
        sys.exit(f"Le texte du post est vide : {a.texte}")
    if len(text) > 3000:
        sys.exit(f"Le texte fait {len(text)} caractères : LinkedIn en accepte 3 000 au plus.")
    media = a.media or []
    kinds = []
    for m in media:
        p = pathlib.Path(m)
        if not p.is_file():
            sys.exit(f"Fichier introuvable : {m}")
        ctype = mimetypes.guess_type(p.name)[0] or ""
        if ctype not in MEDIA_TYPES:
            sys.exit(f"Format non pris en charge pour LinkedIn : {p.name} (images JPG, PNG, WebP, GIF, "
                     "vidéo MP4/MOV/WebM, ou un PDF pour un carrousel).")
        if ctype == "application/pdf" and p.stat().st_size > 100 * 1024 * 1024:
            sys.exit(f"{p.name} pèse plus de 100 Mo, la limite de LinkedIn pour un PDF.")
        kinds.append(MEDIA_TYPES[ctype])
    if ("document" in kinds or "video" in kinds) and len(media) > 1:
        sys.exit("Sur LinkedIn, un PDF (carrousel) ou une vidéo part seul : pas d'autre média avec.")
    if len(media) > 20:
        sys.exit("LinkedIn accepte 20 images au plus par post.")

    requests, s = session()
    items = []
    for m in media:
        url, kind = upload(requests, s, m)
        items.append({"url": url, "type": kind})
        print(f"Média envoyé : {pathlib.Path(m).name}")
    target = {"platform": "linkedin", "accountId": a.compte}
    specific = {}
    if "document" in kinds:
        specific["documentTitle"] = a.titre_document or pathlib.Path(media[0]).stem
    if a.premier_commentaire:
        specific["firstComment"] = a.premier_commentaire
    if specific:
        target["platformSpecificData"] = specific
    body = {"content": text, "platforms": [target]}
    if items:
        body["mediaItems"] = items
    if a.brouillon:
        body["isDraft"] = True
    else:
        # Zernio publie sur-le-champ une date déjà passée : on revérifie après l'envoi des médias.
        if too_soon(when):
            sys.exit("L'envoi des médias a pris trop de temps : la date est désormais trop proche. "
                     "Rien n'a été programmé ; relance avec un créneau plus tard.")
        body["scheduledFor"] = when.isoformat(timespec="seconds")
        body["timezone"] = a.fuseau
    # Clé d'idempotence stable : relancer la même commande ne crée pas de doublon.
    h = hashlib.sha256("\0".join([a.compte, text, a.quand or "brouillon"]).encode())
    for m in media:
        with open(m, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    status, data = call(requests, s, "POST", "/posts", creating=True, json=body,
                        headers={"Idempotency-Key": h.hexdigest()})
    post = data.get("post") or data
    show_post(post)
    if status == 200:
        print("Ce post existait déjà (même demande relancée) : rien de nouveau n'a été créé.")
    if status == 207 or post.get("publishedAt") or post.get("status") in ("published", "publishing", "partial", "failed"):
        print("Attention : Zernio a tenté une publication immédiate ou signale un échec. "
              "Vérifie tout de suite sur zernio.com et sur LinkedIn.")


def cmd_statut(a):
    requests, s = session()
    _, data = call(requests, s, "GET", f"/posts/{a.post_id}")
    show_post(data.get("post") or data)


def cmd_annuler(a):
    requests, s = session()
    _, data = call(requests, s, "GET", f"/posts/{a.post_id}")
    post = data.get("post") or data
    if post.get("status") not in ("draft", "scheduled", "failed"):
        sys.exit(f"Ce post est au statut {post.get('status')} : seul un brouillon, un post programmé "
                 "ou en échec s'annule ici. Un post publié se supprime sur LinkedIn.")
    if not a.confirme:
        show_post(post)
        sys.exit("Rien n'est supprimé. Relance avec --confirme après l'accord de la personne.")
    call(requests, s, "DELETE", f"/posts/{a.post_id}")
    print(f"Post {a.post_id} supprimé de Zernio (il ne partira pas).")


def cmd_importer(a):
    """Rattache à Zernio un post publié à la main, pour en suivre les statistiques."""
    requests, s = session()
    _, data = call(requests, s, "POST", "/posts/sync-external", json={"accountId": a.compte, "url": a.url})
    print(f"Post importé ({data.get('postsFound', '?')} post(s) lus sur LinkedIn). "
          "Ses statistiques apparaîtront dans `resultats` (délai de LinkedIn : jusqu'à 24 h).")


def cmd_resultats(a):
    """Statistiques des posts suivis par Zernio sur ce compte, en CSV."""
    requests, s = session()
    since = (datetime.date.today() - datetime.timedelta(days=a.jours)).isoformat()
    posts, page = [], 1
    while page <= 10:
        _, data = call(requests, s, "GET", "/analytics",
                       params={"platform": "linkedin", "accountId": a.compte, "fromDate": since,
                               "limit": 100, "page": page})
        batch = data.get("posts") or []
        posts += batch
        if len(batch) < 100:
            break
        page += 1
    if not posts:
        sys.exit("Aucun post suivi sur cette période. Sur un profil personnel, seuls les posts publiés "
                 "via Zernio, ou importés avec `importer --url`, ont des statistiques.")
    rows = []
    for p in posts:
        m = p.get("analytics") or {}
        row = {"date": p.get("publishedAt") or p.get("scheduledFor"), "url": p.get("platformPostUrl"),
               "format": p.get("mediaType") or "texte",
               "origine": "hors Zernio" if p.get("isExternal") else "Zernio",
               "zernio_id": p.get("_id"), "texte": p.get("content") or ""}
        row.update({k: m.get(k, "") for k in METRICS})
        rows.append(row)
    rows.sort(key=lambda r: str(r["date"]), reverse=True)
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["date", "url", "format", "origine", "zernio_id"] + METRICS + ["texte"]
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} posts avec leurs statistiques dans {out} "
          f"(relevé du {datetime.date.today().isoformat()}, depuis le {since}).")


def cmd_creneaux(a):
    tz = zone(a.fuseau)
    requests, s = session()
    _, data = call(requests, s, "GET", "/analytics/best-time",
                   params={"platform": "linkedin", "accountId": a.compte})
    slots = sorted(data.get("slots") or [], key=lambda x: -(x.get("avg_engagement") or 0))
    if not slots:
        print("Pas encore assez de posts publiés pour dégager des créneaux.")
        return
    # Lundi de la semaine en cours : la conversion UTC -> heure locale suit l'heure d'été du moment.
    today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    monday = today - datetime.timedelta(days=today.weekday())
    for sl in slots[:8]:
        loc = (monday + datetime.timedelta(days=sl["day_of_week"], hours=sl["hour"])).astimezone(tz)
        print(f"{DAYS[loc.weekday()]} {loc.hour} h : engagement moyen {sl.get('avg_engagement')}, "
              f"sur {sl.get('post_count')} post(s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("comptes", help="lister tes comptes LinkedIn connectés à Zernio")
    p = sub.add_parser("programmer", help="programmer un post (ou l'enregistrer en brouillon)")
    p.add_argument("--compte", required=True, help="id du compte (voir `comptes`)")
    p.add_argument("--texte", required=True, help="fichier texte du post, tel qu'il sera publié")
    p.add_argument("--media", nargs="*", help="image(s), une vidéo ou le PDF du carrousel")
    p.add_argument("--quand", help="date et heure locales, ex. 2026-10-27T08:00")
    p.add_argument("--fuseau", default=DEFAULT_TZ, help=f"fuseau IANA (défaut {DEFAULT_TZ})")
    p.add_argument("--titre-document", help="titre affiché sur un carrousel PDF")
    p.add_argument("--premier-commentaire", help="premier commentaire ajouté après la publication")
    p.add_argument("--brouillon", action="store_true", help="enregistrer en brouillon, sans date")
    p = sub.add_parser("statut", help="où en est un post (programmé, publié, en échec)")
    p.add_argument("post_id")
    p = sub.add_parser("annuler", help="supprimer un brouillon ou un post programmé")
    p.add_argument("post_id")
    p.add_argument("--confirme", action="store_true")
    p = sub.add_parser("importer", help="suivre un post publié à la main (son URL LinkedIn)")
    p.add_argument("--compte", required=True)
    p.add_argument("--url", required=True)
    p = sub.add_parser("resultats", help="statistiques des posts suivis, en CSV")
    p.add_argument("--compte", required=True)
    p.add_argument("--jours", type=int, default=90, help="période en jours (défaut 90, max 366)")
    p.add_argument("--out", default=str(ROOT / "bilans" / "performances.csv"))
    p = sub.add_parser("creneaux", help="les jours et heures où tes posts marchent le mieux")
    p.add_argument("--compte", required=True)
    p.add_argument("--fuseau", default=DEFAULT_TZ)
    a = ap.parse_args()
    if a.cmd == "resultats" and not 1 <= a.jours <= 366:
        sys.exit("--jours doit être entre 1 et 366.")
    {"comptes": cmd_comptes, "programmer": cmd_programmer, "statut": cmd_statut,
     "annuler": cmd_annuler, "importer": cmd_importer, "resultats": cmd_resultats,
     "creneaux": cmd_creneaux}[a.cmd](a)


if __name__ == "__main__":
    main()
