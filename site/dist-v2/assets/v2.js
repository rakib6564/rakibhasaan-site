// v2 motion layer: GSAP + ScrollTrigger + Lenis on one clock.
// Loaded after dc-static.js has mounted the page. The page scripts skip their own reveals,
// theme switching, Home marquee and Home horizontal scroll when window.__V2 is set; this file does them.
(function () {
var run = function () {
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var all = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // ---------- smooth scroll on GSAP's ticker ----------
  var lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true, anchors: true });
    window.__lenis = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    // pause smooth scroll while the full-screen menu is open (the page sets overflow:hidden on <html>)
    new MutationObserver(function () {
      if (document.documentElement.style.overflow === 'hidden') lenis.stop(); else lenis.start();
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['style'] });
  }
  var velocity = function () { return lenis ? lenis.velocity * 60 : 0; };

  // ---------- themes: tween the page colours only when a section boundary is crossed ----------
  var THEMES = {
    ink:    { '--bg': '#0B0B0C', '--fg': '#EDE8DF', '--muted': '#8F8A82', '--line': '#2A2926', '--accent': '#FF5A1F' },
    bone:   { '--bg': '#EDE8DF', '--fg': '#0B0B0C', '--muted': '#6B665E', '--line': '#D2CBBE', '--accent': '#D9480F' },
    navy:   { '--bg': '#0D1A3A', '--fg': '#E9ECF5', '--muted': '#9AA6C4', '--line': '#24335A', '--accent': '#8EA2FF' },
    orange: { '--bg': '#FF5A1F', '--fg': '#0B0B0C', '--muted': '#5A1F08', '--line': '#E04A12', '--accent': '#0B0B0C' }
  };
  var root = document.getElementById('bd-root');
  var current = '';
  var setTheme = function (name, instant) {
    if (!root || !THEMES[name] || name === current) return;
    current = name;
    gsap.to(root, Object.assign({ duration: instant || reduce ? 0 : 0.6, ease: 'power2.out', overwrite: 'auto' }, THEMES[name]));
  };
  var themed = all('#bd-root [data-theme]').filter(function (s) { return !s.parentElement.closest('[data-theme]'); });
  var themeTriggers = function () {
    themed.forEach(function (sec) {
      ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%',
        onEnter: function () { setTheme(sec.getAttribute('data-theme')); },
        onEnterBack: function () { setTheme(sec.getAttribute('data-theme')); } });
    });
  };

  // ---------- helpers ----------
  // Split a text-only element into words (kept whole) made of letters; screen readers get one copy of the text.
  var splitChars = function (el) {
    if (el.children.length || !el.textContent.trim()) return null;
    var text = el.textContent;
    el.textContent = '';
    var vis = document.createElement('span'); vis.setAttribute('aria-hidden', 'true');
    text.split(/(\s+)/).forEach(function (w) {
      if (!w) return;
      if (/^\s+$/.test(w)) { vis.appendChild(document.createTextNode(' ')); return; }
      var ws = document.createElement('span'); ws.className = 'v2-w';
      for (var i = 0; i < w.length; i++) { var c = document.createElement('span'); c.className = 'v2-c'; c.textContent = w[i]; ws.appendChild(c); }
      vis.appendChild(ws);
    });
    var sr = document.createElement('span'); sr.className = 'bd-sr'; sr.textContent = text;
    el.appendChild(vis); el.appendChild(sr);
    return all('.v2-c', vis);
  };
  // Wrap each word of a text-only heading in a clipping mask.
  var splitWords = function (el) {
    if (el.children.length || !el.textContent.trim()) return null;
    var text = el.textContent;
    el.textContent = '';
    var vis = document.createElement('span'); vis.setAttribute('aria-hidden', 'true');
    var inner = [];
    text.trim().split(/\s+/).forEach(function (w, i) {
      if (i) vis.appendChild(document.createTextNode(' '));
      var m = document.createElement('span'); m.className = 'v2-m';
      var s = document.createElement('span'); s.className = 'v2-mi'; s.textContent = w;
      m.appendChild(s); vis.appendChild(m); inner.push(s);
    });
    var sr = document.createElement('span'); sr.className = 'bd-sr'; sr.textContent = text;
    el.appendChild(vis); el.appendChild(sr);
    return inner;
  };

  var hero = document.getElementById('bd-hero');
  var hs = null; // Home horizontal work tween (container for image parallax)

  var mm = gsap.matchMedia();
  mm.add({ motion: '(prefers-reduced-motion: no-preference)', wide: '(min-width: 900px) and (min-height: 560px)' }, function (ctx) {
    if (!ctx.conditions.motion) return;
    var wide = ctx.conditions.wide;

    // ---------- headlines ----------
    var ups = all('[data-up]');
    var heroUps = hero ? ups.filter(function (el) { return hero.contains(el); }) : [];
    var heroChars = [];
    heroUps.forEach(function (el) {
      if (el.closest('h1')) { var cs = splitChars(el); if (cs) { heroChars = heroChars.concat(cs); el.__split = true; } }
    });
    if (heroChars.length) gsap.from(heroChars, { yPercent: 115, rotate: 7, opacity: 0, duration: 1.15, ease: 'expo.out', stagger: 0.022, delay: 0.1 });
    var heroLines = heroUps.filter(function (el) { return !el.__split; });
    if (heroLines.length) gsap.from(heroLines, { yPercent: function (i, el) { return el.parentElement.classList.contains('bd-line') ? 105 : 0; }, y: function (i, el) { return el.parentElement.classList.contains('bd-line') ? 0 : 26; }, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: 0.1, delay: heroChars.length ? 0.45 : 0.1 });
    if (hero) {
      var heroIn = all(':scope > *', hero).filter(function (c) { return c.tagName !== 'CANVAS' && getComputedStyle(c).position !== 'absolute'; });
      if (heroIn.length) gsap.to(heroIn, { yPercent: -12, opacity: 0.25, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
      var heroMeta = all('.bd-hero-top, .bd-hero-meta, .bd-hero-stats, .bd-hero-side', hero);
      if (heroMeta.length) gsap.from(heroMeta, { y: 22, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.1, delay: 0.55 });
    }
    ups.filter(function (el) { return heroUps.indexOf(el) < 0; }).forEach(function (el) {
      var line = el.parentElement && el.parentElement.classList.contains('bd-line') ? el.parentElement : null;
      gsap.from(el, { yPercent: line ? 105 : 0, y: line ? 0 : 30, opacity: 0, duration: 1.1, ease: 'expo.out',
        scrollTrigger: { trigger: line || el, start: 'top 90%', once: true } });
    });

    // ---------- section headings: words rise out of a mask ----------
    all('main h2').forEach(function (h) {
      if (hero && hero.contains(h)) return;
      if (h.closest('#bd-track, .bd-iq, .bd-cs-nav, [data-up]')) return;
      var ws = splitWords(h);
      if (!ws) return;
      gsap.from(ws, { yPercent: 110, duration: 1, ease: 'expo.out', stagger: 0.05, scrollTrigger: { trigger: h, start: 'top 88%', once: true } });
    });

    // ---------- blocks rise in batches ----------
    var riseSel = '.bd-cardx, .bd-tile, .bd-rv, .bd-tl-card, .bd-price, .bd-quote, .bd-faq, .bd-tablewrap, .bd-pcard, .bd-split-r > .bd-p';
    var rise = all(riseSel);
    if (rise.length) {
      gsap.set(rise, { opacity: 0, y: 40 });
      ScrollTrigger.batch(rise, { start: 'top 90%', once: true,
        onEnter: function (b) { gsap.to(b, { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out', stagger: 0.08, overwrite: true, clearProps: 'transform' }); } });
    }

    // ---------- images: clip open + settle (inside the Home track they follow the horizontal scroll) ----------
    var workSec = document.getElementById('bd-work'), track = document.getElementById('bd-track');
    var pin = workSec ? $('.bd-pin', workSec) : null;
    if (wide && workSec && track && pin) {
      var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth + 56); };
      hs = gsap.to(track, { x: function () { return -dist(); }, ease: 'none',
        scrollTrigger: { trigger: workSec, start: 'top top', end: function () { return '+=' + Math.max(1, workSec.offsetHeight - pin.offsetHeight); }, scrub: 0.8, invalidateOnRefresh: true } });
    }
    all('[data-clip]').forEach(function (el) {
      var im = $('img', el), inTrack = hs && track.contains(el);
      var st = inTrack ? { trigger: el, containerAnimation: hs, start: 'left 95%', once: true } : { trigger: el, start: 'top 88%', once: true };
      gsap.fromTo(el, { clipPath: 'inset(12% 8% 12% 8% round 16px)' }, { clipPath: 'inset(0% 0% 0% 0% round 16px)', duration: 1.3, ease: 'expo.out', scrollTrigger: st });
      if (im) gsap.fromTo(im, { scale: 1.18 }, { scale: 1, duration: 1.7, ease: 'expo.out', scrollTrigger: st });
      if (inTrack && im) gsap.fromTo(im, { xPercent: -5 }, { xPercent: 5, ease: 'none', scrollTrigger: { trigger: el, containerAnimation: hs, start: 'left right', end: 'right left', scrub: true } });
    });

    // ---------- statement lines + Home manifesto: words light up as you read ----------
    all('.bd-stmt-lead, #bd-manifesto').forEach(function (el) {
      var ws = all('[data-w]', el);
      if (!ws.length) return;
      gsap.set(ws, { opacity: 0.15, transition: 'none' });
      gsap.to(ws, { opacity: 1, stagger: 0.05, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: 0.6 } });
    });

    // ---------- Home image marquee: constant drift, velocity adds speed and lean ----------
    var m1 = document.getElementById('bd-mq1'), m2 = document.getElementById('bd-mq2');
    if (m1 && m2) {
      var rows = [{ el: m1, dir: 1, x: 0 }, { el: m2, dir: -1, x: 0 }];
      rows.forEach(function (r) { r.set = gsap.quickSetter(r.el, 'x', 'px'); r.half = r.el.scrollWidth / 2; });
      var lean = gsap.quickTo([m1, m2], 'skewX', { duration: 0.5, ease: 'power3' });
      var mqOn = false, mqSec = m1.closest('section') || m1.parentElement;
      ScrollTrigger.create({ trigger: mqSec, start: 'top bottom', end: 'bottom top', onToggle: function (s) { mqOn = s.isActive; } });
      gsap.fromTo([m1.parentElement, m2.parentElement], { rotateX: function (i) { return i ? -10 : 10; } }, { rotateX: function (i) { return i ? 8 : -8; }, ease: 'none', transformPerspective: 1200,
        scrollTrigger: { trigger: mqSec, start: 'top bottom', end: 'bottom top', scrub: true } });
      var mqTick = function (t, dt) {
        if (!mqOn) return;
        var v = velocity(), boost = Math.min(14, Math.abs(v) * 0.014);
        lean(gsap.utils.clamp(-6, 6, v * -0.005));
        rows.forEach(function (r) {
          r.half = r.el.scrollWidth / 2 || 1;
          r.x = gsap.utils.wrap(-r.half, 0, r.x - (1 + boost) * r.dir * (dt / 16.67));
          r.set(r.x);
        });
      };
      gsap.ticker.add(mqTick);
      return function () { gsap.ticker.remove(mqTick); };
    }
  });

  themeTriggers();
  ScrollTrigger.sort();
  // pick the theme for wherever the page opens (reload mid-page, #anchor)
  var start = themed.filter(function (s) { var r = s.getBoundingClientRect(); return r.top <= innerHeight / 2 && r.bottom > innerHeight / 2; })[0];
  setTheme(start ? start.getAttribute('data-theme') : 'ink', true);

  // keep trigger positions right as images load, filters change and menus open
  var rT = 0, lastH = 0;
  var refresh = function () { clearTimeout(rT); rT = setTimeout(function () { ScrollTrigger.refresh(); }, 180); };
  if ('ResizeObserver' in window) new ResizeObserver(function () { var h = document.body.scrollHeight; if (Math.abs(h - lastH) > 4) { lastH = h; refresh(); } }).observe(document.body);
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  document.documentElement.classList.add('v2');
};
// dc-static.js mounts on DOMContentLoaded; this listener is added after its own, so the page exists when run() starts
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
