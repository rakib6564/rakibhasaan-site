class Component extends DCLogic {
  constructor(props) {
    super(props);
    this.state = { /*PAGE_STATE*/ sent: false, mega: false, full: false, fsIdx: 0, chatShown: false, chatHidden: false, chatOpen: false, chatSent: false, chatTopic: '', chatMsg: '', tick: 0 };
    this._off = [];
  }

  componentDidMount() {
    var self = this;
    this._alive = true;
    var mq = function (q) { return !!(window.matchMedia && window.matchMedia(q).matches); };
    var reduced = mq('(prefers-reduced-motion: reduce)');
    var on = function (t, ev, fn, opt) { if (!t) return; t.addEventListener(ev, fn, opt); self._off.push(function () { t.removeEventListener(ev, fn, opt); }); };
    var $ = function (id) { return document.getElementById(id); };
    var all = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };
    var hex = function (h) { return [parseInt(h.substr(1, 2), 16) / 255, parseInt(h.substr(3, 2), 16) / 255, parseInt(h.substr(5, 2), 16) / 255]; };
    var ease = 'cubic-bezier(.2,.8,.2,1)';

    // ---------- Themes ----------
    var themes = {
      ink:    { bg: '#0B0B0C', fg: '#EDE8DF', muted: '#8F8A82', line: '#2A2926', accent: '#FF5A1F' },
      bone:   { bg: '#EDE8DF', fg: '#0B0B0C', muted: '#6B665E', line: '#D2CBBE', accent: '#D9480F' },
      navy:   { bg: '#0D1A3A', fg: '#E9ECF5', muted: '#9AA6C4', line: '#24335A', accent: '#8EA2FF' },
      orange: { bg: '#FF5A1F', fg: '#0B0B0C', muted: '#5A1F08', line: '#E04A12', accent: '#0B0B0C' }
    };
    var setVars = function (el, t) {
      el.style.setProperty('--bg', t.bg); el.style.setProperty('--fg', t.fg);
      el.style.setProperty('--muted', t.muted); el.style.setProperty('--line', t.line); el.style.setProperty('--accent', t.accent);
    };
    var root = $('bd-root'), head = $('bd-header'), prog = $('bd-prog');
    var sections = all('[data-theme]'), pageTheme = '', headTheme = '', lastY = window.scrollY;
    var themeAt = function (y) {
      for (var i = 0; i < sections.length; i++) {
        var r = sections[i].getBoundingClientRect();
        if (r.top <= y && r.bottom > y) return sections[i].getAttribute('data-theme');
      }
      return 'ink';
    };
    var onScroll = function () {
      var y = window.scrollY;
      var pt = themeAt(window.innerHeight * 0.5);
      if (pt !== pageTheme && themes[pt] && root) { pageTheme = pt; setVars(root, themes[pt]); }
      if (head) {
        var ht = themeAt(44);
        if (ht !== headTheme && themes[ht]) { headTheme = ht; setVars(head, themes[ht]); }
        head.classList.toggle('bd-scrolled', y > 40);
        var down = y > lastY + 2, up = y < lastY - 2;
        if (down && y > 500 && !self.state.mega && !self.state.full) head.classList.add('bd-hidden');
        else if (up || y < 500) head.classList.remove('bd-hidden');
        if (root) root.classList.toggle('bd-headhidden', head.classList.contains('bd-hidden'));
      }
      if (prog) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        prog.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0).toFixed(4) + ')';
      }
      var por = $('bd-portrait');
      if (por && !reduced) {
        var pr = por.parentElement.getBoundingClientRect();
        if (pr.bottom > 0 && pr.top < window.innerHeight) por.style.translate = '0 ' + (((pr.top + pr.height / 2 - window.innerHeight / 2) / window.innerHeight) * -7).toFixed(2) + '%';
      }
      all('.bd-band-img img').forEach(function (bi) {
        if (reduced) return;
        var br = bi.parentElement.getBoundingClientRect();
        if (br.bottom > 0 && br.top < window.innerHeight) bi.style.transform = 'translateY(' + ((br.top / window.innerHeight) * -8).toFixed(2) + '%)';
      });
      var ci = document.querySelector('#bd-case-img img');
      if (ci && !reduced) {
        var cr = ci.parentElement.getBoundingClientRect();
        if (cr.bottom > 0 && cr.top < window.innerHeight) ci.style.transform = 'translateY(' + (((cr.top) / window.innerHeight) * -9 - 4).toFixed(2) + '%)';
      }
      lastY = y;
    };
    on(window, 'scroll', onScroll, { passive: true });
    on(window, 'resize', onScroll, { passive: true });
    onScroll();

    // ---------- Headline line reveals ----------
    var ups = all('[data-up]');
    if (!reduced && 'IntersectionObserver' in window) {
      ups.forEach(function (el) { el.style.transform = 'translateY(105%)'; el.style.opacity = '0'; });
      var map = new Map(); ups.forEach(function (el) { map.set(el.parentElement && el.parentElement.classList.contains('bd-line') ? el.parentElement : el, el); });
      var uio = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = map.get(en.target), i = ups.indexOf(el) % 4;
          el.style.transition = 'transform 1.1s ' + ease + ' ' + (i * 0.1) + 's, opacity 0.9s ease ' + (i * 0.1) + 's';
          el.style.transform = 'translateY(0)'; el.style.opacity = '1';
          uio.unobserve(en.target);
        });
      }, { threshold: 0.2 });
      map.forEach(function (v, k) { uio.observe(k); });
      this._off.push(function () { uio.disconnect(); });
    }

    // ---------- Soft rise for blocks ----------
    var rise = all('.bd-cardx, .bd-tile, .bd-rv, .bd-tl-card, .bd-price, .bd-quote, .bd-faq, .bd-tablewrap, .bd-pcard, .bd-split-r > .bd-p');
    if (!reduced && 'IntersectionObserver' in window) {
      rise.forEach(function (el) { el.style.opacity = '0'; el.style.transform = 'translateY(26px)'; });
      var rio = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target, sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) % 6 : 0;
          el.style.transition = 'opacity 0.9s ease ' + (sib * 0.07) + 's, transform 1s ' + ease + ' ' + (sib * 0.07) + 's';
          el.style.opacity = '1'; el.style.transform = 'none';
          rio.unobserve(el);
        });
      }, { threshold: 0.12 });
      rise.forEach(function (el) { rio.observe(el); });
      this._off.push(function () { rio.disconnect(); });
    }

    // ---------- Image clip reveals ----------
    var clips = all('[data-clip]');
    if (!reduced && 'IntersectionObserver' in window) {
      clips.forEach(function (el) { el.style.clipPath = 'inset(12% 8% 12% 8% round 16px)'; el.style.transition = 'clip-path 1.2s ' + ease; var im = el.querySelector('img'); if (im) { im.style.scale = '1.16'; im.style.transition = 'scale 1.6s ' + ease + ', transform 1.1s ' + ease; } });
      var cio = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.style.clipPath = 'inset(0% 0% 0% 0% round 16px)';
          var im = en.target.querySelector('img'); if (im) im.style.scale = '1';
          cio.unobserve(en.target);
        });
      }, { threshold: 0.12 });
      clips.forEach(function (el) { cio.observe(el); });
      this._off.push(function () { cio.disconnect(); });
    }

    // ---------- Magnetic buttons (measure the static wrapper; clamp the pull) ----------
    if (!reduced) {
      all('.bd-magnet').forEach(function (mag) {
        var wrap = mag.parentElement;
        on(wrap, 'pointermove', function (e) {
          var r = wrap.getBoundingClientRect();
          var c = function (v) { return Math.max(-16, Math.min(16, v)); };
          mag.style.transform = 'translate(' + c((e.clientX - r.left - r.width / 2) * 0.22).toFixed(1) + 'px,' + c((e.clientY - r.top - r.height / 2) * 0.22).toFixed(1) + 'px) scale(1.05)';
        });
        on(wrap, 'pointerleave', function () { mag.style.transform = ''; });
      });
    }

    // ---------- Bento glow follows the cursor ----------
    all('.bd-bc').forEach(function (c) {
      on(c, 'pointermove', function (e) { var r = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px'); });
    });
    // ---------- Statement lines: words light up as you scroll ----------
    var leads = all('.bd-stmt-lead');
    var onLeads = function () {
      leads.forEach(function (el) {
        var ws = el.querySelectorAll('[data-w]'), r = el.getBoundingClientRect(), vh = window.innerHeight;
        var p = reduced ? 1 : Math.max(0, Math.min(1, (vh * 0.85 - r.top) / (vh * 0.5 + r.height * 0.5)));
        var lit = Math.round(p * ws.length);
        for (var i = 0; i < ws.length; i++) ws[i].style.opacity = i < lit ? '1' : '0.18';
      });
    };
    if (leads.length) { on(window, 'scroll', onLeads, { passive: true }); onLeads(); }

    // ---------- Checklist ticks, timeline rail, review bars ----------
    var onEls = all('.bd-checks li, .bd-tl'), rails = all('.bd-timeline'), grows = all('[data-grow]');
    var onProgress = function () {
      var vh = window.innerHeight;
      onEls.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top < vh * 0.72) el.classList.add('bd-on'); else if (el.classList.contains('bd-tl')) el.classList.remove('bd-on'); });
      rails.forEach(function (tl) {
        var r = tl.getBoundingClientRect();
        var p = Math.max(0, Math.min(1, (vh * 0.72 - r.top) / Math.max(1, r.height)));
        tl.style.setProperty('--tlp', reduced ? 1 : p.toFixed(3));
      });
      grows.forEach(function (g) { var r = g.getBoundingClientRect(); if (r.top < vh * 0.9) g.style.width = g.getAttribute('data-grow'); });
    };
    if (onEls.length || grows.length) { on(window, 'scroll', onProgress, { passive: true }); on(window, 'resize', onProgress, { passive: true }); onProgress(); }

    // ---------- WebGL hero (shared shader) ----------
    var st = { mx: 0.65, my: 0.55, tx: 0.65, ty: 0.55, col: hex('#FF5A1F'), target: hex('#FF5A1F') };
    on(window, 'pointermove', function (e) { st.tx = e.clientX / window.innerWidth; st.ty = 1 - e.clientY / window.innerHeight; }, { passive: true });
    if ($('bd-gl')) this._startGL(st, reduced);

/*PAGE_MOUNT*/
  }

  componentDidUpdate(prevProps, prevState) {
    var hd = document.getElementById('bd-header');
    if (prevState.mega !== this.state.mega && hd) {
      hd.classList.toggle('bd-open', !!this.state.mega);
      if (this.state.mega) hd.classList.remove('bd-hidden');
    }
    if (prevState.full !== this.state.full) {
      document.documentElement.style.overflow = this.state.full ? 'hidden' : '';
      if (hd && this.state.full) hd.classList.remove('bd-hidden');
    }
  }

  componentWillUnmount() {
    document.documentElement.style.overflow = '';
    this._alive = false;
    if (this._raf) cancelAnimationFrame(this._raf);
    this._off.forEach(function (fn) { fn(); });
    this._off = [];
  }

/*GL*/
  renderVals() {
    var self = this, S = this.state, X = {};
/*SHARED_VALS*/
/*PAGE_VALS*/
    return X;
  }
}
