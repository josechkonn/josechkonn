import json, os, sys, urllib.request
from collections import Counter
USER = os.environ.get("GH_USER", "josechkonn")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
def api(path):
    r = urllib.request.Request("https://api.github.com" + path, headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(r))
repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
stars = sum(r["stargazers_count"] for r in repos)
try: commits = api(f"/search/commits?q=author:{USER}&per_page=1")["total_count"]
except Exception: commits = 0
langs = Counter()
for r in repos:
    try: langs.update(api(f"/repos/{USER}/{r['name']}/languages"))
    except Exception: pass
total = sum(langs.values()) or 1
langs.pop("Python", None)
total = sum(langs.values()) or 1
top = langs.most_common(6)
RED, BLK, WHT, GRY = "#FF1E1E", "#0A0A0A", "#FFFFFF", "#8A8A8A"
shades = ["#FF1E1E", "#D91616", "#B01010", "#8A0C0C", "#5E0808", "#3A0505"]
F = "font-family='JetBrains Mono,Menlo,Consolas,monospace'"
items = [("REPOS", len(repos)), ("COMMITS", commits), ("STARS", stars), ("LENGUAJES", len(langs))]
cards = ""
for i, (k, v) in enumerate(items):
    x = 20 + i * 195
    cards += f"<g transform='translate({x},20)'><path d='M0 0H165L180 15V90H15L0 75Z' fill='#111' stroke='{RED}' stroke-width='1.5'/><text x='20' y='42' fill='{GRY}' font-size='12' letter-spacing='2' {F}>{k}</text><text x='20' y='78' fill='{WHT}' font-size='32' font-weight='700' {F}>{v}</text></g>"
bar, legend, x = "", "", 20
for i, (l, b) in enumerate(top):
    w = 780 * b / sum(c for _, c in top)
    bar += f"<rect x='{x:.1f}' y='150' width='{w:.1f}' height='14' fill='{shades[i]}'/>"
    x += w
    lx = 20 + (i % 3) * 265; ly = 195 + (i // 3) * 24
    legend += f"<rect x='{lx}' y='{ly-10}' width='10' height='10' fill='{shades[i]}'/><text x='{lx+18}' y='{ly}' fill='{WHT}' font-size='13' {F}>{l} <tspan fill='{GRY}'>{100*b/total:.1f}%</tspan></text>"
svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='820' height='260' viewBox='0 0 820 260'><rect width='820' height='260' fill='{BLK}'/>{cards}<text x='20' y='138' fill='{RED}' font-size='12' letter-spacing='3' {F}>// LENGUAJES</text>{bar}{legend}</svg>"
os.makedirs("dist", exist_ok=True)
open("dist/stats.svg", "w").write(svg)
print("ok", len(repos), commits, stars, top)
