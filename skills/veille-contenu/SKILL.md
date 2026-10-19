---
name: veille-contenu
description: Veille de contenu hebdomadaire multi-agents, calibrée sur la niche, les piliers et la cible de la personne (profile/veille.md, profile/cible.md, voice/identite-editoriale.md). Croise actus chaudes, signaux faibles, sources institutionnelles et écoute sociale sur les 14 derniers jours, avec un journal anti-redondance qui évite de resservir un angle déjà traité. Sort une shortlist d'idées de sujets LinkedIn sourcées et datées, avec accroche candidate et format visuel. Déclencher quand elle demande "ma veille", "une veille", "de quoi je peux parler", "des idées de posts", "des idées de sujets", "les actus de la semaine", "qu'est-ce qui buzze", "un signal faible", ou en exécution planifiée (mode routine). Pour écrire le post retenu, enchaîner avec my-viral-post.
---

# veille-contenu : la veille hebdo qui ne se répète jamais

Repérer ce qui bouge maintenant dans la niche de la personne, et ce qui commence à peine à bouger sans que personne ne le traite encore, pour en tirer des idées de posts à fort potentiel. Trois principes :

1. **Plusieurs sources en parallèle.** Un sous-agent par catégorie de sources, lancés ensemble, plutôt qu'un balayage séquentiel.
2. **Fenêtre glissante de 14 jours.** Semaine en cours et précédente. La veille reste chaude.
3. **Mémoire anti-redondance.** Un journal relu à chaque fois. Un angle déjà proposé récemment ou publié ne revient pas.

**La vraie plus-value : ne pas répéter ce que tout le monde dit déjà.** Un sujet que 20 comptes traitent cette semaine n'apporte rien, même bien écrit. Le but est de trouver l'angle avant la saturation, ou l'angle que personne d'autre ne prend sur un sujet connu.

## À lire en premier, chaque fois

1. **`profile/veille.md`** : axes suivis, sources par catégorie, ce qu'on écarte, routine. S'il est encore un gabarit, ne lance pas une veille à l'aveugle : propose de le remplir (étape 9 de l'onboarding), ou, si elle insiste, déduis des axes provisoires de l'identité éditoriale et dis-le en tête du rapport.
2. **`veille/journal.md`** : la mémoire. S'il n'existe pas, crée-le à partir du gabarit en fin de skill.
3. **La doctrine** : `voice/identite-editoriale.md` (positionnement, piliers, registres), `profile/cible.md` (problèmes, vocabulaire, ce qu'elle lit), `profile/recette.md` (registres qui marchent), `voice/anti-ai-writing-style.md` (voix, interdits), `voice/bibliotheque-hooks-texte.md` (accroches).

Filtre de pertinence : un angle est retenu s'il sert un de ses piliers **et** parle à sa cible.

## Méthode (dans cet ordre)

### 0. Charger la mémoire
Lis `veille/journal.md`. Extrais les angles des 8 dernières semaines. Un angle `publié` est écarté d'office, sauf angle radicalement neuf sur le même thème. Un angle `proposé` non publié ne revient que si le nouvel angle est nettement meilleur.

### 1. Cadrer
Fenêtre par défaut : 14 jours. Axes : ceux de `profile/veille.md`. Demande-lui si elle a une actu ou un angle en tête (facultatif ; sauté en mode routine).

### 2. Lancer les sous-agents en parallèle
Un sous-agent par catégorie **non vide** de `profile/veille.md` (Agent tool, une seule salve, 6 au plus ; 3 au plus pour la première veille de l'onboarding, sur les catégories les mieux fournies, pour qu'elle tienne en quelques minutes). Chacun couvre la fenêtre de 14 jours sur ses sources et rend une liste de candidats avec : le fait, la source primaire datée et son lien, où ça se discute, pourquoi maintenant, et un niveau de saturation estimé.

| Catégorie | Ce que le sous-agent cherche | Limites connues à lui rappeler |
|---|---|---|
| Presse et médias du secteur | Annonces, chiffres, décisions, lancements | Remonter à la source primaire, pas à l'article qui la cite |
| Newsletters et blogs d'experts | Analyses, prises de position, retours d'expérience | Distinguer opinion et fait |
| Comptes et créateurs LinkedIn | Ce qui est déjà sur-traité cette quinzaine (sert le test de saturation) | LinkedIn est mal indexé : récupérer ce qui est visible, sans surestimer la couverture |
| Forums et communautés | Questions récurrentes, frustrations, débats, vocabulaire réel de la cible | Reddit est souvent inaccessible en direct : trianguler via les articles qui citent les discussions. Ne jamais inventer de compteurs de votes ou de réponses ; les dire non vérifiés |
| Institutionnel, études, académique | Rapports, réglementation, publications récentes | Dater la donnée, juger le biais de l'émetteur |
| Signaux faibles | Sources étrangères pas encore relayées, changelogs discrets, offres d'emploi révélatrices, le chiffre enterré page 40 d'un rapport | À valoriser même si la chaleur est faible |

Sans outil de sous-agents, couvre les catégories une par une, en le signalant.

### 3. Vérifier et dater (non négociable)
Pour chaque fait retenu : source primaire, donnée la plus récente, date notée, biais jugé (un cabinet qui vend une solution gonfle le problème), source fragile signalée. Pas de claim sans source.

### 4. Dédupliquer et tester la saturation
- **Contre le journal** : écarter les angles des 8 dernières semaines.
- **Contre la sur-exposition** : un angle déjà porté par une dizaine de comptes cette semaine ne se garde que si la personne a un angle vraiment à elle (retex de terrain, contre-pied, donnée qui contredit le discours ambiant).
- **Émergent** : peu ou pas encore traité en France, à valoriser même si moins chaud.

### 5. Scorer
Quatre critères : **chaleur** (ça bouge cette quinzaine), **avance** (elle parmi les premières, ou angle unique sur un sujet connu), **fit** (sert un pilier et un registre qui marche pour elle), **valeur cible** (ça parle et ça aide sa cible). Garde 4 à 6 angles (5 lors de la première veille de l'onboarding), dont au moins 1 ou 2 signaux faibles identifiés comme tels.

### 6. Livrer le rapport
Format ci-dessous, dans sa voix pour les accroches.

### 7. Journaliser
- Rapport daté : `veille/AAAA-MM-JJ-veille.md`.
- Chaque angle ajouté à `veille/journal.md` avec le statut `proposé`.
- En session interactive, mets à jour `Dernière veille lue :` dans `profile/veille.md` avec la date du rapport présenté.
- Quand elle publie un post tiré d'un angle, passe l'angle à `publié` (c'est ce statut qui protège le plus fort contre la redondance). `my-viral-post` le fait au moment de journaliser le post.

## Format du rapport

```
# Veille : semaine du [JJ mois] (fenêtre : [JJ] au [JJ])
[Veille automatique, le cas échéant]

## A. Idées de sujets (4 à 6)
Pour chaque idée :
- Statut : actu chaude | signal faible
- Le fait (1 phrase) + source datée + lien
- Ton angle : registre activé + point de vue (pas juste le sujet)
- Accroche candidate : dans ta voix, sans tiret cadratin ni parallélisme négatif, sans te prêter un fait que tu n'as pas raconté (sinon : « à garder seulement si c'est vrai »)
- Format visuel conseillé : texte seul / image / meme / carte / carrousel / infographie
- CTA de clôture

## B. Ce dont ta cible discute
3 à 5 fils qui montent dans les communautés : le sujet, où, ce qui s'y dit, l'angle exploitable.

## C. Signaux faibles à garder sous le coude
Ce qui n'est pas encore mûr mais a une trajectoire, à sortir avant saturation.

## D. Déjà traité récemment
Les thèmes écartés parce que proposés ou publiés sur les 8 dernières semaines.

## Reco
Les 1 ou 2 idées à sortir en priorité, et le signal faible le plus prometteur.
```

## Le journal (mémoire)

Fichier `veille/journal.md`, une section par semaine, de la plus récente à la plus ancienne :

```
# Journal de veille

## Semaine du AAAA-MM-JJ
- [statut: proposé|publié] [thème court] : [angle] (source : [lien daté]) (format : [type])
```

Fenêtre de déduplication : 8 semaines glissantes. Un angle `publié` est le plus fortement exclu ; un angle `proposé` non publié peut ressortir si le nouvel angle est meilleur. Élague les entrées de plus de 6 mois.

## Mode routine (exécution planifiée)

Quand la skill tourne sans la personne (tâche planifiée, routine cloud, n8n) :
- saute la question de cadrage de l'étape 1, prends les axes de `profile/veille.md` ;
- lance la recherche, livre le rapport dans `veille/AAAA-MM-JJ-veille.md` et mets à jour le journal ;
- signale en tête du rapport que c'est une veille automatique ;
- ne touche pas à `Dernière veille lue :` : c'est ce qui permet à l'agent d'annoncer le rapport à la prochaine session ;
- en routine cloud, fais d'abord `git pull` (pour récupérer les angles passés à `publié` en local), puis commite `veille/` avec le message « Veille du AAAA-MM-JJ » et pousse sur la branche par défaut du dépôt (`main`), jamais sur une branche à part : c'est là que l'agent local la retrouve.

## Règles

- **Voix de la personne** pour les accroches. Interdits absolus : tiret cadratin, parallélismes négatifs (« ce n'est pas X, c'est Y » et variantes), jargon de hype, recette magique, IA pour l'IA. Doctrine complète dans `voice/anti-ai-writing-style.md`.
- **Pas de claim sans source**, la plus récente, datée et vérifiée.
- **Chaque idée se termine par un CTA clair.**
- **Méthodes tierces citées**, jamais appropriées (`profile/config.md`, garde-fous).
- **Respecter `Ce qu'on écarte`** dans `profile/veille.md` et les sujets interdits de `profile/config.md`.
- **Anti-redondance systématique** : si tous les angles trouvés sont déjà au journal, creuser plus loin (académique, terrain, sources étrangères) plutôt que de resservir.

## La chaîne de production

1. **Veille** (cette skill) : idées de sujets, journal à jour.
2. **Écrire** : `my-viral-post` sur l'idée retenue (lui passer le fait, la source, l'accroche, le CTA).
3. **Illustrer, composer** : `image-linkedin`, `carte-linkedin`, `carrousel-linkedin` selon le format conseillé.
