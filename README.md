# Kit Stories à la une SYSTEM

Par Brennan SONNET. Tes stories à la une Instagram (highlights) prêtes à publier, à tes couleurs, avec tes vraies preuves, faites par Claude en une soirée.

Exemple de profil obtenu : **Ma méthode · Résultats · Qui suis-je · FAQ · Commencer**, chaque story à la une avec ses stories (1080x1920) et son icône ronde, toutes dans le même style.

## Ce que fait le kit
Tu écris « **fais mes stories à la une** » dans Claude Code. Ensuite :
1. **Le plan** (`plan-a-la-une`) : Claude lit ta fiche `ma-marque.md`, tes photos et tes preuves, te pose les questions qui manquent, choisit 4 à 6 stories à la une dans le bon ordre et écrit le texte exact de chaque story.
2. **La fabrication** (`stories-a-la-une`) : une story d'essai d'abord, puis toute la série. Photo réelle de toi en fond, titres géants à ta couleur, preuves chiffrées, mot-clé DM à la fin. Contrôle automatique : rien ne passe sous la barre de réponse Instagram.
3. **Les témoignages vidéo** : transcription mot à mot, bandeau prénom + résultat, sous-titres, capture du résultat incrustée.
4. **Les icônes** (`icones-a-la-une`) : une icône par story à la une, même style partout, plus l'aperçu de la ligne de ton profil.

Tout finit dans `mes-donnees/a-publier/`. C'est **toi** qui publies, depuis ton téléphone. Claude ne se connecte jamais à ton Instagram.

## En 3 étapes
1. **Télécharge le kit** (bouton vert « Code » → « Download ZIP », ou le lien direct que t'a donné Brennan) et dézippe-le.
2. **Remplis tes données** dans le dossier `mes-donnees/` :
   - `ma-marque.md` : tes couleurs, ton offre, ta méthode, tes preuves, ton mot-clé DM (10 minutes) ;
   - `photos/` : au moins 6 photos de toi, toutes différentes ;
   - `preuves/` : captures de tes vrais résultats ;
   - `temoignages/` : vidéos de tes clients (si tu en as).
3. **Donne le dossier à Claude** : ouvre l'app Claude → onglet **Code** → choisis le dossier du kit, puis écris :
   > installe le kit et fais mes stories à la une

Les détails d'installation (Python, Chrome, ffmpeg) : [INSTALLER.md](INSTALLER.md).

## Les règles du kit
- **Que du vrai** : aucune preuve, aucun chiffre, aucun témoignage inventé. Pas de preuve ? Pas de story à la une « Résultats » : Claude te propose autre chose.
- **Pas de promesse de gain garanti, pas de prix** dans les stories.
- **Ton visage, tes photos** : pas d'image générée par IA pour les stories.
- **Toi seul publies**, depuis ton téléphone (ne connecte jamais ton Instagram à un navigateur piloté par une IA : risque de suspension).
- Chaque correction que tu fais est notée dans ton plan pour ne jamais revenir.

## Contenu
- `skills/plan-a-la-une` : le stratège (point d'entrée).
- `skills/stories-a-la-une` : la fabrication des stories (`gen.py`), des témoignages vidéo (`tr.py`, `temoignage.py`).
- `skills/icones-a-la-une` : les icônes et l'aperçu du profil (`icone.py`).
- `mes-donnees/` : tes infos, photos, preuves, témoignages, et le résultat (`a-publier/`).
- `installer.ps1` (Windows) / `installer.sh` (Mac) : installent les 3 skills dans Claude Code. Rien n'est supprimé.

Polices : Space Grotesk, Inter et Montserrat (libres, licence SIL Open Font License 1.1), chargées depuis Google Fonts / Fontsource à l'utilisation. Voir [THIRD_PARTY.md](THIRD_PARTY.md).
