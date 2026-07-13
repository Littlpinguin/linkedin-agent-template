# Système de compositions — carrousels LinkedIn

Référentiel de mise en page pour les carrousels LinkedIn (portrait 1080×1350). Fondé sur les systèmes de grille des graphistes seniors (Josef Müller-Brockmann *Grid Systems*, *The Vignelli Canon*, style typographique suisse, canon de page de Tschichold) et sur les contraintes réelles de lisibilité mobile (WCAG + physique de l'écran). Source de vérité de mise en page pour `carrousel-linkedin` et, par héritage, `carte-linkedin`.

> **Principe fondateur.** Le « premium » ne vient pas d'un layout magique. Il vient de trois choses : une **grille constante**, l'**alternance disciplinée** des compositions (jamais deux slides voisines au même squelette), et l'**absence de tics IA**. La constance de la grille, plus que n'importe quel effet, produit la sensation « designé par un senior ».

> **Variables du profil (agnostique de marque).** Ce référentiel ne code aucune couleur ni police en dur. Partout où l'un ou l'autre est cité, il renvoie aux variables de `profile/config.md` et au style observé dans `profile/style-visuel.md` :
> - **couleur d'accent** — l'accent unique du profil (`--accent`) ;
> - **couleur de fond** — le fond du profil (`--paper` clair par défaut, `--dark` pour les slides sombres ponctuelles) ;
> - **couleur d'encre / texte** — le texte principal (`--ink`) ;
> - **couleur de métadonnée** — le texte secondaire / les sources (`--ink-soft`, ou une version douce de l'accent sur fond sombre) ;
> - **police display** — les titres (`--font-display`) ;
> - **police cursive d'accent** — si le profil en définit une ; sinon, l'accent se fait par la couleur, pas par une cursive.
>
> La **grille, l'échelle mobile-safe, les 8 compositions, le rythme et les tics bannis sont universels** : ils s'appliquent tels quels, quelle que soit la marque.

---

## 1. Grille de référence (posée une fois, valable pour toutes les slides)

- **Canvas** : 1080 × 1350 px (4:5 portrait).
- **Marges** : **80 px latéral · 120 px haut · 160 px bas** → bloc de contenu utile **920 × 1070 px** centré. Le bas à 160 px tient le contenu vital hors de la zone où LinkedIn superpose son compteur de slides et les réactions.
- **Colonnes** : 12 colonnes sur le bloc de 920 px, gouttières de 24 px (colonne ≈ 54 px). Une grille souple, pas une cage : elle sert à aligner, pas à remplir.
- **Point focal fort** : haut-droite, vers (720, 500) — nombre d'or / règle des tiers. On ancre l'élément-clé sur une intersection, **jamais au centre géométrique** (sauf slide de clôture).
- **Baseline** : trame de 9 px ; caler l'interligne du corps sur un multiple (≈ 63–72 px pour un corps à 48–52 px).
- **Fond** : suit le style du profil (`profile/style-visuel.md`). Par défaut clair (`--paper`), avec des slides sombres ponctuelles (`--dark`) pour le rythme. Varier les **nuances** d'un même registre d'une slide à l'autre (par ex. `--paper` / `--paper-2` / `--paper-3`, ou un dégradé radial subtil positionné différemment) plutôt que d'alterner clair↔sombre à chaque slide. Quel que soit le fond, la **bibliothèque d'illustrations line-art de la marque** doit garder un contraste franc avec lui.

## 2. Échelle typographique MOBILE-SAFE (non négociable)

Un canvas de 1080 px est réduit à ~390 px sur un téléphone : **taille perçue ≈ taille canvas × 0,36**. Un corps à 30 px ne fait donc que ~11 px à l'écran, illisible dans le feed. Barème plancher :

| Rôle | Plancher | Cible confort | ≈ écran (cible) |
|---|---|---|---|
| Hook hero (court, slide de couverture) | 110 px | **130–180 px** | 47–65 px |
| Titre de slide | 72 px | **88–110 px** | 32–40 px |
| Sous-titre | 52 px | **60–72 px** | 22–26 px |
| Corps / puce | **44 px** | **48–56 px** | 17–20 px |
| Légende / source | **28 px** | **32–36 px** | 11–13 px |
| Numéro de slide, mention légale | 26 px | 30 px | ~10 px |
| Chiffre-ancre (composition n°3) | 200 px | **240–330 px** | — |
| Interligne corps | 1,4 | 1,4–1,6 | — |
| Interligne titres / display | 1,0 | 1,05–1,15 | — |

Police : la **police display du profil** pour les titres et le chiffre-ancre (graisse SemiBold/Bold pour les titres, ExtraBold pour le display), la **police corps du profil** pour le corps et les légendes. La **police cursive d'accent** (si le profil en définit une) est réservée à **UN** mot-accent ou un chiffre-héros par slide, jamais un titre entier ; les **guillemets « » et marques de citation** peuvent aussi la porter. Graisse minimale du petit texte : 500 (une graisse fine casse à la compression JPEG du feed).

## 3. Couleur & contraste (WCAG, calculé sur le fond réel du profil)

Le principe est universel ; les valeurs se lisent dans le profil. Sur le fond choisi (`--paper` ou `--dark`) :

- **Corps** : viser un ratio de contraste **≥ 4,5:1** (WCAG 1.4.3, AA) contre le fond. **Grand texte** (titres, display) : **≥ 3:1**. Privilégier l'**encre** et l'**accent** du profil pour tout ce qui est hook, corps et chiffres — ce sont eux qui doivent passer le plus largement.
- **Métadonnée / source** : la couleur de métadonnée du profil reste lisible tant qu'elle passe le ratio ; ne jamais descendre en dessous.
- **Interdit : « griser » une légende pour la discrétiser** si ça la fait passer sous le ratio. Baisser plutôt la taille, ou réduire l'opacité de l'encre tout en restant au-dessus du seuil de contraste.
- **Un seul accent par slide.** Jamais une couleur d'accent différente d'une slide à l'autre : l'accent unique est la colonne vertébrale visuelle de la série.

## 4. Densité & lisibilité en 1 seconde

- **1 idée par slide.** Si deux idées → deux slides.
- **≤ 30 mots par slide** ; **6–8 lignes** de corps maximum.
- **Longueur de ligne 30–50 caractères** (garantie par la colonne à un corps ≥ 48 px ; si ça dépasse, réduire la colonne ou couper la slide).
- **Hook ≤ 12 mots**, lisible en < 1 s : c'est une audition de 2 secondes, l'algorithme tranche après.
- **Un seul point focal par slide**, obtenu par les 4 leviers de hiérarchie : taille, graisse, couleur, position.

---

## 5. Le répertoire des 8 compositions (à faire alterner)

Chaque composition = un squelette réutilisable ancré dans un principe. On les fait tourner ; **deux slides voisines ne partagent jamais le même squelette**.

### 1. Couverture cadrée — *canon de page (Tschichold / Van de Graaf)*
Titre display (130–180 px) **flush-left ancré en haut-gauche**, 2–4 lignes courtes, le mot-clé sur sa propre ligne. Un seul mot en cursive d'accent (si le profil en a une). Grand vide en bas (30–40 %). Illustration absente ou très discrète. **→ slide de couverture / hook.**

### 2. Champ 7/5 asymétrique — *grille suisse (Müller-Brockmann)*
**Titre en pleine largeur en haut** (78–110 px, 1–2 lignes) suivi d'une règle d'accent ; ne jamais enfermer le titre dans la colonne étroite, il se resserre en 3–4 lignes. En dessous, deux champs : illustration line-art d'un côté, liste de puces (corps 46–48 px) de l'autre, **côté alterné gauche↔droite d'une slide à l'autre**. C'est le cheval de bataille (60–70 % des slides de contenu). **→ une idée + un visuel.**

### 3. Ancre-nombre — *contraste d'échelle (Ruder / Gerstner)*
Chiffre géant ExtraBold (240–330 px, ou en cursive d'accent) posé au point focal, débordant volontairement la colonne. Légende 48 px accrochée à sa baseline. **→ stat, étape chiffrée, preuve.** (Un pourcentage, une note, une durée, un volume.)

### 4. Étapes numérotées — *module répété*
Numéro gros dans une colonne dédiée à gauche + titre d'étape + micro-description, **3 à 5 items au même gabarit**, interligne généreux. Le numéro porte du contenu séquentiel (≠ tic décoratif 01/02/03). **→ méthode, checklist, process.**

### 5. Comparaison 2 colonnes — *deux champs égaux, lecture horizontale*
Deux colonnes de largeur égale, en-têtes contrastés (« Sans » / « Avec »), items alignés **rangée par rangée** pour comparer d'un coup d'œil. Un titre pose l'axe. **→ opposition, avant/après, mythe/réalité.**

### 6. Citation pleine — *pull-quote + accent unique (Vignelli)*
Une phrase en display (88–128 px), 6–12 mots, un seul mot en cursive d'accent, énorme vide autour. Nuance de fond différente (plus profonde) pour marquer la respiration. **→ punchline, manifeste, respiration entre deux blocs denses.**

### 7. Hero illustration — *picture window*
Illustration en **grand et pleine opacité** (haut ou centre, elle domine), titre net en dessous. L'illustration est le sujet. **→ slide-clé, moment émotionnel.** (Ne jamais mettre l'illustration en filigrane derrière le texte : elle disparaît.)

### 8. Signoff / CTA — *symétrie de clôture*
Récap en 1 ligne + **une seule** action + signoff (si le style du profil en porte un : avatar + Prénom Nom + titre de signature). Le centrage symétrique, banni ailleurs, devient ici un signal de fin. **→ dernière slide uniquement.**

**Liants transverses :** un **pied constant** (site + éventuel compteur) verrouillé sur la même baseline, hors de la zone de danger basse. Option de **continuité** : un élément (trait, illustration) qui déborde d'une slide sur la suivante pour pousser au swipe (par touches, 1–2 fois max).

## 6. Rythme d'une séquence de 9 slides

Arc **Hook → Contexte → 3× Valeur → Preuve → Respiration → Signoff**. Exemple d'alternance vérifiée (aucune paire voisine au même squelette) :

| # | Rôle | Composition |
|---|---|---|
| 1 | Hook | Couverture cadrée |
| 2 | Contexte / chiffre | Ancre-nombre |
| 3 | Valeur 1 | Champ 7/5 (illus gauche) |
| 4 | Valeur-pivot | Comparaison 2 colonnes **ou** Hero illustration |
| 5 | Valeur 2 | Champ 7/5 (illus droite) |
| 6 | Valeur 3 | Étapes numérotées |
| 7 | Preuve / loi | Champ 7/5 (illus gauche) |
| 8 | Punchline | Citation pleine |
| 9 | Signoff | Signoff / CTA |

## 7. Tics « template IA / Canva » à bannir

Le tic **n°1** : **label en CAPITALES espacées au-dessus du titre** (le « kicker » / eyebrow répété). Interdit. Plier l'info dans le titre. Aussi :
- Tuile d'icône arrondie répétée au-dessus de chaque titre.
- Grille de cartes identiques ; cartes imbriquées.
- Centrage systématique de tout, sur toutes les slides.
- Marqueurs 01/02/03 en décoration (hors vraies étapes).
- Gradient violet→cyan ; glassmorphism/glow gratuit ; ombre noire portée sous les CTA (garder un éventuel glow d'accent, jamais l'ombre noire).
- Texte en dégradé ; métadonnée délavée sous le seuil de contraste ; un accent différent par slide.
- Texte qui touche les bords ; espacement monotone (même valeur partout).
- Hook générique (« 10 astuces pour… ») sans point de vue.
- Côté copie (rappel liste noire, voir `voice/anti-ai-writing-style.md`) : tiret cadratin, parallélisme négatif (« ce n'est pas X, c'est Y »), jargon de hype.

## 8. Checklist mobile (avant export)

1. Corps ≥ 48 px (jamais < 44) ; hook 130–180 px ; titres 88–110 px ; légendes ≥ 32 px.
2. Bloc 920 × 1070 centré (marges 80 / 120 / 160) ; rien de vital dehors.
3. Contraste : encre ou accent du profil sur le fond ; corps ≥ 4,5:1, grand texte ≥ 3:1 ; aucune métadonnée sous le seuil.
4. 1 idée + 1 point focal par slide ; ≤ 30 mots ; ≤ 6–8 lignes.
5. Longueur de ligne 30–50 caractères.
6. Deux slides voisines de compositions différentes.
7. Zéro eyebrow en capitales, zéro tic de la section 7.
8. Aucun point final sur titre/accroche/chute/CTA ; pas de tiret cadratin ; pas d'emoji Unicode.
9. Un seul accent ; illustrations line-art à pleine opacité (jamais en filigrane).
10. **Test réel** : ouvrir le PDF sur un téléphone, lire chaque slide **sans zoomer**.

---

## Sources

Müller-Brockmann, *Grid Systems in Graphic Design* · *The Vignelli Canon* (RIT) · style typographique suisse · canon de page Van de Graaf/Tschichold · grille composée Gerstner · WCAG 1.4.3 (W3C, WebAIM) · specs carrousel LinkedIn/mobile · principes de hiérarchie & de hook · littérature sur les tics de templates génératifs. La **grille, l'échelle mobile-safe et les 8 compositions** sont universelles ; seules les couleurs et polices se lisent dans `profile/config.md`.
