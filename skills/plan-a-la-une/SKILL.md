---
name: plan-a-la-une
description: Le stratège des stories à la une Instagram. Lit les données de la personne (dossier mes-donnees du kit, ou son Brain / coffre Obsidian), choisit les 4 à 6 stories à la une qui transforment un visiteur du profil en message privé (Ma méthode, Résultats, Qui suis-je, FAQ, Commencer…), dans le bon ordre, écrit le texte exact de chaque story avec les vraies preuves, puis lance la fabrication (stories-a-la-une) et les icônes (icones-a-la-une). Point d'entrée du kit Stories à la une. Use when "fais mes stories à la une", "mes highlights", "plan de stories à la une", "refais mon profil Instagram", "quelles stories à la une", "plan-a-la-une".
---

# Plan des stories à la une (point d'entrée)

Les stories à la une sont la vitrine du profil : quelqu'un découvre une vidéo, ouvre le profil, et décide en quelques secondes s'il écrit ou s'il part. Chaque story à la une a UN rôle, et toutes poussent vers le même message privé (le mot-clé DM).

## 0. Démarrage rapide (kit)
1. Lis `mes-donnees/ma-marque.md` en entier. Regarde ce qu'il y a dans `mes-donnees/photos/`, `mes-donnees/preuves/` et `mes-donnees/temoignages/` (liste les fichiers, ouvre les images).
2. S'il existe un Brain / coffre Obsidian, cherche aussi : marque, couleur, offre, cible, méthode, preuve, témoignage, mot-clé DM.
3. Fais une fiche en 8 lignes de ce que tu sais, et pose en UNE fois toutes les questions qui manquent, en questions cliquables (ton option recommandée en premier). Ne devine jamais une couleur, un chiffre ou une preuve.

## 1. Choisir les stories à la une (4 à 6, pas plus)
Méthode SYSTEM, dans cet ordre de priorité (les premières à gauche se voient sans faire défiler) :

| Ordre | Story à la une | Son rôle | Condition |
|---|---|---|---|
| 1 | **Ma méthode** | Vendre l'accompagnement : promesse, pour qui, étapes, objection levée, DM mot-clé | Toujours |
| 2 | **Résultats** (ou Avis) | Prouver : captures et témoignages de vrais clients, 1 story par client | Seulement avec de vraies preuves |
| 3 | **Qui suis-je** | Créer la confiance : avant, le déclic, aujourd'hui, pourquoi je t'aide, DM | Toujours |
| 4 | **FAQ** | Lever les freins : temps, prix (sans afficher le prix), « je pars de zéro », « ça marche pour moi ? », garantie s'il y en a une | Si la personne vend un accompagnement |
| 5 | **Commencer** | Donner la prochaine étape : ressource gratuite ou mot-clé DM, rien d'autre | Si elle a une ressource gratuite ou un tunnel |
| 6 | **Coulisses** | Montrer le quotidien et le travail réel | Option, seulement si elle a des photos et vidéos du quotidien |

Pas de preuve vraie = pas de story à la une « Résultats » : à la place, note « à créer quand tu auras tes premiers résultats clients » et propose « Coulisses ».

Noms : 12 caractères maximum (Instagram coupe au-delà), un ou deux mots, sans emoji.

## 2. Écrire le plan (montre-le, attends le OK)
Écris `mes-donnees/plan-a-la-une.md` avec, pour chaque story à la une :
- le nom, le pictogramme (voir `icones-a-la-une`), son rôle en une phrase ;
- chaque story (4 à 8 par story à la une, 6 pour « Ma méthode ») : le texte EXACT à afficher (pas de crochets), la photo prévue (`photos/…`), la preuve utilisée (`preuves/…`) ;
- la dernière story de chaque story à la une = mot-clé DM (le même partout).

Règles d'écriture (validées sur des séries réelles) :
- **Je, jamais on** si la personne travaille seule. Phrases courtes, une idée par story, lisible en 3 secondes.
- **Les mots de la cible** (ses vraies phrases, trouvées dans les DM, les appels, les commentaires) battent les formules.
- **Preuves = résultats réels**, sans ambiguïté sur à qui est le chiffre (« sur mes propres vidéos », « mon client Paul »). Jamais de chiffre inventé, jamais de promesse de gain garanti, jamais de prix.
- **Moins de mots = plus de messages** : coupe tout ce qui n'aide pas à décider.
- Témoignage vidéo : visage visible, résultat chiffré dans le bandeau. Un vocal sans visage ou un avis vague ne sert pas de preuve.
- Pas de tiret cadratin (—), pas d'emoji dans le texte des stories.

## 3. Fabriquer (échantillon d'abord)
1. Une story à la une à la fois, en commençant par « Ma méthode » : suis le skill `stories-a-la-une` (il génère 1 story d'échantillon, attend le OK, puis toute la série, et contrôle que rien ne déborde).
2. Témoignages vidéo : `stories-a-la-une/scripts/tr.py` (transcription) puis `temoignage.py` (bandeau prénom + chiffre, sous-titres, capture du résultat).
3. Les icônes : skill `icones-a-la-une`, puis montre `planche-profil.png`.
4. Tout finit dans `mes-donnees/a-publier/<nom-de-la-story-a-la-une>/` : stories numérotées dans l'ordre + icône.

## 4. Livrer
- Un récap court : quelles stories à la une, dans quel ordre, où sont les fichiers.
- Comment publier, depuis le téléphone :
  1. Publier les stories une par une, dans l'ordre (01, 02…).
  2. Profil → rond « + » (Nouveau) sous la bio → cocher les stories → Suivant → nom → Ajouter.
  3. Couverture : appui long sur la story à la une → Modifier → Modifier la couverture → l'icône.
  (L'interface change souvent : si un bouton a un autre nom, cherche « story à la une » dans l'aide Instagram.)
- Ne te connecte jamais à Instagram dans un navigateur et ne publie rien toi-même : c'est la personne qui publie, depuis son téléphone.
- Enregistre dans `mes-donnees/plan-a-la-une.md` (et dans le Brain s'il existe) chaque correction de la personne, en une ligne : ce qui n'allait pas → la règle. Une correction ne doit jamais revenir.
