"""Témoignage vidéo en story 9:16 premium : bandeau (prénom + chiffre), sous-titres mot à mot, dashboard incrusté.

Usage :
    python temoignage.py <config.json>

config.json :
{
  "video": "chemin/video.mp4",           # vidéo de l'élève (n'importe quel format, recadrée en 9:16)
  "mots": "lea.words.json",               # transcription mot a mot [{w,s,e}] : python tr.py video.mp4
  "corrections": {"2027": "2 800"},       # mots mal transcrits -> bon mot (optionnel)
  "prenom": "Léa",
  "chiffre": "[son vrai résultat, ex. 1re vente en 12 jours]",
  "dashboard": "chemin/dash.jpg",         # optionnel : capture recadrée sur le chiffre
  "dashboard_legende": "Son dashboard Stripe",
  "dashboard_de": 24.0, "dashboard_a": 31.0,
  "debut": 0, "fin": 60,                  # coupe (60 s max pour une story)
  "or": "#7C3AED", "fond": "#0B1020",     # couleur de la marque + fond sombre
  "sortie": "chemin/05-temoignage-lea.mp4"
}
Polices : Montserrat 800 + Inter 600, telechargees toutes seules dans ../fonts a la 1re utilisation (Fontsource, licence OFL).
Besoin : ffmpeg (https://ffmpeg.org/download.html) et Chrome ou Edge.
"""
import json, os, subprocess, sys, tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(ICI, "..", "fonts"))
sys.path.insert(0, ICI)
from gen import chrome  # même navigateur que gen.py

POLICES = {  # polices libres (SIL OFL 1.1), recuperees sur le CDN Fontsource si absentes
    "Montserrat-800.ttf": "https://cdn.jsdelivr.net/fontsource/fonts/montserrat@latest/latin-800-normal.ttf",
    "Inter-600.woff2": "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-600-normal.woff2",
}


def assure_polices():
    os.makedirs(FONTS, exist_ok=True)
    for f, url in POLICES.items():
        p = os.path.join(FONTS, f)
        if not os.path.exists(p):
            import urllib.request
            print("Téléchargement de la police", f, "...")
            urllib.request.urlretrieve(url, p)


def nom_police(chemin):
    """Nom complet de la police (table 'name', id 4), pour les sous-titres ffmpeg/libass."""
    import struct
    with open(chemin, "rb") as fh:
        d = fh.read()
    n = struct.unpack(">H", d[4:6])[0]
    for i in range(n):
        tag, _, off, _ = struct.unpack(">4sIII", d[12 + 16 * i: 28 + 16 * i])
        if tag == b"name":
            _, count, so = struct.unpack(">HHH", d[off:off + 6])
            noms = {}
            for j in range(count):
                pid, eid, lid, nid, ln, o = struct.unpack(">HHHHHH", d[off + 6 + 12 * j: off + 18 + 12 * j])
                raw = d[off + so + o: off + so + o + ln]
                txt = raw.decode("utf-16-be", "ignore") if pid in (0, 3) else raw.decode("latin-1", "ignore")
                if nid in (1, 4) and txt:
                    noms.setdefault(nid, txt)
            return noms.get(4) or noms.get(1) or "Montserrat"
    return "Montserrat"


MOTS_OR = ("€", "euros", "système", "systèmes", "ca", "mois", "clients", "vente", "ventes", "résultat", "résultats")


def html_overlay(cfg, quoi):
    o, f = cfg.get("or", "#C8A24B"), cfg.get("fond", "#0B1626")
    mont = "file:///" + os.path.join(FONTS, "Montserrat-800.ttf").replace("\\", "/")
    inter = "file:///" + os.path.join(FONTS, "Inter-600.woff2").replace("\\", "/")
    css = f"""@font-face{{font-family:M;src:url('{mont}')}}@font-face{{font-family:I;src:url('{inter}')}}
html,body{{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}}"""
    if quoi == "bandeau":
        corps = f"""<div style="position:absolute;inset:0 0 auto 0;height:640px;background:linear-gradient(180deg,{f} 0%,{f}e6 38%,{f}00 100%)"></div>
<div style="position:absolute;top:235px;left:60px;right:60px;text-align:center">
<div style="font:600 30px I;letter-spacing:6px;color:#F4F0E6;opacity:.85">{cfg.get('etiquette', 'TÉMOIGNAGE ÉLÈVE')}</div>
<div style="font:800 64px/1 M;color:#fff;margin-top:14px;text-transform:uppercase;letter-spacing:-1px">{cfg['prenom']}</div>
<div style="font:800 84px/1.02 M;color:{o};margin-top:10px;text-transform:uppercase;letter-spacing:-2px;text-shadow:0 0 34px {o}99,0 4px 18px #000a">{cfg['chiffre']}</div></div>"""
    else:
        img = "file:///" + os.path.abspath(cfg["dashboard"]).replace("\\", "/")
        corps = f"""<div style="position:absolute;left:150px;right:150px;top:1270px;padding:16px;border-radius:28px;background:{f}eb;border:5px solid {o};box-shadow:0 0 40px {o}88,0 16px 40px #000c;text-align:center">
<img src="{img}" style="width:100%;display:block;border-radius:16px">
<div style="font:800 34px M;color:{o};margin-top:12px;text-transform:uppercase">{cfg.get('dashboard_legende','')}</div></div>"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{corps}</body></html>"


def capture(html, out, nav):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1080,1920", "--default-background-color=00000000", "--virtual-time-budget=4000",
                    "--allow-file-access-from-files", f"--screenshot={out}", "file:///" + t.name.replace("\\", "/")],
                   capture_output=True)
    if not os.path.exists(out):
        sys.exit(f"ERREUR : overlay non généré ({out})")


def ass_time(t):
    t = max(0, t)
    return "%d:%02d:%05.2f" % (t // 3600, t % 3600 // 60, t % 60)


def sous_titres(cfg, out):
    W = json.load(open(cfg["mots"], encoding="utf-8"))
    corr = cfg.get("corrections", {})
    d0, d1 = cfg.get("debut", 0), cfg.get("fin", 60)
    # recolle les morceaux (« j 'ai », « ce mois -ci ») et applique les corrections
    toks = []
    for w in W:
        if w["s"] < d0 or w["s"] >= d1:
            continue
        txt = corr.get(w["w"], w["w"])
        if toks and (txt.startswith("'") or txt.startswith("-")):
            toks[-1]["w"] += txt
            toks[-1]["e"] = w["e"]
        else:
            toks.append({"w": txt, "s": w["s"] - d0, "e": w["e"] - d0})
    # blocs de 3 mots max, coupés aux ponctuations
    blocs, cur = [], []
    for t in toks:
        cur.append(t)
        if len(cur) >= 3 or t["w"].endswith((".", ",", "?", "!")):
            blocs.append(cur); cur = []
    if cur:
        blocs.append(cur)
    o = cfg.get("or", "#C8A24B").lstrip("#")
    bgr = "&H00%s%s%s&" % (o[4:6], o[2:4], o[0:2])
    da, db = cfg.get("dashboard_de", -1) - d0, cfg.get("dashboard_a", -1) - d0
    lignes = []
    for i, b in enumerate(blocs):
        s = b[0]["s"]
        e = blocs[i + 1][0]["s"] if i + 1 < len(blocs) else b[-1]["e"] + 0.4
        e = min(e, b[-1]["e"] + 0.6)
        if cfg.get("dashboard") and s < db and e > da:
            continue  # pendant le dashboard, pas de sous-titres
        mots = []
        for t in b:
            m = t["w"].strip(".,")
            if any(c.isdigit() for c in m) or m.lower() in MOTS_OR:
                mots.append("{\\c%s}%s{\\c&H00FFFFFF&}" % (bgr, t["w"]))
            else:
                mots.append(t["w"])
        lignes.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},S,,0,0,0,,{{\\fad(60,0)}}" + " ".join(mots).upper())
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,{POLICE_SOUS_TITRES},74,&H00FFFFFF,&H00FFFFFF,&H00261611,&H96000000,0,0,0,0,100,100,0,0,1,6,3,2,70,70,380,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(lignes) + "\n"
    open(out, "w", encoding="utf-8").write(ass)


POLICE_SOUS_TITRES = "Montserrat"


def main():
    global POLICE_SOUS_TITRES
    assure_polices()
    POLICE_SOUS_TITRES = nom_police(os.path.join(FONTS, "Montserrat-800.ttf"))
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    os.chdir(base)
    nav = chrome()
    tmp = os.path.join(base, "_tmp_" + cfg["prenom"].lower())
    os.makedirs(tmp, exist_ok=True)
    band = os.path.join(tmp, "bandeau.png"); capture(html_overlay(cfg, "bandeau"), band, nav)
    ass = os.path.join(tmp, "st.ass")
    if cfg.get("sous_titres", True):
        sous_titres(cfg, ass)
    d0, d1 = cfg.get("debut", 0), cfg.get("fin", 60)
    # les PNG doivent BOUCLER sur toute la durée, sinon une image fixe ne dure qu'1 frame (dashboard invisible)
    dur = str(d1 - d0)
    inputs = ["-ss", str(d0), "-to", str(d1), "-i", cfg["video"], "-loop", "1", "-t", dur, "-i", band]
    if cfg.get("fond_image"):
        # vidéo inutilisable à l'écran (enregistrement d'écran, vocal) : on garde le son, image premium en fond + lent zoom
        inputs += ["-loop", "1", "-t", dur, "-i", cfg["fond_image"]]
        n = inputs.count("-i") - 1  # index de l'entrée image
        fc = (f"[{n}:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,setsar=1,"
              f"zoompan=z='min(zoom+0.0004,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
              f"eq=brightness=-0.12:saturation=1.05[v0];[v0][1:v]overlay=0:0[v1]")
    else:
        fc = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
              "eq=contrast=1.04:saturation=1.05[v0];[v0][1:v]overlay=0:0[v1]")
    last = "v1"
    if cfg.get("dashboard"):
        dash = os.path.join(tmp, "dash.png"); capture(html_overlay(cfg, "dash"), dash, nav)
        inputs += ["-loop", "1", "-t", dur, "-i", dash]
        k = len([x for x in inputs if x == "-i"]) - 1
        a, b = cfg["dashboard_de"] - d0, cfg["dashboard_a"] - d0
        fc += (f";[{k}:v]format=rgba,fade=in:st={a}:d=0.25:alpha=1,fade=out:st={b-0.25}:d=0.25:alpha=1[dz];"
               f"[v1][dz]overlay=0:0:enable='between(t,{a},{b})'[v2]")
        last = "v2"
    fonts = FONTS.replace("\\", "/").replace(":", "\\:")
    assp = ass.replace("\\", "/").replace(":", "\\:")
    if cfg.get("sous_titres", True):  # false si la vidéo a déjà ses sous-titres incrustés
        fc += f";[{last}]subtitles='{assp}':fontsdir='{fonts}'[vout]"
    else:
        fc += f";[{last}]null[vout]"
    out = cfg["sortie"]
    if os.path.exists(out):
        os.remove(out)
    r = subprocess.run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", fc, "-map", "[vout]", "-map", "0:a?",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-shortest", "-pix_fmt", "yuv420p", "-r", "30",
                        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-movflags", "+faststart", out],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode or not os.path.exists(out):
        sys.exit("ERREUR ffmpeg :\n" + r.stderr[-2000:])
    print("OK", out, os.path.getsize(out), "octets")


if __name__ == "__main__":
    main()
