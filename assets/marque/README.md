# assets/marque/ — ton kit visuel (optionnel)

Personal branding pur : pas de marque secondaire ni de personnage compagnon. Ce dossier porte juste ce qui rend tes visuels reconnaissables.

## Sous-dossiers

- **`logos/`** — ton logo (ou celui de ton entreprise) en `.svg` (idéal) ou `.png` à fond transparent. Sert de petit clin d'œil discret en coin de carte / carrousel. Optionnel.
- **`fonts/`** — tes polices de marque en `.woff2`, si tu en as. Par défaut, le template tourne avec des polices système (aucune installation). Pour un rendu pixel-perfect :
  1. dépose ici `display.woff2` (titres) et `body.woff2` (texte) ;
  2. décommente le bloc `@font-face` dans `templates/carousel-linkedin-base.html` ;
  3. renseigne les noms dans `profile/config.md` (Police display / Police corps).
  - N'utilise que des polices dont tu as la licence. Ne redistribue pas de police payante.
- **`icons/`** — icônes générées par IA (via `image-linkedin`) pour remplacer les emojis Unicode dans les visuels. Se remplit au fil de l'eau.

## Couleur d'accent

Ta couleur de marque ne vit pas ici mais dans `profile/config.md` (champ « Couleur d'accent »). Un seul accent, utilisé là où ton style l'appelle (titres, et liseré si ton style en a un). Ton style visuel global est décrit dans `profile/style-visuel.md`.
