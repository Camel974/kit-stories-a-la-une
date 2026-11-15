---
name: stories-a-la-une
description: Crée des stories à la une Instagram (highlights) prêtes à publier, aux couleurs et aux polices de la marque - 6 stories 1080x1920 qui vendent l'offre (couverture + preuve, je fais quoi, pour qui, étapes, objection levée, DM mot-clé + preuve), fond photo réelle de la personne assombri, gros titre, mots clés en couleur, plus l'icône de couverture. Lit d'abord le branding dans le Brain / coffre Obsidian, pose les questions qui manquent, montre 1 échantillon avant de tout faire, contrôle automatiquement que rien ne déborde. Use when "story à la une", "stories à la une", "highlight", "highlights", "ma méthode en stories", "stories pour mon profil", "couverture de story à la une", "icône de highlight".
---

# Stories à la une (highlights Instagram)

Tu fabriques une série de stories fixes (images, pas de vidéo) qu'on range dans une story à la une sur le profil Instagram. Elles expliquent l'offre et poussent à envoyer un mot-clé en DM. Rendu : HTML + capture Chrome headless (script `scripts/gen.py`). Jamais Canva, jamais d'image générée par IA pour les stories elles-mêmes.

Résultat type : une série cohérente, sombre, photo réelle de la personne en bas, texte centré en haut, titre géant à la couleur de la marque, mots clés colorés, cases « preuve » chiffrées, dernière story = DM « MOT ».

## 0. Avant de commencer (1 minute)
- Vérifie que Python 3 et Google Chrome (ou Microsoft Edge) sont installés : `python --version`. Pillow est optionnel (`pip install pillow`) : il fait la planche d'aperçu.
- Crée un dossier projet pour cette story à la une (là où la personne range son contenu), par exemple `<Contenu>/stories-a-la-une/<nom-du-highlight>/`, avec un sous-dossier `photos/`.

## 1. Le branding d'abord (OBLIGATOIRE, avant d'écrire une seule story)
Kit SYSTEM : commence par `mes-donnees/ma-marque.md` (la fiche remplie par la personne) et le plan `mes-donnees/plan-a-la-une.md` s'il existe (skill `plan-a-la-une`). Puis cherche dans le Brain / coffre Obsidian de la personne (Grep sur tout le coffre, puis lis les fichiers trouvés) : `marque`, `branding`, `charte`, `DA`, `direction artistique`, `couleur`, `#` + hex, `police`, `font`, `logo`, `offre`, `prix`, `cible`, `avatar`, `méthode`, `étapes`, `preuve`, `résultat`, `témoignage`, `CTA`, `mot-clé`, `DM`, `voix`, `ton`, `tutoie`. Un fichier `marque.json` ou `da.md` fait foi s'il existe.

Remplis cette fiche dans ta tête (et montre-la en 6 lignes à la personne) :

| Champ | Exemple | Obligatoire |
|---|---|---|
| Couleur principale (hex) | #7C3AED | oui |
| Police des titres / du texte | Space Grotesk / Inter | non (défaut : ces deux-là) |
| Tu ou vous | tu | oui |
| L'offre en 1 phrase + qui elle vise (1 ou 2 profils) | « j'aide X à faire Y » | oui |
| La méthode en 3 étapes (ou 3 à 5) | 1… 2… 3… | oui |
| L'objection n°1 de la cible | « je ne suis pas technique » | oui |
| 2 preuves chiffrées VRAIES de la personne | « 100K vues en moins de 3 jours » | oui (si aucune : on n'en met pas) |
| Mot-clé DM | « IA » | oui |
| Nom de la story à la une | « Ma méthode » | oui |

Ce qui manque : pose TOUTES les questions en une fois, en questions cliquables (ton option recommandée en premier). Ne devine jamais une couleur, une preuve ou un chiffre. Une preuve inventée = faute grave.

Polices : sans fichier de police, le script charge Space Grotesk et Inter depuis Google Fonts (connexion internet nécessaire). Si la marque utilise une autre police Google Fonts, mets juste son nom (`"police_titre": "Montserrat"`), le script la charge (internet nécessaire). Police payante ou perso : mets le chemin du fichier dans `"police_titre_fichier"`. Titres : une police grasse et condensée rend le mieux.

## 2. Le plan (montre-le, attends le OK)
Structure par défaut « Ma méthode », 6 stories, une idée par story :

1. **Couverture** : petite ligne qui interpelle la cible (question) · titre géant = la promesse en 3-4 mots · 1 phrase « je t'apprends à… » avec les mots clés en couleur · case preuve n°1 (chiffre géant + ce qu'il mesure + sur quoi).
2. **Je fais quoi ?** : « Concrètement, » · titre « Je fais quoi ? » · « un seul accompagnement : » + les 2 temps de l'offre · pastille couleur = le bénéfice final en une ligne.
3. **Pour qui ?** : titre seul · 2 profils soulignés (« Tu as déjà… » / « Tu pars de zéro ») · sous chacun, ce que tu fais pour lui, mots clés en couleur.
4. **N étapes** : « Comment je t'aide, » · titre « 3 étapes » · liste numérotée (gros chiffres couleur), 1-2 lignes par étape.
5. **Objection levée** : la peur n°1 de la cible retournée (ex. « Zéro code ») · 3 puces « pas besoin de… / même si tu pars de zéro, c'est possible ».
6. **CTA** : « À la fin, » · titre = le résultat final · trait blanc lumineux · **DM « MOT »** en géant · « pour que je t'aide à… » · case preuve n°2.

Autres highlights possibles avec le même moteur (adapte le plan, même style) : « Témoignages » (citations courtes + chiffre du client, une story par client ; les vidéos témoignages se montent à part), « Qui suis-je », « Résultats », « FAQ ». Garde 4 à 8 stories.

Écris le plan avec les vrais textes de chaque story (pas de crochets), montre-le, corrige jusqu'au OK.

## 3. Règles d'écriture (apprises sur des séries validées, à respecter)
- **Je, jamais on**, si la personne travaille seule. « Je fais quoi ? », « je t'aide », « je t'apprends ».
- **Mots clés en couleur par groupes entiers** : « des <span class="v">vidéos qui marchent</span> », pas un mot isolé au milieu. Tout le reste en blanc. 2 à 4 groupes colorés par story, pas plus.
- **Preuves = les résultats de la personne, sans ambiguïté** : écrire « sur mes propres vidéos », « gagnés grâce à cette automatisation ». Jamais de doute sur à qui est le chiffre. Jamais de prix dans les stories.
- **Ce qui est réservé aux clients ne s'affiche pas** (ex. WhatsApp 1-1, bonus) si la personne ne veut pas le montrer : demande.
- Pas de story « ce que tu as » (liste du contenu de l'offre) : on vend le résultat, pas le colis.
- Phrases courtes, mots simples, une idée par story. Si ça ne se lit pas en 3 secondes, coupe.
- Les mots de la cible (ses vraies phrases, trouvées dans le Brain : calls, DM) battent les formules.
- Pas de tiret cadratin (—), pas d'emoji dans le texte des stories.

## 4. Les photos de fond
- Les photos sont dans `mes-donnees/photos/` (kit). Il en faut **1 par story, toutes différentes** (lieux, tenues, cadrages), format portrait, en haute qualité. Elles vont dans `photos/`. Sans photo pour une story : laisse `"photo": ""`, le script met un fond dégradé couleur (bien pour 1 story, pas pour toutes).
- La photo occupe le bas de la story, le haut est un fondu sombre où vit le texte. On règle sa hauteur avec `"dy"` (en px, 250 à 900 : plus grand = photo plus bas). Le visage ne doit jamais passer sous le texte ni être coupé en bas.
- **Photo « pro » de vente** : regard sérieux et concentré, dans l'action (au bureau, en train de travailler ou de tourner). Pas de photo floue, pas de pose ratée. Demande à la personne ce qu'elle trouve « pro » pour elle.
- L'écran visible sur une photo montre l'outil qu'elle utilise vraiment pour son offre.
- Retouche IA d'une photo seulement si la personne le demande, et en gardant son vrai visage.

## 5. Fabriquer (échantillon d'abord)
1. Copie `exemple/stories.json` dans le dossier projet et remplis-le : bloc `marque` (couleur, polices, `majuscules` true/false) puis une entrée par story (`nom`, `photo`, `dy`, `html`). Classes disponibles dans `html` :
   - `sur` petite ligne au-dessus du titre · `titre` titre géant · `txt` paragraphe · `v` mot clé en couleur · `pill` pastille couleur
   - `liste` > `it` > (`pt` puce ronde | `num` gros numéro) + texte · `sl` souligné couleur · `b` gras
   - `preuve` > `big` (chiffre) + `lab` (ce qu'il mesure) + `small` (précision) · `trait` séparateur lumineux · `dm` mot-clé DM géant
   - Coupures de ligne : `<br>`. Ajustement ponctuel : `style="font-size:112px"` ou `style="margin-top:20px"`.
2. Génère **la story 1 seule** : `python <skill>/scripts/gen.py <dossier_projet> 01-couverture`. Ouvre le PNG, regarde-le toi-même (lisibilité, visage, contraste), puis montre-le à la personne. Attends son OK sur le style avant le reste.
3. Génère tout : `python <skill>/scripts/gen.py <dossier_projet>`. Regarde la `planche.jpg` (toutes les stories côte à côte) : la série doit être cohérente.
4. **Lis les ALERTES du script et corrige-les toutes** avant de livrer : texte qui descend sous y=1600 (couvert par la barre de réponse Instagram), texte qui déborde sur les côtés, « DM » / pastille / chiffre qui passe sur 2 lignes. Zéro alerte = condition pour livrer.
5. Corrections de la personne : change le texte ou `dy` dans `stories.json`, régénère seulement la story concernée (`gen.py <dossier> 03-pour-qui`).

Goûts validés à garder : un séparateur se colle aux textes qu'il sépare (pas de grand vide autour) ; le fond doit laisser voir la photo (ne pas l'assombrir à fond) ; la case preuve se place sous le titre (story 1) ou sous le DM (story 6).

## 6. L'icône de la story à la une
- Format carré 1080x1080, **fond plein à la couleur de la marque, pictogramme blanc au trait arrondi, sans aucun texte**, centré (Instagram la recadre en rond).
- L'icône illustre le **titre** de la story à la une, pas l'offre : « Ma méthode » = livre ouvert ; « Témoignages » = petits personnages + bulle avec une étoile ; « Résultats » = graphique qui monte ; « Qui suis-je » = silhouette.
- Utilise le skill `icones-a-la-une` (script `icone.py`) : même style garanti pour toutes les icônes du profil, aperçu de la ligne du profil inclus. En dernier recours, ce prompt à coller dans un générateur d'images :
  `Icône carrée 1080x1080 pour une story à la une Instagram. Fond uni couleur <HEX>. Au centre, un pictogramme <OBJET> dessiné en trait blanc épais et arrondi, style minimaliste, avec une petite étincelle. Aucun texte, aucune lettre, pas d'ombre, pas de dégradé, marges généreuses.`
- Toutes les icônes du profil gardent le même style.

## 6 bis. Témoignages vidéo (story à la une « Résultats »)
- Vidéos des clients dans `mes-donnees/temoignages/`. Visage visible obligatoire, résultat chiffré vrai.
- Transcription mot à mot : `python <skill>/scripts/tr.py <video>` (une fois : `pip install faster-whisper`). Relis les chiffres.
- Montage 9:16 (bandeau prénom + chiffre, sous-titres mot à mot, capture du résultat incrustée) : `python <skill>/scripts/temoignage.py <config.json>` (modèle du config.json en tête du script). Besoin de ffmpeg. Les polices se téléchargent seules la 1re fois.
- 60 secondes maximum par story. Montre la 1re vidéo avant de faire les autres.

## 7. Livrer
- Tous les fichiers finaux dans **un seul dossier** : `mes-donnees/a-publier/<nom-de-la-story-a-la-une>/` (stories numérotées dans l'ordre + icône). Pas de fichiers éparpillés.
- Dis à la personne comment publier, depuis son téléphone :
  1. Publier les stories une par une, dans l'ordre 1 → 6.
  2. Profil → rond « + » (Nouveau) dans la ligne des stories à la une sous la bio → cocher les stories → Suivant → nom (ex. « Ma méthode ») → Ajouter.
  3. Couverture : appui long sur la story à la une → Modifier → Modifier la couverture → icône depuis la galerie.
  (L'interface Instagram change souvent : si un bouton a un autre nom, cherche « story à la une » dans l'aide Instagram avant de répondre.)

## 8. Mémoire
- Enregistre dans le Brain / coffre Obsidian de la personne : où sont les fichiers, le nom du highlight, les textes validés, et chaque correction qu'elle a faite (en une ligne : ce qui n'allait pas → règle), plus une ligne dans son journal s'il en a un. Une correction ne doit jamais revenir.
- Ne publie jamais rien toi-même sur Instagram et ne t'y connecte jamais dans un navigateur (risque de suspension du compte) : c'est la personne qui publie, depuis son téléphone.
