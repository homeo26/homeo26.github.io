# homeo26.github.io

Personal portfolio of Homam Manasra, served by GitHub Pages at https://homeo26.github.io.

Plain HTML, CSS and JavaScript with no build step.

| File | What it does |
|---|---|
| `index.html` | All content: experience, projects, contest results, skills, contact |
| `styles.css` | Layout, palette tokens (with contrast ratios), motion |
| `boot.js` | Adds the `js` class before first paint so reveal styles don't flash |
| `script.js` | Nav state, scroll reveal, count-ups, terminal typing, timeline, year tabs, project filter, 2D fallback field |
| `hero3d.js` | three.js point field behind the hero; falls back to the 2D field without WebGL and freezes on slow GPUs |
| `vendor/three.module.min.js` | three.js r170, vendored (MIT, see `vendor/LICENSE-three.txt`) |

Run locally:

```sh
python3 -m http.server 8137 --bind 127.0.0.1
```

Motion respects `prefers-reduced-motion`. The Content-Security-Policy allows scripts from this origin only.
