"""Screenshots of the live app for the home page and the social preview.
Runs in GitHub Actions after every refresh, so the images always show the current week's data.
Makes a dark and a light set: full screens for the hero tour, and close crops for the feature rows.
Usage: python tools/shots.py <site folder served at http://localhost:8000/>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(sys.argv[1])
BASE = "http://localhost:8000/"
BRAND = "Borjan"
# feature crops: (view, CSS selector of the part to show, max height in CSS px)
CROPS = [("inbox", ".inbox", 620), ("competitors", ".panel", 560), ("customers", ".tiles", 560), ("digest", ".mail", 640)]


def go(pg, view):
    pg.goto(BASE + "app.html#" + view)
    pg.reload(wait_until="networkidle")
    pg.evaluate("document.fonts.ready")   # shoot only after the web fonts are in, or spacing comes out wrong
    pg.wait_for_timeout(2500)


with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ["dark", "light"]:
        d = out / "shots" / theme
        d.mkdir(parents=True, exist_ok=True)
        pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.25)
        pg.goto(BASE + "app.html")
        pg.evaluate(f"""localStorage.setItem('jp_theme', '"{theme}"'); localStorage.setItem('jp_ws', '"{BRAND}"');
                        localStorage.setItem('jp_seen', JSON.stringify({{}})); localStorage.setItem('jp_toured', 'true')""")
        for view in ["today", "inbox", "competitors", "digest"]:
            go(pg, view)
            pg.screenshot(path=str(d / f"{view}.jpg"), type="jpeg", quality=80)
            print("shot", theme, view)
        pg.close()
        pg = b.new_page(viewport={"width": 1340, "height": 1700}, device_scale_factor=1.5)
        pg.goto(BASE + "app.html")
        pg.evaluate(f"""localStorage.setItem('jp_theme', '"{theme}"'); localStorage.setItem('jp_ws', '"{BRAND}"'); localStorage.setItem('jp_toured', 'true')""")
        for view, sel, max_h in CROPS:
            go(pg, view)
            pg.add_style_tag(content=".topbar, .tabbar, .toast { display: none !important; } * { animation: none !important; transition: none !important; }")
            pg.wait_for_timeout(300)
            box = pg.locator(sel).first.bounding_box()
            pad = 14
            clip = {"x": max(box["x"] - pad, 0), "y": max(box["y"] - pad, 0), "width": box["width"] + 2 * pad,
                    "height": min(box["height"], max_h) + 2 * pad}
            pg.screenshot(path=str(d / f"crop-{view}.jpg"), type="jpeg", quality=82, clip=clip)
            print("crop", theme, view)
        pg.close()
    og = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
    og.goto(BASE)
    og.evaluate("""localStorage.setItem('jp_theme', '"dark"')""")
    og.reload(wait_until="networkidle")
    og.evaluate("document.fonts.ready")
    og.wait_for_timeout(2500)
    og.screenshot(path=str(out / "preview.jpg"), type="jpeg", quality=85)
    b.close()
