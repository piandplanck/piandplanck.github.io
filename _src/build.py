"""Pi & Planck site builder (standard library only).
Usage: python3 _src/build.py --out _site [--through YYYY-MM-DD]
Weekly publishing: shows only pieces dated on or before --through (default: the most recent Saturday, Pacific time)."""
import json, os, re, sys, shutil, html, datetime
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "_site"
PAL = {"bg": "#15171C", "panel": "#1F232B", "cu": "#FF9F68", "cy": "#7FD0FF", "br": "#F4D35E", "ink": "#F4F5F7", "gray": "#9AA3B2"}
if "--through" in sys.argv: through = sys.argv[sys.argv.index("--through") + 1]
else:
    d = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).date() - datetime.timedelta(days=1)
    while d.weekday() != 5: d -= datetime.timedelta(days=1)   # weekly: show everything up to the most recent Saturday
    through = d.isoformat()
ALL = json.load(open(HERE + "/data/pieces.json"))
pieces = sorted([p for p in ALL if p["date"] <= through], key=lambda p: p["date"], reverse=True)
if os.path.exists(OUT): shutil.rmtree(OUT)
for d in ("assets", "assets/img", "assets/fonts", "p"): os.makedirs(f"{OUT}/{d}")
open(OUT + "/.nojekyll", "w").write("")
shutil.copytree(HERE + "/assets", OUT + "/assets", dirs_exist_ok=True)
E = html.escape
SOC = [("X", "https://x.com/piandplanck"), ("Instagram", "https://www.instagram.com/piandplanck/"), ("Threads", "https://www.threads.com/@piandplanck"),
       ("Facebook", "https://www.facebook.com/profile.php?id=61595703724533"), ("GitHub", "https://github.com/piandplanck")]
CSS = f"""
@font-face{{font-family:'LM Roman';src:url(/assets/fonts/lmroman-bold.woff) format("woff");font-weight:700}}
:root{{--bg:{PAL['bg']};--panel:{PAL['panel']};--cu:{PAL['cu']};--cy:{PAL['cy']};--br:{PAL['br']};--ink:{PAL['ink']};--gray:{PAL['gray']}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--bg);color:var(--ink);font:18px/1.6 Inter,system-ui,sans-serif;
background-image:linear-gradient(rgba(154,163,178,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(154,163,178,.07) 1px,transparent 1px);background-size:32px 32px}}
a{{color:var(--cy)}}h1,h2,h3{{font-family:'LM Roman',Georgia,serif;font-weight:700;line-height:1.15;margin:0 0 .5em}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 20px}}
header.top{{border-bottom:1px solid #2a303b;background:rgba(21,23,28,.9);position:sticky;top:0;z-index:5;backdrop-filter:blur(6px)}}
header.top .wrap{{display:flex;align-items:center;gap:18px;height:64px}}
.brand{{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink);font-family:'LM Roman',serif;font-weight:700;font-size:26px}}
.brand img{{width:40px;height:40px;border-radius:50%}}.brand b{{color:var(--cu)}}
nav{{margin-left:auto;display:flex;gap:18px;font-size:16px}}nav a{{color:var(--gray);text-decoration:none}}nav a:hover{{color:var(--ink)}}
.hero{{padding:56px 0 30px;display:flex;gap:40px;align-items:center;flex-wrap:wrap}}
.hero img{{width:190px;height:190px;border-radius:50%;border:4px solid var(--cu)}}
.hero h1{{font-size:clamp(40px,7vw,72px)}}.hero h1 b{{color:var(--cu)}}
.tag{{color:var(--gray);font-size:22px}}.tag span{{color:var(--cy)}}
.chips{{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}}
.chips a{{background:var(--panel);border-left:5px solid var(--cu);padding:6px 14px;border-radius:8px;text-decoration:none;color:var(--ink);font-size:16px}}
.chips a:nth-child(2n){{border-color:var(--cy)}}.chips a:nth-child(3n){{border-color:var(--br)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:20px;margin:24px 0 60px}}
.card{{background:var(--panel);border-radius:14px;overflow:hidden;text-decoration:none;color:var(--ink);border-top:5px solid var(--cu);display:block;transition:transform .15s}}
.card:hover{{transform:translateY(-3px)}}.card img{{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}}
.card div{{padding:14px 18px 18px}}.card small{{color:var(--gray);font-size:14px;letter-spacing:.04em;text-transform:uppercase}}
.card h3{{font-size:23px;margin:.2em 0 0}}
.soon{{background:var(--panel);border-radius:14px;padding:34px;margin:24px 0 60px;border-left:6px solid var(--br)}}
.pic{{width:100%;border-radius:14px;border:2px solid #2a303b;display:block}}
.tabs{{display:flex;gap:8px;margin:20px 0}}.tabs button{{background:var(--panel);color:var(--ink);border:2px solid #2a303b;border-radius:10px;padding:8px 22px;font:600 16px Inter;cursor:pointer}}
.tabs button.on{{border-color:var(--cu);color:var(--cu)}}
.lang{{display:none}}.lang.on{{display:block}}.fa{{direction:rtl;text-align:right;font-family:Vazirmatn,Inter,sans-serif;line-height:1.9}}
.box{{background:var(--panel);border-radius:12px;padding:18px 22px;margin:18px 0;border-left:5px solid var(--cy)}}
.box h3{{font-size:21px}}ol.src{{padding-left:22px;color:var(--gray);font-size:15px}}.fa ol.src{{padding:0 22px 0 0}}
footer{{border-top:1px solid #2a303b;margin-top:40px;padding:28px 0 50px;color:var(--gray);font-size:15px}}
.meta{{color:var(--gray);font-size:15px;letter-spacing:.05em;text-transform:uppercase}}
"""
open(OUT + "/assets/style.css", "w").write(CSS)
def shell(title, desc, body, path="/", og="/assets/og.png"):
    soc = " · ".join(f'<a href="{u}">{n}</a>' for n, u in SOC)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="icon" href="/assets/favicon.png">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="https://piandplanck.github.io{og}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Vazirmatn:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="/"><img src="/assets/logo.png" alt="Pi &amp; Planck logo">Pi <b>&amp;</b> Planck</a>
<nav><a href="/archive.html">Archive</a><a href="/about.html">About</a></nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap">Pi &amp; Planck · @piandplanck · Measure everything. Start at π.<br>{soc}</div></footer></body></html>'''
def img_for(p, lang):
    for suf in ("", "_t"):
        shutil.copy(f"{HERE}/img/{p['id']}_{lang}{suf}.jpg", f"{OUT}/assets/img/{p['id']}_{lang}{suf}.jpg")
    return f"/assets/img/{p['id']}_{lang}.jpg", f"/assets/img/{p['id']}_{lang}_t.jpg"
def linkify(t): return re.sub(r"(https?://[^\s)]+)", r'<a href="\1">\1</a>', E(t))
def piece_page(p):
    en = img_for(p, "en"); fa = img_for(p, "fa"); slug = p["slug"]
    p["thumb"] = en[1]
    d = datetime.date.fromisoformat(p["date"]); ds = d.strftime("%B %-d, %Y")
    src = "".join(f"<li>{linkify(s)}</li>" for s in p["sources"])
    body = f'''<p class="meta">{E(p["topic"].split("(")[0].strip())} · {ds}</p>
<div class="tabs"><button class="on" data-l="en">English</button><button data-l="fa">فارسی</button></div>
<section class="lang on" id="en"><h1>{E(p["title"])}</h1><img class="pic" src="{en[0]}" alt="{E(p["alt"])}">
<div class="box"><h3>In short</h3><p>{E(p["caption"])}</p></div>
<div class="box" style="border-color:var(--br)"><h3>Sources</h3><ol class="src">{src}</ol></div></section>
<section class="lang fa" id="fa"><h1>{E(p["title_fa"])}</h1><img class="pic" src="{fa[0]}" alt="{E(p["alt_fa"])}">
<div class="box"><h3>خلاصه</h3><p>{E(p["caption_fa"])}</p></div>
<div class="box" style="border-color:var(--br)"><h3>منابع</h3><ol class="src" style="direction:ltr;text-align:left">{src}</ol></div></section>
<p><a href="/archive.html">← All posts</a></p>
<script>const b=document.querySelectorAll('.tabs button');function s(l){{b.forEach(x=>x.classList.toggle('on',x.dataset.l==l));document.querySelectorAll('.lang').forEach(x=>x.classList.toggle('on',x.id==l));history.replaceState(null,'','#'+l)}}
b.forEach(x=>x.onclick=()=>s(x.dataset.l));if(location.hash=='#fa')s('fa')</script>'''
    os.makedirs(f"{OUT}/p/{slug}"); open(f"{OUT}/p/{slug}/index.html", "w").write(shell(p["title"] + " | Pi & Planck", p["caption"], body, og=en[0]))
for p in pieces: piece_page(p)
def card(p):
    d = datetime.date.fromisoformat(p["date"]).strftime("%b %-d")
    return f'<a class="card" href="/p/{p["slug"]}/"><img src="{p["thumb"]}" alt="" loading="lazy"><div><small>{E(p["topic"].split("(")[0].strip())} · {d}</small><h3>{E(p["title"])}</h3></div></a>'
chips = "".join(f'<a href="{u}">{n}</a>' for n, u in SOC)
if pieces:
    latest = f'<h2>Latest</h2><div class="grid">{"".join(card(p) for p in pieces[:6])}</div><p><a href="/archive.html">See all {len(pieces)} posts →</a></p>'
else:
    latest = '<div class="soon"><h2>The first posts arrive soon</h2><p>Daily math and physics infographics, in English and Farsi. Follow an account below and check back: this page is updated every Sunday with the week’s posts.</p></div>'
home = f'''<section class="hero"><img src="/assets/logo.png" alt="Pi &amp; Planck atom-pi logo"><div>
<h1>Pi <b>&amp;</b> Planck</h1><div class="tag"><span>Math</span> &amp; <span>physics</span>, drawn. Measure everything. Start at π.</div>
<div class="chips">{chips}</div></div></section>{latest}
<div class="box"><h3>What you will find here</h3><p>A new infographic every day: problems with checked solutions, new discoveries, history, and how big or small things really are. Every post has a sourced write-up in English and فارسی.</p></div>'''
open(OUT + "/index.html", "w").write(shell("Pi & Planck: math & physics, drawn", "Daily math and physics infographics in English and Farsi. Measure everything. Start at π.", home))
arch = "<h1>Archive</h1>" + (f'<div class="grid">{"".join(card(p) for p in pieces)}</div>' if pieces else "<p>Nothing here yet. The first week’s posts will appear after the first Sunday update.</p>")
open(OUT + "/archive.html", "w").write(shell("Archive | Pi & Planck", "All Pi & Planck posts.", arch))
about = f'''<h1>About</h1><div class="box"><p>Pi &amp; Planck is a daily math and physics account: one infographic a day, in English and Farsi, built from primary sources (journals, arXiv with status stated, university and observatory pages, NASA, CERN, NIST, MacTutor). Numbers are recomputed in code before they are published.</p>
<p>The name joins π, the constant of the circle, with Planck, the scale where known physics runs out.</p></div>
<div class="box" style="border-color:var(--cu)"><h3>Find us</h3><div class="chips">{chips}</div></div>'''
open(OUT + "/about.html", "w").write(shell("About | Pi & Planck", "About Pi & Planck.", about))
open(OUT + "/404.html", "w").write(shell("Not found | Pi & Planck", "Page not found", '<h1>Page not found</h1><p><a href="/">Back to the home page</a></p>'))
open(OUT + "/robots.txt", "w").write("User-agent: *\nAllow: /\n")
n = sum(len(fs) for _, _, fs in os.walk(OUT)); print("through", through, "pieces", len(pieces), "files", n)
