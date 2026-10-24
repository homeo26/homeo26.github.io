#!/usr/bin/env python3
"""Build assets/logos.svg (a symbol sprite) and tools/logos.json from Simple Icons.

Brand colours that are too light for a white page are darkened toward navy until they
reach 3:1 against white. Glyphs that Simple Icons doesn't carry are drawn here.
Run: python3 tools/fetch_logos.py
"""
import json, os, re, urllib.request

VERSION = "16.35.0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDS = [
    "openjdk", "kotlin", "typescript", "javascript", "python", "cplusplus", "apachegroovy", "ruby", "gnubash",
    "swift", "react", "expo", "nextdotjs", "android", "tailwindcss", "html5", "css", "framer", "springboot",
    "nodedotjs", "flask", "postgresql", "mysql", "sqlite", "firebase", "googlecloud", "docker", "kubernetes",
    "githubactions", "gradle", "git", "linux", "github", "jupyter", "pandas", "numpy", "scikitlearn", "homebrew",
    "pypi", "claude", "netlify", "yaml", "modelcontextprotocol", "codeforces", "leetcode", "ieee", "facebook",
    "androidauto", "youtube", "whatsapp", "mermaid", "json", "apple",
]
# Marks no longer shipped by Simple Icons 16 (slug: title, brand hex, path from an earlier release).
EXTRA_BRANDS = {
    "linkedin": ("LinkedIn", "0A66C2", "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"),
}
NAVY = (11, 31, 58)

# Stroke glyphs (24x24, drawn with currentColor) for things without a brand mark.
GLYPHS = {
    "aws": ("AWS", '<path d="M7 17.5h10.2a4.3 4.3 0 0 0 .6-8.56A6 6 0 0 0 6.3 10.1 3.7 3.7 0 0 0 7 17.5z"/><path d="M8 20.5c2.6 1 5.4 1 8 0"/><path d="m15.2 19.4 1.4 1.1-1.6.6"/>'),
    "dynamodb": ("DynamoDB", '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v13c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-13"/><path d="M5 12c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5"/>'),
    "reactnative": ("React Native", '<ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/>'),
    "lock": ("Private", '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 14.5v2.5"/>'),
    "trophy": ("Trophy", '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4"/><path d="M12 13v4M8.5 20.5h7M10 17h4v3.5h-4z"/>'),
    "cap": ("Graduation", '<path d="m2.5 9 9.5-4.5L21.5 9 12 13.5z"/><path d="M6.5 11v4.2c1.6 1.5 3.4 2.3 5.5 2.3s3.9-.8 5.5-2.3V11"/><path d="M21.5 9v5"/>'),
    "mic": ("Microphone", '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/>'),
    "film": ("Video", '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14M17 5v14M3 9.5h4M3 14.5h4M17 9.5h4M17 14.5h4"/>'),
    "terminal": ("Terminal", '<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="m6.5 9 3 3-3 3M12 15h5"/>'),
    "chart": ("Chart", '<path d="M4 20V4M4 20h16"/><path d="m7 15 4-4 3 3 5-6"/>'),
    "tree": ("Tree", '<circle cx="12" cy="4.5" r="2"/><circle cx="5.5" cy="13" r="2"/><circle cx="12" cy="13" r="2"/><circle cx="18.5" cy="13" r="2"/><path d="M12 6.5v4.5M10.6 5.9 6.7 11.4M13.4 5.9l3.9 5.5"/><path d="M5.5 15v3M12 15v3M18.5 15v3"/>'),
    "car": ("Car", '<path d="M4 15.5v-3l2-4.5h12l2 4.5v3z"/><path d="M4 15.5V18h2.5v-2.5M17.5 15.5V18H20v-2.5"/><circle cx="7.5" cy="12.8" r="1"/><circle cx="16.5" cy="12.8" r="1"/>'),
    "phone": ("Phone", '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>'),
    "card": ("Card", '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/>'),
    "shield": ("Shield", '<path d="M12 2.5 4 5.5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10v-6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>'),
    "stream": ("Events", '<path d="M4 7h10M4 12h16M4 17h7"/><circle cx="18" cy="7" r="2"/><circle cx="15" cy="17" r="2"/>'),
    "devices": ("Devices", '<rect x="2.5" y="4" width="13" height="10" rx="1.5"/><path d="M6 18h6"/><rect x="16.5" y="8" width="5" height="12" rx="1.2"/>'),
    "external": ("Open", '<path d="M7 17 17 7M9 7h8v8"/>'),
    "arrow": ("Arrow", '<path d="M5 12h14m-6-6 6 6-6 6"/>'),
    "pdf": ("PDF", '<path d="M6 2.5h8.5L19 7v14.5H6z"/><path d="M14.5 2.5V7H19M9 13h6M9 16.5h4"/>'),
    "globe": ("Website", '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>'),
    "users": ("People", '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.6-3.3 3-5.3 6-5.3s5.4 2 6 5.3"/><path d="M16 5.2a3 3 0 0 1 0 5.6M18.5 14.9c1.4.8 2.3 2.5 2.6 5.1"/>'),
    "desktop": ("Desktop", '<rect x="2.5" y="4" width="19" height="13" rx="2"/><path d="M8.5 21h7M12 17v4"/>'),
    "server": ("Backend", '<rect x="3.5" y="3.5" width="17" height="7" rx="1.8"/><rect x="3.5" y="13.5" width="17" height="7" rx="1.8"/><path d="M7.5 7h.01M7.5 17h.01M11.5 7h5M11.5 17h5"/>'),
    "pause": ("Pause", '<path d="M9 6v12M15 6v12"/>'),
    "play": ("Play", '<path d="M8 5.5v13l10.5-6.5z"/>'),
    "chev-l": ("Previous", '<path d="m14.5 6-6 6 6 6"/>'),
    "chev-r": ("Next", '<path d="m9.5 6 6 6-6 6"/>'),
    "mail": ("Email", '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>'),
    "zoom": ("Enlarge", '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5M10.5 8v5M8 10.5h5"/>'),
    "close": ("Close", '<path d="M6 6l12 12M18 6 6 18"/>'),
    "bell": ("Notifications", '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z"/><path d="M10 20.5a2.2 2.2 0 0 0 4 0"/>'),
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "logo-builder"}), timeout=30) as r:
        return r.read().decode()


def lum(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_on_white(rgb):
    return 1.05 / (lum(rgb) + 0.05)


def for_white(hexcol):
    rgb = tuple(int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    t = 0.0
    out = rgb
    while contrast_on_white(out) < 3.0 and t < 1:
        t += 0.02
        out = tuple(round(c + (n - c) * t) for c, n in zip(rgb, NAVY))
    return "#%02x%02x%02x" % out, round(contrast_on_white(out), 2)


meta = {i["slug"]: i for i in json.loads(fetch(f"https://cdn.jsdelivr.net/npm/simple-icons@{VERSION}/data/simple-icons.json"))}
symbols, data = [], {}
for slug in BRANDS:
    svg = fetch(f"https://cdn.jsdelivr.net/npm/simple-icons@{VERSION}/icons/{slug}.svg")
    d = re.search(r'<path d="([^"]+)"', svg).group(1)
    col, cr = for_white(meta[slug]["hex"])
    data[slug] = {"title": meta[slug]["title"], "color": col, "brand": "#" + meta[slug]["hex"], "contrast": cr, "kind": "brand"}
    symbols.append(f'<symbol id="{slug}" viewBox="0 0 24 24"><path fill="currentColor" d="{d}"/></symbol>')
for slug, (title, hexcol, d) in EXTRA_BRANDS.items():
    col, cr = for_white(hexcol)
    data[slug] = {"title": title, "color": col, "brand": "#" + hexcol, "contrast": cr, "kind": "brand"}
    symbols.append(f'<symbol id="{slug}" viewBox="0 0 24 24"><path fill="currentColor" d="{d}"/></symbol>')
for slug, (title, body) in GLYPHS.items():
    data[slug] = {"title": title, "color": "#1e3a8a", "kind": "glyph"}
    symbols.append(f'<symbol id="{slug}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                   f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{body}</symbol>')

sprite = ('<svg xmlns="http://www.w3.org/2000/svg">\n<!-- Brand marks: Simple Icons ' + VERSION +
          ' (CC0). Each mark remains a trademark of its owner. -->\n' + "\n".join(symbols) + "\n</svg>\n")
os.makedirs(f"{ROOT}/assets", exist_ok=True)
open(f"{ROOT}/assets/logos.svg", "w").write(sprite)
json.dump(data, open(f"{ROOT}/tools/logos.json", "w"), indent=1, ensure_ascii=False)
adj = [f"{k} {v['brand']}->{v['color']}" for k, v in data.items() if v["kind"] == "brand" and v["brand"].lower() != v["color"]]
print(f"{len(data)} symbols, {len(sprite) // 1024} KB; darkened for 3:1 on white: {', '.join(adj)}")
