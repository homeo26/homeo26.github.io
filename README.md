# homeo26.github.io

Personal portfolio of Homam Manasra, served by GitHub Pages at https://homeo26.github.io.

Plain HTML, CSS and JavaScript. `index.html` and `assets/logos.css` are generated from Python
data so content lives in one place; the generated files are committed, so Pages serves them as-is.

```sh
python3 tools/build.py          # regenerate index.html + assets/logos.css from tools/content.py
python3 tools/fetch_logos.py    # rebuild assets/logos.svg + tools/logos.json from Simple Icons
python3 -m http.server 8137 --bind 127.0.0.1   # preview
```

| Path | What it is |
|---|---|
| `tools/content.py` | All page content: experience, projects, skills, contests |
| `tools/art.py` | Inline SVG illustrations for experience entries and projects (motion on hover) |
| `tools/build.py` | Renders the page |
| `styles.css` | White and navy theme, layout, illustration motion |
| `boot.js` | Adds the `js` class before first paint so reveal styles don't flash |
| `script.js` | Nav state, reveal, count-ups, terminal typing, timeline, year tabs, project filter, logo orbit, 2D fallback field |
| `hero3d.js` | three.js point field behind the hero; 2D fallback without WebGL, still frame on slow GPUs |
| `assets/` | Portraits (background removed), project screenshots, logo sprite |
| `vendor/three.module.min.js` | three.js r170 (MIT, see `vendor/LICENSE-three.txt`) |

SEO: `robots.txt`, `sitemap.xml`, Open Graph / Twitter tags with `assets/og-image.png`, and schema.org Person + WebSite
JSON-LD in the page head. After a deploy, submit `https://homeo26.github.io/sitemap.xml` in Google Search Console.

Brand marks come from [Simple Icons](https://simpleicons.org) (CC0) and remain trademarks of their owners.
Motion respects `prefers-reduced-motion`. The Content-Security-Policy allows scripts from this origin only.
