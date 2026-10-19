---
name: bilan-performance
description: Analyse ce qu'ont donné les posts LinkedIn publiés (impressions, portée, réactions, commentaires, partages, enregistrements) pour ajuster la stratégie de la personne. Compare les résultats à sa recette, classe ce qui a marché par registre, format, accroche, créneau et source de veille, puis propose 3 décisions concrètes pour le mois suivant et, avec son accord, met à jour sa recette, ses créneaux et les axes de sa veille. Données via Zernio (scripts/zernio.py), ou chiffres collés à la main, ou un nouveau relevé Apify. Déclencher quand elle demande "mon bilan", "bilan du mois", "analyse mes posts", "qu'est-ce qui a marché", "mes stats LinkedIn", "comment ajuster ma stratégie", "quels posts ont le mieux marché", ou en exécution planifiée (mode routine).
---

# bilan-performance : ce que tes posts ont donné, et ce qu'on change

La veille trouve les sujets, `my-viral-post` écrit, Zernio publie. Ce bilan ferme la boucle : il regarde les vrais résultats et décide de ce qu'on garde, de ce qu'on arrête et de ce qu'on teste. Sans lui, la recette reste figée sur les posts d'avant l'agent.

## À lire en premier

1. `profile/recette.md` : la recette en vigueur (médiane, registres classés, formats, accroches). C'est la référence à laquelle on compare.
2. `outputs/registry.csv` : les posts `programmé` et `publié`, leur slug, leur `post.md` (registre, angle, visuel, source de veille dans l'en-tête), l'id Zernio dans `notes`.
3. `veille/journal.md` : quels angles venaient de la veille.
4. `profile/config.md` : `Publication`, `Comptes de publication`, `Créneaux de publication`, `Objectifs`.
5. `bilans/` : les bilans précédents, pour suivre les décisions déjà prises.

## Récupérer les chiffres

Selon `Publication` dans `profile/config.md` :

- **zernio** : `python3 scripts/zernio.py resultats --compte <id>` écrit `bilans/performances.csv` (les posts suivis des 90 derniers jours, avec impressions, portée, réactions, commentaires, partages, enregistrements, envois, taux d'engagement). Sur un profil personnel, seuls les posts publiés via Zernio sont suivis d'office : avant le relevé, importe ceux du registre publiés à la main (`python3 scripts/zernio.py importer --compte <id> --url <URL>`, chiffres sous 24 h). Ajoute `python3 scripts/zernio.py creneaux --compte <id>` pour les jours et heures. Si Zernio refuse les statistiques (offre), dis-le et passe à une autre voie.
- **manuelle** : demande-lui de coller, pour chaque post du mois, les impressions et les réactions affichées sous le post (LinkedIn les montre à l'auteur). Écris-les dans `bilans/performances.csv`, mêmes colonnes, cases inconnues vides.
- **Apify**, en dépannage : `python3 scripts/scrape-linkedin-posts.py --profile <URL> --max 30` donne réactions, commentaires et partages, sans impressions. Payant : annonce le coût et attends son oui.

Garde chaque relevé : copie `bilans/performances.csv` en `bilans/AAAA-MM-JJ-performances.csv`. Les chiffres d'un post bougent pendant 1 à 2 semaines : un post de moins de 7 jours se signale comme « trop récent » et ne compte pas dans les conclusions.

## Analyser (dans cet ordre)

1. **Relier chaque post à sa fiche** : rapproche chaque ligne du relevé d'un slug du registre (URL ou URN dans `notes`, sinon date et début du texte). Un post publié hors agent reste dans l'analyse, marqué « hors agent ». Pour un post importé (`origine` = hors Zernio), Zernio indique souvent un format « text » et un texte vide : prends le format et l'accroche dans le registre ou dans le relevé Apify (`outputs/onboarding/posts.csv`).
2. **La mesure** : par défaut, le taux d'engagement et les impressions. Si l'objectif est `leads`, regarde d'abord les commentaires et les envois ; si `autorité`, les enregistrements et partages ; si `reach`, les impressions et la portée.
3. **Contre la recette** : médiane du mois contre la médiane de `profile/recette.md`, et chaque post en multiple de la médiane du mois.
4. **Ce qui a marché, par dimension** : registre, format (texte, image, carrousel, vidéo, lien), famille d'accroche, jour et heure, sujet venu de la veille ou de sa matière à elle, longueur. Donne toujours le nombre de posts derrière chaque conclusion : sous 3 posts, c'est une piste, pas une règle.
5. **Le post le plus vu contre le plus engageant** : ils diffèrent souvent ; dis ce que chacun apprend.
6. **Les décisions précédentes** : si le bilan d'avant demandait un test, dis s'il a marché.

Rien d'inventé : chaque affirmation renvoie à des posts précis du relevé. Si moins de 4 posts ont plus de 7 jours, dis que le bilan est prématuré, montre les chiffres bruts sans conclure, et propose de le refaire dans deux semaines.

## Livrer

`bilans/AAAA-MM-bilan.md`, court :

```
# Bilan de [mois] ([N] posts, du [JJ] au [JJ])

## En une phrase
[Ce qui a le mieux marché ce mois-ci, chiffre à l'appui.]

## Les chiffres
[Médiane du mois contre médiane de la recette. Le top 3 et le flop 3, avec leur multiple de la médiane et l'URL.]

## Ce qui marche, ce qui ne marche pas
[Par dimension, avec le nombre de posts derrière chaque ligne.]

## 3 décisions pour le mois prochain
1. Garder : …
2. Arrêter ou réduire : …
3. Tester : … (un seul test à la fois, mesurable au prochain bilan)

## Ajustements proposés
- Recette (`profile/recette.md`) : …
- Créneaux (`profile/config.md`) : …
- Veille (`profile/veille.md`) : axes à renforcer ou à écarter …
```

Montre-lui « En une phrase » et les 3 décisions. **Avec son accord seulement**, applique les ajustements : ajoute à `profile/recette.md` une section datée « Recalibrage du AAAA-MM-JJ » (sans effacer l'historique), mets à jour `Créneaux de publication`, et ajuste les axes de `profile/veille.md`. Respecte `voice/anti-ai-writing-style.md` dans tout ce qui est écrit.

## Mode routine (exécution planifiée)

Le 1er lundi du mois, sans la personne : relevé, analyse, rapport `bilans/AAAA-MM-bilan.md` marqué « Bilan automatique » en tête. N'applique **aucun** ajustement : ils attendent son accord à la session suivante. En routine cloud, commite et pousse `bilans/` sur `main` après un `git pull`, comme la veille.

## Règles

- Les chiffres viennent du relevé, datés. Pas de moyenne sur 2 posts présentée comme une règle.
- Un seul test à la fois : sinon on ne sait pas ce qui a joué.
- Aucune dépense sans accord (relevé Apify, offre Zernio au-delà du gratuit).
- Pas de jugement sur la personne : on parle des posts, du format, du créneau.
