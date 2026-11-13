"""Screenshots of the live app for the landing page and the social preview.
Runs in GitHub Actions after every refresh, so the images always show the current week's data.
Usage: python tools/shots.py <site folder served at http://localhost:8000/>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

out = Path(sys.argv[1]); (out / "shots").mkdir(parents=True, exist_ok=True)
BASE = "http://localhost:8000/"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    pg.goto(BASE + "app.html")
    pg.evaluate("""localStorage.setItem('jp_theme', '"dark"'); localStorage.setItem('jp_ws', '"Borjan"')""")
    for view in ["today", "inbox", "customers", "competitors", "digest"]:
        pg.goto(BASE + "app.html#" + view); pg.reload(wait_until="networkidle"); pg.wait_for_timeout(2000)
        pg.screenshot(path=str(out / "shots" / f"{view}.jpg"), type="jpeg", quality=82)
        print("shot", view)
    og = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
    og.goto(BASE + "app.html"); og.evaluate("""localStorage.setItem('jp_theme', '"dark"')""")
    og.goto(BASE); og.reload(wait_until="networkidle"); og.wait_for_timeout(1500)
    og.screenshot(path=str(out / "preview.jpg"), type="jpeg", quality=85)
    b.close()
