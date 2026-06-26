---
name: onboarding
description: Calibre cet agent LinkedIn sur la voix ET le style visuel d'une nouvelle personne, à partir de ses vrais posts, de son site et de 3-4 visuels qu'elle aime. À déclencher dès la première ouverture du template, quand la personne dit "commencer", "démarrer", "configurer", "on commence", "setup", "start", "begin", "let's go" (ou l'équivalent dans une autre langue), ou ouvre le dossier sans autre consigne ALORS QUE profile/config.md porte encore "STATUT: NON CONFIGURÉ". La skill demande le fichier .xls/.xlsx/.csv des posts LinkedIn + l'URL du site + 3-4 visuels de référence, analyse style d'écriture / contexte / goûts visuels, rédige l'identité éditoriale et le style visuel, remplit la config, adapte README/CLAUDE, pose des questions d'affinage, puis finalise. À NE PAS lancer si l'agent est déjà configuré (STATUT: CONFIGURÉ).
---

# onboarding : calibrer l'agent sur la voix et le style de la personne

Tu transformes ce template générique en l'agent LinkedIn personnel de la personne qui l'ouvre. Tu pars de **sa matière réelle** (ses posts, son site, les visuels qu'elle aime), pas de généralités. À la fin, son identité éditoriale est rédigée, son style visuel défini, sa config remplie, et elle peut écrire son premier post.

**Vérifie d'abord** que `profile/config.md` porte bien `STATUT: NON CONFIGURÉ`. Si c'est déjà `CONFIGURÉ`, ne relance pas l'onboarding sans confirmation explicite (propose plutôt de re-calibrer la voix, le style visuel, ou les deux).

Travaille en français, dans une voix simple et directe. Respecte `voice/anti-ai-writing-style.md` dans tout ce que tu rédiges (surtout l'identité éditoriale).

## Étape 1 — Collecter la matière

Demande à la personne, via l'outil de questions (ou en clair), **trois choses** :

1. **Le fichier de ses posts LinkedIn** : chemin vers un `.xls`, `.xlsx` ou `.csv`. (Export LinkedIn « Shares », ou n'importe quel tableur avec une ligne par post : texte, et si possible likes / commentaires / partages / date.)
2. **L'URL du site de son entreprise** (ou de son site perso / page de présentation).
3. **3 à 4 visuels de posts qu'elle aime** : à déposer dans `assets/references-visuelles/`. Les siens, ou ceux d'autres personnes / marques dont le style lui plaît. C'est ce qui personnalise son style visuel et évite un rendu standard.

Si elle n'a pas l'export LinkedIn, propose deux options : (1) un scraper « LinkedIn Posts Scraper » sur **Apify** (apify.com) lancé sur l'URL de son profil, puis export du dataset en **Excel/CSV** (récupère le texte + likes/commentaires/partages, idéal pour repérer ce qui marche ; rester sur son propre profil et dans les conditions de LinkedIn) ; (2) *Préférences → Confidentialité des données → Obtenir une copie de vos données → cocher les publications*. Si elle n'a pas de visuels de référence sous la main, ce n'est pas bloquant : tu construiras un style neutre, à affiner plus tard. Adapte-toi à ce qu'elle fournit.

## Étape 2 — Analyser les posts (le style d'écriture)

Lis le fichier avec la **skill xlsx** (pour `.xls`/`.xlsx`) ou directement (pour `.csv`). Repère par heuristique la colonne du **texte du post** et, si présentes, les colonnes d'**engagement** et de **date**.

Extrais, et note dans `outputs/onboarding/analyse-style.md` (crée le dossier) :

- **Ce que disent les chiffres** : médiane d'engagement, le ou les outliers, ce qui distingue le haut du bas de classement. Si pas de colonnes d'engagement, dis-le et travaille le style sans le classement.
- **Les accroches** : comment elle ouvre ses posts (affirmation + deux-points ? question ? contre-pied ? chiffre ?). Cite 3-5 vraies accroches.
- **Les registres** : opinion, contre-pied, retex/vécu, pédagogique, personnel, annonces… Classe-les par performance si possible.
- **La cadence et la voix** : longueur des phrases et paragraphes, « je »/« vous », contractions, manière de chiffrer, tics de clôture, ponctuation.
- **Les formats** : texte seul, image, carrousel, capture. Lesquels reviennent, lesquels marchent.
- **Le vocabulaire signature** : mots et tournures qui reviennent et qui sonnent « elle ».

Reste factuel : tu décris ce que tu observes dans l'export.

## Étape 3 — Analyser le site (le contexte)

Récupère le contenu du site avec WebFetch (accueil + à-propos / offres). Extrais : l'entreprise (nom, secteur), l'offre (proposition de valeur), la cible, le ton, le positionnement. Si le site est inaccessible, demande à la personne de te résumer ces points.

## Étape 4 — Déduire le style visuel (à partir des visuels qu'elle aime)

**Regarde** chaque visuel déposé dans `assets/references-visuelles/` (lis les images). Cherche ce qui revient d'un visuel à l'autre, c'est ça sa signature de goût. Décris ce que tu observes, sans imposer :

- **Archétype de composition** : plein cadre photo ? carte à marges ? texte sur aplat ? collage ? graphique minimal ?
- **Cadre & marges** : liseré / bordure, ou bord à bord ? marges larges ? coins arrondis ? **Si elle n'aime pas les cadres, note-le** pour qu'aucun liseré ne soit forcé.
- **Titre** : placement (haut / centré / incrusté / bas / aucun), typo (display ou discrète), fond derrière le texte.
- **Couleur & contraste** : palette dominante, usage de l'accent, clair vs sombre, photos désaturées vs vives.
- **Signature** : photo + nom + titre ? logo discret ? URL ? rien ? **Si elle préfère sans signature, note-le.**
- **Image / illustration** : photos, illustrations, memes, captures ? traitement ? le visage est-il présent ?
- **Mood** en une phrase, et **ce qu'on évite**.

Écris le tout dans `profile/style-visuel.md` (en remplaçant le gabarit). Si aucun visuel n'a été fourni, garde un style neutre et signale-le, plutôt que d'inventer une signature.

## Étape 5 — Rédiger l'identité éditoriale

Réécris **entièrement** `voice/identite-editoriale.md` (en remplaçant le gabarit) en suivant ses 8 sections, remplies avec les éléments **réels** des étapes 2 et 3 : positionnement, mission, piliers, voix (signatures réelles illustrées d'extraits), audience et registres classés, titre de profil, idées de posts. C'est le livrable le plus important. Écris-le dans **sa** voix. Pas de section vide, pas de « TODO ».

## Étape 6 — Remplir la config

Remplis `profile/config.md` : prénom, nom, titre de signature, entreprise, site, cible, objectifs, et l'identité visuelle (couleur d'accent, fonts, logo). Pour le cadre / la mise en page, renvoie à `profile/style-visuel.md`. Laisse `STATUT: NON CONFIGURÉ` pour l'instant.

## Étape 7 — Adapter README et CLAUDE

Personnalise la **surface** de `README.md` (titre, son prénom, son entreprise) sans casser la structure. Dans `CLAUDE.md`, personnalise l'intro mais **garde intactes** la section onboarding et les règles. Ne touche pas aux scripts ni aux autres skills.

## Étape 8 — Questions d'affinage

Montre une **synthèse courte** (positionnement, 3 piliers, registres top, cible, et le style visuel résumé en une phrase) et pose, via l'outil de questions, ce que l'analyse n'a pas tranché :

- **Cible prioritaire** et son état d'esprit.
- **Objectif principal** : reach, leads, autorité, recrutement ?
- **Couleur d'accent** (hex), ou propose-en une cohérente avec ses références.
- **Titre de signature** exact.
- **Style visuel** : confirme le résumé déduit (cadre ou pas, signature ou pas), corrige si besoin.
- **Sujets / angles interdits**, au-delà de la liste anti-IA.
- **Polices de marque** : en a-t-elle (woff2 dans `assets/marque/fonts/`) ou polices système ?

Intègre ses réponses dans `voice/identite-editoriale.md`, `profile/style-visuel.md` et `profile/config.md`.

## Étape 9 — Finaliser

1. Passe `profile/config.md` à `STATUT: CONFIGURÉ`.
2. Rappelle de déposer 3-5 photos dans `assets/moi/` (Identity Lock) + l'avatar de signature, et de remplir `.env` pour générer des images.
3. Récap en 5 lignes : positionnement, registres qui marchent, couleur, style visuel, prochaine action.
4. Propose d'enchaîner : *« On écrit ton premier post ? »* → bascule sur `my-viral-post`.

## Garde-fous

- Ne produis **aucun post ni visuel** pendant l'onboarding. L'onboarding configure, il ne publie pas.
- N'invente ni chiffres, ni clients, ni signature de goût : tout vient de l'export, du site, ou des visuels fournis. Pas de claim sans source.
- Si la matière est mince (peu de posts, pas de visuels), dis-le honnêtement et construis une base prudente, à affiner avec le temps.
- Respecte `voice/anti-ai-writing-style.md` dans chaque ligne que tu rédiges.
