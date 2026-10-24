#!/usr/bin/env python3
"""Render index.html and assets/logos.css from tools/content.py. Run: python3 tools/build.py"""
import html
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402
from art import EXP, PROJECT_ART  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS = json.load(open(os.path.join(ROOT, "tools", "logos.json")))
NAMES = {"openjdk": "Java", "gnubash": "Bash", "apachegroovy": "Groovy", "nodedotjs": "Node.js", "nextdotjs": "Next.js",
         "cplusplus": "C++", "modelcontextprotocol": "MCP", "framer": "Framer Motion", "githubactions": "GitHub Actions",
         "googlecloud": "Google Cloud", "html5": "HTML", "reactnative": "React Native", "postgresql": "PostgreSQL"}
GENERIC = {"tree", "devices", "mic", "film", "pdf", "stream", "lock", "trophy", "cap", "phone", "globe", "card", "shield"}
e = html.escape


def name(slug):
    return NAMES.get(slug, LOGOS[slug]["title"])


def logo(slug, cls="lg"):
    if slug not in LOGOS:
        raise SystemExit(f"unknown logo: {slug}")
    return f'<svg class="{cls}" data-l="{slug}" aria-hidden="true"><use href="assets/logos.svg#{slug}"/></svg>'


def tags(items, cls="tags"):
    out = []
    for t in items:
        slug, label = (t if isinstance(t, tuple) else (t, name(t)))
        out.append(f'<li>{logo(slug)}<span>{e(label)}</span></li>')
    return f'<ul class="{cls}">{"".join(out)}</ul>'


def ext(href, label, cls="btn btn-ghost", icon=None, trailing=None):
    lead = logo(icon, "lg lg-btn") if icon else ""
    tail = logo(trailing, "lg lg-btn") if trailing else ""
    return f'<a class="{cls}" href="{e(href)}" target="_blank" rel="noopener noreferrer">{lead}{e(label)}{tail}</a>'


def img(src, w, h, alt, cls="", lazy=True):
    load = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}" width="{w}" height="{h}" alt="{e(alt)}"{load}>'


def phones(shots, cls="phones"):
    figs = "".join(f'<figure class="phone">{img(*s)}</figure>' for s in shots)
    return f'<div class="{cls}">{figs}</div>'


def browser(shot, url):
    return (f'<div class="browser"><div class="bbar" aria-hidden="true"><i></i><i></i><i></i><span>{e(url)}</span></div>'
            f'{img(*shot)}</div>')


def media(p):
    kind, val = p["media"]
    if kind == "art":
        return f'<div class="media media-art">{PROJECT_ART[val]}</div>'
    if kind == "phones":
        return f'<div class="media media-phones">{phones(val)}</div>'
    return f'<div class="media media-browser">{browser(val, "github.com/homeo26/" + p.get("name", p["repo"]))}</div>'


# ---------------------------------------------------------------- sections
def hero():
    stats = "".join(f'<div><dt>{e(lbl)}</dt><dd data-count="{n}" data-suffix="{e(sfx)}">{e(txt)}</dd></div>'
                    for txt, n, sfx, lbl in C.HERO_STATS)
    orbit = "".join(f'<span class="orb" title="{e(name(s))}">{logo(s)}</span>' for s in C.ORBIT)
    lines = []
    for kind, val in C.TERMINAL:
        if kind == "cmd":
            lines.append(f'<span class="ln"><span class="p">$</span> <span class="cmd">{e(val)}</span></span>')
        elif kind == "out":
            lines.append(f'<span class="ln out">{e(val)}</span>')
        elif kind == "dirs":
            lines.append('<span class="ln out">' + "  ".join(f"<b>{e(d)}</b>" for d in val) + "</span>")
        else:
            lines.append(f'<span class="ln out"><em>{e(val[0])}</em>{e(val[1])}</span>')
    lines.append('<span class="ln"><span class="p">$</span> <span class="caret" aria-hidden="true"></span></span>')
    term = "\n".join(lines)
    return f'''
    <section class="hero" aria-labelledby="hero-title">
      <canvas class="field" aria-hidden="true"></canvas>
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="eyebrow mono"><span class="pulse" aria-hidden="true"></span>SDE I at Amazon · Amman, Jordan</p>
          <h1 id="hero-title">Homam Manasra</h1>
          <p class="lead">Full-stack software engineer. I build payment systems at Amazon, and ship Android, React Native and web apps on my own.</p>
          <div class="cta">
            <a class="btn btn-primary" href="#projects">See projects{logo("arrow", "lg lg-btn")}</a>
            {ext(C.GITHUB, "GitHub", icon="github")}
            {ext(C.LINKEDIN, "LinkedIn", icon="linkedin")}
          </div>
          <dl class="stats">{stats}</dl>
        </div>
        <div class="hero-visual">
          <div class="halo" aria-hidden="true"></div>
          <div class="orbit" aria-hidden="true">{orbit}</div>
          {img("assets/portrait-hero.webp", 589, 1103, "Portrait of Homam Manasra", "portrait", lazy=False)}
          <figure class="term" aria-label="Summary in terminal form">
            <div class="term-bar" aria-hidden="true"><i></i><i></i><i></i><span class="mono">~/homam</span></div>
            <pre class="term-body mono"><code>{term}</code></pre>
          </figure>
        </div>
      </div>
    </section>'''


def sec_head(idx, title, hid, note=None):
    n = f'<p class="sec-note">{e(note)}</p>' if note else ""
    return f'<header class="sec-head" data-reveal><p class="mono idx">{idx}</p><h2 id="{hid}">{e(title)}</h2>{n}</header>'


def experience():
    items = []
    for x in C.EXPERIENCE:
        d0, l0, d1, l1 = x["dates"]
        end = f'<time datetime="{d1}">{l1}</time>' if d1 else l1
        body = f'<p>{e(x["summary"])}</p>'
        if "years" in x:
            ys = list(x["years"])
            tabs = "".join(f'<button type="button" role="tab" id="yt-{y}" aria-controls="yp-{y}" aria-selected="{str(i == 0).lower()}"'
                           f'{"" if i == 0 else " tabindex=\"-1\""}>{y}</button>' for i, y in enumerate(ys))
            panels = "".join(f'<div class="year-panel" role="tabpanel" id="yp-{y}" aria-labelledby="yt-{y}" tabindex="0">'
                             f'<h4 class="mono">{y}</h4><ul class="work">' + "".join(f"<li>{e(w)}</li>" for w in x["years"][y]) +
                             "</ul></div>" for y in ys)
            body += (f'<div class="years" data-tabs><div class="year-tabs" role="tablist" aria-label="Work by year">{tabs}</div>'
                     f'{panels}</div><p class="also">{e(x["also"])}</p>')
        items.append(f'''
          <li class="tl-item" data-reveal>
            <div class="tl-meta"><p class="mono"><time datetime="{d0}">{l0}</time> – {end}</p>{EXP[x["art"]]}</div>
            <div class="tl-card">
              <h3>{e(x["role"])} <span class="at">{e(x["org"])}</span></h3>
              <p class="where mono">{e(x["where"])}</p>
              {body}
              {tags(x["tags"])}
            </div>
          </li>''')
    focus = "".join(f'<article class="focus-card {cls}" data-reveal><span class="focus-ico">{logo(ic, "lg lg-focus")}</span>'
                    f'<h3>{e(t)}</h3><p>{e(d)}</p></article>' for ic, cls, t, d in C.FOCUS)
    return f'''
    <section class="section" id="experience" aria-labelledby="exp-title">
      <div class="wrap">
        {sec_head("01", "Experience", "exp-title")}
        <ol class="timeline">{"".join(items)}
        </ol>
        <div class="focus">{focus}</div>
      </div>
    </section>'''


def featured():
    f = C.FEATURED
    pts = "".join(f'<li>{logo(ic, "lg lg-pt")}<div><strong>{e(t)}</strong><span>{e(d)}</span></div></li>' for ic, t, d in f["points"])
    return f'''
        <article class="featured" data-reveal>
          <div class="feat-copy">
            <p class="card-kicker mono">{e(f["kicker"])}</p>
            <div class="feat-title">
              {img(f["logo"], 192, 192, "ربوع الناصرة logo", "feat-logo")}
              <div><h3 lang="ar" dir="rtl">{e(f["title_ar"])}</h3><p class="feat-latin mono">{e(f["title"])}</p></div>
            </div>
            <p class="badge-private">{logo("lock", "lg")}Private repositories · source not public</p>
            <p>{e(f["desc"])}</p>
            <ul class="feat-points">{pts}</ul>
            {tags(f["tags"])}
            <div class="cta">{ext(f["site"], "Visit nasrapack.com", cls="btn btn-primary", trailing="external")}</div>
          </div>
          <div class="feat-media">
            {browser(f["desktop"], "nasrapack.com")}
            {phones(f["phones"], "phones phones-feat")}
          </div>
        </article>'''


def projects():
    chips = "".join(f'<button type="button" class="chip" aria-pressed="{str(k == "all").lower()}" data-filter="{k}">{e(v)}</button>'
                    for k, v in C.FILTERS)
    cards = []
    for p in C.PROJECTS:
        nm = p.get("name", p["repo"])
        cards.append(f'''
          <li class="card" data-cat="{p["cat"]}" data-reveal>
            {media(p)}
            <div class="card-body">
              <p class="card-kicker mono">{e(p["kicker"])}</p>
              <h3><a href="{C.GITHUB}/{p["repo"]}" target="_blank" rel="noopener noreferrer">{e(nm)}</a>{logo("github", "lg lg-gh")}</h3>
              <p>{e(p["desc"])}</p>
              {tags(p["tags"])}
            </div>
          </li>''')
    return f'''
    <section class="section alt" id="projects" aria-labelledby="proj-title">
      <div class="wrap">
        {sec_head("02", "Projects", "proj-title", "Things I built outside work.")}
        {featured()}
        <div class="filters" role="group" aria-label="Filter public projects">{chips}
          <p class="count mono" aria-live="polite"><span id="proj-count">{len(C.PROJECTS)}</span> public projects</p>
        </div>
        <ul class="grid" id="proj-grid">{"".join(cards)}
        </ul>
        <div class="more">{ext(C.GITHUB + "?tab=repositories", "All repositories on GitHub", icon="github", trailing="external")}</div>
      </div>
    </section>'''


def donut():
    total = sum(C.LANG_BYTES.values())
    top = sorted(C.LANG_BYTES.items(), key=lambda kv: -kv[1])[:4]
    rows = top + [("Other", total - sum(v for _, v in top))]
    r, sw = 54, 20
    circ = 2 * math.pi * r
    segs, legend, start = [], [], 0.0
    for lang, v in rows:
        frac = v / total
        ln = max(frac * circ - 1.5, 0.5)
        col = C.LANG_COLORS[lang]
        segs.append(f'<circle class="seg" cx="70" cy="70" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" '
                    f'stroke-dasharray="{ln:.2f} {circ:.2f}" stroke-dashoffset="{-start:.2f}" transform="rotate(-90 70 70)"/>')
        legend.append(f'<li><i class="sw" data-c="{lang}"></i><span>{e(lang)}</span><b class="mono">{100 * frac:.1f}%</b></li>')
        start += frac * circ
    return f'''
          <figure class="chart donut" data-reveal>
            <figcaption><h3>Code by language</h3><p>Share of code in my public repos, as GitHub measures it.</p></figcaption>
            <div class="donut-body">
              <svg viewBox="0 0 140 140" role="img" aria-label="Code by language: {", ".join(f"{l} {100 * v / total:.0f}%" for l, v in rows)}">
                <circle cx="70" cy="70" r="{r}" fill="none" stroke="#eef3fa" stroke-width="{sw}"/>{"".join(segs)}
                <text x="70" y="66" text-anchor="middle" class="d-big">{len(C.LANG_BYTES)}</text>
                <text x="70" y="84" text-anchor="middle" class="d-small">languages</text>
              </svg>
              <ul class="legend">{"".join(legend)}</ul>
            </div>
          </figure>'''


def tech_bars():
    counts = {}
    for p in [C.FEATURED] + C.PROJECTS:
        for t in p["tags"]:
            slug = t[0] if isinstance(t, tuple) else t
            if slug not in GENERIC:
                counts[slug] = counts.get(slug, 0) + 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], name(kv[0])))[:8]
    mx = top[0][1]
    rows = "".join(f'<li><span class="bl">{logo(s)}{e(name(s))}</span>'
                   f'<svg class="bt" viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true"><rect width="100" height="10" rx="5" fill="#eef3fa"/>'
                   f'<rect class="bf" width="{100 * n / mx:.1f}" height="10" rx="5"/></svg><b class="mono">{n}</b></li>' for s, n in top)
    return f'''
          <figure class="chart bars" data-reveal>
            <figcaption><h3>Most-used technologies</h3><p>Number of my projects on this page that use each one.</p></figcaption>
            <ul class="bar-list">{rows}</ul>
          </figure>'''


def skills():
    groups = "".join(f'<div class="skill-group" data-reveal><h3 class="mono">{e(g)}</h3><ul class="logo-grid">' +
                     "".join(f'<li>{logo(s, "lg lg-tile")}<span>{e(name(s))}</span></li>' for s in items) +
                     "</ul></div>" for g, items in C.SKILLS)
    prac = "".join(f"<li>{e(p)}</li>" for p in C.PRACTICES)
    return f'''
    <section class="section" id="skills" aria-labelledby="skills-title">
      <div class="wrap">
        {sec_head("03", "Skills", "skills-title")}
        <div class="charts">{donut()}{tech_bars()}</div>
        <div class="skills">{groups}
          <div class="skill-group practices" data-reveal><h3 class="mono">Practices</h3><ul class="chips-plain">{prac}</ul></div>
        </div>
      </div>
    </section>'''


def contests():
    cards = []
    for c in C.CONTESTS:
        pre = f'<span class="small">{e(c["prefix"])}</span> ' if c.get("prefix") else ""
        num = (f'<p class="rank-num mono">{pre}<span data-count="{c["count"]}" data-suffix="{e(c["suffix"])}">{c["count"]}{e(c["suffix"])}</span></p>'
               if pre else f'<p class="rank-num mono" data-count="{c["count"]}" data-suffix="{e(c["suffix"])}">{e(c["num"])}</p>')
        bar = ""
        if "ahead" in c:
            bar = (f'<div class="ahead"><svg viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true">'
                   f'<rect width="100" height="8" rx="4" fill="#eef3fa"/><rect class="af" width="{c["ahead"]}" height="8" rx="4"/></svg>'
                   f'<p class="mono">Ahead of {c["ahead"]}% of participants</p></div>')
        cards.append(f'''
          <li class="rank" data-reveal>
            <span class="rank-logo">{logo(c["logo"], "lg lg-rank")}</span>
            {num}
            <p class="rank-of mono">{e(c["of"])}</p>
            <p class="rank-name">{e(c["name"])}</p>
            <p class="rank-year mono">{e(c["year"])}</p>
            {bar}
          </li>''')
    return f'''
    <section class="section alt" id="contests" aria-labelledby="cp-title">
      <div class="wrap">
        {sec_head("04", "Competitive Programming", "cp-title", "Contest results and training.")}
        <ul class="ranks">{"".join(cards)}
        </ul>
        <div class="profiles" data-reveal>{ext(C.CODEFORCES, "Codeforces", icon="codeforces")}{ext(C.LEETCODE, "LeetCode", icon="leetcode")}</div>
      </div>
    </section>'''


def contact():
    return f'''
    <section class="section contact" id="contact" aria-labelledby="contact-title">
      <div class="wrap contact-grid">
        <div class="avatar" data-reveal>{img("assets/portrait-contact.webp", 640, 640, "Homam Manasra")}</div>
        <div>
          {sec_head("05", "Contact", "contact-title")}
          <p class="contact-line" data-reveal>Happy to talk about payments, distributed systems, mobile, or a contest problem.</p>
          <div class="cta" data-reveal>
            {ext(C.LINKEDIN, "Message on LinkedIn", cls="btn btn-primary", icon="linkedin")}
            {ext(C.GITHUB, "github.com/homeo26", icon="github")}
          </div>
        </div>
      </div>
    </section>'''


NAV = [("experience", "Experience"), ("projects", "Projects"), ("skills", "Skills"), ("contests", "Contests"), ("contact", "Contact")]

PAGE = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>Homam Manasra · Full-Stack Software Engineer</title>
  <meta name="description" content="Homam Manasra, full-stack software engineer and SDE I at Amazon in Amman, Jordan. Payment systems, Android, React Native and web projects, competitive programming.">
  <link rel="canonical" href="https://homeo26.github.io/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Homam Manasra · Full-Stack Software Engineer">
  <meta property="og:description" content="SDE I at Amazon. Payment systems, Android, React Native and web projects, competitive programming.">
  <meta property="og:url" content="https://homeo26.github.io/">
  <meta property="og:image" content="https://homeo26.github.io/assets/portrait-contact.webp">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" href="logo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">
  <link rel="preload" href="assets/portrait-hero.webp" as="image" type="image/webp">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="assets/logos.css">
  <script src="boot.js"></script>
  <script src="script.js" defer></script>
  <script type="module" src="hero3d.js"></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav" id="top">
    <div class="nav-inner">
      <a class="brand" href="#top" aria-label="Homam Manasra, back to top"><img src="logo.svg" alt="" width="32" height="32"><span>Homam Manasra</span></a>
      <nav aria-label="Sections"><ul class="nav-links">{"".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in NAV)}</ul></nav>
    </div>
  </header>
  <main id="main">{hero()}{experience()}{projects()}{skills()}{contests()}{contact()}
  </main>
  <footer class="foot">
    <div class="wrap foot-inner mono">
      <span>© <span id="year">2026</span> Homam Manasra</span>
      <span class="foot-note">Logos are trademarks of their owners.</span>
      <a href="#top">Back to top ↑</a>
    </div>
  </footer>
</body>
</html>
'''

css = ["/* Generated by tools/build.py: logo colours, darkened where needed to reach 3:1 on white. */"]
css += [f'.lg[data-l="{k}"]{{color:{v["color"]}}}' for k, v in LOGOS.items()]
css += [f'.sw[data-c="{k}"]{{background:{v}}}' for k, v in C.LANG_COLORS.items()]
open(os.path.join(ROOT, "assets", "logos.css"), "w").write("\n".join(css) + "\n")
open(os.path.join(ROOT, "index.html"), "w").write(PAGE)
print(f"index.html {len(PAGE) // 1024} KB, {len(C.PROJECTS)} public projects + featured, {PAGE.count('<use ')} logo uses")
