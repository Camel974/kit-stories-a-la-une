"""Transcription mot a mot d'une video (pour les sous-titres des temoignages en story).

Usage :
    python tr.py video.mp4 [modele]      ->  video.words.json  [{"w": "mot", "s": debut_s, "e": fin_s}, ...]

Besoin (une seule fois) : pip install faster-whisper
Modele par defaut : "small" (bon en francais, rapide sur un PC normal). "medium" = plus precis, plus lent.
Relis toujours les chiffres : un montant mal entendu se corrige dans "corrections" du config.json de temoignage.py.
"""
import json, os, sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
video = sys.argv[1]
modele = sys.argv[2] if len(sys.argv) > 2 else "small"
try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit("Installe d'abord faster-whisper :  pip install faster-whisper")

m = WhisperModel(modele, device="cpu", compute_type="int8")
segments, _ = m.transcribe(video, language="fr", word_timestamps=True, vad_filter=True)
mots = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for seg in segments for w in (seg.words or []) if w.word.strip()]
sortie = os.path.splitext(video)[0] + ".words.json"
with open(sortie, "w", encoding="utf-8") as f:
    json.dump(mots, f, ensure_ascii=False, indent=0)
print(f"{len(mots)} mots -> {sortie}")
