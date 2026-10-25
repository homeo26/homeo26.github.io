#!/usr/bin/env python3
"""Render index.html and assets/logos.css from tools/content.py. Run: python3 tools/build.py"""
import html
import json
import os
import re
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


def zoom(shot, lazy):
    src, w, h, alt = shot
    return (f'<button type="button" class="zoom" data-zoom="{src}" data-w="{w}" data-h="{h}" aria-label="Enlarge: {e(alt)}">'
            f'{img(*shot, lazy=lazy)}<span class="zoom-ico" aria-hidden="true">{logo("zoom", "lg")}</span></button>')


def phones(shots, cls="phones", lazy=True):
    figs = "".join(f'<figure class="phone" data-ar="{s[1]}x{s[2]}">{zoom(s, lazy)}</figure>' for s in shots)
    return f'<div class="{cls}">{figs}</div>'


def browser(shot, url, lazy=True):
    return (f'<div class="browser"><div class="bbar" aria-hidden="true"><i></i><i></i><i></i><span>{e(url)}</span></div>'
            f'{zoom(shot, lazy)}</div>')


def media(p):
    kind, val = p["media"]
    if kind == "art":
        return f'<div class="media media-art">{PROJECT_ART[val]}</div>'
    if kind == "site":
        desk, phone = val
        url = p["live"].split("//", 1)[1].rstrip("/")
        return (f'<div class="media media-site">{browser(desk, url, lazy=False)}'
                f'{phones([phone], "phones phones-site", lazy=False)}</div>')
    if kind == "phones":
        return f'<div class="media media-phones">{phones(val, lazy=False)}</div>'
    # Carousel slides load eagerly: lazy images inside a sideways scroller only load once a slide is reached.
    return f'<div class="media media-browser">{browser(val, "github.com/homeo26/" + p.get("name", p["repo"]), lazy=False)}</div>'


# ---------------------------------------------------------------- sections
def hero():
    stats = "".join(f'<div><dt>{e(lbl)}</dt><dd data-count="{n}" data-suffix="{e(sfx)}">{e(txt)}</dd></div>'
                    for txt, n, sfx, lbl in C.HERO_STATS)
    orbit = "".join(f'<span class="orb" title="{e(name(s))}">{logo(s)}</span>' for s in C.ORBIT)
    return f'''
    <section class="hero" aria-labelledby="hero-title">
      <canvas class="field" aria-hidden="true"></canvas>
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <div class="hero-name">
            <h1 id="hero-title">Homam Manasra</h1>
            <p class="role-title">{e(C.ROLE_TITLE)}</p>
          </div>
          <p class="hero-loc">{logo("globe", "lg")}{e(C.LOCATION)}</p>
          <p class="lead">{e(C.TAGLINE)}</p>
          <div class="cta">
            <a class="btn btn-primary" href="#projects">See projects{logo("arrow", "lg lg-btn")}</a>
            {ext(C.GITHUB, "GitHub", icon="github")}
            {ext(C.LINKEDIN, "LinkedIn", icon="linkedin")}
            <a class="btn btn-ghost" href="mailto:{C.EMAIL}">{logo("mail", "lg lg-btn")}Email me</a>
          </div>
          <dl class="stats">{stats}</dl>
        </div>
        <div class="hero-visual">
          <div class="halo" aria-hidden="true"></div>
          <div class="orbit" aria-hidden="true">{orbit}</div>
          <div class="portrait">{img("assets/portrait-hero.webp", 588, 1103, "Portrait of Homam Manasra", lazy=False)}</div>
        </div>
      </div>
    </section>'''


def sec_head(idx, title, hid, note=None):
    n = f'<p class="sec-note">{e(note)}</p>' if note else ""
    return f'<header class="sec-head" data-reveal><p class="idx">{idx}</p><h2 id="{hid}">{e(title)}</h2>{n}</header>'


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
                             f'<h4>{y}</h4><ul class="work">' + "".join(f"<li>{e(w)}</li>" for w in x["years"][y]) +
                             "</ul></div>" for y in ys)
            body += (f'<div class="years" data-tabs><div class="year-tabs" role="tablist" aria-label="Work by year">{tabs}</div>'
                     f'{panels}</div><p class="also">{e(x["also"])}</p>')
        items.append(f'''
          <li class="tl-item" data-reveal>
            <div class="tl-meta"><p><time datetime="{d0}">{l0}</time> – {end}</p>{EXP[x["art"]]}</div>
            <div class="tl-card">
              <h3>{e(x["role"])} <span class="at">{e(x["org"])}</span></h3>
              <p class="where">{e(x["where"])}</p>
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


def live_link(p):
    if "live" not in p:
        return ""
    url = p["live"].split("//", 1)[1].rstrip("/")
    fb = f' data-fallback="{e(p["fallback"])}"' if p.get("fallback") else ""
    return (f'<a class="live" href="{e(p["live"])}"{fb} target="_blank" rel="noopener noreferrer">'
            f'{logo("globe", "lg")}<span class="host">{e(url)}</span>{logo("external", "lg")}</a>')


def robou3_slide():
    f = C.FEATURED
    pts = "".join(f'<li>{logo(ic, "lg lg-pt")}<div><strong>{e(t)}</strong><span>{e(d)}</span></div></li>' for ic, t, d in f["points"])
    visit = (f'<a class="btn btn-primary" href="{e(f["site"])}" data-fallback="{e(f["fallback"])}" target="_blank" rel="noopener noreferrer">'
             f'Visit <span class="host">{e(f["site"].split("//", 1)[1])}</span>{logo("external", "lg lg-btn")}</a>')
    return f'''
            <article class="spot-slide" aria-roledescription="slide" aria-label="1 of {len(C.PROJECTS) + 1}: {e(f["title"])}">
              <div class="feat-copy">
                <p class="card-kicker">{e(f["kicker"])}</p>
                <div class="feat-title">{img(f["logo"], 192, 192, f["title"] + " logo", "feat-logo", lazy=False)}<h3>{e(f["title"])}</h3></div>
                <p class="badge-private">{logo("lock", "lg")}Private repositories · source not public</p>
                <p>{e(f["desc"])}</p>
                <ul class="feat-points">{pts}</ul>
                {tags(f["tags"])}
                <div class="cta">{visit}</div>
              </div>
              <div class="feat-media">
                {browser(f["desktop"], "nasrapack.com", lazy=False)}
                {phones(f["phones"], "phones phones-feat", lazy=False)}
              </div>
            </article>'''


def app_icon(p, cls):
    """The project's own app icon, or a matching glyph tile when it has none."""
    nm = p.get("name", p["repo"])
    if p.get("icon"):
        return img(p["icon"], 192, 192, f"{nm} app icon", cls, lazy=False)
    return f'<span class="{cls} glyph-ico">{logo(p.get("glyph", "github"), "lg")}</span>'


def public_slide(p, n, total):
    nm = p.get("name", p["repo"])
    live = ""
    if p.get("live"):
        url = p["live"].split("//", 1)[1].rstrip("/")
        live = (f'<a class="btn btn-ghost" href="{e(p["live"])}" data-fallback="{e(p["fallback"])}" target="_blank" rel="noopener noreferrer">'
                f'{logo("globe", "lg lg-btn")}<span class="host">{e(url)}</span>{logo("external", "lg lg-btn")}</a>')
    return f'''
            <article class="spot-slide" aria-roledescription="slide" aria-label="{n} of {total}: {e(nm)}">
              <div class="feat-copy">
                <p class="card-kicker">{e(p["kicker"])}</p>
                <div class="feat-title">{app_icon(p, "feat-logo")}<h3>{e(nm)}</h3></div>
                <p class="badge-public">{logo("github", "lg")}Public repository · open source</p>
                <p>{e(p["desc"])}</p>
                {tags(p["tags"])}
                <div class="cta">{ext(f"{C.GITHUB}/{p['repo']}", "View on GitHub", cls="btn btn-primary", icon="github")}{live}</div>
              </div>
              {showcase(p)}
            </article>'''


def showcase(p):
    """Robou3-style media: a browser screenshot with phones over it, or a row of phones."""
    sc = p.get("showcase")
    if not sc:
        return f'<div class="spot-media">{media(p)}</div>'
    phones_html = phones(sc["phones"], "phones phones-feat", lazy=False) if sc.get("phones") else ""
    if sc.get("desktop"):
        over = (f'<div class="browser browser-over"><div class="bbar" aria-hidden="true"><i></i><i></i><i></i></div>{zoom(sc["overlay"], False)}</div>'
                if sc.get("overlay") else "")
        return f'<div class="feat-media">{browser(sc["desktop"], sc["url"], lazy=False)}{phones_html}{over}</div>'
    return f'<div class="feat-media only-phones">{phones(sc["phones"], "phones phones-stage", lazy=False)}</div>'


def spotlight():
    by_repo = {p["repo"]: p for p in C.PROJECTS}
    order = [by_repo[r] for r in C.SPOTLIGHT]
    total = len(order) + 1
    slides = robou3_slide() + "".join(public_slide(p, k + 2, total) for k, p in enumerate(order))
    names = [C.FEATURED["title"]] + [p.get("name", p["repo"]) for p in order]
    dots = "".join(f'<button type="button" class="spot-dot" data-i="{k}" aria-label="Show {e(nm)}"{" aria-current=\"true\"" if k == 0 else ""}></button>'
                   for k, nm in enumerate(names))
    return f'''
        <div class="spot" data-spot data-reveal aria-roledescription="carousel" aria-label="Project spotlight">
          <div class="spot-stage">
            <div class="spot-track" tabindex="0">{slides}
            </div>
            <button type="button" class="spot-side spot-prev" data-spot-ctl="prev" aria-label="Previous project">{logo("chev-l", "lg lg-btn")}</button>
            <button type="button" class="spot-side spot-next" data-spot-ctl="next" aria-label="Next project">{logo("chev-r", "lg lg-btn")}</button>
          </div>
          <div class="spot-timer" aria-hidden="true"><span></span></div>
          <div class="spot-foot">
            <div class="spot-dots" role="group" aria-label="Choose a project">{dots}</div>
            <p class="spot-count" aria-live="polite">1 / {total}</p>
            <div class="car-ctrl">
              <button type="button" class="ctl" data-spot-ctl="pause" aria-label="Pause slideshow" aria-pressed="false">{logo("pause", "lg lg-btn i-pause")}{logo("play", "lg lg-btn i-play")}</button>
            </div>
          </div>
        </div>'''


def projects():
    chips = "".join(f'<button type="button" class="chip" aria-pressed="{str(k == "all").lower()}" data-filter="{k}">{e(v)}</button>'
                    for k, v in C.FILTERS)
    cards = []
    for p in C.PROJECTS:
        nm = p.get("name", p["repo"])
        cards.append(f'''
          <li class="card" data-cat="{p["cat"]}">
            {media(p)}
            <div class="card-body">
              <p class="card-kicker">{e(p["kicker"])}</p>
              <h3>{app_icon(p, "card-ico")}<a href="{C.GITHUB}/{p["repo"]}" target="_blank" rel="noopener noreferrer">{e(nm)}</a>{logo("github", "lg lg-gh")}</h3>
              <p>{e(p["desc"])}</p>
              {live_link(p)}
              {tags(p["tags"])}
            </div>
          </li>''')
    ctrl = (f'<div class="car-ctrl">'
            f'<button type="button" class="ctl" data-car="prev" aria-label="Previous projects">{logo("chev-l", "lg lg-btn")}</button>'
            f'<button type="button" class="ctl" data-car="next" aria-label="Next projects">{logo("chev-r", "lg lg-btn")}</button></div>')
    return f'''
    <section class="section alt" id="projects" aria-labelledby="proj-title">
      <div class="wrap">
        {sec_head("02", "Projects", "proj-title", "Things I built outside work.")}
        {spotlight()}
        <div class="carousel" data-carousel data-reveal>
          <div class="car-head">
            <h3 class="sub-head">Browse by category</h3>
            <div class="filters" role="group" aria-label="Filter public projects">{chips}</div>
            {ctrl}
          </div>
          <ul class="track" id="proj-grid" tabindex="0" aria-label="Public projects">{"".join(cards)}
          </ul>
          <div class="car-progress" aria-hidden="true"><span></span></div>
        </div>
        <div class="more">{ext(C.GITHUB + "?tab=repositories", "All repositories on GitHub", icon="github", trailing="external")}</div>
      </div>
    </section>'''


def skills():
    groups = "".join(f'<div class="skill-group" data-reveal><h3>{e(g)}</h3><ul class="logo-grid">' +
                     "".join(f'<li>{logo(s, "lg lg-tile")}<span>{e(name(s))}</span></li>' for s in items) +
                     "</ul></div>" for g, items in C.SKILLS)
    topics = "".join(f'<div class="skill-group topic" data-reveal><h3>{logo(ic, "lg lg-topic")}{e(t)}</h3><ul class="chips-plain">' +
                     "".join(f"<li>{e(x)}</li>" for x in items) + "</ul></div>" for ic, t, items in C.SKILL_TOPICS)
    return f'''
    <section class="section" id="skills" aria-labelledby="skills-title">
      <div class="wrap">
        {sec_head("03", "Skills", "skills-title")}
        <div class="skills">{groups}
          {topics}
        </div>
      </div>
    </section>'''


def contests():
    cards = []
    for c in C.CONTESTS:
        pre = f'<span class="small">{e(c["prefix"])}</span> ' if c.get("prefix") else ""
        num = (f'<p class="rank-num">{pre}<span data-count="{c["count"]}" data-suffix="{e(c["suffix"])}">{c["count"]}{e(c["suffix"])}</span></p>'
               if pre else f'<p class="rank-num" data-count="{c["count"]}" data-suffix="{e(c["suffix"])}">{e(c["num"])}</p>')
        bar = ""
        if "ahead" in c:
            bar = (f'<div class="ahead"><svg viewBox="0 0 100 8" preserveAspectRatio="none" aria-hidden="true">'
                   f'<rect width="100" height="8" rx="4" fill="#eef3fa"/><rect class="af" width="{c["ahead"]}" height="8" rx="4"/></svg>'
                   f'<p>Ahead of {c["ahead"]}% of participants</p></div>')
        cards.append(f'''
          <li class="rank" data-reveal>
            <span class="rank-logo">{logo(c["logo"], "lg lg-rank")}</span>
            {num}
            <p class="rank-of">{e(c["of"])}</p>
            <p class="rank-name">{e(c["name"])}</p>
            <p class="rank-year">{e(c["year"])}</p>
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
    plats = "".join(f'<li>{logo(s, "lg lg-plat")}<span>{e(t)}</span></li>' for s, t in C.PLATFORMS)
    return f'''
    <section class="section contact" id="contact" aria-labelledby="contact-title">
      <div class="wrap contact-grid">
        <div class="avatar" data-reveal>{img("assets/portrait-contact.webp", 640, 640, "Homam Manasra")}</div>
        <div>
          {sec_head("05", "Contact", "contact-title")}
          <p class="contact-line" data-reveal>{e(C.CONTACT_LINE)}</p>
          <ul class="platforms" data-reveal>{plats}</ul>
          <div class="cta" data-reveal>
            <a class="btn btn-primary" href="mailto:{C.EMAIL}">{logo("mail", "lg lg-btn")}Email me · {C.EMAIL}</a>
            {ext(C.LINKEDIN, "Message on LinkedIn", icon="linkedin")}
            {ext(C.GITHUB, "github.com/homeo26", icon="github")}
          </div>
        </div>
      </div>
    </section>'''


SITE = "https://homeo26.github.io/"
DESC = ("Homam Manasra, Software Development Engineer in Amman, Jordan. Delivering software solutions: payment systems "
        "at Amazon, plus Android, iOS and web apps.")
LD = json.dumps([
    {"@context": "https://schema.org", "@type": "Person", "@id": SITE + "#person", "name": "Homam Manasra",
     "url": SITE, "image": SITE + "assets/portrait-contact.webp", "jobTitle": C.ROLE_TITLE,
     "worksFor": {"@type": "Organization", "name": "Amazon"},
     "alumniOf": {"@type": "CollegeOrUniversity", "name": "Jordan University of Science and Technology"},
     "address": {"@type": "PostalAddress", "addressLocality": "Amman", "addressCountry": "JO"},
     "email": "mailto:" + C.EMAIL, "sameAs": [C.GITHUB, C.LINKEDIN, C.CODEFORCES, C.LEETCODE],
     "knowsAbout": ["Payment systems", "Distributed systems", "Android", "iOS", "React Native", "Java", "Kotlin",
                    "TypeScript", "Python", "AWS", "Competitive programming"]},
    {"@context": "https://schema.org", "@type": "WebSite", "name": "Homam Manasra", "url": SITE,
     "author": {"@id": SITE + "#person"}, "inLanguage": "en"},
], ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

NAV = [("experience", "Experience"), ("projects", "Projects"), ("skills", "Skills"), ("contests", "Contests"), ("contact", "Contact")]

PAGE = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://nasrapack.com https://greenbranchs.com; object-src 'none'; base-uri 'self'; form-action 'none'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>Homam Manasra · Software Development Engineer</title>
  <meta name="description" content="{e(DESC)}">
  <meta name="author" content="Homam Manasra">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="google-site-verification" content="SmUwQSA5brxP1DU5GfvlAZL5WU9U61glFrWdhUGgNXI">
  <link rel="canonical" href="{SITE}">
  <meta property="og:type" content="profile">
  <meta property="og:site_name" content="Homam Manasra">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="Homam Manasra · Software Development Engineer">
  <meta property="og:description" content="{e(DESC)}">
  <meta property="og:url" content="{SITE}">
  <meta property="og:image" content="{SITE}assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Homam Manasra, Software Development Engineer">
  <meta property="profile:first_name" content="Homam">
  <meta property="profile:last_name" content="Manasra">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Homam Manasra · Software Development Engineer">
  <meta name="twitter:description" content="{e(DESC)}">
  <meta name="twitter:image" content="{SITE}assets/og-image.png">
  <meta name="theme-color" content="#ffffff">
  <link rel="me" href="{C.GITHUB}">
  <link rel="me" href="{C.LINKEDIN}">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="sitemap" type="application/xml" href="sitemap.xml">
  <script type="application/ld+json">{LD}</script>
  <link rel="icon" href="logo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
  <link rel="preload" href="assets/portrait-hero.webp" as="image" type="image/webp">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="assets/logos.css">
  <script src="boot.js"></script>
  <script src="script.js" defer></script>
  <script type="module" src="hero3d.js"></script>
</head>
<body id="top">
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav">
    <div class="nav-inner">
      <a class="brand" href="#top" aria-label="Homam Manasra, back to top"><img src="logo.svg" alt="" width="32" height="32"><span>Homam Manasra</span></a>
      <nav aria-label="Sections"><ul class="nav-links">{"".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in NAV)}</ul></nav>
    </div>
  </header>
  <main id="main">{hero()}{experience()}{projects()}{skills()}{contests()}{contact()}
  </main>
  <dialog class="lightbox" aria-label="Enlarged screenshot">
    <button type="button" class="lb-close" aria-label="Close">{logo("close", "lg lg-btn")}</button>
    <img class="lb-img" src="data:," alt="">
    <p class="lb-cap"></p>
  </dialog>
  <footer class="foot">
    <div class="wrap foot-inner">
      <span>© <span id="year">2026</span> Homam Manasra</span>
      <span class="foot-note">Logos are trademarks of their owners.</span>
      <a href="#top">Back to top ↑</a>
    </div>
  </footer>
</body>
</html>
'''

if re.search(r"[\u0600-\u06FF]", PAGE):
    raise SystemExit("Arabic script found in the page; use English only.")
css = ["/* Generated by tools/build.py: logo colours, darkened where needed to reach 3:1 on white. */"]
css += [f'.lg[data-l="{k}"]{{color:{v["color"]}}}' for k, v in LOGOS.items()]
# Each phone frame takes its screenshot's exact proportions, so nothing is cropped or letterboxed.
ratios = sorted(set(re.findall(r'class="phone" data-ar="(\d+)x(\d+)"', PAGE)))
css += [f'.phone[data-ar="{w}x{h}"]{{aspect-ratio:{w}/{h}}}' for w, h in ratios]
open(os.path.join(ROOT, "assets", "logos.css"), "w").write("\n".join(css) + "\n")
open(os.path.join(ROOT, "index.html"), "w").write(PAGE)
print(f"index.html {len(PAGE) // 1024} KB, {len(C.PROJECTS)} public projects + featured, {PAGE.count('<use ')} logo uses")
