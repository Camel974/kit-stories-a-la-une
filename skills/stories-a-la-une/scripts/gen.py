"""Stories à la une : une page HTML par story (1080x1920), capturée en PNG par Chrome (ou Edge) headless.

Usage :
    python gen.py <dossier_projet>                 # toutes les stories
    python gen.py <dossier_projet> 01-couverture   # une seule (échantillon)

Le dossier projet contient :
    stories.json   la marque + les stories (voir exemple/stories.json)
    photos/        les photos de fond
Sortie : <dossier_projet>/png/*.png + planche.jpg (aperçu côte à côte, si Pillow est installé).
Contrôle automatique : le texte doit rester dans la zone utile (y 250 → 1600, marges 90 px), sinon ALERTE.
"""
import json, os, re, shutil, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.normpath(os.path.join(ICI, "..", "fonts"))
POLICES_LOCALES = {  # polices libres (OFL) : utilisees si leurs fichiers sont dans ../fonts, sinon Google Fonts
    "space grotesk": [("SpaceGrotesk-700.woff2", 700)],
    "inter": [("Inter-600.woff2", 600), ("Inter-800.woff2", 800)],
}
ZONE_HAUT, ZONE_BAS, MARGE = 250, 1600, 90


def chrome():
    cands = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
             r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    for p in cands:
        if os.path.exists(p):
            return p
    for n in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]:
        if shutil.which(n):
            return shutil.which(n)
    sys.exit("ERREUR : ni Chrome ni Edge trouvé. Installe Google Chrome puis relance.")


# ---------- couleurs dérivées de la couleur de la marque ----------
def hex2rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in c)


def melange(c, avec, t):
    return tuple(a + (b - a) * t for a, b in zip(c, avec))


def luminance(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def palette(m):
    c = hex2rgb(m["couleur"])
    blanc, noir = (255, 255, 255), (0, 0, 0)
    fond = hex2rgb(m["fond"]) if m.get("fond") else melange(c, noir, 0.88)
    # sur fond sombre, la couleur doit rester lisible : on l'éclaircit pour les titres et les mots clés
    eclair = 0.0 if luminance(c) > 0.35 else 0.3
    p = {
        "c": rgb2hex(c),
        "titre": m.get("couleur_titre") or rgb2hex(melange(c, blanc, eclair)),
        "mot": m.get("couleur_mots") or rgb2hex(melange(c, blanc, eclair + 0.12)),
        "pale": rgb2hex(melange(c, blanc, 0.78)),
        "sous": rgb2hex(melange(c, blanc, 0.93)),
        "fond": rgb2hex(fond),
        "rgb": "%d,%d,%d" % c,
        "frgb": "%d,%d,%d" % tuple(round(v) for v in fond),
        # texte posé SUR la couleur (pastille, case preuve) : blanc, ou noir si la couleur est très claire
        # choix au contraste réel (WCAG) : l'or/jaune moyen (lum ~0.4) donnait du blanc illisible avec un seuil fixe à 0.5
        "sur_c": "#111111" if (luminance(c) + 0.05) / 0.0559 > 1.05 / (luminance(c) + 0.05) else "#FFFFFF",
    }
    return p


# ---------- polices ----------
def polices(m):
    """Renvoie (css @font-face / @import, famille titre, famille texte)."""
    css, imports = "", []
    out = []
    for cle, defaut in (("police_titre", "Space Grotesk"), ("police_texte", "Inter")):
        nom = m.get(cle) or defaut
        fichier = m.get(cle + "_fichier")
        alias = "T" if cle == "police_titre" else "X"
        if fichier:  # police de la marque fournie en fichier (ttf, otf, woff2)
            url = fichier.replace("\\", "/")
            for w in (600, 700, 800):
                css += "@font-face{font-family:%s;src:url('%s');font-weight:%d}\n" % (alias, url, w)
            out.append(alias)
        elif nom.lower() in POLICES_LOCALES and all(os.path.exists(os.path.join(FONTS, f)) for f, _ in POLICES_LOCALES[nom.lower()]):
            for f, w in POLICES_LOCALES[nom.lower()]:
                url = "file:///" + os.path.join(FONTS, f).replace("\\", "/")
                css += "@font-face{font-family:%s;src:url('%s');font-weight:%d}\n" % (alias, url, w)
            out.append(alias)
        else:  # Google Fonts (connexion internet nécessaire)
            imports.append("family=" + nom.replace(" ", "+") + ":wght@600;700;800")
            out.append("'%s'" % nom)
    if imports:
        css = "@import url('https://fonts.googleapis.com/css2?%s&display=block');\n" % "&".join(imports) + css
    return css, out[0], out[1]


def feuille(m):
    p = palette(m)
    fcss, T, X = polices(m)
    maj = "uppercase" if m.get("majuscules", True) else "none"
    return fcss + f"""
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{p['fond']}}}
.bg{{position:absolute;left:0;top:0;width:1080px;height:auto;filter:brightness(.82) saturate(.95);transform:translateY(var(--dy,0px));-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 420px)}}
.vide{{position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 100%,rgba({p['rgb']},.55),transparent 70%),{p['fond']}}}
.voile{{position:absolute;inset:0;background:linear-gradient(180deg,{p['fond']} 0%,rgba({p['frgb']},.9) calc(var(--dy,0px) + 60px),rgba({p['frgb']},.35) calc(var(--dy,0px) + 380px),rgba({p['frgb']},.05) 78%,rgba({p['frgb']},.35) 100%)}}
.z{{position:absolute;left:{MARGE}px;right:{MARGE}px;top:280px;text-align:center;color:#fff}}
.sur{{font:700 56px/1.08 {T};letter-spacing:-1px;text-transform:{maj};color:{p['sous']}}}
.titre{{font:700 132px/.95 {T};letter-spacing:-4px;text-transform:{maj};color:{p['titre']};margin-top:26px;
       text-shadow:0 0 40px rgba({p['rgb']},.55),0 6px 24px rgba(0,0,0,.5)}}
.txt{{font:600 40px/1.38 {X};margin-top:44px;text-shadow:0 2px 12px rgba(0,0,0,.7)}}
.pill{{display:inline-block;background:{p['c']};color:{p['sur_c']};font-weight:800;padding:0 16px 4px;border-radius:12px;box-shadow:0 6px 20px rgba({p['rgb']},.45)}}
.v{{color:{p['mot']};font-weight:800}}
.liste{{margin:50px auto 0;text-align:left;display:inline-block;max-width:900px}}
.it{{display:flex;gap:28px;align-items:flex-start;font:600 40px/1.35 {X};margin-bottom:38px;text-shadow:0 2px 12px rgba(0,0,0,.7)}}
.it b{{font-weight:800}}
.sl{{text-decoration:underline;text-decoration-color:{p['c']};text-decoration-thickness:5px;text-underline-offset:9px}}
.num{{flex:none;width:74px;font:700 96px/.9 {T};color:{p['titre']};text-shadow:0 0 30px rgba({p['rgb']},.5)}}
.pt{{flex:none;width:18px;height:18px;border-radius:50%;background:{p['c']};margin-top:18px;box-shadow:0 0 14px rgba({p['rgb']},.8)}}
.preuve{{display:inline-flex;align-items:center;gap:24px;margin-top:40px;padding:18px 34px 20px;border-radius:24px;background:rgba({p['rgb']},.28);border:3px solid {p['c']};box-shadow:0 10px 30px rgba(0,0,0,.35),0 0 30px rgba({p['rgb']},.35);text-align:left}}
.preuve .big{{font:700 96px/1 {T};letter-spacing:-3px;color:#fff;text-shadow:0 0 24px rgba({p['rgb']},.8)}}
.preuve .lab{{font:700 36px/1.2 {X};color:#fff}}
.preuve .lab small{{display:block;font:600 28px/1.3 {X};color:{p['pale']};margin-top:4px}}
.trait{{width:780px;height:5px;margin:22px auto 0;border-radius:3px;background:#fff;box-shadow:0 0 14px rgba(255,255,255,.95),0 0 34px rgba(255,255,255,.6)}}
.dm{{font:700 170px/1 {T};letter-spacing:-5px;color:{p['titre']};margin-top:70px;text-shadow:0 0 50px rgba({p['rgb']},.6),0 6px 24px rgba(0,0,0,.5)}}
"""


MESURE = """<script>
document.fonts.ready.then(()=>{const z=document.querySelector('.z'),r=z.getBoundingClientRect();
let bas=r.bottom,gauche=r.left,droite=r.right;
z.querySelectorAll('*').forEach(e=>{const b=e.getBoundingClientRect();if(!b.width)return;
bas=Math.max(bas,b.bottom);gauche=Math.min(gauche,b.left);droite=Math.max(droite,b.right);});
const casse=[];z.querySelectorAll('.dm,.pill,.big,.num').forEach(e=>{const fs=parseFloat(getComputedStyle(e).fontSize);
if(e.getBoundingClientRect().height>fs*1.6)casse.push(e.className+' « '+e.textContent.trim().slice(0,30)+' »');});
z.querySelectorAll('*').forEach(e=>{if(e.scrollWidth>e.clientWidth+2&&e.clientWidth>0){const rr=e.getBoundingClientRect();
gauche=Math.min(gauche,rr.left);droite=Math.max(droite,rr.left+e.scrollWidth);}});
document.body.setAttribute('data-casse',casse.join(' | '));
document.body.setAttribute('data-mesure',[Math.round(r.top),Math.round(bas),Math.round(gauche),Math.round(droite)].join(','));});
</script>"""


def page(css, photo, corps, dy, mesure=False):
    if photo:
        fond = f'<img class="bg" style="--dy:{dy}px" src="{photo}"><div class="voile" style="--dy:{dy}px"></div>'
    else:
        fond = '<div class="vide"></div>'
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body>'
            f'{fond}<div class="z">{corps}</div>{MESURE if mesure else ""}</body></html>')


def lancer(nav, args):
    return subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                           "--window-size=1080,1920", "--virtual-time-budget=8000", "--allow-file-access-from-files"] + args,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    proj = os.path.abspath(sys.argv[1])
    cfg = json.load(open(os.path.join(proj, "stories.json"), encoding="utf-8"))
    css = feuille(cfg["marque"])
    nav = chrome()
    os.makedirs(os.path.join(proj, "png"), exist_ok=True)
    os.makedirs(os.path.join(proj, "html"), exist_ok=True)
    filtre = sys.argv[2:]
    faits, alertes = [], []
    for s in cfg["stories"]:
        nom = s["nom"]
        if filtre and nom not in filtre:
            continue
        photo = ""
        if s.get("photo"):
            chemin = os.path.join(proj, "photos", s["photo"])
            if not os.path.exists(chemin):
                sys.exit(f"ERREUR : photo introuvable pour {nom} : {chemin}")
            photo = "file:///" + chemin.replace("\\", "/")
        dy = s.get("dy", 0)
        h = os.path.join(proj, "html", f"{nom}.html")
        # 1) mesure du texte (zone utile)
        open(h, "w", encoding="utf-8").write(page(css, photo, s["html"], dy, mesure=True))
        dom = lancer(nav, ["--dump-dom", "file:///" + h.replace("\\", "/")]).stdout
        m = re.search(r'data-mesure="(-?\d+),(-?\d+),(-?\d+),(-?\d+)"', dom)
        if m:
            haut, bas, g, d = map(int, m.groups())
            if bas > ZONE_BAS:
                alertes.append(f"{nom} : le texte descend jusqu'à y={bas} (max {ZONE_BAS}). Raccourcis ou réduis.")
            if g < MARGE - 2 or d > 1080 - MARGE + 2:
                alertes.append(f"{nom} : le texte déborde sur les côtés ({g} → {d}). Raccourcis les lignes ou ajoute <br>.")
        c = re.search(r'data-casse="([^"]+)"', dom)
        if c:
            alertes.append(f"{nom} : passe sur 2 lignes alors que ça doit tenir sur 1 : {c.group(1)}. Raccourcis ou baisse la taille (style=\"font-size:…\").")
        if not m:
            alertes.append(f"{nom} : mesure impossible (vérifie l'image à l'œil).")
        # 2) capture
        open(h, "w", encoding="utf-8").write(page(css, photo, s["html"], dy))
        out = os.path.join(proj, "png", f"{nom}.png")
        # l'ancien PNG est supprimé AVANT la capture : sinon une capture ratée en silence garde l'ancienne image
        # et le script dit « OK » (bug vu le 08/11/2026). Une 2e tentative si la 1re échoue.
        for _ in range(2):
            if os.path.exists(out):
                os.remove(out)
            lancer(nav, [f"--screenshot={out}", "file:///" + h.replace("\\", "/")])
            if os.path.exists(out) and os.path.getsize(out) > 0:
                break
        if not os.path.exists(out):
            sys.exit(f"ERREUR : capture ratée pour {nom}.")
        faits.append(out)
        print("OK", nom, os.path.getsize(out), "octets")
    # 3) planche (aperçu côte à côte de toutes les stories)
    try:
        from PIL import Image
        tous = [os.path.join(proj, "png", f"{s['nom']}.png") for s in cfg["stories"]]
        tous = [t for t in tous if os.path.exists(t)]
        if tous:
            w = 300
            pl = Image.new("RGB", (w * len(tous), 533), "black")
            for i, t in enumerate(tous):
                pl.paste(Image.open(t).convert("RGB").resize((w, 533)), (i * w, 0))
            pl.save(os.path.join(proj, "planche.jpg"), quality=88)
            print("Planche :", os.path.join(proj, "planche.jpg"))
    except ImportError:
        print("(Pillow absent : pas de planche. pip install pillow pour l'avoir.)")
    for a in alertes:
        print("ALERTE", a)
    if not alertes:
        print("Zone utile : OK pour toutes les stories générées.")


if __name__ == "__main__":
    main()
