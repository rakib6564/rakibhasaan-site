# Scroll-reactive project marquee for inner pages: two rows that drift in opposite directions,
# follow the scroll direction, speed up and lean with scroll velocity, slow down on hover,
# and open the case study on click.
IMGQ_PAGES = {'Services.dc.html', 'SvcWordPress.dc.html', 'SvcCustom.dc.html', 'SvcSEO.dc.html', 'SvcApps.dc.html',
              'SvcPlatforms.dc.html', 'SvcBrand.dc.html', 'Process.dc.html', 'About.dc.html', 'FAQ.dc.html'}

def imgq_html(cases, label='Recent work', title='250+ sites, a few of them here', only=None):
  items = [c for c in cases if not only or c['industry'] == only]
  def card(c, img):
    return ('<a class="bd-iq-card" href="Case.dc.html#%s" style="--c:%s"><span class="bd-iq-img"><img src="%s" alt="%s" loading="lazy"></span>'
            '<span class="bd-iq-cap"><b>%s</b><span class="bd-mono">%s · %s</span></span></a>') % (
      c['slug'], c.get('color', '#FF5A1F'), img, html.escape(c['name'] + ' website'), html.escape(c['name']),
      html.escape(c['industry'].split(' &')[0]), html.escape(c.get('year') or ''))
  a = [card(c, c['img']) for c in items[0::2]] + [card(c, c['img2'] or c['img']) for c in items[1::2]]
  b = [card(c, c['img']) for c in items[1::2]] + [card(c, c['img2'] or c['img']) for c in items[0::2]]
  if len(a) < 6: a = a * 2
  if len(b) < 6: b = b * 2
  row = lambda xs, d: '<div class="bd-iq-row" data-dir="%d"><div class="bd-iq-track">%s%s</div></div>' % (d, ''.join(xs), ''.join(xs))
  return '''<section data-theme="bone" class="bd-iq" aria-label="%s">
<div class="bd-wrap bd-iq-head"><div class="bd-mono bd-lab">%s</div><h2 class="bd-iq-h">%s</h2><a class="bd-iq-all bd-mono" href="Work.dc.html">See all work →</a></div>
%s
%s
</section>''' % (html.escape(label), html.escape(label), title, row(a, 1), row(b, -1))

IMGQ_CSS = r'''
/* ---------- scroll-reactive project marquee ---------- */
.bd-iq{padding:110px 0 120px;overflow:hidden}
.bd-iq-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px 32px;margin-bottom:40px}
.bd-iq-head .bd-lab{width:100%}
.bd-iq-h{margin:0;font-size:clamp(32px,4vw,60px);font-weight:200;letter-spacing:-.045em;line-height:1}
.bd-iq-all{font-size:11px;color:var(--muted);transition:color .3s}
.bd-iq-all:hover{color:var(--accent)}
.bd-iq-row{padding:10px 0}
.bd-iq-track{display:flex;gap:20px;width:max-content;will-change:transform;transform:translate3d(var(--x,0px),0,0) skewX(var(--sk,0deg))}
.bd-iq-card{position:relative;flex:none;display:block;width:clamp(240px,26vw,420px);text-decoration:none;color:inherit}
.bd-iq-img{display:block;aspect-ratio:3/2;border-radius:18px;overflow:hidden;background:#D8D2C8;transition:transform .6s cubic-bezier(.2,.8,.2,1),border-radius .6s}
.bd-iq-img img{width:100%;height:100%;object-fit:cover;display:block;transform:scale(1.04);transition:transform 1.1s cubic-bezier(.2,.8,.2,1)}
.bd-iq-cap{position:absolute;left:14px;bottom:14px;display:flex;flex-direction:column;gap:2px;padding:10px 14px;border-radius:14px;background:rgba(11,11,12,.82);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#F2E9D8;opacity:0;transform:translateY(10px);transition:opacity .35s,transform .45s cubic-bezier(.2,.8,.2,1);pointer-events:none}
.bd-iq-cap b{font-weight:400;font-size:15px;letter-spacing:-.01em}
.bd-iq-cap .bd-mono{font-size:9.5px;color:#9A958C}
.bd-iq-cap::before{content:'';position:absolute;left:-4px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:var(--c);box-shadow:0 0 12px var(--c)}
.bd-iq-card:hover .bd-iq-img{transform:scale(.97);border-radius:26px}
.bd-iq-card:hover .bd-iq-img img{transform:scale(1.12)}
.bd-iq-card:hover .bd-iq-cap{opacity:1;transform:none}
.bd-iq-card:focus-visible{outline:none}.bd-iq-card:focus-visible .bd-iq-img{box-shadow:0 0 0 3px var(--accent)}
@media (max-width: 760px){.bd-iq{padding:72px 0 80px}.bd-iq-card{width:72vw}.bd-iq-cap{opacity:1;transform:none}}
'''

IMGQ_JS = r'''
    // ---------- Scroll-reactive project marquee ----------
    (function () {
      var rows = all('.bd-iq-row');
      if (!rows.length) return;
      var st = rows.map(function (r) { return { el: r.querySelector('.bd-iq-track'), dir: +r.getAttribute('data-dir') || 1, x: 0, slow: 1, hover: false }; });
      st.forEach(function (s, i) {
        on(rows[i], 'mouseenter', function () { s.hover = true; });
        on(rows[i], 'mouseleave', function () { s.hover = false; });
      });
      var lastY = window.scrollY, vel = 0, sdir = 1, vis = true, raf = 0, prev = performance.now();
      on(window, 'scroll', function () { var y = window.scrollY, d = y - lastY; lastY = y; vel += d; if (Math.abs(d) > 1) sdir = d > 0 ? 1 : -1; }, { passive: true });
      var sec = rows[0].closest('.bd-iq');
      if ('IntersectionObserver' in window && sec) {
        var io = new IntersectionObserver(function (es) { vis = es[0].isIntersecting; }, { rootMargin: '200px 0px' });
        io.observe(sec); self._off.push(function () { io.disconnect(); });
      }
      var tick = function (now) {
        if (!self._alive) return;
        var dt = Math.min(50, now - prev) / 16.67; prev = now;
        var v = vel; vel *= 0.86;
        if (vis) {
          st.forEach(function (s) {
            s.slow += ((s.hover ? 0.15 : 1) - s.slow) * 0.08;
            var w = s.el.scrollWidth / 2 || 1;
            var speed = reduced ? 0 : (0.9 + Math.min(18, Math.abs(v) * 0.25)) * s.slow * dt;
            s.x -= speed * s.dir * sdir;
            if (s.x <= -w) s.x += w; if (s.x > 0) s.x -= w;
            var sk = reduced ? 0 : Math.max(-4, Math.min(4, v * 0.08 * s.dir));
            s.el.style.setProperty('--x', s.x.toFixed(1) + 'px');
            s.el.style.setProperty('--sk', sk.toFixed(2) + 'deg');
          });
        }
        raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
      self._off.push(function () { cancelAnimationFrame(raf); });
    })();
'''
