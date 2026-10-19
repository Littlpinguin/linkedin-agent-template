# assets/moi/ : ton visage et ta signature

Ce dossier sert à deux choses : te mettre en scène dans les images générées par IA avec ton vrai visage, reconnaissable, et fournir ta photo de signature pour les cartes et carrousels.

## Les 3 photos (noms fixes)

| Fichier | Ce qu'on voit | Sert à |
|---|---|---|
| `face.jpg` | Toi de face, regard caméra | Scènes où tu fais face au lecteur, avatar de signature |
| `profil-gauche.jpg` | Ton profil, nez tourné vers la gauche de l'image (de trois quarts à profil complet) | Scènes où tu regardes vers la gauche du cadre |
| `profil-droit.jpg` | Ton profil, nez tourné vers la droite de l'image | Scènes où tu regardes vers la droite du cadre |

`.jpeg` et `.png` sont acceptés. L'agent choisit la photo dont l'orientation colle à la scène : c'est ce qui donne un visage ressemblant.

**Ce qui marche** : une seule personne, visage net et assez grand (au moins un tiers de la hauteur de la photo), lumière du jour de face ou de côté, expression naturelle, fond simple. Une photo de téléphone suffit.

**Ce que l'agent te redemandera** : flou, contre-jour ou ombre forte sur le visage, lunettes de soleil, casquette qui cache les yeux, plusieurs personnes, visage coupé, filtre beauté appuyé.

**Avatar de signature** (facultatif) : `avatar-signature.jpg`, carré, recadré sur le visage. Utilisé en bas des cartes et carrousels si ton style visuel prévoit une signature. Sans lui, l'agent recadre `face.jpg`.

**Anciens noms** : si tu as configuré une première version du template, tes `visage-1.jpeg`, `visage-2.jpeg`… restent utilisables. L'agent te proposera de les renommer.

## Consentement et confidentialité

- Seul ton visage, avec ton accord, va ici. Aucune autre personne réelle sans la sienne.
- Ce dossier est exclu de git (voir `.gitignore`) : tes photos ne partent jamais dans un dépôt, même si tu pousses ton agent sur GitHub. Garde-en une copie ailleurs.
