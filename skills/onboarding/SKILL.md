---
name: onboarding
description: Accompagne pas à pas une nouvelle personne pour calibrer son agent LinkedIn en une séance d'environ 30 minutes, reprenable à tout moment. Récupère ses anciens posts (Apify piloté par l'agent, export LinkedIn ou copier-coller) pour régler ton et style éditorial, configure sa cible, son style visuel, ses 3 photos (face, profil gauche, profil droit), son moyen de générer des images (clé Google, connecteur Magnific ou Higgsfield, ou rien), et installe une veille de contenu hebdomadaire automatisée qui lui propose des idées de sujets. À déclencher à la première ouverture du template, quand la personne dit "commencer", "démarrer", "configurer", "on commence", "setup", "start", "begin", "let's go", "reprendre", "continuer l'onboarding" (ou l'équivalent dans une autre langue), ou ouvre le dossier sans autre consigne ALORS QUE profile/config.md porte "STATUT: NON CONFIGURÉ". Aussi en mode mise à niveau quand l'agent est configuré sans la section "Progression de l'onboarding" ou avec cette section entièrement décochée (version 1 du template, mise à jour ou non par git pull), ou quand elle demande "mets à jour mon agent", "configure la génération d'images", "configure ma veille", "recalibre ma voix". Ne relance pas un onboarding complet sur un agent déjà configuré sans confirmation explicite.
---

# onboarding : calibrer l'agent sur la personne, pas à pas

Tu transformes ce template générique en l'agent LinkedIn personnel de la personne qui l'ouvre. Tu pars de **sa matière réelle** : ses posts, son site, les visuels qu'elle aime, ses photos, ses réponses. À la fin, sa voix, sa recette, sa cible, son style visuel et ses outils sont écrits dans `voice/` et `profile/`, une veille tourne chaque semaine, et elle peut écrire son premier post.

Beaucoup de personnes qui ouvrent ce template ne sont pas techniciennes. Parle simplement, une question à la fois, et ne laisse jamais une erreur technique sans explication ni solution.

## Principes (valables à chaque étape)

1. **Progression sauvegardée.** La section `## Progression de l'onboarding` de `profile/config.md` a une case par étape. Coche une case (`- [x]`) dès que le fichier de sortie de l'étape est écrit, et mets à jour `Étape en cours :`. Une étape sautée reste `- [ ]` et prend la mention « (sautée) ».
2. **Reprise.** À chaque déclenchement, relis cette section. S'il y a déjà des cases cochées, résume en deux lignes ce qui est fait, puis reprends à la première case vide.
3. **Trois voies par outil**, dont une gratuite. Pour chacune, dis en une phrase ce qu'elle permet **et** ce qu'elle ne permet pas. Recommande-en une, laisse choisir.
4. **Toute étape se saute**, sauf la 2 (le minimum pour que l'agent sache qui il sert). Une étape sautée est reproposée une fois en fin de parcours, puis une fois en début de session suivante, sans insister.
5. **Les secrets ne passent jamais par le chat.** Pour une clé ou un jeton : crée `.env` à partir de `.env.example` s'il n'existe pas (`[ -f .env ] || cp .env.example .env`, jamais un `cp` nu qui écraserait les clés déjà remplies), dis quelle ligne remplir et ouvre-lui le fichier (`open -e .env` sur Mac : `.env` est un fichier caché, introuvable dans le Finder sans Cmd+Maj+.), puis attends qu'elle dise « c'est fait ». Pour vérifier, utilise uniquement `grep -c '^NOM_DE_LA_CLE=.' .env` (renvoie 1 si la ligne est remplie, sans afficher la valeur). S'il renvoie 0 après « c'est fait », le fichier n'a pas été enregistré ou ce n'était pas le bon : rouvre-le avec `open -e .env` et demande un Cmd+S. N'affiche jamais le contenu de `.env` (ni `cat`, ni `grep` sans `-c`), ne recopie la valeur nulle part. **Si une clé est collée dans le chat malgré tout** : ne la réécris pas, dis-lui qu'elle est désormais dans l'historique de la conversation, conseille de la révoquer et d'en générer une nouvelle, à mettre dans `.env`.
6. **Aucune dépense sans accord.** Apify, la génération d'images et certains connecteurs coûtent des crédits. Annonce le coût probable avant de lancer, attends un oui.
7. **Rien d'inventé.** Chiffres, accroches, clients, goûts visuels : tout vient de l'export, du site, des visuels ou de ses réponses. Si la matière est mince, dis-le et construis une base prudente.
8. **Voix.** Tout ce que tu écris dans `voice/` et `profile/` respecte `voice/anti-ai-writing-style.md`, et l'identité éditoriale est écrite dans **sa** voix.
9. **Ne touche ni à `README.md` ni à `CLAUDE.md`, ni aux scripts, ni aux autres skills.** Toute la personnalisation vit dans `profile/` et `voice/` : le template se met ainsi à jour sans conflit.
10. **Pas de contenu publié pendant l'onboarding.** Seules exceptions : l'image test de l'étape 8 et la première veille de l'étape 9, qui servent à vérifier que les outils marchent.
11. **Remplacer un gabarit, c'est réécrire tout le fichier** : titre sans « [GABARIT À REMPLIR] » et sans la note d'en-tête qui l'explique. Un fichier qui garde cette note passe encore pour un gabarit aux yeux des autres skills.

## Choisir le mode au démarrage

Lis `profile/config.md` :

- **`STATUT: NON CONFIGURÉ`** : onboarding complet, ou reprise s'il y a des cases cochées.
- **`STATUT: CONFIGURÉ` avec au moins une case cochée dans la section Progression** : l'agent est prêt. Ne relance rien sans confirmation ; propose plutôt l'action ciblée demandée (rejouer une étape : voix, cible, photos, images, veille). S'il reste des étapes « (sautées) », propose-les une fois.
- **`STATUT: CONFIGURÉ` sans section Progression, ou avec une section Progression où aucune case n'est cochée** (version 1 du template ; le second cas vient d'un `git pull`, qui fusionne la section vide du template dans son `config.md`) : **mode mise à niveau**. Explique en trois lignes ce que la nouvelle version apporte (cible détaillée, 3 photos, génération d'images par clé ou connecteur, veille automatique). Puis :
  1. mets dans `profile/config.md`, sous la ligne `STATUT`, ces deux sections (les étapes 1, 2, 4 et 6 sont déjà faites en version 1). Si `git pull` les a déjà ajoutées, ne les duplique pas : coche les cases et corrige `Étape en cours` à leur place.
     ```
     ## Progression de l'onboarding
     Version de l'onboarding : 2
     Étape en cours : 3
     - [x] 1. Accueil et vérification de l'installation
     - [x] 2. Toi et ton activité
     - [ ] 3. Tes anciens posts
     - [x] 4. Restitution de ta voix
     - [ ] 5. Ta cible
     - [x] 6. Ton style visuel
     - [ ] 7. Tes 3 photos
     - [ ] 8. Génération d'images
     - [ ] 9. Ta veille
     - [ ] 10. Fin et premier post

     ## Outils
     - Environnement :
     - Récupération des posts :
     - Génération d'images :
     - Mention « Visuel généré par IA » :  oui
     - Consentement visage :
     - Photos de référence :
     ```
     Ajoute aussi la ligne `- URL du profil LinkedIn :` dans `## Identité` si elle manque. Si une clé Google est déjà remplie dans `.env` (`grep -c '^GOOGLE_AI_API_KEY=.' .env` renvoie 1), note `Génération d'images : google`.
  2. déplace la recette existante (chiffres, registres classés, accroches, outliers) de `voice/identite-editoriale.md` vers `profile/recette.md`, sans réécrire le reste de l'identité éditoriale (s'il n'y a pas de recette chiffrée à déplacer, ou si `profile/recette.md` manque parce que la mise à jour s'est faite par ZIP, crée-le avec l'en-tête `Base : aucun post analysé` et fais de l'étape 3 la prochaine étape proposée) ;
  3. propose l'étape 3 en option (récupérer l'engagement via Apify pour affiner la recette), puis joue les étapes 5, 7, 8 et 9 ;
  4. pour les photos, si `assets/moi/visage-*` existent (`.jpeg`, `.jpg` ou `.png`), regarde-les et propose de les renommer en `face`, `profil-gauche`, `profil-droit` selon leur angle, en demandant celles qui manquent ;
  5. **photos déjà dans git** : la version 1 n'excluait pas `assets/moi/`. Lance `git ls-files assets/moi` (si le dossier est un dépôt git). S'il liste des photos, explique qu'elles sont suivies par git et peut-être déjà poussées, propose `git rm --cached assets/moi/<fichier>` pour chacune puis un commit, et préviens que l'historique du dépôt (et toute copie publique) les contient encore : si le dépôt est public, le passer en privé ou le recréer.

**Fichiers que la personne a personnalisés** (ne jamais les remplacer par la version du template lors d'une mise à jour) : `profile/*.md`, `voice/identite-editoriale.md`, `veille/`, `assets/`. Si elle a récupéré la nouvelle version et que l'un d'eux est revenu à l'état de gabarit, demande-lui de restaurer sa copie avant d'aller plus loin.

## Étape 1 : accueil et installation

Présente-toi en quatre phrases : ce que l'agent va faire, la durée (environ 30 minutes, en plusieurs fois si elle veut), le fait qu'elle peut sauter une étape ou s'arrêter quand elle veut, et ce qu'il est utile d'avoir sous la main :
- l'URL de son profil LinkedIn et celle de son site ;
- 3 ou 4 visuels de posts qu'elle aime (les siens ou ceux d'autres) ;
- 3 photos d'elle : une de face, une de profil gauche, une de profil droit ;
- si elle veut, un compte Apify (pour récupérer ses posts avec leurs chiffres) et un moyen de générer des images.

Puis vérifie l'installation, sans lui demander de le faire :

```bash
python3 --version
python3 -c "import requests" && echo requests-ok
python3 -m playwright --version
curl -sS -o /dev/null -w "%{http_code}" https://api.apify.com/v2
ls ~/Library/Caches/ms-playwright 2>/dev/null || ls ~/.cache/ms-playwright 2>/dev/null
command -v pdftoppm
```

- Python absent : donne le lien d'installation (python.org) et continue, les étapes de rédaction n'en ont pas besoin.
- `requests` ou Playwright absents : propose de lancer `python3 -m pip install requests` et `python3 -m pip install playwright && python3 -m playwright install chromium`, avec son accord (passer par `python3 -m` évite les `pip` et `playwright` introuvables dans le PATH). Si pip refuse avec `externally-managed-environment` (Python de Homebrew), ajoute `--user`, ou crée un environnement virtuel dans le dossier de l'agent (`python3 -m venv .venv`) en l'expliquant.
- `pdftoppm` absent : pas bloquant, propose `brew install poppler` (Mac) pour des carrousels nets au moment du premier carrousel.
- Réseau sortant bloqué (`curl` affiche `000` ou une erreur ; n'importe quel code HTTP, `404` compris, veut dire que le réseau passe) ou Chromium impossible à installer (aucun dossier `chromium-*` dans le cache Playwright après `playwright install chromium`) : tu es probablement dans un environnement restreint (Cowork par exemple). Note `Environnement : cowork` dans `profile/config.md` et adapte la suite : à l'étape 3, export LinkedIn ou copier-coller ; à l'étape 8, connecteur ou aucune ; les cartes et carrousels seront livrés en HTML à ouvrir dans un navigateur. Dis-le simplement, sans alarmer.
- Sinon, note `Environnement : desktop` (application Claude, onglet Code) ou `cli` (terminal).

Sortie : `profile/config.md` (Environnement). Coche l'étape 1.

## Étape 2 : toi et ton activité

Demande prénom, nom, URL du profil LinkedIn, URL du site (ou d'une page qui présente son activité). Récupère le site avec WebFetch (accueil, à-propos, offres) et extrais : l'entreprise, le secteur, l'offre, la cible apparente, le ton, le positionnement. Si le site est inaccessible, demande-lui de résumer ces points en quelques lignes.

Sorties : `profile/config.md` (Identité), `outputs/onboarding/analyse-site.md`. Coche l'étape 2.

## Étape 3 : tes anciens posts

But : récupérer de 30 à 100 de ses posts, idéalement avec leurs chiffres d'engagement. Présente les trois voies et recommande la première :

1. **Apify, piloté par l'agent (recommandé).** Elle crée un compte sur apify.com (des crédits sont offerts à l'inscription), copie son jeton personnel (*Settings > API & Integrations*) dans `.env` à la ligne `APIFY_TOKEN=`, et dit « c'est fait ». Tu lances :
   ```bash
   python3 scripts/scrape-linkedin-posts.py --profile <URL du profil> --max 100 --visuels
   ```
   Le script écrit `outputs/onboarding/posts.csv`, du plus récent au plus ancien (date, texte, likes, commentaires, partages, URL, `format`, `nb_visuels`, `visuels`), le JSON complet d'Apify à côté (`posts-brut.json`), et, avec `--visuels`, les images, les pages des carrousels et les miniatures de vidéos dans `outputs/onboarding/visuels/` (gratuit, de l'ordre de 10 Mo pour 20 posts). Il affiche aussi son titre LinkedIn : propose-le comme titre de signature (`profile/config.md`, § 7 de l'identité éditoriale), elle confirme ou corrige. Les liens des visuels expirent sous quelques jours : pour les récupérer après coup sans repayer, `--dernier-lancement --visuels` relit le dernier lancement. Permet : l'engagement et le format de chaque post, donc le classement de ce qui marche. Ne permet pas : la gratuité au-delà des crédits offerts (de l'ordre de 1,50 à 2 $ les 1 000 posts au moment de l'écriture de ce template). À utiliser sur son propre profil, dans le respect des conditions de LinkedIn. Si le script échoue, reprends son message en clair, explique-le, et propose la voie 2 ou 3.
2. **Export officiel LinkedIn (gratuit).** *Préférences > Confidentialité des données > Obtenir une copie de vos données > Publications*. LinkedIn envoie un lien par e-mail, de quelques minutes à 24 h. Elle dépose le fichier (`Shares.csv` ou un `.xlsx`) dans le dossier et te donne le chemin. Permet : tous ses posts, gratuitement. Ne permet pas : les likes et commentaires. Si l'attente est longue, propose de passer aux étapes 5 à 9 et de revenir ici ensuite.
3. **Copier-coller (gratuit).** Elle colle au moins 15 posts, de préférence ceux qui ont le mieux marché, avec leurs likes si elle les connaît. Permet : démarrer tout de suite. Ne permet pas : un échantillon représentatif.

Lis un `.xls`/`.xlsx` avec la skill xlsx, un `.csv` directement. Repère par heuristique la colonne du texte et, si elles existent, celles de l'engagement et de la date. Écarte les reposts sans commentaire (ce n'est pas sa plume). Moins de 10 posts originaux : dis-le, et construis une base prudente à recalibrer plus tard.

Sorties : le fichier de posts, `Récupération des posts` dans `profile/config.md`. Coche l'étape 3.

## Étape 4 : restitution de ta voix

**Sans posts** (étape 3 sautée ou vide) : ne fabrique pas de recette. Pose 4 questions de voix, une à la fois (comment tu ouvres un post, quelle longueur, ce que tu ne dirais jamais, un post d'un autre que tu aurais aimé écrire), et demande 2 ou 3 textes qu'elle a écrits ailleurs (mail, page du site, article). Rédige l'identité éditoriale à partir de ça et du site. Dans `profile/recette.md`, écris seulement l'en-tête avec `Base : aucun post analysé` et `Engagement disponible : non`, sans aucune section inventée, puis laisse l'étape 3 décochée « (sautée) » pour la reproposer. Coche l'étape 4 et passe à la 5.

Analyse les posts et note tout dans `outputs/onboarding/analyse-style.md` :
- **Ce que disent les chiffres** : médiane d'engagement d'un post original, outliers et leur multiple de la médiane, ce qui distingue le haut du bas du classement. Sans chiffres, dis-le et classe à l'œil.
- **Les accroches** : comment elle ouvre (affirmation + deux-points, question, contre-pied, chiffre). 3 à 5 vraies accroches citées mot pour mot.
- **Les registres** : opinion, contre-pied, retex, pédagogique, personnel, annonces… classés par performance.
- **Cadence et voix** : longueur des phrases et paragraphes, « je »/« vous », manière de chiffrer, clôtures, ponctuation, emojis.
- **Les formats** : texte seul, image, carrousel, vidéo, lien, citation. Avec la colonne `format` du CSV Apify, donne la médiane d'engagement par format et le nombre de posts derrière chaque médiane (un format vu 2 fois ne permet pas de conclure). Sans elle (export LinkedIn, copier-coller), classe à l'œil.
- **Le vocabulaire signature**, et **les tics** (dont ceux de la liste noire de `voice/anti-ai-writing-style.md` qu'elle utilise déjà).

**Montre-lui une synthèse courte avant d'écrire quoi que ce soit** : 3 accroches qui ont marché, ses 2 ou 3 registres les plus forts, 2 ou 3 tics repérés. Demande ce qui sonne faux ou manque. Intègre ses corrections.

Puis rédige :
- **`profile/recette.md`** (en remplaçant le gabarit) : chiffres, formats, angles classés, accroches, voix et cadence, modèle de visuel, outliers avec leurs URL ;
- **`voice/identite-editoriale.md`** (en remplaçant le gabarit) : ses 8 sections remplies avec les éléments réels des étapes 2 à 4 et écrites dans sa voix. C'est le livrable le plus important. Pas de section vide, pas de « TODO ».

Coche l'étape 4.

## Étape 5 : ta cible

Cinq questions, **une à la fois**. Pour chacune, propose d'abord ta réponse tirée du site et des posts (« d'après ton site, je dirais… »), elle corrige :
1. Qui précisément ?
2. Quel problème a cette personne, et que lui coûte-t-il ?
3. Qu'est-ce qu'elle lit et qui suit-elle ?
4. Qu'est-ce qui la fait hésiter ?
5. Que doit-elle faire après avoir lu un de tes posts ?

Ajoute l'objectif principal de la personne sur LinkedIn (reach, leads, autorité, recrutement) et les sujets qu'elle refuse de traiter.

Sorties : `profile/cible.md` (en remplaçant le gabarit), `Cible prioritaire`, `Objectifs` et `Garde-fous` dans `profile/config.md`, `§ 5` de l'identité éditoriale. Coche l'étape 5.

## Étape 6 : ton style visuel

Si `outputs/onboarding/visuels/` existe (étape 3 avec `--visuels`), commence par là : **regarde** les visuels de ses 3 ou 4 posts les plus performants (pour un carrousel, `page-01` suffit), propose-les comme références et copie dans `assets/references-visuelles/` ceux qu'elle garde. Elle peut en ajouter d'autres qu'elle admire, ou tout remplacer. Sinon, elle dépose 3 ou 4 visuels de posts qu'elle aime dans `assets/references-visuelles/`. **Regarde** chaque image et cherche ce qui revient de l'une à l'autre :
- archétype de composition (plein cadre photo, carte à marges, texte sur aplat, collage, graphique minimal) ;
- cadre et marges (si elle n'aime pas les cadres, note-le pour qu'aucun liseré ne soit forcé) ;
- titre (placement, typo, fond derrière le texte) ;
- couleur et contraste (palette, usage de l'accent, clair ou sombre) ;
- signature (photo + nom + titre, logo, URL, rien) ;
- image (photos, illustrations, memes, captures ; visage présent ou non) ;
- mood en une phrase, et ce qu'on évite.

Résume en une phrase, fais confirmer, puis demande : la couleur d'accent (hex, ou propose-en une cohérente avec ses références), ses polices de marque si elle en a (`.woff2` dans `assets/marque/fonts/`, sinon polices système), son logo éventuel, son titre de signature exact.

Sans visuels de référence : style neutre, signalé comme tel, à affiner plus tard.

Sorties : `profile/style-visuel.md` (en remplaçant le gabarit), `Identité visuelle` et `Titre de signature` dans `profile/config.md`. Coche l'étape 6.

## Étape 7 : tes 3 photos

Explique à quoi elles servent : la mettre en scène dans des images personnalisées avec son vrai visage. Le modèle copie l'angle qu'il voit, d'où trois angles. Demande-lui de déposer dans `assets/moi/` :
- `face.jpg` : de face, regard caméra ;
- `profil-gauche.jpg` : nez tourné vers la gauche de l'image (de trois quarts à profil complet) ;
- `profil-droit.jpg` : nez tourné vers la droite de l'image.

Une photo de téléphone suffit : une seule personne, visage net et assez grand, lumière du jour, fond simple. `.jpeg` et `.png` acceptés.

**Regarde chaque photo** et redemande-la, en expliquant pourquoi, si : visage trop petit (moins d'un tiers de la hauteur), flou, contre-jour ou ombre forte, lunettes de soleil, casquette sur les yeux, plusieurs personnes, visage coupé, filtre beauté appuyé, ou angle qui ne correspond pas au nom du fichier. Propose de recadrer toi-même si seul le cadrage pèche (recadrer oui, étirer jamais).

**Demande explicitement son consentement** : « J'utiliserai ces photos uniquement pour générer des images de toi, à ta demande, pour tes posts. D'accord ? » Note `Consentement visage : oui (AAAA-MM-JJ)` dans `profile/config.md`. Sans consentement, pas de génération avec ses photos, et dis-le.

Précise que `assets/moi/` est exclu de git : ses photos ne partiront jamais dans un dépôt.

Avatar de signature : si son style visuel prévoit une signature, propose de recadrer `face.jpg` en carré (`avatar-signature.jpg`) ou d'utiliser sa photo de profil LinkedIn.

Sorties : les photos, `Consentement visage` et `Photos de référence` dans `profile/config.md`. Coche l'étape 7.

## Étape 8 : génération d'images

Présente les voies et recommande selon sa situation (déjà abonnée à un service : le connecteur ; sinon : Google, le plus intégré) :

1. **Clé Google AI Studio (Nano Banana 2.1).** Elle crée une clé sur aistudio.google.com (*Get API key*), la met dans `.env` à `GOOGLE_AI_API_KEY=`. Permet : la génération la mieux intégrée à l'agent (prompts, références, journal automatique). Ne permet pas : la gratuité au-delà du quota gratuit (quelques centimes par image).
2. **Un connecteur branché à Claude : Magnific ou Higgsfield.** Cherche dans la session les outils de génération d'images disponibles (recherche d'outils par mot-clé, par exemple « image generate »). S'ils y sont, c'est prêt. Sinon, explique comment ajouter le connecteur dans les réglages de Claude (Connecteurs), puis ouvrir une nouvelle session. Permet : les modèles du service, sans clé à gérer. Ne permet pas : la gratuité (abonnement ou crédits du service). Pour Magnific, donne le lien de parrainage de l'auteur du template, en le présentant comme tel : https://referral.magnific.com/mzV9vem
3. **Sans génération (gratuit).** Cartes et carrousels avec ses vraies photos. Ne permet pas : les scènes détournées.

Note le choix dans `Génération d'images` (`google`, `magnific`, `higgsfield` ou `aucune`), et demande si elle veut la mention « Visuel généré par IA » en légende de ses posts (défaut : oui ; note `Mention « Visuel généré par IA »`).

**Image test** : si elle a choisi une voie de génération et donné son consentement à l'étape 7, propose une image test (elle en scène, avec `face.jpg`, selon `skills/image-linkedin/SKILL.md`) **en annonçant que c'est payant**, et ne la lance qu'après un oui. Montre le résultat, recueille son avis sur la ressemblance.

Sorties : `## Outils` de `profile/config.md`. Coche l'étape 8.

## Étape 9 : ta veille

1. **Propose les axes et les sources.** À partir de ses piliers (étape 4), de sa cible et de ce que sa cible lit (étape 5), propose 3 à 6 axes et des sources réelles pour chaque catégorie de `profile/veille.md` : presse du secteur, newsletters et blogs, comptes LinkedIn à surveiller, forums et communautés, sources institutionnelles et études, signaux faibles. Vérifie qu'une source existe avant de la proposer. Elle retire, elle ajoute.
2. **Première veille en direct.** Lance la skill `veille-contenu` sur la fenêtre des 14 derniers jours, limitée à 5 angles. Montre-lui les 5 idées de sujets, sourcées et datées : c'est ce qu'elle recevra chaque semaine.
3. **Installe la routine.** Demande le jour et l'heure (défaut : lundi 8 h). Présente les voies :
   - **Tâche planifiée de l'application Claude (recommandé, desktop ou Cowork).** Crée-la avec l'outil de tâches planifiées disponible dans la session, avec ce prompt : « Dans le dossier <chemin absolu de l'agent>, lance la skill veille-contenu en mode routine. » Permet : zéro manipulation. Ne permet pas : de tourner si l'ordinateur est éteint ou l'application fermée (la tâche part au prochain lancement).
   - **Routine cloud Claude Code (`/schedule`).** Tourne sans l'ordinateur. Ne permet pas : de s'en passer d'un dépôt GitHub **privé** à elle. Si elle n'en a pas, guide sa création selon le cas :
     - dossier téléchargé en ZIP (pas de dépôt git, `git rev-parse` échoue) : `git init && git add -A && git commit -m "Mon agent LinkedIn"` puis `gh repo create <nom> --private --source . --push` ;
     - dossier cloné depuis le template (`origin` pointe vers le template public) : `gh repo create <nom> --private` puis `git remote rename origin template && git remote add origin <URL du nouveau dépôt> && git push -u origin main`.
     Vérifie avec `git remote get-url origin` que le dépôt est bien le sien et privé avant tout push. Crée ensuite la routine avec le même prompt ; elle pousse ses rapports sur `main`. Note `Voie : routine cloud` dans `profile/veille.md` : l'agent fera `git pull` en début de session pour récupérer les rapports.
   - **n8n (open source)**, si elle en a un sur la même machine que l'agent : un nœud planifié (*Schedule Trigger*) suivi d'un nœud *Execute Command* qui lance, dans le dossier de l'agent, `claude -p "lance la skill veille-contenu en mode routine" --allowedTools "Read,Write,Edit,WebSearch,WebFetch,Agent,Bash(git:*)"` (sans liste d'outils autorisés, le mode non interactif refuse la recherche et l'écriture, et la veille n'est jamais écrite). Ne permet pas : de se passer d'installer et maintenir n8n.
   - Aucune : elle dira « ma veille » quand elle voudra.
   Si l'outil de tâches planifiées n'est pas disponible dans la session, dis-le et propose les autres voies.

Sorties : `profile/veille.md` (axes, sources, routine, identifiant de la routine), `veille/journal.md` et le premier rapport. Coche l'étape 9.

## Étape 10 : fin et premier post

1. Passe `profile/config.md` à `STATUT: CONFIGURÉ` et `Étape en cours : terminé`.
2. Récap en 5 lignes : positionnement, registres qui marchent, cible, style visuel, routine de veille (jour, heure, voie).
3. Rappelle les étapes sautées, une ligne chacune, avec la phrase qui les relance (« configure la génération d'images », « configure ma veille »…).
4. Propose : « On écrit ton premier post ? » à partir d'une des 5 idées de la veille → bascule sur `my-viral-post`.

Coche l'étape 10.

## Garde-fous

- Jamais de post publié ni de visuel livré pendant l'onboarding, hors image test et première veille.
- Jamais de chiffre, d'accroche, de client ou de goût visuel inventé.
- Jamais de clé ou de jeton lu, recopié ou commité.
- Jamais de dépense sans un oui.
- Jamais de photo d'une autre personne réelle.
- Respecte `voice/anti-ai-writing-style.md` dans chaque ligne rédigée.
