"""Icones de stories a la une : fond plein a la couleur de la marque, pictogramme blanc au trait arrondi, sans texte.
Toutes dans le meme style (Instagram les affiche en rond). Rendu par Chrome ou Edge headless, aucune IA d'image.

Usage :
    python icone.py <couleur_hex> <picto[:Nom]> [<picto[:Nom]> ...] [--dossier sortie] [--sans-etincelle] [--fond-degrade]

Exemple :
    python icone.py "#7C3AED" methode:"Ma méthode" temoignages:"Avis" resultats faq commencer:"Commencer" --dossier png

Pictos : methode, temoignages, resultats, qui, faq, offre, pourqui, commencer, coulisses, contact, preuves, etapes,
         gratuit, avant-apres, routine, outils
Sortie : icone-<picto>.png (1080x1080) pour chaque picto + planche-profil.png (apercu de la ligne du profil).
"""
import os, shutil, subprocess, sys, tempfile

# Pictogrammes dessines sur une grille 24x24 (trait blanc, bouts arrondis). Dessins originaux, libres.
PICTOS = {
    "methode": '<path d="M12 7c-1.8-1.3-4.3-2-7-2v12c2.7 0 5.2.7 7 2 1.8-1.3 4.3-2 7-2V5c-2.7 0-5.2.7-7 2z"/><path d="M12 7v12"/>',
    "temoignages": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H11l-4 3.5V16h-.5A2.5 2.5 0 0 1 4 13.5z"/><path d="M12 7.3l1 2 2.2.3-1.6 1.5.4 2.2-2-1-2 1 .4-2.2-1.6-1.5 2.2-.3z"/>',
    "resultats": '<path d="M4 20h16"/><path d="M6 16l4-4 3 3 5-6"/><path d="M15 9h3v3"/>',
    "qui": '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c.6-3.8 3.4-6 7-6s6.4 2.2 7 6"/>',
    "faq": '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1.1.9-1.1 1.6v.7"/><path d="M12 16.9v.1"/>',
    "offre": '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M3 9h18"/><path d="M12 9v11"/><path d="M12 9c-1.5-3.5-5-4-5-1.5S10 9 12 9c2 0 5-.2 5-1.5S13.5 5.5 12 9z"/>',
    "pourqui": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "commencer": '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
    "coulisses": '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M4 9l2-4.5h14L18 9"/><path d="M9 4.5L7.5 9M14 4.5L12.5 9M19 4.5L17.5 9"/>',
    "contact": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H11l-4 3.5V16h-.5A2.5 2.5 0 0 1 4 13.5z"/><path d="M8.5 10h.01M12 10h.01M15.5 10h.01"/>',
    "preuves": '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5.5a2.5 2.5 0 0 0 2.6 3.6M16 6h2.5a2.5 2.5 0 0 1-2.6 3.6"/><path d="M12 13v3.5"/><path d="M8.5 20h7l-.8-3.5H9.3z"/>',
    "etapes": '<path d="M4 19h5v-5h5V9h5V4"/>',
    "gratuit": '<path d="M20 12l-8 8-8-8V4h8z"/><circle cx="8" cy="8" r="1.3"/>',
    "avant-apres": '<rect x="3.5" y="5" width="7" height="14" rx="1.5"/><rect x="13.5" y="5" width="7" height="14" rx="1.5"/><path d="M11.5 12h1"/>',
    "routine": '<circle cx="12" cy="13" r="7.5"/><path d="M12 9v4l2.5 2"/><path d="M9.5 3.5h5"/>',
    "outils": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.4 2.4-2.6-.6-.6-2.6z"/>',
}
ETINCELLE = '<path d="M20.6 1.2l.5 1.6 1.6.5-1.6.5-.5 1.6-.5-1.6-1.6-.5 1.6-.5z" fill="#fff" stroke="none"/>'


def chrome():
    cands = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
             os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    for p in cands:
        if os.path.exists(p):
            return p
    for n in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]:
        if shutil.which(n):
            return shutil.which(n)
    sys.exit("ERREUR : ni Chrome ni Edge trouvé. Installe Google Chrome puis relance.")


def melange(hexa, avec, t):
    h = hexa.lstrip("#")
    c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    a = [int(avec.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(c[i] + (a[i] - c[i]) * t) for i in range(3))


def svg(picto, etincelle, taille):
    return (f'<svg viewBox="0 0 24 24" width="{taille}" height="{taille}" fill="none" stroke="#fff" stroke-width="1.55" '
            f'stroke-linecap="round" stroke-linejoin="round"><g transform="translate(0.6 1.6) scale(.86)">{PICTOS[picto]}</g>'
            f'{ETINCELLE if etincelle else ""}</svg>')


def capture(nav, html, out, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(html)
    if os.path.exists(out):
        os.remove(out)
    subprocess.run([nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={w},{h}",
                    "--virtual-time-budget=2000", f"--screenshot={os.path.abspath(out)}", "file:///" + t.name.replace("\\", "/")], capture_output=True)
    os.remove(t.name)
    if not os.path.exists(out):
        sys.exit(f"ERREUR : capture ratée pour {out}")


def main():
    opts = sys.argv[1:]
    args, saute = [], False
    for i, a in enumerate(opts):  # la valeur qui suit --dossier n'est pas un picto
        if saute:
            saute = False
            continue
        if a == "--dossier":
            saute = True
            continue
        if not a.startswith("--"):
            args.append(a)
    if len(args) < 2 or not args[0].startswith("#"):
        sys.exit(__doc__)
    couleur, items = args[0], []
    for a in args[1:]:
        p, _, nom = a.partition(":")
        if p not in PICTOS:
            sys.exit(f"Picto inconnu : {p}. Choix : {', '.join(PICTOS)}")
        items.append((p, nom or p.capitalize()))
    dossier = opts[opts.index("--dossier") + 1] if "--dossier" in opts else "."
    os.makedirs(dossier, exist_ok=True)
    etincelle = "--sans-etincelle" not in opts
    fond = (f"radial-gradient(circle at 35% 30%, {melange(couleur, '#ffffff', .18)}, {couleur} 55%, {melange(couleur, '#000000', .25)})"
            if "--fond-degrade" in opts else couleur)
    nav = chrome()
    for p, _ in items:
        html = (f"<!doctype html><html><body style='margin:0;width:1080px;height:1080px;background:{fond};display:grid;place-items:center'>"
                f"{svg(p, etincelle, 560)}</body></html>")
        out = os.path.join(dossier, f"icone-{p}.png")
        capture(nav, html, out, 1080, 1080)
        print("icône :", out)
    # Apercu de la ligne des stories a la une sur le profil (ronds + noms).
    ronds = "".join(f"<div style='text-align:center;width:150px'><div style='width:122px;height:122px;margin:0 auto;border-radius:50%;padding:4px;"
                    f"border:2px solid #3a3a3a'><div style='width:100%;height:100%;border-radius:50%;background:{fond};display:grid;place-items:center'>"
                    f"{svg(p, etincelle, 64)}</div></div><div style='font:500 22px Arial,sans-serif;color:#f5f5f5;margin-top:10px;white-space:nowrap;"
                    f"overflow:hidden;text-overflow:ellipsis'>{nom}</div></div>" for p, nom in items)
    w = max(600, 60 + 160 * len(items))
    html = f"<!doctype html><html><body style='margin:0;background:#000;width:{w}px;height:260px;display:flex;gap:10px;padding:40px 30px;box-sizing:border-box'>{ronds}</body></html>"
    capture(nav, html, os.path.join(dossier, "planche-profil.png"), w, 260)
    print("aperçu du profil :", os.path.join(dossier, "planche-profil.png"))


if __name__ == "__main__":
    main()
