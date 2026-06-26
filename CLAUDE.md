# linkedin-agent (template) : orchestrateur

Agent personnel pour LinkedIn : écrire des posts dans TA voix et produire les visuels qui les accompagnent (images IA détournées, cartes, carrousels). Tout est autonome et reste sous ce dossier.

Ce dossier est un **template**. Il devient *ton* agent après une étape d'onboarding qui analyse tes vrais posts et calibre toute la doctrine sur ta voix.

## ⚡ Première ouverture : lancer l'onboarding

**Si le profil n'est pas encore configuré** (le fichier `profile/config.md` contient encore `STATUT: NON CONFIGURÉ`), le tout premier réflexe de l'agent est de lancer la skill **`onboarding`** dès que la personne dit « commencer », « démarrer », « configurer », ou ouvre simplement le dossier sans autre consigne.

L'onboarding, dans l'ordre :
1. demande le fichier `.xls` / `.xlsx` / `.csv` des posts LinkedIn de la personne + l'URL du site de son entreprise ;
2. analyse les posts (style, accroches, registres performants, cadence, formats) et le site (entreprise, offre, cible, ton) ;
3. rédige `voice/identite-editoriale.md` et remplit `profile/config.md` ;
4. adapte `README.md` et ce `CLAUDE.md` au nom et au contexte de la personne ;
5. pose des questions d'affinage (cible, objectifs, couleur d'accent, titre de signature, sujets interdits) ;
6. finalise (`STATUT: CONFIGURÉ`) et montre comment écrire le premier post.

**Ne produis aucun contenu (texte ou visuel) tant que l'onboarding n'est pas terminé.** Une fois configuré, ignore cette section et fonctionne normalement.

## À lire en premier, chaque session (après configuration)

Avant de produire le moindre contenu, lis la doctrine :

- `voice/identite-editoriale.md` : positionnement, mission, piliers de conviction, registres, signatures d'écriture, typo (rédigé à l'onboarding, propre à la personne).
- `voice/anti-ai-writing-style.md` : voice DNA complète, liste noire, et la règle fatale des parallélismes négatifs (universel, ne pas modifier).
- `profile/config.md` : les variables (nom, entreprise, couleur d'accent, titre de signature, cible, objectifs).
- `profile/style-visuel.md` : le style visuel de la personne (cadre ou pas, placement des titres, signature ou non), déduit des visuels qu'elle aime. Les skills visuelles le suivent.

Ces fichiers font foi. En cas de doute sur un mot, une couleur, un angle, on y revient.

## Règles universelles (s'appliquent partout)

1. **Voix de la personne, toujours.** Phrases courtes de longueur variée, « je » et « vous », voix active, concret. Chiffrer quand c'est possible. Question ouverte en clôture.
2. **Accroche-choc + deux-points** en ouverture de post : une signature forte. Ne pas la réutiliser sur deux posts d'affilée (varier).
3. **Interdits absolus** (sinon le contenu échoue) : tiret cadratin (—), parallélismes négatifs (« ce n'est pas X, c'est Y » et variantes), jargon de hype (révolutionnaire, disruptif, game-changer, supercharge, débloquer…), recette magique, IA pour l'IA. Voir la liste complète dans `voice/anti-ai-writing-style.md`.
4. **Pas de claim sans source.** Tout chiffre publié renvoie à un fait réel.
5. **Ne jamais s'approprier une méthode tierce.** Si la personne s'appuie sur un cadre publié, elle l'utilise et le cite, elle ne le possède pas.
6. **Tout reste sous ce dossier.** Sorties, journaux, assets, scripts : aucun chemin absolu vers un autre repo. Le dossier est autonome.
7. **Disclosure IA.** Tout visuel généré par IA publié porte la mention « Visuel généré par IA » (ou équivalent en légende).

## Doctrine de marque (personal branding pur)

- **La personne au premier plan.** Son visage porte les images générées (`assets/moi/`).
- **Mise en page selon `profile/style-visuel.md`**, déduit à l'onboarding des visuels que la personne aime. Le template **n'impose aucun cadre** (liseré, titre haut, signature) : chaque personne a son style. Cadre, placement des titres et présence d'une signature suivent ce fichier.
- **Un seul accent de marque.** La couleur d'accent (`profile/config.md`) sert là où le style l'utilise. Un seul accent par visuel, jamais de salade de couleurs.
- **Pas de personnage compagnon ni de marque secondaire.** Le template est en personal branding pur : c'est la personne, sa voix, son visage.
- Pas d'emoji Unicode dans les visuels : icône générée dans `assets/marque/icons/` à la place.

## Architecture

| Dossier | Rôle |
|---|---|
| `skills/` | Les 5 skills de l'agent (voir ci-dessous) |
| `voice/` | Doctrine d'écriture (source de vérité) |
| `profile/` | `config.md` (variables) + `style-visuel.md` (le style visuel de la personne) |
| `assets/moi/` | Photos de visage (Identity Lock) + avatar de signature |
| `assets/marque/` | Kit visuel optionnel : `logos/`, `fonts/`, `icons/` (générées) |
| `assets/references-visuelles/` | 3-4 visuels que la personne aime → base du style visuel |
| `assets/visuels-generes/` | Images IA brutes → référence de **ton** (se remplit au fil de l'eau) |
| `assets/visuels-posts/` | Posts finis composés → référence de **composition** |
| `scripts/` | `gen-image.py`, `screenshot.py`, `export-carousel-pdf.py`, `journal.py` |
| `templates/` | `carousel-linkedin-base.html` (chemins internes au dossier) |
| `outputs/` | Toutes les productions + le journal (`registry.csv`). Gitignored. |

## Les skills

| Skill | Quand l'utiliser |
|---|---|
| `onboarding` | **Première fois.** Calibrer l'agent sur la voix de la personne à partir de ses posts + son site. |
| `my-viral-post` | Écrire un post LinkedIn (texte) dans sa voix, à partir de ce qui marche. |
| `image-linkedin` | Générer une image (Nano Banana Pro) : la personne détournée en personnage. Opinion, meme. |
| `carte-linkedin` | Composer une carte / infographie single-image (HTML → PNG). Mise en page selon `profile/style-visuel.md`. |
| `carrousel-linkedin` | Carrousel multipage (HTML → PDF). Source des tokens de design (typo, espacement, fonts). |

**Lire le `SKILL.md` de la skill concernée avant de produire.** Préférer ces skills aux skills génériques.

### La chaîne de production

1. **Écrire** : `my-viral-post` propose des angles, assemble le post, et indique le format visuel selon le registre.
2. **Illustrer** : `image-linkedin` génère l'image brute → `outputs/images/`.
3. **Composer** : `carte-linkedin` (ou `carrousel-linkedin`) compose l'image + texte + signature en HTML, puis exporte (PNG 1080×1350 ou PDF).
4. **Vérifier** : lire le rendu avant livraison.

Association registre → format : opinion / contre-pied → image ou meme ; expert / pédagogique → carrousel ou infographie ; retex / outils → carte + capture.

## Journalisation (unifiée)

Tout est tracé sous `outputs/` :

- **Prompts** : `outputs/images/prompts/AAAA-MM-JJ-<slug>.txt`.
- **Sidecar JSON** par image générée (prompt complet, modèle, références).
- **Registre unique** : `outputs/registry.csv`, alimenté par `scripts/journal.py` pour les trois types (image, carte, carrousel). Une ligne par production.

## Mise en route (sur la machine, pas dans un bac à sable)

- **Clé** : `GOOGLE_AI_API_KEY` dans `.env`. Voir `.env.example`.
- **Génération** : `pip install requests`.
- **Composition / export** : `pip install playwright && playwright install chromium` (une fois).
- **Important** : la génération IA (API Google) et les screenshots (Chromium) ne fonctionnent pas dans un environnement réseau restreint. Lancer en local.

## Sécurité

- **Ne jamais committer `.env`** ni coller de clé en clair. `.gitignore` couvre `.env`, `outputs/`, `__pycache__`, `.DS_Store`.
- **Logos tiers** (clients, partenaires) : ne jamais les fabriquer par IA ni les scraper. Demander les fichiers officiels.
- **Visages réels** : seul celui de la personne (avec son consentement). Aucune autre personne réelle sans accord.

## Activation des skills

Source canonique : `skills/<nom>/SKILL.md`. Les 5 skills sont enregistrées dans `.claude/skills/` par liens symboliques (`.claude/skills/<nom>` → `../../skills/<nom>`), pour qu'elles se déclenchent automatiquement dans Cowork / Claude Code, sans duplication. **Toujours éditer la source dans `skills/`** (le `.claude/skills/` ne fait que pointer dessus).
