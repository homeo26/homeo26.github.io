(() => {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMQ = matchMedia('(prefers-reduced-motion: reduce)');
  const reduced = () => reduceMQ.matches;
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

  const year = $('#year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- Nav: border on scroll, active section ---------- */
  const nav = $('.nav');
  const onScrollNav = () => nav.classList.toggle('scrolled', scrollY > 8);
  onScrollNav();
  addEventListener('scroll', onScrollNav, { passive: true });

  const links = new Map($$('.nav-links a').map(a => [a.getAttribute('href').slice(1), a]));
  const navList = $('.nav-links');
  const onNavScroll = () => navList.classList.toggle('at-end', navList.scrollLeft + navList.clientWidth >= navList.scrollWidth - 2);
  navList.addEventListener('scroll', onNavScroll, { passive: true });
  addEventListener('resize', onNavScroll);
  onNavScroll();
  const spy = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      links.forEach(a => a.classList.remove('active'));
      const a = links.get(e.target.id);
      if (a) {
        a.classList.add('active');
        // Keep the active link visible when the nav scrolls sideways on phones.
        if (navList.scrollWidth > navList.clientWidth) {
          const left = navList.scrollLeft + a.getBoundingClientRect().left - navList.getBoundingClientRect().left - 8;
          navList.scrollTo({ left, behavior: reduced() ? 'auto' : 'smooth' });
        }
      }
    }
  }, { rootMargin: '-45% 0px -50% 0px' });
  $$('main section[id]').forEach(s => spy.observe(s));

  /* ---------- Count-up numbers ---------- */
  const countUp = el => {
    const target = Number(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduced() || !Number.isFinite(target)) { el.textContent = target + suffix; return; }
    const dur = 1100;
    const t0 = performance.now();
    const step = now => {
      const p = clamp((now - t0) / dur, 0, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    el.textContent = '0' + suffix;
    requestAnimationFrame(step);
  };
  const counters = $$('[data-count]');
  const countIO = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      countIO.unobserve(e.target);
      countUp(e.target);
    }
  }, { threshold: 0.6 });
  counters.forEach(el => countIO.observe(el));

  /* ---------- Scroll reveal with sibling stagger ---------- */
  const revealEls = $$('[data-reveal]');
  revealEls.forEach(el => {
    const sibs = [...el.parentElement.children].filter(c => c.hasAttribute('data-reveal'));
    const i = Math.min(sibs.indexOf(el), 6);
    el.style.setProperty('--d', `${i * 70}ms`);
  });
  const finishReveal = el => {
    // Hand transitions back to the component once it has settled.
    const done = () => { el.removeAttribute('data-reveal'); el.style.removeProperty('--d'); };
    if (reduced()) { done(); return; }
    el.addEventListener('transitionend', function te(ev) {
      if (ev.target !== el || ev.propertyName !== 'opacity') return;
      el.removeEventListener('transitionend', te);
      done();
    });
  };
  const revealIO = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      revealIO.unobserve(e.target);
      e.target.classList.add('in');
      finishReveal(e.target);
    }
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  revealEls.forEach(el => revealIO.observe(el));

  /* ---------- Timeline progress ---------- */
  const timeline = $('.timeline');
  if (timeline) {
    const fill = document.createElement('span');
    fill.className = 'tl-fill';
    fill.setAttribute('aria-hidden', 'true');
    timeline.prepend(fill);
    const items = $$('.tl-item', timeline);
    let ticking = false;
    const update = () => {
      ticking = false;
      const line = innerHeight * 0.62;
      const r = timeline.getBoundingClientRect();
      fill.style.setProperty('--p', clamp((line - r.top) / r.height, 0, 1).toFixed(4));
      for (const it of items) it.classList.toggle('passed', it.getBoundingClientRect().top + 28 < line);
    };
    const req = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    addEventListener('scroll', req, { passive: true });
    addEventListener('resize', req);
    update();
  }

  /* ---------- Year tabs ---------- */
  $$('[data-tabs]').forEach(box => {
    const tabs = $$('[role="tab"]', box);
    const panels = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));
    const select = (i, focus) => {
      tabs.forEach((t, j) => {
        const on = i === j;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
        if (on && !reduced()) {
          panels[j].classList.remove('enter');
          void panels[j].offsetWidth;
          panels[j].classList.add('enter');
        }
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i, false));
      t.addEventListener('keydown', e => {
        const k = e.key;
        let n = null;
        if (k === 'ArrowRight') n = (i + 1) % tabs.length;
        else if (k === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
        else if (k === 'Home') n = 0;
        else if (k === 'End') n = tabs.length - 1;
        if (n !== null) { e.preventDefault(); select(n, true); }
      });
    });
    panels.forEach(p => p.addEventListener('animationend', () => p.classList.remove('enter')));
    select(0, false);
  });

  /* ---------- Project filter + card spotlight ---------- */
  const grid = $('#proj-grid');
  if (grid) {
    const cards = $$('.card', grid);
    const chips = $$('.chip');
    const count = $('#proj-count');
    chips.forEach(chip => chip.addEventListener('click', () => {
      const f = chip.dataset.filter;
      chips.forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
      let n = 0;
      cards.forEach(card => {
        const show = f === 'all' || card.dataset.cat === f;
        card.classList.toggle('hide', !show);
        card.classList.remove('show');
        if (show) {
          n++;
          card.classList.add('in');
          if (!reduced()) { void card.offsetWidth; card.classList.add('show'); }
        }
      });
      if (count) count.textContent = String(n);
      grid.dispatchEvent(new CustomEvent('carousel:refresh'));
    }));
    grid.addEventListener('animationend', e => e.target.classList?.remove('show'));
    grid.addEventListener('pointermove', e => {
      const card = e.target.closest('.card');
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  }


  /* ---------- Live-site links: if a custom domain doesn't answer, switch to the Netlify address ---------- */
  const liveLinks = $$('a[data-fallback]');
  if (liveLinks.length) {
    // A no-cors request resolves for any HTTP answer and rejects on DNS, TLS or connection failure.
    const reachable = (url, ms) => Promise.race([
      fetch(url, { mode: 'no-cors', cache: 'no-store', credentials: 'omit', referrerPolicy: 'no-referrer' }).then(() => true, () => false),
      new Promise(r => setTimeout(() => r(false), ms)),
    ]);
    const probed = new Map();
    const check = a => {
      const origin = new URL(a.href).origin;
      // One retry, so a single dropped request doesn't switch a healthy domain to its fallback.
      if (!probed.has(origin)) probed.set(origin, reachable(origin + '/', 4000).then(ok => ok ||
        new Promise(r => setTimeout(r, 1200)).then(() => reachable(origin + '/', 4000))));
      probed.get(origin).then(ok => {
        if (ok) return;
        a.href = a.dataset.fallback;
        const host = $('.host', a);
        if (host) host.textContent = new URL(a.dataset.fallback).host;
        a.dataset.routed = 'fallback';
      });
    };
    const projectsSec = $('#projects');
    const io = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return;
      io.disconnect();
      liveLinks.forEach(check);
    }, { rootMargin: '600px 0px' });
    if (projectsSec) io.observe(projectsSec); else liveLinks.forEach(check);
  }

  /* ---------- Lightbox: any screenshot opens enlarged ---------- */
  const lb = $('.lightbox');
  if (lb && typeof lb.showModal === 'function') {
    const lbImg = $('.lb-img', lb), cap = $('.lb-cap', lb);
    document.addEventListener('click', e => {
      const z = e.target.closest('.zoom');
      if (!z) return;
      e.preventDefault();
      const im = $('img', z);
      const w = Number(z.dataset.w), h = Number(z.dataset.h);
      lbImg.src = z.dataset.zoom; lbImg.alt = im.alt; lbImg.width = w; lbImg.height = h;
      lbImg.classList.toggle('is-phone', h > w);
      cap.textContent = im.alt;
      lb.showModal();
      lb.dispatchEvent(new Event('opened'));
    });
    $('.lb-close', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
  }

  /* ---------- Project spotlight: one project at a time, advancing on its own ---------- */
  const spot = $('[data-spot]');
  if (spot) {
    const track = $('.spot-track', spot);
    const slides = $$('.spot-slide', spot);
    const dots = $$('.spot-dot', spot);
    const count = $('.spot-count', spot);
    const bar = $('.spot-timer span', spot);
    const btnPause = $('[data-spot-ctl="pause"]', spot);
    const INTERVAL = 5500;
    let idx = 0, timer = 0, hovered = false, focused = false, visible = false, userPaused = reduced();
    bar.style.setProperty('--spot-ms', `${INTERVAL}ms`);
    const mark = () => {
      slides.forEach((sl, k) => { sl.classList.toggle('active', k === idx); sl.inert = k !== idx; });
      dots.forEach((d, k) => (k === idx ? d.setAttribute('aria-current', 'true') : d.removeAttribute('aria-current')));
      count.textContent = `${idx + 1} / ${slides.length}`;
    };
    const restartBar = on => {
      bar.classList.remove('run');
      if (on) { void bar.offsetWidth; bar.classList.add('run'); }
    };
    const running = () => !userPaused && !hovered && !focused && visible && !document.hidden && !(lb && lb.open);
    const schedule = () => {
      clearTimeout(timer); timer = 0;
      const on = running();
      restartBar(on);
      if (on) timer = setTimeout(() => goTo(idx + 1), INTERVAL);
    };
    function goTo(i, smooth = true) {
      idx = (i + slides.length) % slides.length;
      track.scrollTo({ left: idx * track.clientWidth, behavior: smooth && !reduced() ? 'smooth' : 'auto' });
      mark();
      schedule();
    }
    // Swipes and trackpad scrolls settle on a slide; follow it.
    let settle = 0;
    track.addEventListener('scroll', () => {
      clearTimeout(settle);
      settle = setTimeout(() => {
        const k = Math.round(track.scrollLeft / Math.max(1, track.clientWidth));
        if (k !== idx) { idx = k; mark(); schedule(); }
      }, 140);
    }, { passive: true });
    track.addEventListener('pointerenter', () => { hovered = true; schedule(); });
    track.addEventListener('pointerleave', () => { hovered = false; schedule(); });
    track.addEventListener('focusin', () => { focused = true; schedule(); });
    track.addEventListener('focusout', e => { if (!track.contains(e.relatedTarget)) { focused = false; schedule(); } });
    track.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(idx + 1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(idx - 1); }
    });
    $('[data-spot-ctl="prev"]', spot).addEventListener('click', () => goTo(idx - 1));
    $('[data-spot-ctl="next"]', spot).addEventListener('click', () => goTo(idx + 1));
    dots.forEach((d, k) => d.addEventListener('click', () => goTo(k)));
    const setPauseUi = () => {
      btnPause.setAttribute('aria-pressed', String(userPaused));
      btnPause.setAttribute('aria-label', userPaused ? 'Play slideshow' : 'Pause slideshow');
    };
    btnPause.addEventListener('click', () => { userPaused = !userPaused; setPauseUi(); schedule(); });
    new IntersectionObserver(([en]) => { visible = en.isIntersecting; schedule(); }, { threshold: 0.35 }).observe(track);
    document.addEventListener('visibilitychange', schedule);
    if (lb) { lb.addEventListener('opened', schedule); lb.addEventListener('close', schedule); }
    addEventListener('resize', () => track.scrollTo({ left: idx * track.clientWidth, behavior: 'auto' }));
    setPauseUi(); mark();
    window.__spot = { running: () => timer !== 0, index: () => idx, interval: INTERVAL };
  }

  /* ---------- Browse row: filterable, scrolled with the arrows, a swipe or the keyboard ---------- */
  const car = $('[data-carousel]');
  if (car) {
    const track = $('.track', car);
    const bar = $('.car-progress span', car);
    const step = () => {
      const c = $('.card:not(.hide)', track);
      return c ? c.getBoundingClientRect().width + (parseFloat(getComputedStyle(track).columnGap) || 18) : track.clientWidth;
    };
    const maxScroll = () => track.scrollWidth - track.clientWidth;
    const go = dir => {
      const m = maxScroll();
      if (m <= 2) return;
      let x = track.scrollLeft + dir * step();
      if (dir > 0 && track.scrollLeft >= m - 4) x = 0;
      else if (dir < 0 && track.scrollLeft <= 4) x = m;
      track.scrollTo({ left: x, behavior: reduced() ? 'auto' : 'smooth' });
    };
    const progress = () => {
      const vis = Math.min(1, track.clientWidth / Math.max(1, track.scrollWidth));
      const m = maxScroll();
      const ratio = m > 0 ? track.scrollLeft / m : 0;
      bar.style.setProperty('--w', `${(vis * 100).toFixed(1)}%`);
      bar.style.setProperty('--x', `${(ratio * (1 - vis) * bar.parentElement.clientWidth).toFixed(1)}px`);
    };
    track.addEventListener('scroll', () => requestAnimationFrame(progress), { passive: true });
    track.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
    });
    track.addEventListener('carousel:refresh', () => { track.scrollTo({ left: 0, behavior: 'auto' }); progress(); });
    $('[data-car="prev"]', car).addEventListener('click', () => go(-1));
    $('[data-car="next"]', car).addEventListener('click', () => go(1));
    addEventListener('resize', progress);
    // Touch screens have no hover: mark cards in view so their illustration plays once.
    const slideIO = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) en.target.classList.add('in'); }), { root: track, threshold: 0.6 });
    $$('.card', track).forEach(c => slideIO.observe(c));
    progress();
  }

  /* ---------- Logos orbiting the portrait ---------- */
  const visual = $('.hero-visual');
  const portrait = $('.portrait');
  const portraitImg = $('.portrait img');
  const orbs = $$('.orb');
  if (visual && portrait && portraitImg && orbs.length) {
    let geo = null, raf = 0, onScreen = true;
    // Desktop: the photo's top lines up with the name; its height is capped by the hero's bottom.
    const heroEl = $('.hero'), h1 = $('#hero-title');
    const wide = matchMedia('(min-width: 1021px)');
    const alignPortrait = () => {
      if (!wide.matches) { portrait.style.removeProperty('top'); portrait.style.removeProperty('height'); return; }
      const v = visual.getBoundingClientRect(), t = h1.getBoundingClientRect(), hb = heroEl.getBoundingClientRect().bottom;
      const want = clamp(innerHeight * 0.64, 380, 600);
      portrait.style.top = `${(t.top - v.top).toFixed(1)}px`;
      portrait.style.height = `${Math.max(240, Math.min(want, hb - t.top)).toFixed(1)}px`;
    };
    const measure = () => {
      alignPortrait();
      if (!orbs[0].offsetParent) { geo = null; return; }
      const v = visual.getBoundingClientRect(), p = portrait.getBoundingClientRect();
      const rx = clamp(p.width * 0.92, 170, 320);
      geo = { cx: p.left - v.left + p.width * 0.5, cy: p.top - v.top + p.height * 0.36, rx, ry: rx * 0.3 };
    };
    const place = t => {
      if (!geo) return;
      const n = orbs.length;
      orbs.forEach((o, i) => {
        const a = t * 0.00016 + (i / n) * Math.PI * 2;
        const depth = Math.sin(a); // > 0 is the near side of the ring
        const k = (depth + 1) / 2;
        const x = geo.cx + geo.rx * Math.cos(a), y = geo.cy + geo.ry * depth;
        o.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) scale(${(0.72 + 0.34 * k).toFixed(3)})`;
        o.style.opacity = (0.45 + 0.55 * k).toFixed(3);
        o.style.zIndex = depth > 0 ? '3' : '1';
      });
    };
    const tick = t => { place(t); raf = requestAnimationFrame(tick); };
    const run = () => {
      cancelAnimationFrame(raf);
      measure();
      if (reduced()) { place(0); return; }
      if (onScreen && !document.hidden && geo) raf = requestAnimationFrame(tick);
    };
    if (portraitImg.complete) run(); else portraitImg.addEventListener('load', run, { once: true });
    new ResizeObserver(run).observe(visual);
    wide.addEventListener?.('change', run);
    document.fonts?.ready.then(run);
    new IntersectionObserver(([en]) => { onScreen = en.isIntersecting; run(); }).observe(visual);
    document.addEventListener('visibilitychange', run);
    reduceMQ.addEventListener?.('change', run);
  }

  /* ---------- Hero dot field (2D fallback when WebGL is unavailable) ---------- */
  window.__startDotField = () => {
  const canvas = $('.field');
  const hero = $('.hero');
  if (canvas && hero && canvas.getContext) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    canvas.classList.add('ready');
    window.__hero3d = { mode: '2d' };
    const GAP = 26, R = 170, R2 = R * R;
    let w = 0, h = 0, dots = new Float32Array(0);
    const m = { x: -1e4, y: -1e4, tx: -1e4, ty: -1e4 };
    let raf = 0, onScreen = true;

    const build = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      w = hero.clientWidth; h = hero.clientHeight;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const cols = Math.floor(w / GAP) + 1, rows = Math.floor(h / GAP) + 1;
      const ox = (w - (cols - 1) * GAP) / 2, oy = (h - (rows - 1) * GAP) / 2;
      dots = new Float32Array(cols * rows * 2);
      let k = 0;
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { dots[k++] = ox + c * GAP; dots[k++] = oy + r * GAP; }
    };

    const draw = t => {
      ctx.clearRect(0, 0, w, h);
      m.x += (m.tx - m.x) * 0.14; m.y += (m.ty - m.y) * 0.14;
      const still = reduced();
      ctx.fillStyle = '#1e3a8a';
      const hot = [];
      for (let i = 0; i < dots.length; i += 2) {
        const x = dots[i], y = dots[i + 1];
        const dx = x - m.x, dy = y - m.y, d2 = dx * dx + dy * dy;
        if (d2 < R2) { hot.push(x, y, dx, dy, d2); continue; }
        const wave = still ? 0.5 : (Math.sin(x * 0.011 + y * 0.016 - t * 0.0011) + 1) * 0.5;
        ctx.globalAlpha = 0.08 + wave * 0.12;
        ctx.fillRect(x - 0.8, y - 0.8, 1.6, 1.6);
      }
      ctx.fillStyle = '#2563eb';
      for (let i = 0; i < hot.length; i += 5) {
        const d = Math.sqrt(hot[i + 4]) || 1;
        let k = 1 - d / R; k *= k;
        const px = hot[i] + (hot[i + 2] / d) * k * 9, py = hot[i + 1] + (hot[i + 3] / d) * k * 9;
        ctx.globalAlpha = 0.12 + k * 0.85;
        ctx.beginPath(); ctx.arc(px, py, 0.9 + k * 1.7, 0, Math.PI * 2); ctx.fill();
      }
      ctx.globalAlpha = 1;
    };

    const loop = t => { draw(t); raf = requestAnimationFrame(loop); };
    const start = () => {
      cancelAnimationFrame(raf);
      if (reduced()) { draw(0); return; }
      if (onScreen && !document.hidden) raf = requestAnimationFrame(loop);
    };

    build(); start();
    new ResizeObserver(() => { build(); if (reduced()) draw(0); }).observe(hero);
    new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; start(); }).observe(hero);
    document.addEventListener('visibilitychange', start);
    reduceMQ.addEventListener?.('change', start);
    hero.addEventListener('pointermove', e => {
      const r = hero.getBoundingClientRect();
      m.tx = e.clientX - r.left; m.ty = e.clientY - r.top;
      if (m.x < -1e3) { m.x = m.tx; m.y = m.ty; }
    });
    hero.addEventListener('pointerleave', () => { m.tx = -1e4; m.ty = -1e4; m.x = -1e4; m.y = -1e4; });
  }
  };
})();
