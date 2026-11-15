---
name: icones-a-la-une
description: Fabrique les icônes (couvertures rondes) des stories à la une Instagram, toutes dans le même style premium - fond à la couleur de la marque (plein ou dégradé), pictogramme blanc au trait arrondi, petite étincelle, aucun texte - plus un aperçu de la ligne du profil pour choisir avant de publier. Sans IA d'image, sans Canva. Use when "icône de story à la une", "couverture de highlight", "icônes highlights", "couvertures à la une", "icones-a-la-une".
---

# Icônes des stories à la une

Une icône par story à la une : carré 1080x1080 qu'Instagram affiche en rond. Le but : un profil propre et cohérent, qu'on comprend en un coup d'œil.

## 1. Avant
- Couleur de la marque : lis `mes-donnees/ma-marque.md` (ou le Brain / coffre Obsidian de la personne). Ne devine jamais une couleur : demande-la si elle manque.
- La liste des stories à la une à créer : celle du plan (`plan-a-la-une`), sinon demande-la.
- Python 3 et Google Chrome (ou Edge) doivent être installés.

## 2. Choisir le pictogramme
L'icône illustre le **nom de la story à la une**, pas l'offre :

| Story à la une | Picto |
|---|---|
| Ma méthode, Mon programme | `methode` (livre ouvert) |
| Avis, Témoignages | `temoignages` (bulle + étoile) |
| Résultats | `resultats` (courbe qui monte) |
| Qui suis-je, Mon histoire | `qui` (silhouette) |
| FAQ, Questions | `faq` (point d'interrogation) |
| Offre, Accompagnement | `offre` (cadeau) |
| Pour qui | `pourqui` (cible) |
| Commencer, Start | `commencer` (éclair) |
| Coulisses | `coulisses` (clap) |
| Contact, DM | `contact` (bulle avec points) |
| Preuves | `preuves` (trophée) |
| Étapes | `etapes` (escalier) |
| Gratuit, Ressources | `gratuit` (étiquette) |
| Avant / après | `avant-apres` |
| Routine, Planning | `routine` (chrono) |
| Outils | `outils` (clé) |

## 3. Fabriquer
```
python <skill>/scripts/icone.py "<#HEX>" methode:"Ma méthode" temoignages:"Avis" faq:"FAQ" --dossier <projet>/png
```
- `--fond-degrade` : léger dégradé lumineux (plus premium sur l'or, le bleu, le violet). Sans l'option : fond plein.
- `--sans-etincelle` : enlève la petite étincelle.
- Le script crée `icone-<picto>.png` pour chaque story à la une + `planche-profil.png` (aperçu de la ligne du profil sur fond noir).

## 4. Vérifier puis livrer
- Ouvre `planche-profil.png` et regarde-la toi-même : même style partout, pictos lisibles en petit, noms courts (12 caractères max, sinon Instagram coupe). Montre-la à la personne avant de livrer.
- Livre les icônes dans le même dossier `png/` que les stories.
- Pour publier (depuis le téléphone) : appui long sur la story à la une → Modifier → Modifier la couverture → choisir l'icône dans la galerie. L'interface Instagram change souvent : si un bouton a un autre nom, cherche « modifier couverture story à la une » dans l'aide Instagram.
- Ne te connecte jamais à Instagram dans un navigateur : c'est la personne qui publie, depuis son téléphone.
