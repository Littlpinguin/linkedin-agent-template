---
name: carrousel-linkedin
description: Génère un carrousel LinkedIn (PDF multipage 1080×1350 portrait), pensé pour être utile et enregistré. Souvent dérivé d'un article de blog ou d'un post expert. Cadrage stratégique en 5 couches, page de garde avec la personne en scène, PDF rastérisé prêt à publier. Utilise cette skill quand elle demande "un carrousel LinkedIn", "des slides LinkedIn", "un post carrousel", "transforme cet article en carrousel". Pour une image unique → carte-linkedin. Pour une scène IA → image-linkedin.
---

# carrousel-linkedin : carrousels LinkedIn

Tu construis des carrousels LinkedIn en PDF multipage 1080×1350 portrait. Objectif assumé : **être assez utile pour qu'on l'enregistre** (posts experts, méthodes, exemples tirés d'articles de blog). Cette skill est la **source des tokens de design** (typo, espacement, palette, fonts) pour `carte-linkedin`.

**Environnement restreint** : si `Environnement : cowork` dans `profile/config.md`, ou si Chromium ou `pdftoppm` manquent, ne lance pas les scripts d'export. Livre `index.html` et explique comment l'exporter soi-même : ouvrir le fichier dans Chrome, Imprimer, Enregistrer en PDF, format personnalisé 1080×1350 px, marges aucune, graphiques d'arrière-plan cochés.

Avant de composer, lis `profile/style-visuel.md` (le style de la personne : cadre, titres, signature ou non), `profile/config.md` (couleur d'accent, fonts, titre de signature, site), `voice/identite-editoriale.md` (ton, registres) et `voice/compositions-carrousel.md` (la grille, l'échelle mobile-safe et le répertoire des 8 compositions : source de vérité de mise en page).

## Doctrine de marque (selon le style de la personne)

- **La mise en page suit `profile/style-visuel.md`**, pas un gabarit imposé. Cadre, placement des titres et présence d'une signature dépendent de ses goûts.
- **Signature** : seulement si son style en porte une. Le cas échéant, sur la slide finale : avatar `assets/moi/avatar-signature.jpg` (à défaut, `face.jpg` ou `face.jpeg`/`.png` recadré, ou l'ancien `visage-1.*`) + **Prénom Nom** + **titre de signature** (`profile/config.md`). Si son style n'en porte pas, ne l'ajoute pas.
- **Pas de marque secondaire ni de personnage compagnon.** Option discrète si son style l'admet : logo (`assets/marque/logos/`) + URL du site.
- Le contenu sert l'autorité de la personne. Si `profile/style-visuel.md` est encore un gabarit, propose 2-3 partis pris et laisse-la choisir.

## Cadrage stratégique (obligatoire, avant tout plan de slides)

Passe le sujet dans cette grille avant de proposer le moindre plan. Une seule idée forte par carrousel : **1 audience, 1 problème, 1 solution**. Résiste à l'envie de tout dire. L'audience par défaut est celle de `profile/cible.md`.

| # | Couche | Objectif | Ce qu'on y montre |
|---|---|---|---|
| 1 | **Hook** : stopper le scroll | Capter l'attention en 1 seconde | Affirmation forte, avis tranché, bénéfice clair (voir `voice/bibliotheque-hooks-visuels.md` § B) |
| 2 | **Contexte** : se sentir compris | Le lecteur se reconnaît | Le problème, une erreur commune, une situation familière |
| 3 | **Insight** : l'idée centrale | Livrer la leçon principale | Une idée claire, un cadre simple, un changement de perspective |
| 4 | **Preuve** : rendre crédible | Faire croire que ça marche | Avant/après, exemple concret, chiffre réel sourcé |
| 5 | **Action** : la suite | Dire quoi faire ensuite | CTA doux, action à faible effort (celle de `profile/cible.md` § 5) |

## La page de garde : la personne en scène, si le style l'admet

Une scène photo de la personne, générée via `image-linkedin` et mise en scène avec humour, arrête mieux le scroll qu'un titre sur aplat. C'est la couverture par défaut quand `profile/style-visuel.md` admet les photos et que `Génération d'images` n'est pas `aucune`. Sinon, couverture typographique (composition n°1).

1. **La scène occupe tout le cadre** (`object-fit:cover`), la personne dans une posture qui incarne le sujet au premier degré, avec un accessoire qui porte la blague.
2. **Calque de dégradé sur le bas** (transparent vers la couleur de fond, hauteur ≈ 44 %) pour que le hook reste lisible quel que soit le fond.
3. **Hook en bas, aligné à gauche, 90-100 px, 2 lignes**, un mot à l'accent. Il **joue avec la scène** au lieu de la décrire : texte et image se répondent, la boucle reste ouverte.
4. **Indice de swipe** discret en bas à droite.
5. Tout texte ajouté est composé en HTML par-dessus, jamais généré par l'IA.

L'humour vient de la posture et de la mise en scène, jamais d'une caricature du visage.

## Workflow

1. **Brief court** : audience, message-clé, copy du post, source (article de blog ?), nombre de slides (8-10 typique, moins si chaque slide ne porte pas sa propre idée).
2. **Plan de slides** : passer par le cadrage stratégique, puis 1 hook + 1 plot twist + actes/preuves + manifeste + signoff/CTA. 1 ligne par slide, validé.
3. **HTML standalone** dans `outputs/carrousel-<slug>-<date>/index.html`, dupliqué depuis `templates/carousel-linkedin-base.html`.
4. **Assets** : logo depuis `assets/marque/logos/` (optionnel), chemins relatifs. Jamais d'emoji Unicode → icône générée via `image-linkedin`, déposée dans `assets/marque/icons/`. Référence de composition : `assets/visuels-posts/`.
5. **Export PDF** : `python3 scripts/export-carousel-pdf.py outputs/carrousel-<slug>-<date>/index.html outputs/carrousel-<slug>-<date>/exports/<slug>.pdf`
6. **Vérification visuelle** : lire les pages clés du PDF, itérer en éditant le HTML.
7. **PDF rastérisé** pour la publication (voir plus bas).
8. **Livrable** : le PDF à publier (`-hd.pdf`) + le PDF vectoriel + l'HTML + le brief.

## Format LinkedIn

- **1080×1350 px** (4:5 portrait), optimum feed mobile (~80% du trafic).
- **Marges : 80 px latéral · 120 px haut · 160 px bas** → bloc de contenu utile **920 × 1070 px** centré. Le bas à 160 px garde le contenu vital hors de la zone où LinkedIn superpose son compteur de slides et les réactions. Rien de vital hors de ce bloc.
- PDF document multipage, max 100 MB, max 20 pages.
- **Plancher lisible mobile : 32 px** pour tout texte de contenu (26 px uniquement pour le numéro de slide / la mention légale). En dessous = illisible au feed.

## Échelle typographique MOBILE-SAFE (aucune taille hors barème)

Un canvas de 1080 px est réduit à ~390 px sur un téléphone : **taille perçue ≈ taille canvas × 0,36**. Un corps à 30 px n'y fait que ~11 px, illisible dans le feed. D'où ces planchers (calibrés pour la lecture mobile réelle, pas pour l'écran d'édition) :

| Rôle | Classe | Taille source | Line-height | ≈ écran mobile |
|---|---|---|---|---|
| Hook hero (couverture, 1 slide max) | `.h-xxl` | **130–180px** | 0.95 | 47–65px |
| Chiffre-ancre (stat géante) | `.h-num` ¹ | **240–330px** | 0.90 | n/a |
| Titre de slide | `.h-l` | **88–110px** | 1.0 | 32–40px |
| Sous-titre | `.h-m` | **60–72px** | 1.08 | 22–26px |
| Corps / puce | `.body-l` | **≥ 48px** (48–56) | 1.42 | 17–20px |
| Légende / source | `.caption` | **≥ 32px** (32–36) | 1.35 | 12–13px |
| Numéro de slide / mention légale | `.footer` | 26–30px | 1.2 | ~10px |

¹ `.h-num` : plus grand que toute classe standard : à définir en inline ou via une classe dédiée.

> Paliers intermédiaires (`.h-sub`, `.lede`, `.body-m`) : tolérés, mais **jamais sous le plancher de leur rôle** : un corps reste ≥ 48px, une légende ≥ 32px. L'ancienne échelle (corps ~28-30px, footer 22px) est trop petite pour le feed mobile : ne plus l'utiliser.
> Ces tailles supposent la police display du profil pour les titres. Sans police de marque (polices système), raccourcis les titres pour éviter les débordements, ou ajoute ta police (voir Polices).

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
2. **Tic IA n°1, banni : aucun label en CAPITALES espacées au-dessus du titre** (le « kicker » / eyebrow répété, type « ACTE 1 », « MÉTHODE », « ÉTAPE »). Plier l'info dans le titre lui-même. La classe `.eyebrow` du template ne sert qu'à un usage exceptionnel, jamais en label répété au-dessus de chaque titre.
3. **Pas de point final** sur les titres et CTA courts. Les paragraphes longs gardent leur ponctuation.
4. **Pas de tiret cadratin (—)** : virgule, deux-points, ou reformuler.
5. **Pas d'emoji Unicode** : utiliser une icône générée (`assets/marque/icons/`, via `image-linkedin`).
6. Pas de gradient sur titres standards (réservé au hook `.h-xxl`).
7. Déclarer `font-size` explicitement à chaque niveau (éviter tout héritage sous le plancher mobile : 32 px pour le contenu, 26 px pour le numéro / la mention légale).

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

## Compositions & alternance (répertoire)

Le répertoire complet des **8 compositions nommées** (Couverture cadrée, Partition 3 registres, Ancre-nombre, Étapes numérotées, Comparaison 2 colonnes, Citation pleine, Hero illustration, Signoff/CTA), la grille de référence et le rythme d'une séquence type vivent dans `voice/compositions-carrousel.md`. **Le lire avant de figer le plan de slides.**

Règle de fer : **jamais deux slides voisines au même squelette.** On fait tourner les compositions d'une slide à l'autre : c'est cette alternance, plus qu'aucun effet, qui donne le rendu « designé par un senior ». Les patterns ci-dessous sont un sous-ensemble rapide de ce répertoire.

## Patterns de slides réutilisables

- **Hook** : fond clair, `.h-xxl`, flèche `→` (swipe horizontal), pas de point final.
- **Plot twist / manifeste** : fond sombre `#1A1A2E`, `.h-xxl` clair, pas de visage (les traits fins se perdent sur dark), centré.
- **Preuve / cards** : fond clair, grid de cards, chiffre clé en `.h-sub`.
- **Étapes / pipeline** : nodes empilés, contraste croissant.
- **Verdict** : 2-3 punchlines en `.h-l`, accents sur les mots-clés.
- **Signoff / CTA** : fond sombre, 1-2 actions max, signoff en bas.

## Leçons de production

- **Le test de la seconde, avant de peaufiner la typo.** Qu'est-ce que le lecteur comprend en une seconde, et qu'est-ce qui lui donne envie de swiper ? Les corrections de fond viennent de là, pas des tailles de police. La meilleure image ouvre le carrousel, elle ne dort pas en slide 2.
- **Un avant/après ne parle que si les deux côtés traitent la même chose.** Deux textes sur des sujets différents font comparer deux idées et le mécanisme reste invisible. Affiche aussi la demande qui a produit les deux versions.
- **Le contraste de traitement remplace l'étiquette** : côté « sans » terne dans un cadre gris, côté « avec » net, à l'accent. On voit lequel est bon avant de lire. Ne jamais surligner une erreur avec la couleur d'accent.
- **Aucun tiret cadratin sur un visuel, même cité en contre-exemple** : une capture isolée de la slide le lirait comme une faute.
- **Le nombre de slides n'est pas un objectif.** Une slide qui ne porte pas sa propre idée sort.
- **Chiffres tiers confirmés avant la mise en page.** Tout chiffre qui ne vient pas de la personne ou d'une source vérifiée se valide avant de composer.
- **Zone de sécurité basse (160 px) revérifiée après chaque ajout** à une slide déjà composée.
- **Fondus : un calque de dégradé, jamais `mask-image`.** Un masque CSS s'affiche dans Chromium mais disparaît ou se décale selon le lecteur PDF. Pose une `div` en `position:absolute` avec `background:linear-gradient(...)` de la couleur du fond.
- **Avatar rond : pré-rendre le cercle dans l'image** (PIL, suréchantillonnage ×4 puis réduction LANCZOS), jamais par `border-radius` sur un `img` (contour crénelé à l'export). La source doit faire au moins 2× la taille affichée : une photo de 400 px s'affiche à 200 px maximum. Jamais d'agrandissement par IA d'un visage réel (il invente des traits).
- **Texte en flux** : entoure les séparateurs `·` d'espaces (sinon la ligne ne se coupe pas et déborde) et lie les expressions de plusieurs mots par `&nbsp;`.

## Livrer un PDF rastérisé

Le PDF vectoriel de Playwright est propre, mais LinkedIn et les lecteurs PDF le re-rendent à basse résolution : courbes hachées, dégradés banalisés, halos coupés. Livre deux fichiers :

- `exports/<slug>.pdf` : vectoriel, la source qu'on ré-édite ;
- `exports/<slug>-hd.pdf` : **rastérisé, celui qu'on publie**.

```bash
cd outputs/carrousel-<slug>-<date>
mkdir -p hd && pdftoppm -png -r 192 exports/<slug>.pdf hd/page   # 2160 px de large
# recadrer chaque hd/page-*.png à 2160×2700 (pdftoppm arrondit à 2702), puis écrire index-hd.html
# (une <img src="hd/page-N.png"> par page) et repasser scripts/export-carousel-pdf.py dessus
# vers exports/<slug>-hd.pdf
```

`pdftoppm` vient de poppler (`brew install poppler` sur Mac). Le rastérisé pèse environ 4 fois plus, très en dessous de la limite LinkedIn de 100 Mo.

## Journalisation

Chaque carrousel : brief + HTML source + PDF export, tous dans `outputs/carrousel-<slug>-<date>/`. L'export (`export-carousel-pdf.py`) ajoute une ligne dans `outputs/registry.csv`. Mention IA : composition HTML d'assets existants → pas de mention. Si une scène ou une icône générée par IA est intégrée → selon `Mention « Visuel généré par IA »` de `profile/config.md`.

## Vérification (lire le PDF avant de livrer)

Collisions, texte tronqué, tailles sous le plancher mobile (32 px contenu / 26 px numéro-mention), corps ≥ 48 px, marges 80/120/160 respectées, accent unique, zéro eyebrow en capitales, signoff présent (si le style en porte un), pas d'emoji Unicode ni de tiret cadratin. Itérer en éditant le HTML, pas en repartant de zéro.

## Skills liées

- `carte-linkedin` : visuel single-image (hérite des tokens ci-dessus).
- `image-linkedin` : scène / icône générée IA.
- `my-viral-post` : le copy du post qui accompagne le carrousel.
