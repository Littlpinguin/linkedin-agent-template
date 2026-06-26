---
name: image-linkedin
description: Génère une image LinkedIn via Gemini Nano Banana Pro : illustration détournée d'une référence pop/geek/meme avec le visage de la personne, ou meme sur une prise de position. À utiliser quand elle demande "une image détournée", "un meme", "un visuel IA avec ma tête", "détourne telle référence", pour accompagner un post. Pour une carte/infographie texte → carte-linkedin. Pour un carrousel → carrousel-linkedin.
---

# image-linkedin : image IA détournée + meme

Tu génères une image pour un post LinkedIn via Gemini Nano Banana Pro (`scripts/gen-image.py`). Deux usages : une **illustration détournée** (une référence pop/geek/memesque revisitée avec le visage de la personne) ou un **meme** sur une prise de position. **Règle : jamais de requête brute.** Chaque prompt suit la doctrine Nano Banana Pro ci-dessous, et chaque génération est journalisée.

## Doctrine de marque (personal branding pur)

- **La personne est le sujet.** Son visage porte l'image (Identity Lock sur `assets/moi/`).
- Le **ton** est le sien : second degré, référence culturelle assumée, jamais corporate (voir `voice/identite-editoriale.md` et l'inspiration de `assets/visuels-generes/`, sans copier).
- Le **traitement visuel** suit `profile/style-visuel.md` (photo vs illustration vs meme, mood, contraste). Reproduis ses goûts, n'impose pas un rendu type.
- **Un seul accent** (la couleur de `profile/config.md`) si un élément graphique coloré est ajouté. **Pas de personnage compagnon ni de marque secondaire** : c'est elle, point.

## Méthode

On ne génère rien sans brief. Dès l'invocation, utilise l'outil de questions pour récupérer : la prise de position ou le post à illustrer, la référence à détourner (ou propose des idées), le rôle voulu pour la personne dans la scène.

Ensuite :
1. Propose 2 à 3 concepts visuels distincts (référence détournée + rôle de la personne + punchline éventuelle).
2. Elle choisit.
3. Écris le prompt selon le template ci-dessous, lance `scripts/gen-image.py`, vérifie le rendu, itère par édition (pas en repartant de zéro).

## Doctrine de prompting Nano Banana Pro (non négociable)

1. **Langage naturel, pas de soupe de tags.** Briefe le modèle comme un illustrateur humain, en phrases complètes avec une hiérarchie d'importance.
2. **Identity Lock avec « Image 1 ».** Référence l'image par son numéro. « Utilise le visage de l'Image 1. Conserve EXACTEMENT identiques à l'Image 1 : (a) les traits du visage, (b) la coupe de cheveux, (c) la barbe si présente, (d) le teint. »
3. **« Keep X exactly. Change ONLY Y. »** Pour une variation d'une image existante, deux blocs explicites : ce qui ne change pas / la seule chose qui varie.
4. **Edit, don't re-roll.** Pour corriger (artefact, couleur, posture), repasse l'image existante en Image 1 + une courte instruction d'édition. Ne régénère pas de zéro.
5. **Style en prose.** Décris le style en paragraphe (brief d'illustrateur), pas en liste de « INTERDIT » en majuscules. Les hex codes sont permis.
6. **Format en dernier.** Aspect ratio, résolution, cadrage, fond : dans la dernière section (le modèle pondère plus les instructions de fin pour la technique).
7. **Négations reformulées en positif.** « scène urbaine extérieure » plutôt que « pas de bureau ». Exception : pour les tropes « IA » clichés (dégradé violet→néon, robot, cerveau-circuit), la négation explicite reste utile.
8. **Capacité de référence.** Jusqu'à 14 images réf, 6 en haute fidélité. Ici 1 à 3 : le(s) visage(s) de la personne depuis `assets/moi/` (+ éventuel mood de style).

## Template de prompt (à utiliser à chaque génération)

```
[CONTEXTE]
Image pour un post LinkedIn. Sujet du post : <…>. Détournement de : <référence>.

[STYLE]
<Paragraphe en prose : rendu illustratif ou photoréaliste selon le concept, ambiance,
références visuelles. Si meme : format meme reconnaissable, lisible en miniature.>

[RÉFÉRENCE]
Image 1 est le visage de la personne.

[IDENTITY LOCK : non négociable]
Utilise le visage de l'Image 1. Conserve EXACTEMENT identiques à l'Image 1 :
(a) les traits du visage, (b) la coupe de cheveux, (c) la barbe si présente, (d) le teint.

[CHANGEMENT / SCÈNE]
<La scène détournée, formulée positivement. Rôle de la personne dans la scène.>

[FORMAT]
Aspect ratio <1:1 carré feed / 4:5 portrait / 16:9>. <Cadrage, fond, lisibilité miniature.>
```

## Pipeline

Pré-vol : `GOOGLE_AI_API_KEY` rempli dans `.env` (voir `.env.example`), `requests` installé.

```bash
python3 scripts/gen-image.py \
  --slug <slug> \
  --prompt-file <chemin-du-prompt.txt> \
  --ref assets/moi/visage-1.jpeg \
  --aspect 4:5
```

Sortie : `outputs/images/AAAA-MM-JJ-<slug>.png` + sidecar `.json` (prompt complet) + une ligne dans `outputs/registry.csv`. Écris d'abord le prompt complet dans un `.txt`, puis lance le script.

Édition ciblée : relance `gen-image.py` en passant l'image produite en première `--ref` + un prompt court « garde tout identique à l'Image 1, change seulement <…> ».

## Vérification (lire l'image avant de livrer)

- Identité préservée : c'est bien le visage de la personne, pas un sosie.
- Aspect ratio correct, lisible en miniature dans le feed.
- Texte dans l'image (memes) : Gemini le rend imparfaitement. **Vérifie l'orthographe.** Si le texte doit être net, génère l'image sans texte et ajoute la punchline via `carte-linkedin` (HTML).
- Pas de trope « IA » cliché involontaire.

## Garde-fous

- **Visage réel = celui de la personne, avec son consentement.** Ne génère le visage d'aucune autre personne réelle sans accord.
- **Détournement = clin d'œil, pas copie.** Évoque une référence (ambiance, situation, cadrage) sans reproduire à l'identique un personnage protégé, un logo de marque tierce, ou le style signé d'un artiste vivant nommé. Parodie et pastiche, oui ; contrefaçon, non.
- **Logos tiers** : ne jamais les fabriquer par IA ni les scraper.

## Disclosure IA

Tout visuel généré par IA publié porte la mention « Visuel généré par IA » (ou équivalent en légende du post). La mention est aussi conservée dans le sidecar `.json` (`ai_disclosure`).

## Skills liées

- `carte-linkedin` : pour ajouter du texte net par-dessus, ou une carte/infographie.
- `carrousel-linkedin` : carrousel multipage.
- `my-viral-post` : le post qui accompagne le visuel.
