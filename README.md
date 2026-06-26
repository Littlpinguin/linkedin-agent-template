# linkedin-agent-template

**Un template d'agent LinkedIn personnel pour Claude Code / Cowork.** Tu l'ouvres, tu dis « commencer », et il se calibre sur *ta* voix à partir de tes vrais posts. Ensuite, il écrit des posts qui te ressemblent et produit les visuels qui les accompagnent (images IA détournées, cartes, carrousels).

Pas un générateur de contenu générique : un agent qui apprend ton style d'écriture **et** ton style visuel, puis s'y tient.

## Utiliser ce template

1. **Crée ton dépôt** : clique sur **« Use this template »** en haut de cette page (ou `git clone`).
2. **Ouvre le dossier** avec Claude Code (ou Cowork).
3. **Dis simplement « commencer »**. L'agent lance son onboarding.

> Besoin de Claude Code ? Voir [claude.com/claude-code](https://claude.com/claude-code).

## Ce que fait l'onboarding

À la première ouverture, l'agent :

1. te demande **ton export de posts LinkedIn** (`.xls` / `.xlsx` / `.csv`), **l'URL du site de ton entreprise**, et **3-4 visuels de posts que tu aimes** (déposés dans `assets/references-visuelles/`) ;
2. analyse tes posts (accroches, registres qui marchent, cadence, formats), ton site (entreprise, offre, cible, ton) et tes visuels de référence (pour en déduire ton style visuel) ;
3. rédige ton identité éditoriale (`voice/identite-editoriale.md`), ton style visuel (`profile/style-visuel.md`) et remplit ta config (`profile/config.md`) ;
4. te pose quelques questions pour affiner (cible, objectifs, couleur de marque, titre de signature, style visuel, sujets interdits) ;
5. finalise : tu peux écrire ton premier post.

> **Comment récupérer tes posts LinkedIn :** *Préférences → Confidentialité des données → Obtenir une copie de vos données → cocher les publications (« Shares »)*. À défaut, n'importe quel tableur avec une ligne par post convient : une colonne texte, et si possible likes / commentaires / partages / date.

## Prérequis

- **Claude Code** ou **Cowork** (l'agent et ses skills tournent dedans).
- **Python 3** avec :
  - `pip install requests` (génération d'images) ;
  - `pip install playwright && playwright install chromium` (cartes et carrousels).
- **Clé Google AI Studio** pour la génération d'images : copie `.env.example` en `.env` et renseigne `GOOGLE_AI_API_KEY`.
- **3-5 photos de ton visage** dans `assets/moi/` (pour l'« Identity Lock » des images générées).

> La génération IA (API Google) et les screenshots (Chromium) tournent en local, pas en environnement réseau restreint.

## La chaîne de production (après configuration)

1. **Écrire** : `my-viral-post` propose des angles dans ta voix, assemble le post, et indique le format visuel à associer.
2. **Illustrer**, selon le registre :
   - opinion / contre-pied → `image-linkedin` (image détournée avec ton visage, meme) ;
   - expert / pédagogique → `carte-linkedin` (infographie) ou `carrousel-linkedin` ;
   - retex / outils → carte + capture.
3. **Composer puis exporter** : une image brute (`outputs/images/`) se recompose en post fini via `carte-linkedin`, puis s'exporte (PNG 1080×1350 ou PDF).
4. **Vérifier et publier** : chaque skill lit son rendu avant livraison et journalise dans `outputs/`.

## Structure

```
linkedin-agent-template/
├── CLAUDE.md                ← l'orchestrateur (règles + déclencheur d'onboarding)
├── skills/
│   ├── onboarding/              ← calibre l'agent sur ta voix + ton style (première fois)
│   ├── my-viral-post/           ← rédige le post (texte)
│   ├── image-linkedin/          ← image IA détournée + meme (Nano Banana Pro)
│   ├── carte-linkedin/          ← carte / infographie single-image (HTML→PNG)
│   └── carrousel-linkedin/      ← carrousel PDF multipage (source des tokens design)
├── voice/
│   ├── identite-editoriale.md   ← TA voix (rédigée à l'onboarding)
│   └── anti-ai-writing-style.md ← règles anti-IA universelles
├── profile/
│   ├── config.md            ← tes variables (nom, entreprise, couleur, cible, objectifs)
│   └── style-visuel.md      ← TON style visuel (déduit des visuels que tu aimes)
├── assets/
│   ├── moi/                 ← tes photos de visage + avatar de signature
│   ├── marque/             ← ton kit (logo, fonts, icônes) — optionnel
│   ├── references-visuelles/ ← 3-4 visuels que tu aimes (base de ton style)
│   ├── visuels-generes/    ← images IA brutes (réf de TON)
│   └── visuels-posts/      ← posts finis composés (réf de COMPOSITION)
├── scripts/                 ← gen-image.py, screenshot.py, export-carousel-pdf.py, journal.py
├── templates/               ← carousel-linkedin-base.html
├── docs/                    ← note de conception du template
└── .env.example             ← clé Gemini pour la génération d'images
```

## Ce qui rend ce template différent

- **Personal branding pur** : ton visage dans les images. Pas de marque secondaire ni de personnage compagnon.
- **Pas de cadre imposé** : le template ne force ni liseré, ni titre haut, ni signature. Ton style visuel est déduit des 3-4 visuels que tu déposes, pour que tes posts te ressemblent et pas au gabarit de tout le monde.
- **Anti « AI slop »** : `voice/anti-ai-writing-style.md` proscrit le jargon de hype, les parallélismes négatifs (« ce n'est pas X, c'est Y »), le tiret cadratin, et impose une voix concrète et chiffrée.
- **Un seul accent** : ta couleur de marque, choisie à l'onboarding, réglable dans `profile/config.md`.
- **Polices** : par défaut, polices système (rend sans rien installer). Dépose tes `.woff2` dans `assets/marque/fonts/` pour un rendu pixel-perfect.
- **Autonome** : tout reste sous le dossier. Outputs et journal dans `outputs/` (gitignored).

## Sécurité

- Ne committe jamais `.env` (couvert par `.gitignore`).
- Seul ton visage (avec ton consentement) dans `assets/moi/`. Aucune autre personne réelle sans accord.
- Logos tiers : ne jamais les fabriquer par IA ni les scraper. Demander les fichiers officiels.

## Licence

[MIT](LICENSE). Réutilise, modifie, redistribue librement.
