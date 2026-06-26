---
name: carrousel-linkedin
description: Génère un carrousel LinkedIn (PDF multipage 1080×1350 portrait), pensé pour être utile et enregistré. Souvent dérivé d'un article de blog ou d'un post expert. Footer signé (photo + titre de la personne). Utilise cette skill quand elle demande "un carrousel LinkedIn", "des slides LinkedIn", "un post carrousel", "transforme cet article en carrousel". Pour une image unique → carte-linkedin. Pour une scène IA → image-linkedin.
---

# carrousel-linkedin : carrousels LinkedIn

Tu construis des carrousels LinkedIn en PDF multipage 1080×1350 portrait. Objectif assumé : **être assez utile pour qu'on l'enregistre** (posts experts, méthodes, exemples tirés d'articles de blog). Cette skill est la **source des tokens de design** (typo, espacement, palette, fonts) pour `carte-linkedin`.

Avant de composer, lis `profile/style-visuel.md` (le style de la personne : cadre, titres, signature ou non), `profile/config.md` (couleur d'accent, fonts, titre de signature, site) et `voice/identite-editoriale.md` (ton, registres).

## Doctrine de marque (selon le style de la personne)

- **La mise en page suit `profile/style-visuel.md`**, pas un gabarit imposé. Cadre, placement des titres et présence d'une signature dépendent de ses goûts.
- **Signature** : seulement si son style en porte une. Le cas échéant, sur la slide finale : avatar `assets/moi/avatar-signature.jpg` + **Prénom Nom** + **titre de signature** (`profile/config.md`). Si son style n'en porte pas, ne l'ajoute pas.
- **Pas de marque secondaire ni de personnage compagnon.** Option discrète si son style l'admet : logo (`assets/marque/logos/`) + URL du site.
- Le contenu sert l'autorité de la personne. Si `profile/style-visuel.md` est encore un gabarit, propose 2-3 partis pris et laisse-la choisir.

## Workflow

1. **Brief court** : audience, message-clé, copy du post, source (article de blog ?), nombre de slides (8-10 typique).
2. **Plan de slides** : 1 hook + 1 plot twist + actes/preuves + manifeste + signoff/CTA. 1 ligne par slide, validé.
3. **HTML standalone** dans `outputs/carrousel-<slug>-<date>/index.html`, dupliqué depuis `templates/carousel-linkedin-base.html`.
4. **Assets** : logo depuis `assets/marque/logos/` (optionnel), chemins relatifs. Jamais d'emoji Unicode → icône générée via `image-linkedin`, déposée dans `assets/marque/icons/`. Référence de composition : `assets/visuels-posts/`.
5. **Export PDF** : `python3 scripts/export-carousel-pdf.py outputs/carrousel-<slug>-<date>/index.html outputs/carrousel-<slug>-<date>/exports/<slug>.pdf`
6. **Vérification visuelle** : lire les pages clés du PDF, itérer en éditant le HTML.
7. **Livrable** : le PDF + l'HTML + le brief.

## Format LinkedIn

- **1080×1350 px** (4:5 portrait), optimum feed mobile (~80% du trafic).
- PDF document multipage, max 100 MB, max 20 pages.
- Min lisible : **22 px source**. En dessous = erreur.

## Échelle typographique STRICTE (aucune taille hors barème)

| Rôle | Taille | Line-height | Usage |
|---|---|---|---|
| `.h-xxl` | 168px | 0.92 | Hook cover (1 slide max) |
| `.h-xl` | 124px | 0.94 | Titres impact, chiffres clés |
| `.h-l` | 88px | 0.98 | Titres standard |
| `.h-m` | 64px | 1.02 | Sous-titres |
| `.h-sub` | 56px | 1.06 | Valeurs, headers tertiaires |
| `.lede` | 36px | 1.36 | Premier paragraphe |
| `.body-l` | 30px | 1.42 | Texte principal |
| `.body-m` | 28px | 1.42 | Texte secondaire |
| `.caption` | 24px | 1.35 | Légendes |
| `.footer` | 22px | : | Baseline footer (plancher absolu) |

> Ces tailles sont calibrées pour une police display dense / condensée. Avec les polices système par défaut, raccourcis les titres pour éviter les débordements, ou ajoute ta police de marque (voir Polices).

## Échelle d'espacement STRICTE

```css
:root {
  --sp-3xs: 8px; --sp-2xs: 16px; --sp-xs: 24px; --sp-sm: 32px;
  --sp-md: 48px; --sp-lg: 64px; --sp-xl: 80px; --sp-2xl: 100px;
}
```

Minimum `--sp-md` (48px) entre deux blocs sémantiquement distincts. Aucune valeur hardcodée hors barème.

## Couleurs

Base éditoriale neutre (fond clair `#FDFCFA` / `#F5F0EA`, texte sombre `#1A1A2E`) + **un seul accent** par carrousel : la couleur d'accent de `profile/config.md`, utilisée selon le style (titres, et liseré si `profile/style-visuel.md` en prévoit un). Ne pas multiplier les accents.

```css
--ink: #1A1A2E; --paper: #FDFCFA; --paper-2: #F5F0EA;
--accent: <couleur de profile/config.md>;   /* accent unique */
--accent-soft: <version claire>;            /* fonds */
```

## Polices (locales, jamais de Google Fonts CDN)

Par défaut, polices système (le template rend sans rien installer). Pour un rendu pixel-perfect à la marque, dépose les `.woff2` dans `assets/marque/fonts/`, décommente le bloc `@font-face` du template, et renseigne les noms dans `profile/config.md`.

```css
@font-face { font-family:'Ma Display'; src:url('../assets/marque/fonts/display.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Mon Corps';  src:url('../assets/marque/fonts/body.woff2')    format('woff2'); font-weight:400; }
```

## Règles UX LinkedIn (anti-patterns à retirer systématiquement)

1. Pas de folio « 01 / 10 » (LinkedIn affiche sa propre progression).
2. Pas d'eyebrow « Acte 1 / Acte 2 » : le titre parle de lui-même.
3. **Pas de point final** sur les titres et CTA courts. Les paragraphes longs gardent leur ponctuation.
4. **Pas de tiret cadratin (—)** : virgule, deux-points, ou reformuler.
5. **Pas d'emoji Unicode** : utiliser une icône générée (`assets/marque/icons/`, via `image-linkedin`).
6. Pas de gradient sur titres standards (réservé au hook `.h-xxl`).
7. Déclarer `font-size` explicitement à chaque niveau (éviter les héritages sous 22 px).

## Signoff (seulement si le style en porte un)

À n'utiliser que si `profile/style-visuel.md` prévoit une signature. Le cas échéant, sur la dernière slide (et en option discrète sur le hook) :

```html
<div class="signoff">
  <img class="avatar" src="../assets/moi/avatar-signature.jpg" alt="">
  <div class="txt">
    <strong>Prénom Nom</strong>
    Titre de signature
  </div>
</div>
```

Avatar rond 112×112 px, bordure 2px. Nom en `.h-m`, titre en `.body-m`. (Valeurs à reprendre de `profile/config.md`.)

## Patterns de slides réutilisables

- **Hook** : fond clair, `.h-xxl`, flèche `→` (swipe horizontal), pas de point final.
- **Plot twist / manifeste** : fond sombre `#1A1A2E`, `.h-xxl` clair, pas de visage (les traits fins se perdent sur dark), centré.
- **Preuve / cards** : fond clair, grid de cards, chiffre clé en `.h-sub`.
- **Étapes / pipeline** : nodes empilés, contraste croissant.
- **Verdict** : 2-3 punchlines en `.h-l`, accents sur les mots-clés.
- **Signoff / CTA** : fond sombre, 1-2 actions max, signoff en bas.

## Journalisation

Chaque carrousel : brief + HTML source + PDF export, tous dans `outputs/carrousel-<slug>-<date>/`. L'export (`export-carousel-pdf.py`) ajoute une ligne dans `outputs/registry.csv`. Disclosure IA : composition HTML d'assets existants → pas de mention. Si une scène/icône générée IA est intégrée → disclosure.

## Vérification (lire le PDF avant de livrer)

Collisions, texte tronqué, tailles sous 22 px, accent unique respecté, signoff présent, pas d'emoji Unicode ni de tiret cadratin. Itérer en éditant le HTML, pas en repartant de zéro.

## Skills liées

- `carte-linkedin` : visuel single-image (hérite des tokens ci-dessus).
- `image-linkedin` : scène / icône générée IA.
- `my-viral-post` : le copy du post qui accompagne le carrousel.
