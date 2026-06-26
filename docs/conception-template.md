# Note de conception — linkedin-agent (template)

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
