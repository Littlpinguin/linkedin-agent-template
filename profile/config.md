# Profil : variables de l'agent

STATUT: NON CONFIGURÉ
<!-- Passe ce marqueur à "STATUT: CONFIGURÉ" une fois l'onboarding terminé.
     Tant qu'il vaut NON CONFIGURÉ, l'agent lance la skill `onboarding` au démarrage
     (voir CLAUDE.md). Ce fichier est la source de vérité des variables non éditoriales :
     les skills le lisent pour le nom, la couleur d'accent, le titre de signature, les outils. -->

## Progression de l'onboarding
<!-- Cochée par la skill `onboarding` au fil des étapes. Une étape sautée reste décochée
     et porte « (sautée) ». Une relance reprend à la première case vide. -->
Version de l'onboarding : 2
Étape en cours : 1
- [ ] 1. Accueil et vérification de l'installation
- [ ] 2. Toi et ton activité
- [ ] 3. Tes anciens posts
- [ ] 4. Restitution de ta voix
- [ ] 5. Ta cible
- [ ] 6. Ton style visuel
- [ ] 7. Tes 3 photos
- [ ] 8. Génération d'images
- [ ] 9. Ta veille
- [ ] 10. Fin et premier post

## Identité
- Prénom :
- Nom :
- Titre de signature (titre LinkedIn) :
- URL du profil LinkedIn :
- Entreprise :
- Site web :

## Audience & objectifs
- Cible prioritaire :                 # résumé en une ligne, détail dans profile/cible.md
- Objectifs (reach / leads / autorité / recrutement…) :

## Identité visuelle
- Couleur d'accent (hex) :            # ex. #2D6CDF, accent unique
- Couleur d'accent claire (hex) :     # version douce de l'accent, pour les fonds
- Couleur encre / texte (hex) :       # défaut #1A1A2E
- Couleur papier / fond (hex) :       # défaut #FDFCFA
- Police display (titres) :           # nom de la famille (ou "système")
- Police corps (texte) :              # idem
- Logo (chemin) :                     # assets/marque/logos/… (facultatif)
- Style visuel (cadre, titres, signature) : voir profile/style-visuel.md

## Outils
- Environnement :                     # desktop | cli | cowork (détecté à l'étape 1)
- Récupération des posts :            # apify | export-linkedin | copier-coller
- Génération d'images :               # google | magnific | higgsfield | aucune
- Mention « Visuel généré par IA » :  oui   # oui | non ; le sidecar JSON trace l'usage de l'IA dans tous les cas
- Consentement visage :               # oui (date) ; sans oui, aucune image générée avec tes photos
- Photos de référence :               # face.jpg, nez-a-gauche.jpg, nez-a-droite.jpg (ou anciens noms)

## Garde-fous
- Sujets / angles interdits (au-delà de la liste anti-IA universelle) :
- Méthodes ou cadres tiers à toujours créditer (jamais s'approprier) :
- Contraintes (longueur de post, langue, ton, fréquence) :

## Références
- Voix complète : voice/identite-editoriale.md
- Recette gagnante (ce qui marche, chiffres à l'appui) : profile/recette.md
- Cible : profile/cible.md
- Veille : profile/veille.md
- Style visuel : profile/style-visuel.md
- Règles anti-IA (universelles) : voice/anti-ai-writing-style.md
- Hooks attestés : voice/bibliotheque-hooks-texte.md, voice/bibliotheque-hooks-visuels.md
