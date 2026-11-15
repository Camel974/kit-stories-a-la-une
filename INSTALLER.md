# Installer le Kit Stories à la une de A à Z

## 1. Claude (si tu ne l'as pas)
- Télécharge l'app Claude : https://claude.ai/download et connecte-toi (abonnement Pro ou Max nécessaire pour Claude Code).
- Dans l'app, ouvre l'onglet **Code**.

## 2. Python
- Windows : https://www.python.org/downloads/ → coche **« Add python.exe to PATH »** pendant l'installation.
- Mac : Python 3 est souvent déjà là (`python3 --version` dans le Terminal), sinon même lien.
- Optionnel, pour la planche d'aperçu : `pip install pillow`.

## 3. Google Chrome (si tu ne l'as pas)
- https://www.google.com/chrome/ (sur Windows, Microsoft Edge suffit aussi).

## 4. Seulement pour les témoignages vidéo
- ffmpeg : https://ffmpeg.org/download.html (Windows : le plus simple est `winget install ffmpeg` dans le terminal ; Mac : `brew install ffmpeg`).
- La transcription : `pip install faster-whisper` (une seule fois).

## 5. Installer le kit
**Le plus simple :** dans Claude Code, choisis ce dossier (`kit-stories-a-la-une`) comme dossier de travail et écris :
> installe le kit et fais mes stories à la une

**À la main :**
- Windows : clic droit sur le dossier → « Ouvrir dans le terminal », puis :
  ```
  powershell -ExecutionPolicy Bypass -File .\installer.ps1
  ```
- Mac : ouvre le Terminal dans le dossier, puis :
  ```
  bash installer.sh
  ```

Le script copie les 3 skills dans ton dossier `.claude/skills` et vérifie Python, Chrome et ffmpeg. Il ne supprime rien.

## 6. Vérifier
Ouvre une **nouvelle** conversation dans Claude Code, sur le dossier du kit, et écris :
> fais mes stories à la une

Claude doit lire `mes-donnees/ma-marque.md` et te poser les questions qui manquent. Si oui, c'est installé.

## Pour Claude (si on te donne ce dossier ou ce zip)
1. Lance l'installateur (`installer.ps1` sur Windows, `installer.sh` sur Mac) et lis ce qu'il affiche : si Python, Chrome ou ffmpeg manquent, donne le lien à la personne en une ligne.
2. Utilise ensuite le skill `plan-a-la-une` (point d'entrée), avec `mes-donnees/` comme source. Ne te connecte jamais à Instagram dans un navigateur, ne publie rien.

## Mettre à jour
Télécharge la nouvelle version, garde ton dossier `mes-donnees/` (copie-le dans le nouveau kit), puis relance l'étape 5.
