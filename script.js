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

  /* ---------- Terminal typing ---------- */
  const term = $('.term-body');
  if (term && !reduced()) {
    const lines = $$('.ln', term);
    lines.forEach(l => l.classList.add('pending'));
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const run = async () => {
      await sleep(350);
      for (const line of lines) {
        const cmd = $('.cmd', line);
        if (cmd) {
          const text = cmd.textContent;
          cmd.textContent = '';
          line.classList.remove('pending');
          for (let i = 1; i <= text.length; i++) {
            cmd.textContent = text.slice(0, i);
            await sleep(34 + Math.random() * 40);
          }
          await sleep(220);
        } else {
          line.classList.remove('pending');
          await sleep(line.classList.contains('out') ? 140 : 0);
        }
      }
    };
    run();
  }

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
      count.textContent = String(n);
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
      ctx.fillStyle = '#ece2d2';
      const hot = [];
      for (let i = 0; i < dots.length; i += 2) {
        const x = dots[i], y = dots[i + 1];
        const dx = x - m.x, dy = y - m.y, d2 = dx * dx + dy * dy;
        if (d2 < R2) { hot.push(x, y, dx, dy, d2); continue; }
        const wave = still ? 0.5 : (Math.sin(x * 0.011 + y * 0.016 - t * 0.0011) + 1) * 0.5;
        ctx.globalAlpha = 0.06 + wave * 0.09;
        ctx.fillRect(x - 0.8, y - 0.8, 1.6, 1.6);
      }
      ctx.fillStyle = '#ed7d27';
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
