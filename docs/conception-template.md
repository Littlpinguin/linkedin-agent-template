# Note de conception : linkedin-agent (template)

Document pour qui maintient ou fait évoluer ce template. Les utilisateurs finaux n'ont pas besoin de le lire : ils disent « commencer » et suivent l'onboarding.

## But

Rendre réutilisable un agent LinkedIn personnel (écrire des posts dans une voix + produire les visuels). Le template embarque tout le moteur, mais ne contient aucune donnée d'une personne en particulier : il se calibre, à la première ouverture, sur les vrais posts et le site de la personne qui l'ouvre.

## Architecture retenue

**Hybride : moteur générique + onboarding qui personnalise.**

- Le **moteur** (scripts, template HTML, règles anti-IA, structure) est livré générique et stable.
- La **personnalisation** vit dans deux fichiers, source de vérité lue par les skills :
  - `voice/identite-editoriale.md` : la voix (rédigée à l'onboarding).
  - `profile/config.md` : les variables (nom, entreprise, couleur d'accent, titre de signature, cible, objectifs, fonts).
- Les **skills** restent génériques et lisent ces deux fichiers, plutôt que d'être réécrites en dur à chaque onboarding. Avantage : un onboarding raté ne casse jamais le moteur, et on peut re-calibrer plus tard sans rien réinstaller. L'onboarding personnalise aussi la **surface** (README, intro du CLAUDE) au nom de la personne.

## Déclencheur d'onboarding

`profile/config.md` porte un marqueur `STATUT: NON CONFIGURÉ`. Tant qu'il vaut ça, `CLAUDE.md` demande à l'agent de lancer la skill `onboarding` dès la première sollicitation (« commencer », « démarrer », ouverture sans consigne). L'onboarding finit par passer le marqueur à `CONFIGURÉ`, ce qui rend la section inerte.

Flux d'onboarding : demander le `.xls` des posts + l'URL du site → analyser style + contexte → rédiger l'identité éditoriale + remplir la config → adapter README/CLAUDE → questions d'affinage → finaliser.

## Décisions structurantes

1. **Profil complet** : l'onboarding configure voix + business + identité visuelle.
2. **Personal branding pur** : pas de marque secondaire ni de personnage compagnon (différence majeure avec l'agent source, qui portait une marque secondaire omniprésente). Le visage de la personne porte les images ; un seul accent de marque, paramétrable.
3. **Assets vidés + READMEs guidés** : aucune photo ni asset d'une personne tierce. Les dossiers d'assets expliquent quoi déposer.
4. **Fonts** : pas de redistribution de polices payantes. Défaut = polices système ; la personne dépose ses `.woff2` dans `assets/marque/fonts/` si elle veut un rendu pixel-perfect.
5. **Aucun cadre visuel imposé** : le template ne force ni liseré, ni titre haut, ni signature. L'onboarding demande 3-4 visuels que la personne aime (`assets/references-visuelles/`), en déduit son style et l'écrit dans `profile/style-visuel.md`. Les skills visuelles (`carte-linkedin`, `carrousel-linkedin`, `image-linkedin`) lisent ce fichier et suivent ce style ; les anciens éléments de cadre deviennent des options, pas des mandats. But : éviter que tous les utilisateurs sortent les mêmes visuels.

## Ce qui est générique (réutilisé du moteur source)

- `scripts/` : `gen-image.py`, `screenshot.py`, `export-carousel-pdf.py`, `journal.py` (une seule référence de marque retouchée dans `gen-image.py`).
- `voice/anti-ai-writing-style.md` : règles anti-IA universelles, inchangées.
- L'échelle typographique et l'échelle d'espacement du carrousel (tokens de design).

## Ce qui a été régénéré en générique

- Les 5 `SKILL.md` (onboarding nouvelle ; les 4 autres dé-spécialisées, sans nom propre ni marque secondaire).
- `templates/carousel-linkedin-base.html` : palette neutre + accent paramétrable, fonts système avec bloc `@font-face` de marque optionnel, signoff générique.
- `CLAUDE.md`, `README.md`, `voice/identite-editoriale.md` (gabarit), `profile/config.md`, `.env.example`.

## Limites connues / pistes

- L'échelle typo (168 px de hook) est calibrée pour une police dense/condensée ; sans police de marque, raccourcir les titres ou ajouter une police.
- L'onboarding suppose un accès réseau (lecture du site via WebFetch) et la skill xlsx pour parser l'export. Tout cela tourne en local, pas en environnement réseau restreint.
- Re-calibrage : relancer la skill `onboarding` réécrit l'identité éditoriale et la config (les assets déposés sont conservés).

## Version 2 (octobre 2026)

- **Onboarding en 10 étapes, reprenable.** Progression tracée dans `profile/config.md` (`## Progression de l'onboarding`). Toute étape se saute sauf l'identité minimale. Trois voies par outil, dont une gratuite, limites dites.
- **Mise à niveau des agents v1.** `STATUT: CONFIGURÉ` sans section Progression déclenche un mode qui ne joue que les étapes nouvelles et déplace la recette vers `profile/recette.md`, sans réécrire l'identité éditoriale.
- **L'onboarding ne touche plus `README.md` ni `CLAUDE.md`.** Toute la personnalisation vit dans `profile/` et `voice/`, pour qu'un `git pull` des versions suivantes ne crée pas de conflit.
- **Récupération des posts pilotée** : `scripts/scrape-linkedin-posts.py` appelle l'acteur Apify `harvestapi/linkedin-profile-posts` (sans cookie), configurable par `APIFY_LINKEDIN_ACTOR`. Mapping tolérant des champs pour accepter d'autres acteurs. Le format de chaque post (`postImages`, `document`, `postVideo`, `article`, `repost`) et ses visuels sont tirés de la même réponse : les pages d'un carrousel viennent du manifeste d'images en plus haute résolution, car le PDF exposé est souvent tronqué. Le JSON brut est conservé, et `--dernier-lancement` relit le dernier dataset sans relancer l'acteur.
- **Nouveaux fichiers de profil** : `recette.md` (ce qui marche, chiffres à l'appui, séparé de l'identité éditoriale), `cible.md`, `veille.md`.
- **Veille** : skill `veille-contenu` (portée de la veille du studio d'origine, sans newsletter). Rapports et journal dans `veille/`, versionné, pour qu'une routine cloud retrouve sa mémoire. Annonce des veilles non lues en début de session.
- **3 photos aux noms fixes** (`face`, `nez-a-gauche`, `nez-a-droite`), choisies selon l'orientation du sujet dans la scène. `assets/moi/*` exclu de git.
- **Génération d'images par voie** : clé Google, connecteur (Magnific, Higgsfield) ou aucune. Lien de parrainage Magnific de l'auteur présenté comme tel.
- **Mention IA réglable** (défaut oui), traçabilité conservée dans le sidecar et le registre.
- **Leçons de production reportées** du studio d'origine : référence de visage choisie selon le cadrage, jamais de description du visage dans le prompt, optique 85 mm, 2K pour les visages, passe anti-logo, composition en rapports ; cadrage stratégique des carrousels, page de garde avec la personne, PDF rastérisé, fondus par calque ; registre à 5 statuts ; règle d'anaphore.
- **Hors périmètre, volontairement** : vidéo verticale, TikTok, Instagram, newsletter. Le template reste centré sur LinkedIn.
