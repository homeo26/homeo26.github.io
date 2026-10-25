#!/usr/bin/env python3
"""Headless-Chrome checks for the portfolio, run with in-page assertions (no screenshots).

Usage: python3 tools/check_site.py [URL]   (default: http://127.0.0.1:8137/)
Needs: Google Chrome, `pip install websocket-client`. The debugging port binds to 127.0.0.1.
"""
import json, os, signal, subprocess, sys, time, urllib.request
import websocket

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8137/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9342
PROFILE = os.path.expanduser("~/.cache/portfolio-check-chrome")

subprocess.run(["rm", "-rf", PROFILE])
proc = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}", "--remote-debugging-address=127.0.0.1",
                         f"--user-data-dir={PROFILE}", "--no-first-run", "--disable-extensions", "--use-angle=metal", "about:blank"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
fails = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


try:
    for _ in range(60):
        try:
            page = next(t for t in json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")) if t["type"] == "page")
            break
        except Exception:
            time.sleep(0.25)
    ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
    mid, events = [0], []

    def cmd(method, **params):
        mid[0] += 1
        ws.send(json.dumps({"id": mid[0], "method": method, "params": params}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == mid[0]:
                return m.get("result", {})
            events.append(m)

    def js(expr):
        r = cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", r["exceptionDetails"]))
        return r["result"].get("value")

    def load(w, h):
        cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=w < 600)
        cmd("Page.navigate", url=URL)
        time.sleep(2.5)
        js("document.fonts.ready.then(() => true)")
        for y in range(0, 20000, 600):
            js(f"scrollTo(0, {y})"); time.sleep(0.05)
        time.sleep(1.0)
        js("scrollTo(0, 0)"); time.sleep(0.4)

    for d in ("Runtime", "Log", "Page"):
        cmd(f"{d}.enable")

    load(1440, 900)
    errs = [e for e in events if e.get("method") == "Runtime.exceptionThrown"
            or (e.get("method") == "Log.entryAdded" and e["params"]["entry"]["level"] == "error")
            or (e.get("method") == "Runtime.consoleAPICalled" and e["params"]["type"] == "error")]
    check("no console errors or CSP violations", not errs, json.dumps(errs)[:300])
    r = js("[...document.images].filter(i => !i.classList.contains('lb-img') && !(i.complete && i.naturalWidth)).map(i => i.getAttribute('src'))")
    check("all images load", not r, str(r))
    r = js("[...document.querySelectorAll('svg.lg use')].filter(u => u.closest('svg').getBoundingClientRect().width && !(u.getBBox().width > 0)).length")
    check("every visible logo renders", r == 0, f"{r} blank")
    r = js("""(() => { const s = document.querySelector('#skills'), c = document.querySelector('#contact');
      return {topics: [...s.querySelectorAll('.topic h3')].map(h => h.textContent.trim()), tiles: s.querySelectorAll('.logo-grid li').length,
              chips: s.querySelectorAll('.topic .chips-plain li').length, contactList: !!c.querySelector('.skills-csv') || c.innerText.includes('Skills:')}; })()""")
    check("skills are grouped in the Skills section, none listed in Contact",
          r["topics"] == ["Software Design", "Systems & Scale", "APIs & Delivery", "Data & Security"] and r["chips"] == 30 and r["tiles"] >= 37 and not r["contactList"], str(r))
    r = js("""(() => { const lum = c => { const m = c.match(/[\\d.]+/g).map(Number).slice(0, 3).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }); return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]; };
      const bg = el => { for (let e = el; e; e = e.parentElement) { if (e.matches('.btn-primary')) return 'rgb(37,99,235)'; const c = getComputedStyle(e).backgroundColor, a = c.match(/[\\d.]+/g); if (a && (a.length < 4 || +a[3] > 0.5)) return c; } return 'rgb(255,255,255)'; };
      const bad = [];
      for (const el of document.querySelectorAll('#skills h3, #skills li span, #skills .chips-plain li, #contact p, #contact a, .stats dt, .stats dd')) {
        if (!el.offsetWidth || !el.textContent.trim()) continue; const s = getComputedStyle(el);
        const L1 = lum(s.color), L2 = lum(bg(el)), cr = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
        const need = parseFloat(s.fontSize) >= 24 || (+s.fontWeight >= 700 && parseFloat(s.fontSize) >= 18.66) ? 3 : 4.5;
        if (cr < need) bad.push(el.textContent.trim().slice(0, 24) + ' ' + cr.toFixed(2)); }
      return bad; })()""")
    check("text contrast in Skills, Contact and stats", not r, str(r[:6]))

    for w, h in ((1440, 900), (1024, 768), (768, 1024), (375, 812), (320, 640)):
        load(w, h)
        r = js("""(() => { const vw = document.documentElement.clientWidth;
          const off = [...document.querySelectorAll('#skills *, #contact *')].filter(e => { const b = e.getBoundingClientRect(); return b.width && (b.right > vw + 1 || b.left < -1); }).length;
          return {sw: document.documentElement.scrollWidth, vw, off}; })()""")
        check(f"{w}px: no horizontal overflow", r["sw"] <= r["vw"] and r["off"] == 0, str(r))
        rows = js("""(() => { const rows = {}; for (const d of document.querySelectorAll('.stats > div')) { const k = Math.round(d.getBoundingClientRect().top);
          (rows[k] = rows[k] || []).push(Math.round(d.querySelector('dd').getBoundingClientRect().top)); } return Object.values(rows).map(r => new Set(r).size); })()""")
        check(f"{w}px: stats line up", all(n == 1 for n in rows), str(rows))
        r = js("""(() => { const g = [...document.querySelectorAll('#skills .skill-group')].map(e => e.getBoundingClientRect());
          let ov = 0; for (let i = 0; i < g.length; i++) for (let j = i + 1; j < g.length; j++) { const a = g[i], b = g[j];
            if (!(a.right <= b.left + 1 || b.right <= a.left + 1 || a.bottom <= b.top + 1 || b.bottom <= a.top + 1)) ov++; } return ov; })()""")
        check(f"{w}px: skill groups don't overlap", r == 0, str(r))

    print("\nRESULT:", "ALL PASS" if not fails else f"{len(fails)} FAIL: {fails}")
finally:
    os.killpg(proc.pid, signal.SIGTERM)
    subprocess.run(["rm", "-rf", PROFILE])
