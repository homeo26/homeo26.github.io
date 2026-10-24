"""Inline SVG illustrations. Class names (a-*) are animation hooks in styles.css; motion plays on hover/focus."""
import math

NAVY, BLUE, MID, LIGHT, WASH, LINE, WHITE, OK = "#0b1f3a", "#2563eb", "#1e40af", "#cbe0fd", "#eaf1ff", "#c9d5e8", "#ffffff", "#15803d"


def gear(cx, cy, r, teeth=8, depth=3.2, cls="a-gear"):
    pts = []
    for i in range(teeth * 2):
        a = math.pi * i / teeth
        rr = r + (depth if i % 2 == 0 else 0)
        for da in (-0.18, 0.18):
            pts.append(f"{cx + rr * math.cos(a + da):.1f},{cy + rr * math.sin(a + da):.1f}")
    return (f'<g class="{cls}"><polygon points="{" ".join(pts)}" fill="{MID}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.42:.1f}" fill="{WASH}"/></g>')


# ---------- Experience (120x120) ----------
EXP = {
    "pay": f'''<svg class="art art-pay" viewBox="0 0 120 120" aria-hidden="true">
  <circle cx="60" cy="60" r="54" fill="{WASH}"/>
  <g class="a-card"><rect x="18" y="38" width="58" height="38" rx="7" fill="{BLUE}"/>
    <rect x="18" y="47" width="58" height="8" fill="{MID}"/><rect x="25" y="61" width="11" height="8" rx="2" fill="{LIGHT}"/>
    <rect x="41" y="64" width="20" height="3" rx="1.5" fill="{LIGHT}"/></g>
  <g fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round">
    <path class="a-wave a-w1" d="M84 51a12 12 0 0 1 0 16"/><path class="a-wave a-w2" d="M91 45a20 20 0 0 1 0 28"/></g>
  <circle cx="88" cy="88" r="14" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
  <path class="a-check" d="M81.5 88.5l4.5 4.5 8.5-9" fill="none" stroke="{OK}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',
    "ci": f'''<svg class="art art-ci" viewBox="0 0 120 120" aria-hidden="true">
  <circle cx="60" cy="60" r="54" fill="{WASH}"/>
  {gear(60, 36, 11)}
  <path d="M26 78H94" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>
  <path class="a-flow" d="M26 78H94" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" pathLength="100"/>
  <circle class="a-node a-n1" cx="26" cy="78" r="8.5" fill="{WHITE}" stroke="{BLUE}" stroke-width="3"/>
  <circle class="a-node a-n2" cx="60" cy="78" r="8.5" fill="{WHITE}" stroke="{BLUE}" stroke-width="3"/>
  <circle class="a-node a-n3" cx="94" cy="78" r="8.5" fill="{WHITE}" stroke="{BLUE}" stroke-width="3"/>
</svg>''',
    "phone": f'''<svg class="art art-phone" viewBox="0 0 120 120" aria-hidden="true">
  <circle cx="60" cy="60" r="54" fill="{WASH}"/>
  <g class="a-handset"><rect x="40" y="22" width="36" height="66" rx="7" fill="{NAVY}"/>
    <rect x="44" y="30" width="28" height="48" rx="2" fill="{WHITE}"/>
    <rect class="a-bar a-b1" x="48" y="58" width="5" height="16" rx="1.5" fill="{BLUE}"/>
    <rect class="a-bar a-b2" x="55.5" y="50" width="5" height="24" rx="1.5" fill="{BLUE}"/>
    <rect class="a-bar a-b3" x="63" y="42" width="5" height="32" rx="1.5" fill="{MID}"/>
    <rect x="54" y="81.5" width="8" height="2.5" rx="1.2" fill="{LIGHT}"/></g>
  <g fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round">
    <path class="a-wave a-w1" d="M84 34a9 9 0 0 1 6 8"/><path class="a-wave a-w2" d="M86 26a17 17 0 0 1 11 14"/></g>
  <g class="a-db"><ellipse cx="28" cy="80" rx="11" ry="4" fill="{MID}"/><path d="M17 80v12c0 2.2 4.9 4 11 4s11-1.8 11-4V80" fill="{BLUE}"/>
    <ellipse cx="28" cy="80" rx="11" ry="4" fill="{LIGHT}"/></g>
</svg>''',
    "cap": f'''<svg class="art art-cap" viewBox="0 0 120 120" aria-hidden="true">
  <circle cx="60" cy="60" r="54" fill="{WASH}"/>
  <g class="a-book"><path d="M30 80c10-4 20-4 30 2 10-6 20-6 30-2v14c-10-4-20-4-30 2-10-6-20-6-30-2z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
    <path d="M60 82v14" stroke="{LINE}" stroke-width="2"/></g>
  <g class="a-capg"><path d="M22 46 60 30l38 16-38 16z" fill="{NAVY}"/><path d="M38 53v12c6 5 14 7 22 7s16-2 22-7V53l-22 9z" fill="{MID}"/>
    <g class="a-tassel"><path d="M92 49v15" stroke="{BLUE}" stroke-width="2.5"/><circle cx="92" cy="66" r="3.5" fill="{BLUE}"/></g></g>
  <g class="a-code" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
    <path class="a-lt" d="m16 26-7 6 7 6"/><path class="a-gt" d="m104 20 7 6-7 6"/></g>
</svg>''',
}


# ---------- Projects (320x200) ----------
def _frame(inner, cls):
    return (f'<svg class="art art-{cls}" viewBox="0 0 320 200" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<rect width="320" height="200" fill="{WASH}"/>{inner}</svg>')


def _bars(x, y, n, w, gap, hs, cls="a-eq"):
    return "".join(f'<rect class="{cls} {cls}{i % 4}" x="{x + i * (w + gap)}" y="{y - h}" width="{w}" height="{h}" rx="1.5" fill="{BLUE if i % 2 else MID}"/>'
                   for i, h in enumerate(hs[:n]))


SPLIT = _frame(f'''
  <rect x="34" y="34" width="252" height="132" rx="14" fill="{NAVY}"/>
  <rect x="44" y="44" width="114" height="112" rx="6" fill="{WHITE}"/>
  <g stroke="{LINE}" stroke-width="1.5">{"".join(f'<path d="M{44 + i * 19} 44v112"/>' for i in range(1, 6))}{"".join(f'<path d="M44 {44 + i * 19}h114"/>' for i in range(1, 6))}</g>
  <path class="a-route" d="M58 140c14-30 30-10 42-38s28-14 40-46" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linecap="round" pathLength="100"/>
  <circle cx="140" cy="56" r="5" fill="{OK}"/>
  <rect x="166" y="44" width="110" height="112" rx="6" fill="{WHITE}"/>
  <rect x="180" y="56" width="40" height="40" rx="6" fill="{LIGHT}"/><path d="M194 66v20l14-10z" fill="{BLUE}"/>
  <rect x="228" y="62" width="38" height="6" rx="3" fill="{NAVY}"/><rect x="228" y="76" width="26" height="5" rx="2.5" fill="{LINE}"/>
  {_bars(180, 144, 8, 8, 4, [18, 30, 22, 36, 14, 26, 32, 20])}
  <rect class="a-divider" x="157" y="82" width="10" height="36" rx="5" fill="{LIGHT}"/>''', "split")

VOICE = _frame(f'''
  <circle cx="104" cy="100" r="46" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
  <rect x="92" y="72" width="24" height="40" rx="12" fill="{BLUE}"/>
  <path d="M84 100a20 20 0 0 0 40 0M104 120v10M94 132h20" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>
  <g fill="none" stroke="{BLUE}" stroke-width="4" stroke-linecap="round">
    <path class="a-wave a-w1" d="M48 86a24 24 0 0 0 0 28"/><path class="a-wave a-w2" d="M36 76a40 40 0 0 0 0 48"/>
    <path class="a-wave a-w1" d="M160 86a24 24 0 0 1 0 28"/><path class="a-wave a-w2" d="M172 76a40 40 0 0 1 0 48"/></g>
  <circle cx="242" cy="100" r="50" fill="{NAVY}"/>
  <circle cx="242" cy="100" r="38" fill="none" stroke="#24406e" stroke-width="7"/>
  <circle class="a-dial" cx="242" cy="100" r="38" fill="none" stroke="#7fb0ff" stroke-width="7" stroke-linecap="round" pathLength="100" transform="rotate(-90 242 100)"/>
  <g class="a-fan"><g fill="{LIGHT}">{"".join(f'<ellipse cx="242" cy="86" rx="5.5" ry="13" transform="rotate({a} 242 100)"/>' for a in (0, 120, 240))}</g>
    <circle cx="242" cy="100" r="5" fill="{WHITE}"/></g>''', "voice")

VAC = _frame(f'''
  <rect x="30" y="26" width="260" height="148" rx="12" fill="{NAVY}"/>
  <circle cx="48" cy="42" r="4.5" fill="#7fb0ff"/><circle cx="62" cy="42" r="4.5" fill="#24406e"/><circle cx="76" cy="42" r="4.5" fill="#24406e"/>
  <text x="46" y="74" fill="#7fb0ff" font-family="IBM Plex Sans, sans-serif" font-size="13">$</text>
  <text x="60" y="74" fill="{WHITE}" font-family="IBM Plex Sans, sans-serif" font-size="13">vac clean --images</text>
  <g class="a-junk">
    <rect class="a-j a-j1" x="46" y="88" width="190" height="9" rx="4.5" fill="#3b5b8f"/>
    <rect class="a-j a-j2" x="46" y="104" width="226" height="9" rx="4.5" fill="#f59e0b"/>
    <rect class="a-j a-j3" x="46" y="120" width="140" height="9" rx="4.5" fill="#3b5b8f"/></g>
  <rect x="46" y="144" width="226" height="10" rx="5" fill="#24406e"/>
  <rect class="a-prog" x="46" y="144" width="226" height="10" rx="5" fill="#7fb0ff"/>''', "vac")


def _car(x, y, fill_seats, cls):
    seats = "".join(f'<circle class="a-seat a-s{i}" cx="{x + 16 + i * 13}" cy="{y + 15}" r="4.5" fill="{BLUE if i < fill_seats else WHITE}" stroke="{BLUE}" stroke-width="2"/>' for i in range(5))
    return (f'<g class="a-car {cls}"><rect x="{x}" y="{y}" width="84" height="30" rx="10" fill="{WHITE}" stroke="{NAVY}" stroke-width="2.5"/>'
            f'{seats}<circle cx="{x + 18}" cy="{y + 32}" r="6" fill="{NAVY}"/><circle cx="{x + 66}" cy="{y + 32}" r="6" fill="{NAVY}"/></g>')


CARPOOL = _frame(f'''
  <rect x="0" y="128" width="320" height="44" fill="{LIGHT}"/>
  <path class="a-lane" d="M0 150h320" stroke="{WHITE}" stroke-width="4" stroke-dasharray="18 14"/>
  {_car(18, 112, 2, "a-c1")}{_car(118, 112, 4, "a-c2")}{_car(218, 112, 1, "a-c3")}
  <rect x="96" y="30" width="128" height="56" rx="10" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
  <text x="112" y="54" fill="{NAVY}" font-family="IBM Plex Sans, sans-serif" font-weight="700" font-size="15">Confirmed</text>
  <rect x="112" y="64" width="96" height="8" rx="4" fill="{WASH}"/><rect class="a-conf" x="112" y="64" width="96" height="8" rx="4" fill="{OK}"/>''', "carpool")

_PTS = [(52, 150), (64, 142), (76, 146), (88, 128), (100, 132), (112, 118), (124, 124), (136, 104), (148, 112), (160, 96),
        (172, 100), (184, 84), (196, 90), (208, 72), (220, 78), (232, 60), (244, 66), (256, 50), (268, 56)]
SCATTER = _frame(f'''
  <rect x="30" y="20" width="260" height="164" rx="12" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
  <path d="M46 34v134h230" fill="none" stroke="{NAVY}" stroke-width="2.5" stroke-linecap="round"/>
  <g stroke="{WASH}" stroke-width="1.5">{"".join(f'<path d="M48 {60 + i * 26}h226"/>' for i in range(4))}</g>
  {"".join(f'<circle class="a-pt a-p{i % 5}" cx="{x}" cy="{y}" r="4.5" fill="{BLUE if i % 3 else MID}"/>' for i, (x, y) in enumerate(_PTS))}
  <path class="a-fit" d="M50 156L272 48" stroke="{OK}" stroke-width="3.5" stroke-linecap="round" pathLength="100"/>''', "scatter")


def _tree():
    lv = [[(160, 40)], [(76, 98), (160, 98), (244, 98)], [(48 + i * 28, 158) for i in range(9)]]
    letters = "HOMAMSDE!"
    edges = []
    for i, (x, y) in enumerate(lv[1]):
        edges.append(f'<path d="M160 40L{x} {y}"/>')
        for j in range(3):
            cx, cy = lv[2][i * 3 + j]
            edges.append(f'<path d="M{x} {y}L{cx} {cy}"/>')
    nodes = [f'<circle class="a-tn a-l0" cx="160" cy="40" r="14" fill="{NAVY}"/>']
    nodes += [f'<circle class="a-tn a-l1" cx="{x}" cy="{y}" r="12" fill="{MID}"/>' for x, y in lv[1]]
    for k, (x, y) in enumerate(lv[2]):
        nodes.append(f'<g class="a-tn a-l2"><circle cx="{x}" cy="{y}" r="11" fill="{WHITE}" stroke="{BLUE}" stroke-width="2.5"/>'
                     f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" fill="{NAVY}" font-family="IBM Plex Sans, sans-serif" font-weight="700" font-size="12">{letters[k]}</text></g>')
    return _frame(f'<g stroke="{LINE}" stroke-width="2.5">{"".join(edges)}</g>{"".join(nodes)}', "tree")


TREE = _tree()

LEGAL = _frame(f'''
  <g class="a-bub a-bub1"><rect x="28" y="34" width="128" height="44" rx="14" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
    <rect x="44" y="49" width="84" height="6" rx="3" fill="{LINE}"/><rect x="44" y="61" width="58" height="6" rx="3" fill="{LINE}"/></g>
  <g class="a-bub a-bub2"><rect x="60" y="92" width="120" height="44" rx="14" fill="{BLUE}"/>
    <rect x="76" y="107" width="80" height="6" rx="3" fill="{LIGHT}"/><rect x="76" y="119" width="50" height="6" rx="3" fill="{LIGHT}"/></g>
  <g class="a-bub a-bub3"><rect x="28" y="150" width="96" height="30" rx="12" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
    <circle cx="50" cy="165" r="3.5" fill="{MID}"/><circle cx="62" cy="165" r="3.5" fill="{MID}"/><circle cx="74" cy="165" r="3.5" fill="{MID}"/></g>
  <path d="M250 40v128M222 168h56" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>
  <g class="a-beam"><path d="M206 64h88" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>
    <path d="M206 64l-14 34h28zM294 64l-14 34h28z" fill="none" stroke="{MID}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M190 98a16 7 0 0 0 32 0zM278 98a16 7 0 0 0 32 0z" fill="{BLUE}"/></g>
  <circle cx="250" cy="40" r="7" fill="{BLUE}"/>''', "legal")

PROJECT_ART = {"split": SPLIT, "voice": VOICE, "vac": VAC, "carpool": CARPOOL, "scatter": SCATTER, "tree": TREE,
               "legal": LEGAL}
