---
name: carte-linkedin
description: Crée un visuel LinkedIn single-image (1 image finie texte+visuel, pas un carrousel) : carte d'opinion ou infographie pratique pensée pour être enregistrée. La mise en page suit le style visuel de la personne (profile/style-visuel.md), pas un cadre imposé. Utilise cette skill quand elle demande "une carte", "une infographie", "un visuel pour accompagner mon post", "une image LinkedIn". Pour un carrousel multipage → carrousel-linkedin. Pour une scène IA détournée → image-linkedin.
---

# carte-linkedin : visuel LinkedIn single-image

Tu produis **une seule image** LinkedIn finie (texte + visuel intégrés), prête à poster : carte d'opinion ou **infographie pratique conçue pour être enregistrée** (méthode, checklist, avant/après). Cette skill **hérite des tokens de design** (typo, espacement) de `carrousel-linkedin`.

**Avant de composer, lis trois fichiers :**
- `profile/style-visuel.md` : le style visuel de la personne (déduit de ses visuels de référence à l'onboarding). **C'est lui qui décide** de la mise en page : cadre ou pas, placement du titre, signature ou non, traitement photo. Suis-le.
- `profile/config.md` : couleur d'accent, titre de signature, fonts.
- `voice/identite-editoriale.md` : ton, registres.

Et inspire-toi de `assets/references-visuelles/` (les visuels qu'elle aime) et de `assets/visuels-posts/` (ses posts finis, quand il se remplit).

## Principe : pas de cadre imposé

Le template **n'impose aucun gabarit**. La signature visuelle de la personne vient de `profile/style-visuel.md`, pas d'un liseré ou d'un placement obligatoire. Lis ce fichier et reproduis **son** archétype.

- Si son style utilise un liseré → fais-le, dans sa couleur d'accent.
- Si son style est plein cadre sans bordure → pas de liseré.
- Si son style ne porte pas de signature → n'en ajoute pas.
- Si `profile/style-visuel.md` est encore un gabarit (style non défini) → propose 2-3 options de composition à la personne et demande laquelle elle préfère, plutôt que d'imposer.

La personne reste le sujet (son visage, via `image-linkedin` ou une photo), sauf si son style privilégie autre chose (typo seule, capture, illustration).

## Méthode : HTML → screenshot Playwright (jamais Pillow)

Pillow ne charge pas les fonts woff2. Toujours composer en **HTML/CSS** puis screenshot **Playwright/Chromium** → typo pixel-perfect, hex exacts, logos SVG inline.

- Fonts : système par défaut, ou woff2 depuis `assets/marque/fonts/` si fournies (jamais de Google Fonts CDN, pour un rendu hors-ligne fiable).
- Image de fond : une image générée par `image-linkedin` (`outputs/images/`) ou une photo.
- Capture : `python3 scripts/screenshot.py <html> <out.png>` (device_scale_factor=2, viewport 1080×1350 → sortie 2160×2700). Ajoute une ligne dans `outputs/registry.csv`.

## Format & échelle

- **1080×1350** (4:5 portrait) par défaut. **1:1 carré** pour les formats comparaison (« VS »).
- Échelle typo et tokens d'espacement **stricts** de `carrousel-linkedin`. **Plancher absolu 22 px.**
- **Un seul accent** par carte : la couleur de `profile/config.md`. Pas de salade de couleurs.

## Boîte à outils de composition (options, pas obligations)

À piocher selon `profile/style-visuel.md`. Aucune n'est imposée :

- **Image plein cadre** (la personne détournée, ou une photo), avec ou sans liseré.
- **Titre** : en haut, centré, incrusté dans la scène, ou en bas, selon son style. Gros (`.h-xl`/`.h-xxl`), **pas de point final**.
- **Cœur utile** (infographie) : 3 à 5 étapes / checklist / avant-après, hiérarchie claire, le point clé saute aux yeux.
- **Question / chute** en bas, si son style l'appelle.
- **Signature** : seulement si son style en porte une (logo, URL, ou photo+titre). Sinon, rien.
- **Comparaison « VS »** : diptyque 50/50 (carré 1:1), côté positif accentué, côté négatif terne.
- **Texte diégétique** : le message écrit **dans la scène** (tableau, écran, pancarte) plutôt qu'en surimpression. À demander à `image-linkedin`.

## Règles non négociables (universelles, indépendantes du style)

- **Conçue pour être enregistrée** : l'image reste utile relue à froid (une vraie méthode, un vrai chiffre), pas juste décorative.
- **Jamais de collision visuel/texte** : `max-width` sur les paragraphes, couloir réservé pour le sujet.
- Pas de point final sur titres courts · pas de tiret cadratin (—) · espace fine milliers (`1 700`) · pas d'emoji Unicode (icône générée dans `assets/marque/icons/` à la place).
- **Un seul accent** par carte.
- **Logos tiers** : ne jamais les fabriquer par IA ni les scraper. Demander les fichiers officiels.

## Boucle de vérification (lire le PNG avant de livrer)

Cohérent avec `profile/style-visuel.md`, titre lisible, tailles sous 22 px corrigées, pas de collision, accent unique. Itérer en éditant le **HTML/script**, pas en repartant de zéro.

## Disclosure IA

Composition HTML d'assets existants → pas de mention. Si l'image de fond est une scène générée IA (via `image-linkedin`) → disclosure dans la légende du post.

## Skills liées

- `carrousel-linkedin` : source des tokens (typo / espacement) + version multipage.
- `image-linkedin` : la scène / la personne détournée à composer ici.
- `my-viral-post` : le copy du post qui accompagne la carte.
