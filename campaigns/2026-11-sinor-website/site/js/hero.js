/* Home hero: scroll-linked canvas scene (plain JavaScript, Canvas 2D, no libraries).
   The canvas is decorative (aria-hidden). All words are real DOM text.
   Every drawn value is a pure function of scroll progress p (0 to 1), so scrolling back reverses the scene.
   At p = 1 the scene equals the static SVG fallback in index.html (same geometry).
   Static path (no JS, reduced motion, short or narrow viewport, no canvas, script error) is the default HTML and CSS. */
(function () {
  'use strict';
  var root = document.documentElement;
  var hero = document.getElementById('hero');
  if (!hero) return;
  var stage = hero.querySelector('.hero-stage');
  var canvas = hero.querySelector('.hero-canvas');
  var content = hero.querySelector('.hero-content');
  var foot = hero.querySelector('.hero-foot');
  var caps = hero.querySelectorAll('.hero-captions li');
  var ctx = null;
  try { ctx = canvas.getContext('2d'); } catch (e) { ctx = null; }
  if (!ctx || !stage || !content || !foot) { root.classList.remove('hero-live'); return; }

  /* Geometry in ring units (ring radius = 1, y points down, bow at the top). Same numbers as the SVG. */
  var HULL = [[0,-0.72],[0.12,-0.58],[0.22,-0.34],[0.26,0],[0.26,0.46],[0.24,0.66],[-0.24,0.66],[-0.26,0.46],[-0.26,0],[-0.22,-0.34],[-0.12,-0.58],[0,-0.72]];
  var BRIDGE = [[-0.15,-0.4],[0.15,-0.4],[0.15,-0.2],[-0.15,-0.2],[-0.15,-0.4]];
  var DECK = [[-0.17,0.16],[0.17,0.16],[0.17,0.56],[-0.17,0.56],[-0.17,0.16]];
  var BUS = [[0,-0.2],[0,0.56]];
  var THRUSTERS = [[0,-0.52,0.035],[-0.12,0.56,0.04],[0.12,0.56,0.04]];
  var NODES = [[0.7071,-0.7071],[0.7071,0.7071],[-0.7071,0.7071],[-0.7071,-0.7071]];
  var NODE_TARGET = [[0.24,-0.24],[0.24,0.24],[-0.24,0.24],[-0.24,-0.24]];
  var GRID = [1.45,1.9,2.4];
  var TAU = Math.PI * 2;
  var HALF = Math.PI / 2;
  var TICKS = 72;

  var cs = getComputedStyle(root);
  function tok(name, fallback) { var v = cs.getPropertyValue(name).trim(); return v || fallback; }
  var C = { accent: tok('--c-accent', '#5BA4E0'), hi: tok('--c-accent-hi', '#8CC4F2'), steel: tok('--c-steel', '#7F9BB8'), text: tok('--c-text', '#F2F6FA') };
  function rgb(h) { h = h.replace('#', ''); return [parseInt(h.substr(0, 2), 16), parseInt(h.substr(2, 2), 16), parseInt(h.substr(4, 2), 16)]; }
  var A = rgb(C.accent);

  /* Precomputed once, nothing allocated per frame. */
  var cum = [0];
  for (var i = 1; i < HULL.length; i++) {
    cum.push(cum[i - 1] + Math.hypot(HULL[i][0] - HULL[i - 1][0], HULL[i][1] - HULL[i - 1][1]));
  }
  var hullLen = cum[cum.length - 1];
  var tickCos = [], tickSin = [];
  for (var k = 0; k < TICKS; k++) { var a = -HALF + k * TAU / TICKS; tickCos.push(Math.cos(a)); tickSin.push(Math.sin(a)); }
  var glowGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, 1.6);
  glowGrad.addColorStop(0, 'rgba(' + A[0] + ',' + A[1] + ',' + A[2] + ',1)');
  glowGrad.addColorStop(0.45, 'rgba(' + A[0] + ',' + A[1] + ',' + A[2] + ',0.35)');
  glowGrad.addColorStop(1, 'rgba(' + A[0] + ',' + A[1] + ',' + A[2] + ',0)');

  var mqMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var mqView = window.matchMedia('(min-width: 360px) and (min-height: 560px)');
  var live = false, ticking = false, onScreen = true, io = null;
  var W = 0, H = 0, dpr = 1, cx = 0, cy = 0, R = 100, stickyTop = 0;
  var p = 0, lastP = -1, lastIdx = -1;

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function seg(v, a, b) { var t = clamp((v - a) / (b - a)); return t * t * (3 - 2 * t); }
  function glowAt(v) {
    if (v < 0.33) return 0.10 + 0.15 * (v / 0.33);
    if (v < 0.66) return 0.25 + 0.20 * ((v - 0.33) / 0.33);
    return 0.45 - 0.17 * seg(v, 0.66, 1);
  }

  function line(poly, upto) {
    ctx.moveTo(poly[0][0], poly[0][1]);
    var n = poly.length;
    if (upto >= 1) { for (var j = 1; j < n; j++) ctx.lineTo(poly[j][0], poly[j][1]); return; }
    var total = 0, j2, seglen = [];
    for (j2 = 1; j2 < n; j2++) { var l = Math.hypot(poly[j2][0] - poly[j2 - 1][0], poly[j2][1] - poly[j2 - 1][1]); seglen[j2] = l; total += l; }
    var target = total * upto, run = 0;
    for (j2 = 1; j2 < n; j2++) {
      if (run + seglen[j2] <= target) { ctx.lineTo(poly[j2][0], poly[j2][1]); run += seglen[j2]; }
      else { var t = (target - run) / seglen[j2]; ctx.lineTo(poly[j2 - 1][0] + (poly[j2][0] - poly[j2 - 1][0]) * t, poly[j2 - 1][1] + (poly[j2][1] - poly[j2 - 1][1]) * t); break; }
    }
  }

  function hullPath(upto) {
    var target = hullLen * upto;
    ctx.moveTo(HULL[0][0], HULL[0][1]);
    for (var j = 1; j < HULL.length; j++) {
      if (cum[j] <= target) ctx.lineTo(HULL[j][0], HULL[j][1]);
      else {
        var t = (target - cum[j - 1]) / (cum[j] - cum[j - 1]);
        ctx.lineTo(HULL[j - 1][0] + (HULL[j][0] - HULL[j - 1][0]) * t, HULL[j - 1][1] + (HULL[j][1] - HULL[j - 1][1]) * t);
        break;
      }
    }
  }

  function render() {
    var s = R * (1 + 0.06 * (1 - seg(p, 0.66, 1)));
    var px = 1 / s;
    var hullP = 0.4 + 0.6 * seg(p, 0, 0.22);
    var detailA = seg(p, 0.12, 0.33);
    var ringP = seg(p, 0.06, 0.33);
    var tickA = seg(p, 0.22, 0.38);
    var nodeA = seg(p, 0.33, 0.5);
    var lineP = seg(p, 0.45, 0.62);
    var markA = seg(p, 0.5, 0.66);
    var j;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(s, s);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    /* single soft glow, kept inside the ring area */
    ctx.globalAlpha = glowAt(p);
    ctx.fillStyle = glowGrad;
    ctx.beginPath(); ctx.arc(0, 0, 1.6, 0, TAU); ctx.fill();

    /* faint chart grid arcs and horizon */
    ctx.strokeStyle = C.steel; ctx.lineWidth = px;
    ctx.globalAlpha = 0.05 + 0.05 * p;
    ctx.beginPath();
    for (j = 0; j < GRID.length; j++) { ctx.moveTo(GRID[j], 0); ctx.arc(0, 0, GRID[j], 0, TAU); }
    ctx.stroke();
    ctx.globalAlpha = 0.08;
    ctx.beginPath(); ctx.moveTo(-cx / s, 0); ctx.lineTo((W - cx) / s, 0); ctx.stroke();

    /* ring, drawn clockwise from the top */
    if (ringP > 0) {
      ctx.shadowColor = C.accent; ctx.shadowBlur = 12 * dpr;
      ctx.strokeStyle = C.hi; ctx.globalAlpha = 0.95; ctx.lineWidth = 2 * px;
      ctx.beginPath(); ctx.arc(0, 0, 1 + 0.06 * (1 - ringP), -HALF, -HALF + TAU * ringP); ctx.stroke();
      ctx.shadowBlur = 0;
    }
    if (tickA > 0) {
      ctx.strokeStyle = C.steel; ctx.lineWidth = px; ctx.globalAlpha = 0.7 * tickA;
      ctx.beginPath();
      for (j = 0; j < TICKS; j++) {
        var len = j % 6 === 0 ? 0.09 : 0.045;
        ctx.moveTo(tickCos[j] * 1.03, tickSin[j] * 1.03);
        ctx.lineTo(tickCos[j] * (1.03 + len), tickSin[j] * (1.03 + len));
      }
      ctx.stroke();
    }

    /* hull, bow first */
    ctx.shadowColor = C.accent; ctx.shadowBlur = 10 * dpr;
    ctx.strokeStyle = C.hi; ctx.globalAlpha = 1; ctx.lineWidth = 2 * px;
    ctx.beginPath(); hullPath(hullP); ctx.stroke();
    ctx.shadowBlur = 0;

    if (detailA > 0) {
      ctx.globalAlpha = 0.75 * detailA; ctx.lineWidth = 1.25 * px;
      ctx.beginPath(); line(BRIDGE, 1); line(DECK, 1); ctx.stroke();
    }

    /* reference nodes and links to the vessel */
    if (nodeA > 0) {
      for (j = 0; j < 4; j++) {
        var nx = NODES[j][0], ny = NODES[j][1];
        ctx.globalAlpha = 0.25 * nodeA; ctx.fillStyle = C.hi;
        ctx.beginPath(); ctx.arc(nx, ny, 0.09 * nodeA, 0, TAU); ctx.fill();
        ctx.globalAlpha = nodeA; ctx.fillStyle = C.text;
        ctx.beginPath(); ctx.arc(nx, ny, 0.045 * nodeA, 0, TAU); ctx.fill();
        if (lineP > 0) {
          var tx = NODE_TARGET[j][0], ty = NODE_TARGET[j][1];
          ctx.globalAlpha = 0.7; ctx.strokeStyle = C.hi; ctx.lineWidth = px;
          ctx.beginPath(); ctx.moveTo(nx, ny); ctx.lineTo(nx + (tx - nx) * lineP, ny + (ty - ny) * lineP); ctx.stroke();
          if (lineP > 0.98) { ctx.globalAlpha = 0.9; ctx.fillStyle = C.hi; ctx.beginPath(); ctx.arc(tx, ty, 0.02, 0, TAU); ctx.fill(); }
        }
      }
    }

    /* thruster markers and the short line along the hull */
    if (markA > 0) {
      ctx.strokeStyle = C.hi; ctx.lineWidth = 1.5 * px; ctx.globalAlpha = 0.9 * markA;
      ctx.beginPath();
      for (j = 0; j < THRUSTERS.length; j++) { ctx.moveTo(THRUSTERS[j][0] + THRUSTERS[j][2], THRUSTERS[j][1]); ctx.arc(THRUSTERS[j][0], THRUSTERS[j][1], THRUSTERS[j][2], 0, TAU); }
      ctx.stroke();
      ctx.globalAlpha = 0.8 * markA; ctx.lineWidth = px;
      ctx.beginPath(); line(BUS, markA); ctx.stroke();
    }

    /* point at the vessel centre */
    ctx.globalAlpha = 0.9; ctx.fillStyle = C.hi;
    ctx.beginPath(); ctx.arc(0, 0, 0.03, 0, TAU); ctx.fill();
    ctx.restore();
    ctx.globalAlpha = 1;
  }

  function computeP() {
    var r = hero.getBoundingClientRect();
    var travel = r.height - stage.offsetHeight;
    p = travel > 0 ? clamp((stickyTop - r.top) / travel) : 0;
  }

  function updateText() {
    var idx = Math.min(caps.length - 1, Math.round(p * (caps.length - 1)));
    if (idx !== lastIdx) {
      for (var j = 0; j < caps.length; j++) caps[j].classList.toggle('is-active', j === idx);
      lastIdx = idx;
    }
    hero.classList.toggle('is-scrolled', p > 0.05);
  }

  function frame() {
    ticking = false;
    if (!live || !onScreen) return;
    computeP();
    if (p !== lastP) { lastP = p; updateText(); render(); }
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }

  function layout() {
    var sr = stage.getBoundingClientRect();
    W = Math.round(sr.width); H = Math.round(sr.height);
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    stickyTop = parseFloat(getComputedStyle(stage).top) || 0;
    var contentBottom = content.getBoundingClientRect().bottom - sr.top;
    var footTop = foot.getBoundingClientRect().top - sr.top;
    if (W >= 1024) {
      R = Math.min(H * 0.34, W * 0.19);
      cx = W - Math.max(40, W * 0.05) - R * 1.15;
      cy = H * 0.5;
      return contentBottom <= footTop - 8;
    }
    var avail = footTop - contentBottom - 16;
    R = Math.min(W * 0.34, (avail / 2) * 0.94 / 1.06);
    cx = W / 2;
    cy = contentBottom + 8 + avail / 2;
    return R >= 52;
  }

  function onResize() {
    if (!live) return;
    if (!layout()) { stop(); return; }
    lastP = -1; computeP(); frame();
  }
  function onScroll() { request(); }

  function start() {
    root.classList.add('hero-live');
    live = true;
    if (!layout()) { stop(); return; }
    window.addEventListener('scroll', onScroll, { passive: true });
    if ('IntersectionObserver' in window) {
      io = new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        if (onScreen) { lastP = -1; request(); }
      });
      io.observe(hero);
    }
    lastP = -1; lastIdx = -1;
    computeP(); updateText(); render();
  }
  function stop() {
    live = false;
    root.classList.remove('hero-live');
    hero.classList.remove('is-scrolled');
    window.removeEventListener('scroll', onScroll);
    if (io) { io.disconnect(); io = null; }
    onScreen = true;
    for (var j = 0; j < caps.length; j++) caps[j].classList.remove('is-active');
    lastIdx = -1;
  }
  function want() { return !mqMotion.matches && mqView.matches; }
  function sync() {
    if (want()) { if (!live) start(); else onResize(); }
    else if (live) stop();
  }

  function listen(mq, fn) { if (mq.addEventListener) mq.addEventListener('change', fn); else if (mq.addListener) mq.addListener(fn); }
  listen(mqMotion, sync);
  listen(mqView, sync);
  var resizeQueued = false;
  window.addEventListener('resize', function () {
    if (resizeQueued) return;
    resizeQueued = true;
    requestAnimationFrame(function () { resizeQueued = false; sync(); });
  });

  try { sync(); } catch (err) { stop(); }
}());
