---
name: my-viral-post
description: Rédige un nouveau post LinkedIn dans la voix de la personne, à partir de ce qui marche déjà pour elle (son identité éditoriale calibrée à l'onboarding + sa voice DNA). Déclencher dès qu'elle veut écrire un post : "écris-moi un post LinkedIn", "donne-moi des angles pour un post", "aide-moi à poster cette semaine". La skill demande d'abord la matière via l'outil de questions, propose plusieurs angles/accroches au choix, assemble le post complet dans sa voix, et indique le format visuel à associer.
---

# my-viral-post : écrire un post dans ta voix

Écris un nouveau post LinkedIn qui colle au style le plus performant de la personne. Cette skill s'appuie sur son identité éditoriale (rédigée à l'onboarding à partir de ses vrais posts) et sa voice DNA. Elle reflète ce qui marche pour **elle**, pas des conseils LinkedIn génériques.

Lis d'abord, ils font foi :
- `voice/identite-editoriale.md` : positionnement, mission, piliers, registres classés par performance, signatures d'écriture, typo.
- `voice/anti-ai-writing-style.md` : voice DNA complète, liste noire, règle fatale des parallélismes négatifs.
- `profile/config.md` : cible, objectifs, contraintes, garde-fous.

## Méthode

On ne peut pas écrire à la place de la personne sans sa matière. Dès l'invocation, utilise l'outil de questions pour récupérer le brut avant de générer.

1. Propose plusieurs angles/accroches distincts (5 par défaut, plus sur demande), chacun ancré dans un de ses registres qui marchent (voir son identité éditoriale).
2. Laisse-la choisir le ou les angles.
3. Assemble le post complet : l'angle choisi, la caption entière écrite dans sa voix et sa cadence, plus une direction claire sur le média (image / carte / carrousel) à associer.
4. Termine par des prochaines étapes concrètes pour l'améliorer encore.

## Ce qu'il faut demander (via l'outil de questions)

- le sujet ou l'actu, et le registre visé ;
- l'histoire / la donnée / l'exemple concret qu'elle apporte (le vécu que le modèle ne peut pas inventer : une mission, un client nommé, un chiffre réel, un déclic) ;
- l'objectif du post (reach, leads, autorité, recrutement) ;
- toute contrainte (longueur, format, deadline).

Demande avant de générer. Jamais de post générique à froid.

## Sa recette gagnante

Elle vit dans `voice/identite-editoriale.md` : registres classés par performance, accroches qui marchent, exemples de ses propres outliers. Appuie-toi dessus, ne réinvente pas une recette LinkedIn générique.

Structure qui marche presque toujours :
- **Le texte porte le post.** Un visuel faible ne rattrape pas un angle faible ; un bon angle se suffit souvent en texte pur.
- **Accroche forte en ouverture** (souvent une affirmation qui dérange + deux-points qui promet la démonstration), puis la démonstration.
- Paragraphes d'1 à 2 phrases, 3 max. Rythme cassé, phrases courtes mêlées à des plus longues.
- « Je » et « vous », adresse directe, voix active, contractions.
- **Chiffrer systématiquement** (chiffres en chiffres). Un chiffre vaut mieux qu'un adjectif.
- Phrases courtes qui martèlent en clôture de paragraphe.
- Vécu ancré : missions, clients nommés, déclics réels.
- **Question ouverte à la communauté en clôture.**

Association registre → format :
- opinion / contre-pied → texte seul, ou image / meme pour incarner ;
- expert / pédagogique → carrousel ou infographie (objectif enregistrement) ;
- retex / outils → texte + capture ou photo de terrain.

## Règles de voix (rappel non négociable)

Colle exactement à sa voix, telle que capturée dans `voice/identite-editoriale.md` et `voice/anti-ai-writing-style.md`. Interdits absolus (sinon le post échoue) :
- **Parallélismes négatifs et reframes** (« ce n'est pas X, c'est Y », « X est mort, Y est l'avenir »). Le tic IA numéro un. Dis directement ce que c'est, supprime tout ce qui précède l'affirmation positive.
- Tirets cadratins.
- Jargon de hype (révolutionnaire, disruptif, game-changer, supercharge, débloquer, seamless, leverage…).
- Promettre une recette magique. Toujours une méthode, des étapes, des conditions.
- Parler de l'IA pour l'IA. Toujours rattacher à l'humain, l'usage, le résultat.
- S'approprier une méthode tierce : la citer, jamais la posséder (voir garde-fous dans `profile/config.md`).

## Garde-fou honnête

Ne répète pas une seule recette virale en boucle. Reprends les patterns gagnants, varie l'exécution, et signale quand un brouillon s'appuie trop sur une formule déjà utilisée récemment (par exemple l'accroche-deux-points sur deux posts d'affilée).

## Skills liées

- `image-linkedin` : image détournée / meme à associer.
- `carte-linkedin` : carte ou infographie single-image.
- `carrousel-linkedin` : carrousel multipage.
