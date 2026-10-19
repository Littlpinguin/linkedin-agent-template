---
name: image-linkedin
description: Génère une image LinkedIn avec le visage de la personne : scène détournée d'une référence pop/geek/meme, portrait mis en situation, ou meme sur une prise de position. Passe par la voie choisie à l'onboarding (clé Google Nano Banana 2.1 via scripts/gen-image.py, ou connecteur Magnific / Higgsfield). À utiliser quand elle demande "une image détournée", "un meme", "un visuel IA avec ma tête", "mets-moi en scène", "détourne telle référence", pour accompagner un post. Pour une carte/infographie texte → carte-linkedin. Pour un carrousel → carrousel-linkedin.
---

# image-linkedin : la personne en scène, image IA détournée ou meme

Tu génères une image pour un post LinkedIn, avec le vrai visage de la personne. Deux usages : une **scène détournée** (une référence pop, geek ou memesque revisitée, la personne dans un rôle) ou un **meme** sur une prise de position. **Règle : jamais de requête brute.** Chaque prompt suit la doctrine ci-dessous, et chaque génération est journalisée.

## Avant tout : vérifier la voie, le consentement, les photos

Lis `profile/config.md`, section `## Outils` :

- **`Génération d'images` vide** (agent configuré avant cette ligne) : si `GOOGLE_AI_API_KEY` est rempli dans `.env` (vérifie avec `grep -c '^GOOGLE_AI_API_KEY=.' .env`, qui n'affiche jamais la clé), prends la voie `google` et propose de noter le choix ; sinon, traite-la comme `aucune`.
- **`Génération d'images : aucune`** : ne génère rien. Dis-le en une ligne, propose une carte ou un carrousel à la place (`carte-linkedin`, `carrousel-linkedin`), et rappelle que l'étape 8 de l'onboarding se rejoue avec « configure la génération d'images ».
- **`Consentement visage`** qui ne commence pas par `oui` : demande le consentement avant toute image avec ses photos, et note la réponse.
- **Photos** : `assets/moi/face.jpg`, `nez-a-gauche.jpg`, `nez-a-droite.jpg` (`.jpeg` et `.png` acceptés). Si elles manquent mais que d'anciens noms existent (`visage-1.jpeg`, `visage-1.png`…), utilise-les et propose de les renommer. S'il n'y a aucune photo, dis-le et propose soit d'en déposer, soit une scène sans visage.
- **Génération payante** : chaque image coûte quelques centimes (Google) ou des crédits (connecteur). Annonce-le avant la première génération de la session et attends un accord. Les éditions suivantes de la même image n'ont pas besoin d'un nouvel accord.

## Doctrine de marque (personal branding pur)

- **La personne est le sujet.** Son visage porte l'image.
- Le **ton** est le sien : second degré, référence culturelle assumée, jamais corporate (voir `voice/identite-editoriale.md` et `assets/visuels-generes/`, pour s'en inspirer sans copier).
- Le **traitement visuel** suit `profile/style-visuel.md` (photo, illustration ou meme, mood, contraste).
- **Un seul accent** (la couleur de `profile/config.md`) si un élément graphique coloré est ajouté. Pas de personnage compagnon ni de marque secondaire.
- L'humour vient de la **posture, de l'accessoire et de la mise en scène**, jamais d'une caricature du visage.

## Méthode

On ne génère rien sans brief. Récupère via l'outil de questions : le post ou la prise de position à illustrer, la référence à détourner (ou propose des idées), le rôle de la personne dans la scène.

1. Propose 2 à 3 concepts distincts (référence détournée + rôle + punchline éventuelle).
2. Elle choisit.
3. Écris le prompt selon le template, génère par la voie configurée, **lis l'image**, itère par édition.

## Choisir la photo de référence selon le cadrage

Le modèle copie l'angle du visage qu'il voit. Choisis l'Image 1 d'après l'orientation de la personne dans la scène :

| Dans la scène, la personne… | Image 1 | Image 2 (facultative) |
|---|---|---|
| fait face au lecteur, regarde la caméra | `face.jpg` | un profil |
| regarde ou avance vers la gauche du cadre | `nez-a-gauche.jpg` | `face.jpg` |
| regarde ou avance vers la droite du cadre | `nez-a-droite.jpg` | `face.jpg` |
| est vue de trois quarts | le profil du bon côté | `face.jpg` |

**Corriger la référence bat corriger le prompt.** Un selfie pris à bout de bras élargit le visage (effet grand-angle) et le modèle l'extrapole au corps entier dans un plan large. Si le rendu épaissit la personne, change de photo de référence avant de toucher au prompt. Recadrer une photo est permis, l'étirer ou la compresser jamais.

**Une génération validée par la personne** est souvent une meilleure référence d'identité qu'un selfie : réutilise-la en Image 1 pour les scènes suivantes du même style.

## Règle dure : ne jamais décrire le visage dans le prompt

Ni traits, ni barbe, ni cheveux, ni lunettes, ni morphologie. Les images de référence font tout le travail, le prompt les désigne seulement :

> « Photo réaliste de la personne dont le visage, les cheveux, la pilosité, les lunettes et la silhouette sont exactement ceux des images de référence fournies. Reproduire ces images fidèlement, sans les réinterpréter. »

Une description textuelle entre en concurrence avec la photo et gagne : le modèle exagère chaque trait nommé. Seule exception : si la personne a changé de coiffure depuis ses photos et n'en a pas de récente, nomme les cheveux, et seulement eux. Mieux : demande une photo récente.

## Doctrine de prompting (Nano Banana 2.1, valable aussi pour les connecteurs)

1. **Ouvre sur une phrase qui fusionne le medium et la référence** (« Photo réaliste de la personne de l'Image 1… »). Une description de style abstraite avant la référence fait dériver le rendu.
2. **Langage naturel**, en phrases complètes, avec une hiérarchie d'importance. Pas de soupe de mots-clés.
3. **Identity Lock** : « Conserve exactement identiques à l'Image 1 le visage, la coupe de cheveux, la pilosité et le teint. »
4. **Optique, toujours** : « Photographié au téléobjectif 85 mm, depuis environ 2,5 mètres. Proportions naturelles, sans effet grand-angle. » Plus de l'air au-dessus de la tête et autour des épaules. Sans cette consigne, la perspective écrase le visage.
5. **Taille du visage** : dès que le visage doit être reconnaissable, cadrage plan américain (mi-cuisses) ou plus serré, « le visage occupe nettement le tiers supérieur de l'image », « mise au point sur les yeux, yeux symétriques, texture de peau réelle », et `--size 2K` (voie Google). En 1K, un plan en pied laisse environ 70 pixels au visage et le rendu fait « vieille IA ». Une retouche ne rattrape pas un visage trop petit : régénère.
6. **Composition en rapports, pas en hauteurs** : « le bord de la feuille effleure le bas du menton », « visage et objet forment un seul bloc ». « À hauteur de poitrine » place l'objet trop bas.
7. **Négations reformulées en positif** (« scène extérieure » plutôt que « pas de bureau »). Exception : les clichés d'IA (dégradé violet néon, robot, cerveau-circuit) s'excluent explicitement.
8. **Style en prose**, hex codes permis. **Format en dernier** (ratio, résolution, cadrage, fond).
9. **Texte dans l'image** : jusqu'à 3-4 mots en capitales sur un objet (couverture, panneau), le modèle les rend nets. Au-delà, ou en casse mixte, exige « aucune écriture nulle part » et compose le texte en HTML avec `carte-linkedin`.

## Template de prompt

```
[OUVERTURE]
<Medium> de la personne de l'Image 1, dont le visage, les cheveux, la pilosité, les lunettes
et la silhouette sont exactement ceux des images de référence. Reproduire fidèlement.

[CONTEXTE]
Image pour un post LinkedIn. Sujet du post : <…>. Détournement de : <référence>.

[SCÈNE]
<La scène, formulée positivement. Rôle et geste de la personne. Rapports entre les éléments.>

[STYLE]
<Paragraphe : rendu, ambiance, lumière, palette selon profile/style-visuel.md.>

[OPTIQUE ET FORMAT]
Téléobjectif 85 mm, environ 2,5 m, proportions naturelles. Le visage occupe le tiers supérieur.
Ratio <4:5 portrait feed | 1:1 | 16:9>. <Fond, lisibilité en miniature.>
```

## Générer selon la voie

**Voie `google`** (clé `GOOGLE_AI_API_KEY` dans `.env`, `pip install requests`) :

```bash
python3 scripts/gen-image.py --slug <slug> \
  --prompt-file outputs/images/prompts/AAAA-MM-JJ-<slug>.txt \
  --ref assets/moi/face.jpg assets/moi/nez-a-droite.jpg \
  --aspect 4:5 --size 2K
```

Sortie : `outputs/images/AAAA-MM-JJ-<slug>.png` + sidecar `.json` + une ligne dans `outputs/registry.csv`. Écris toujours le prompt dans le `.txt` avant de lancer.

**Voie `magnific` ou `higgsfield`** (connecteur branché à Claude) : cherche l'outil de génération d'images du connecteur dans la session (recherche d'outils par mot-clé, par exemple « image generate »). Envoie le même prompt et les mêmes photos de référence, choisis un modèle qui accepte des images de référence, puis enregistre le résultat dans `outputs/images/AAAA-MM-JJ-<slug>.png`. Écris le prompt dans `outputs/images/prompts/` et journalise toi-même :

```bash
python3 scripts/journal.py --kind image --slug <slug> --output outputs/images/AAAA-MM-JJ-<slug>.png \
  --source outputs/images/prompts/AAAA-MM-JJ-<slug>.txt --model "<connecteur : modèle>" \
  --refs "assets/moi/face.jpg" --ai-disclosure oui --status brut
```

Si le connecteur n'apparaît pas dans la session, dis-le : il faut l'ajouter dans les réglages de Claude (Connecteurs), puis ouvrir une nouvelle session.

**Édition** (toutes voies) : repasse l'image produite en Image 1 avec « garde tout identique à l'Image 1, change seulement <…> ». Ça marche pour une retouche locale (effacer un logo, changer un objet). Pour changer le cadrage ou la composition, réécris le prompt et régénère : l'édition ne recompose pas un plan.

## Pièges connus

- **Faux logos sur les appareils** (ordinateur, téléphone) : le modèle en grave même quand on demande un appareil générique. Prévois une passe d'édition « efface tout logo et toute inscription sur l'appareil » et zoome sur les tranches avant de livrer.
- **Sujet recentré malgré la consigne** (« la personne occupe la moitié droite ») : rattrape-le à la composition dans `carte-linkedin` (image agrandie à 110-120 %, décalée, bord fondu par un dégradé, fond de carte assorti au bord de l'image) plutôt que de régénérer.

## Vérification (lire l'image avant de livrer)

- C'est bien le visage de la personne, pas un sosie, et la silhouette n'est pas épaissie.
- Visage net et assez grand, yeux symétriques.
- Pas de faux logo, pas de charabia dans le décor, orthographe exacte du texte demandé.
- Ratio correct, lisible en miniature dans le fil.
- Pas de cliché d'IA involontaire.

## Garde-fous

- **Visage réel = celui de la personne, avec son consentement.** Aucune autre personne réelle sans accord.
- **Détournement = clin d'œil, pas copie.** Évoque une référence sans reproduire un personnage protégé, un logo de marque tierce, ou le style signé d'un artiste vivant nommé.
- **Logos tiers** : jamais fabriqués par IA, jamais scrapés. Demander les fichiers officiels.
- **Jamais de faux document** (fausse capture, faux graphique de données, fausse preuve client) publié comme authentique.

## Mention IA

Selon `Mention « Visuel généré par IA »` dans `profile/config.md` : `oui` (défaut), rappelle de l'ajouter en légende du post ; `non`, ne la propose pas. Dans tous les cas, le sidecar et le registre gardent `ai_disclosure` pour la traçabilité.

## Skills liées

- `carte-linkedin` : texte net par-dessus, carte ou infographie.
- `carrousel-linkedin` : page de garde avec la personne en scène.
- `my-viral-post` : le post qui accompagne le visuel.
