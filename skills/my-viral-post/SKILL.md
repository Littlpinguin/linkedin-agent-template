---
name: my-viral-post
description: Rédige un nouveau post LinkedIn dans la voix de la personne, à partir de ce qui marche déjà pour elle (sa recette gagnante tirée de ses vrais posts, son identité éditoriale, sa cible, ses derniers posts validés, et les idées de sa veille). Déclencher dès qu'elle veut écrire un post : "écris-moi un post LinkedIn", "donne-moi des angles pour un post", "aide-moi à poster cette semaine", "on écrit le premier post", "développe l'idée n°2 de la veille". La skill demande d'abord la matière via l'outil de questions, propose plusieurs angles et accroches, assemble le post complet dans sa voix, indique le visuel à associer, et journalise le post validé.
---

# my-viral-post : écrire un post dans ta voix

Écris un nouveau post LinkedIn qui colle au style le plus performant de la personne. La skill s'appuie sur ce qui marche pour **elle**, chiffres à l'appui, tirés de ses propres posts.

## À lire d'abord (ils font foi)

- `profile/recette.md` : ce que disent ses chiffres, ses meilleurs formats, ses angles classés par performance, ses accroches qui marchent, sa cadence, ses outliers.
- `voice/identite-editoriale.md` : positionnement, mission, piliers, registres, signatures d'écriture, typo.
- `profile/cible.md` : pour qui elle écrit, le problème de sa cible, son vocabulaire, l'action attendue après lecture.
- `voice/anti-ai-writing-style.md` : voice DNA complète, liste noire, règle fatale des parallélismes négatifs.
- `voice/bibliotheque-hooks-texte.md` : les 10 familles de hooks attestés, leurs niveaux de preuve, les hooks à éviter.
- `profile/config.md` : objectifs, contraintes, garde-fous (sujets interdits, méthodes tierces à créditer).

**Référence de style prioritaire : les 5 derniers posts validés.** Ouvre `outputs/registry.csv`, garde les lignes `kind = post`, prends les 5 slugs les plus récents (la dernière ligne d'un slug fait foi) et lis leur `post.md` (texte final + « Notes de production »). Ces posts, avec les retouches de la personne, priment sur `profile/recette.md` en cas d'écart : ils captent son style le plus à jour.

**Repli** : si `profile/recette.md` ou `profile/cible.md` est encore un gabarit ou manque, dis-le en une ligne, travaille avec `voice/identite-editoriale.md`, et propose de rejouer l'étape correspondante de l'onboarding. Si la recette repose sur une base prudente (moins de 10 posts en tête de `profile/recette.md`) et que le registre compte depuis au moins 10 posts publiés, propose une fois « recalibre ma recette ».

## D'où vient le sujet

- **La veille d'abord.** Si `veille/` contient un rapport de moins de 14 jours, propose ses angles en premier (statut, fait, source datée, accroche candidate). Un angle déjà `publié` dans `veille/journal.md` ne se repropose pas.
- **Sinon, sa matière à elle** : une mission, un échange client, un chiffre, un déclic, une actu qui la fait réagir.

## Méthode

On ne peut pas écrire à la place de la personne sans sa matière. Dès l'invocation, utilise l'outil de questions pour récupérer le brut avant de générer.

1. Propose plusieurs angles et accroches distincts (5 par défaut), chacun ancré dans un registre qui marche pour elle (`profile/recette.md`) et une famille de hooks (`voice/bibliotheque-hooks-texte.md`).
2. Laisse-la choisir le ou les angles.
3. Assemble le post complet : l'angle choisi, la caption entière dans sa voix et sa cadence, le CTA (par défaut l'action de `profile/cible.md` § 5), plus une direction claire sur le visuel à associer (ce qu'il montre, à quoi il ressemble, quelle skill le produit).
4. Termine par des prochaines étapes concrètes pour l'améliorer encore.
5. **Dès qu'elle valide une version**, même après plusieurs itérations, journalise-la (section suivante). C'est systématique, sans attendre qu'elle le demande.

## Ce qu'il faut demander (via l'outil de questions)

- le sujet ou l'actu (ou l'angle de veille retenu), et le registre visé ;
- l'histoire, la donnée ou l'exemple concret qu'elle apporte (le vécu que le modèle ne peut pas inventer : une mission, un client nommé, un chiffre réel, un déclic) ;
- l'objectif du post (reach, leads, autorité, recrutement) ;
- toute contrainte (longueur, format, date de publication).

Demande avant de générer. Jamais de post générique à froid.

## Journalisation du post final

Chaque post validé est un actif de style : accroches qui marchent, structures écartées, formulations à garder ou à éviter.

1. Crée `outputs/post-<slug>-<date>/post.md` avec :
   - un en-tête (sujet, registre, objectif, angle retenu, visuel associé, source de veille éventuelle) ;
   - le texte final du post ;
   - une section « Notes de production » : les itérations écartées et pourquoi, les points de vigilance repérés (un tour de phrase proche d'un parallélisme négatif, corrigé), et ce qu'elle a retouché elle-même.
2. Journalise : `python3 scripts/journal.py --kind post --slug <slug> --output outputs/post-<slug>-<date>/post.md --refs "<sources citées>" --status validé --notes "<résumé en une ligne>"`.
3. Quand elle annonce l'avoir programmé ou publié, rejoue la commande avec le même slug et `--status programmé` ou `--status publié`. Si le sujet venait de la veille, passe aussi l'angle à `publié` dans `veille/journal.md` : c'est ce qui l'empêche de revenir. Si la veille tourne en routine cloud (`Voie` dans `profile/veille.md`), commite et pousse `veille/journal.md` pour que la routine le voie.

## La structure qui marche presque toujours

À ajuster selon `profile/recette.md`, qui prime :

- **Le texte porte le post.** Un visuel faible ne rattrape pas un angle faible ; un bon angle se suffit souvent en texte pur.
- **Accroche courte et spécifique** (moins de 40 caractères engage mieux sur LinkedIn), souvent une affirmation qui dérange + deux-points qui promet la démonstration. La question d'accroche sous-performe : garde la question pour la clôture.
- Paragraphes d'1 à 2 phrases, 3 max. Rythme cassé.
- « Je » et « vous », adresse directe, voix active.
- **Chiffrer**, chiffres en chiffres. Un chiffre vaut mieux qu'un adjectif.
- **Anaphore sur des lignes séparées** : une clause par ligne quand une structure se répète.
- Vécu ancré : missions, clients nommés (avec leur accord), déclics réels.
- **Le contexte logistique (événement, date, remerciements) va en fin de post**, au moment de la preuve ou du CTA, jamais en ouverture.
- **Annoncer une structure** quand le post a plusieurs points (« 3 choses reviennent toujours : »).
- **Pas de lien externe dans le corps** (LinkedIn le pénalise) : renvoyer au lien du profil ou au premier commentaire.
- **Tags** : le nom d'affichage LinkedIn exact de la personne taguée.
- **Question ouverte en clôture.**

Association registre → format :
- opinion / contre-pied → texte seul, ou image détournée / meme pour incarner (`image-linkedin`) ;
- expert / pédagogique → carrousel ou infographie, objectif enregistrement (`carrousel-linkedin`, `carte-linkedin`) ;
- retex / outils → texte + capture ou photo de terrain.

## Règles de voix (rappel non négociable)

Interdits absolus (sinon le post échoue) :
- **Parallélismes négatifs et reframes** (« ce n'est pas X, c'est Y », « non pas X mais Y », « X est mort, Y est l'avenir »). Le tic IA numéro un. Dis directement ce que c'est, supprime tout ce qui précède l'affirmation positive.
- Tirets cadratins.
- Jargon de hype : révolutionnaire, disruptif, game-changer, supercharge, débloquer, seamless, leverage, et toute la liste noire de `voice/anti-ai-writing-style.md`.
- Promettre une recette magique. Toujours une méthode, des étapes, des conditions.
- Parler de l'IA pour l'IA. Toujours rattacher à l'humain, l'usage, le résultat.
- S'approprier une méthode tierce : la citer, jamais la posséder (`profile/config.md`, garde-fous).
- **Pas de claim sans source** : tout chiffre publié renvoie à un fait réel, daté.

## Garde-fou honnête

Ne répète pas une seule recette virale en boucle. Reprends les patterns gagnants, varie l'exécution, et signale quand un brouillon réutilise une formule déjà employée sur l'un des 2 derniers posts validés (par exemple l'accroche-deux-points deux fois de suite).

## Skills liées

- `veille-contenu` : les angles de la semaine, sourcés et dédupliqués.
- `image-linkedin` : la personne en scène, image détournée ou meme.
- `carte-linkedin` : carte ou infographie single-image.
- `carrousel-linkedin` : carrousel multipage.
