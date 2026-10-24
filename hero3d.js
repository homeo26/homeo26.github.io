// Hero background: a field of points rendered with three.js. Waves roll across it,
// rings ripple out from random spots, and the cursor lifts and warms the points under it.
// Falls back to the 2D dot field when WebGL or the module is unavailable.

const canvas = document.querySelector('.field');
const hero = document.querySelector('.hero');
const reduceMQ = matchMedia('(prefers-reduced-motion: reduce)');

const fallback = reason => {
  console.info('hero3d fallback:', reason);
  if (typeof window.__startDotField === 'function') window.__startDotField();
};

const VERT = /* glsl */`
  uniform float uTime;
  uniform vec2 uMouse;
  uniform float uMouseK;
  uniform vec4 uRipples[4];
  uniform float uSize;
  uniform float uPixelRatio;
  varying float vHeat;
  varying float vFade;

  void main() {
    vec3 p = position;
    float t = uTime;
    float h = sin(p.x * 0.33 + t * 0.55) * 0.34
            + cos(p.z * 0.41 - t * 0.42) * 0.28
            + sin((p.x + p.z) * 0.17 + t * 0.27) * 0.24;
    float heat = 0.0;

    float dm = distance(p.xz, uMouse);
    float km = exp(-dm * dm * 0.055) * uMouseK;
    h += km * 1.5;
    heat += km;

    for (int i = 0; i < 4; i++) {
      vec4 r = uRipples[i];
      float age = t - r.z;
      if (age < 0.0 || age > 4.0) continue;
      float d = distance(p.xz, r.xy);
      float ring = exp(-pow(d - age * 4.2, 2.0) * 1.1) * (1.0 - age / 4.0) * r.w;
      h += ring * 0.8;
      heat += ring * 0.9;
    }

    p.y += h;
    vec4 mv = modelViewMatrix * vec4(p, 1.0);
    gl_Position = projectionMatrix * mv;
    float depth = -mv.z;
    gl_PointSize = max(uPixelRatio, uSize * uPixelRatio * (1.0 + heat * 1.1) * (17.0 / depth));
    vHeat = clamp(heat, 0.0, 1.0);
    vFade = smoothstep(50.0, 10.0, depth) * smoothstep(2.5, 6.0, depth);
  }
`;

const FRAG = /* glsl */`
  uniform vec3 uBase;
  uniform vec3 uAccent;
  varying float vHeat;
  varying float vFade;

  void main() {
    float d = length(gl_PointCoord - 0.5);
    if (d > 0.5) discard;
    float soft = smoothstep(0.5, 0.12, d);
    vec3 col = mix(uBase, uAccent, smoothstep(0.05, 0.6, vHeat));
    gl_FragColor = vec4(col, (0.26 + vHeat * 0.72) * soft * vFade);
  }
`;

async function init() {
  if (!canvas || !hero) return;
  // Start fetching three.js first, then probe WebGL on a throwaway canvas so the hero
  // canvas stays free for the 2D fallback and three.js never logs a context error.
  const threeModule = import('./vendor/three.module.min.js');
  const probe = document.createElement('canvas');
  const probeGl = probe.getContext('webgl2') || probe.getContext('webgl');
  if (!probeGl) { threeModule.catch(() => {}); return fallback('no WebGL'); }

  let THREE;
  try {
    THREE = await threeModule;
  } catch (e) {
    return fallback(`module load failed: ${e && e.message}`);
  }

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, powerPreference: 'low-power' });
  } catch (e) {
    return fallback('no WebGL');
  }
  renderer.setClearColor(0x000000, 0);

  const small = matchMedia('(max-width: 760px), (pointer: coarse)').matches;
  const COLS = small ? 64 : 96;
  const ROWS = small ? 44 : 64;
  const W = 66, D = 38, Z0 = -31; // grid spans x [-33, 33], z [-31, 7]

  const pos = new Float32Array(COLS * ROWS * 3);
  let k = 0;
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      pos[k++] = (c / (COLS - 1) - 0.5) * W;
      pos[k++] = 0;
      pos[k++] = Z0 + (r / (ROWS - 1)) * D;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));

  const ripples = Array.from({ length: 4 }, () => new THREE.Vector4(0, 0, -100, 0));
  const uniforms = {
    uTime: { value: 0 },
    uMouse: { value: new THREE.Vector2(0, -999) },
    uMouseK: { value: 0 },
    uRipples: { value: ripples },
    uSize: { value: small ? 3.0 : 2.6 },
    uPixelRatio: { value: 1 },
    uBase: { value: new THREE.Color('#ece2d2') },
    uAccent: { value: new THREE.Color('#ed7d27') },
  };
  const mat = new THREE.ShaderMaterial({
    vertexShader: VERT, fragmentShader: FRAG, uniforms,
    transparent: true, depthWrite: false,
  });
  const scene = new THREE.Scene();
  scene.add(new THREE.Points(geo, mat));

  const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 100);
  let maxDpr = 2;
  const look = new THREE.Vector3(0, -0.6, -8);
  const camBase = new THREE.Vector3(0, 4.6, 12.5);
  camera.position.copy(camBase);
  camera.lookAt(look);

  const resize = () => {
    const w = hero.clientWidth, h = hero.clientHeight;
    const dpr = Math.min(devicePixelRatio || 1, maxDpr);
    renderer.setPixelRatio(dpr);
    renderer.setSize(w, h, false);
    uniforms.uPixelRatio.value = dpr;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };

  // Pointer -> point on the y=0 plane, smoothed.
  const ray = new THREE.Raycaster();
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const ndc = new THREE.Vector2();
  const hit = new THREE.Vector3();
  const target = { x: 0, z: -999, k: 0, px: 0, py: 0 };
  hero.addEventListener('pointermove', e => {
    const r = hero.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    target.px = ndc.x; target.py = ndc.y;
    ray.setFromCamera(ndc, camera);
    if (ray.ray.intersectPlane(plane, hit)) {
      target.x = hit.x; target.z = hit.z; target.k = 1;
      if (uniforms.uMouse.value.y < -500) uniforms.uMouse.value.set(hit.x, hit.z);
    } else {
      target.k = 0;
    }
  });
  hero.addEventListener('pointerleave', () => { target.k = 0; target.px = 0; target.py = 0; });

  let nextRipple = 1.2, slot = 0;
  const spawnRipple = t => {
    const v = ripples[slot];
    v.set((Math.random() - 0.5) * 40, -24 + Math.random() * 22, t, 0.7 + Math.random() * 0.5);
    slot = (slot + 1) % ripples.length;
    nextRipple = t + 1.4 + Math.random() * 1.6;
  };

  const state = { mode: 'webgl', frames: 0, points: COLS * ROWS };
  window.__hero3d = state;

  const clock = new THREE.Clock();
  let raf = 0, onScreen = true, frozen = false;

  // Frame-rate guard: after a 1 s warm-up, a slow 2 s window drops to 1x pixels;
  // a second slow window freezes the field on a still frame.
  const perf = { t0: 0, n: 0, warm: true, strikes: 0, done: false };
  const watchPerf = now => {
    if (!perf.t0) { perf.t0 = now; perf.n = 0; return; }
    perf.n++;
    const dt = now - perf.t0;
    if (perf.warm) { if (dt > 1000) { perf.warm = false; perf.t0 = 0; } return; }
    if (dt < 2000) return;
    const fps = (perf.n * 1000) / dt;
    state.fps = Math.round(fps);
    perf.t0 = 0;
    if (fps >= 30) { perf.done = true; return; }
    perf.strikes++;
    if (maxDpr > 1 && (devicePixelRatio || 1) > 1) { maxDpr = 1; resize(); return; }
    if (perf.strikes >= 2) { frozen = true; state.mode = 'webgl-static'; }
  };

  const frame = () => {
    const t = clock.getElapsedTime();
    uniforms.uTime.value = t;
    const m = uniforms.uMouse.value;
    m.x += (target.x - m.x) * 0.1;
    m.y += (target.z - m.y) * 0.1;
    uniforms.uMouseK.value += (target.k - uniforms.uMouseK.value) * 0.06;
    camera.position.x += (camBase.x + target.px * 1.4 - camera.position.x) * 0.04;
    camera.position.y += (camBase.y + target.py * 0.6 - camera.position.y) * 0.04;
    camera.lookAt(look);
    if (t > nextRipple) spawnRipple(t);
    renderer.render(scene, camera);
    state.frames++;
    state.mouseK = uniforms.uMouseK.value;
  };

  const staticFrame = () => {
    uniforms.uTime.value = 0;
    uniforms.uMouseK.value = 0;
    ripples.forEach(v => v.set(0, 0, -100, 0));
    camera.position.copy(camBase);
    camera.lookAt(look);
    renderer.render(scene, camera);
    state.frames++;
  };

  const loop = now => {
    frame();
    if (!perf.done) watchPerf(now);
    if (frozen) { staticFrame(); return; }
    raf = requestAnimationFrame(loop);
  };
  const start = () => {
    cancelAnimationFrame(raf);
    perf.t0 = 0; perf.warm = true;
    if (reduceMQ.matches || frozen) { staticFrame(); return; }
    if (onScreen && !document.hidden) raf = requestAnimationFrame(loop);
  };

  // Lit-pixel count of a fresh render, for automated checks.
  state.sample = () => {
    renderer.render(scene, camera);
    const gl = renderer.getContext();
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    const px = new Uint8Array(w * h * 4);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
    let lit = 0, warm = 0;
    for (let i = 0; i < px.length; i += 4) {
      if (px[i + 3] > 8) lit++;
      if (px[i + 3] > 40 && px[i] > px[i + 2] + 60) warm++;
    }
    return { lit, warm };
  };

  resize();
  start();
  canvas.classList.add('ready');
  new ResizeObserver(() => { resize(); if (reduceMQ.matches || frozen) staticFrame(); }).observe(hero);
  new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; start(); }).observe(hero);
  document.addEventListener('visibilitychange', start);
  reduceMQ.addEventListener?.('change', start);
  canvas.addEventListener('webglcontextlost', e => { e.preventDefault(); cancelAnimationFrame(raf); });
  canvas.addEventListener('webglcontextrestored', start);
}

init().catch(e => fallback(String(e)));
