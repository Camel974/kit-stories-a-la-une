#!/bin/bash
# Installe le Kit Stories à la une SYSTEM (Mac / Linux). Lancer depuis le dossier du kit :  bash installer.sh
# Ne supprime rien. Les skills du kit sont mis à jour ; un skill externe déjà présent chez toi est gardé tel quel.
set -e
KIT="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"
mkdir -p "$DEST"
MAISON=" plan-a-la-une stories-a-la-une icones-a-la-une "

for d in "$KIT"/skills/*/; do
  n="$(basename "$d")"
  if [ -d "$DEST/$n" ] && [[ "$MAISON" != *" $n "* ]]; then echo "garde   $n (déjà installé chez toi)"; continue; fi
  if [ -d "$DEST/$n" ]; then cp -R "$d". "$DEST/$n/"; echo "à jour  $n"; else cp -R "$d" "$DEST/$n"; echo "ajouté  $n"; fi
done

if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then echo "Python : OK"; else
  echo; echo "[À FAIRE] Installe Python 3 : https://www.python.org/downloads/ puis relance ce script."; fi
if [ -d "/Applications/Google Chrome.app" ] || [ -d "/Applications/Microsoft Edge.app" ] || command -v google-chrome >/dev/null 2>&1 || command -v chromium >/dev/null 2>&1; then echo "Navigateur : OK"; else
  echo "[À FAIRE] Installe Google Chrome : https://www.google.com/chrome/"; fi
if command -v ffmpeg >/dev/null 2>&1; then echo "ffmpeg : OK"; else echo "[Optionnel, témoignages vidéo] Installe ffmpeg : brew install ffmpeg"; fi
mkdir -p "$KIT/mes-donnees/a-publier"
echo; echo "Kit Stories à la une installé. Remplis mes-donnees/ma-marque.md, mets tes photos dans mes-donnees/photos,"
echo "puis ouvre une NOUVELLE conversation Claude Code sur ce dossier et écris : fais mes stories à la une"
