# "Worldwide" section: dot-matrix world map with live arcs from Dhaka, pulsing client markers, tooltips and an auto tour.
import math, html, json, os

DHAKA = (23.81, 90.41)
COUNTRIES = [
  # name, code, lat, lon, continent
  ('United States', 'US', 38.90, -77.04, 'N. America'), ('Belgium', 'BE', 50.85, 4.35, 'Europe'),
  ('United Kingdom', 'GB', 51.51, -0.13, 'Europe'), ('Canada', 'CA', 45.42, -75.70, 'N. America'),
  ('Germany', 'DE', 52.52, 13.40, 'Europe'), ('Hungary', 'HU', 47.50, 19.04, 'Europe'),
  ('Slovakia', 'SK', 48.15, 17.11, 'Europe'), ('Denmark', 'DK', 55.68, 12.57, 'Europe'),
  ('Latvia', 'LV', 56.95, 24.11, 'Europe'), ('Azerbaijan', 'AZ', 40.41, 49.87, 'Asia'),
  ('Nigeria', 'NG', 9.08, 7.40, 'Africa'), ('Uganda', 'UG', 0.35, 32.58, 'Africa'),
  ('Vietnam', 'VN', 21.03, 105.85, 'Asia'), ('New Zealand', 'NZ', -41.29, 174.78, 'Oceania'),
]
CONTINENTS = 5
WREVIEWS = {'US': 72, 'BE': 10, 'GB': 4, 'AZ': 3, 'DE': 2, 'NG': 2, 'NZ': 2, 'SK': 1, 'HU': 1, 'VN': 1, 'CA': 1, 'LV': 1, 'DK': 1, 'UG': 0}
_MD = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'geo', 'mapdata.json')))
MW, MH, LAT0 = _MD['w'], _MD['h'], _MD['lat0']

def dist_km(lat1, lon1, lat2, lon2):
  p1, p2, dl = math.radians(lat1), math.radians(lat2), math.radians(lon2 - lon1)
  return 2 * 6371 * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))

def proj(lat, lon):
  return ((lon + 180) / 360.0 * MW, (LAT0 - lat) / 360.0 * MW)

SECTION = '''<section id="{sid}" data-theme="{theme}" class="bd-world">
<div class="bd-wrap">
<div class="bd-world-top">
<div>
<div class="bd-mono bd-world-k"><span class="bd-world-live"></span>{label}</div>
<h2 class="bd-world-h">250+ websites,<br>shipped from <span>one desk in Dhaka.</span></h2>
</div>
<div class="bd-world-stats">
<div><b data-count="250" data-suffix="+">250+</b><span class="bd-mono">Websites shipped</span></div>
<div><b data-count="14">14</b><span class="bd-mono">Countries</span></div>
<div><b data-count="{cont}">{cont}</b><span class="bd-mono">Continents</span></div>
<div><b data-count="101">101</b><span class="bd-mono">Fiverr reviews</span></div>
</div>
</div>
<div class="bd-mapcard">
<div class="bd-board-head bd-mono"><span class="bd-board-title"><span class="bd-board-dot"></span>Client map</span><span class="bd-board-clock">Dhaka <span id="bd-board-time">--:--</span></span><span class="bd-board-page"><span id="bd-map-n">01</span> / 14</span></div>
<div class="bd-map">
<svg class="bd-map-svg" viewBox="0 0 {mw} {mh}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
<path class="bd-map-base" d="{base}"></path>
{cls}
<path class="bd-map-home" d="{home}"></path>
<g class="bd-arcs">{arcs}</g>
<g class="bd-pkts">{pkts}</g>
</svg>
{mks}
<div class="bd-mk-home" style="left:{hx:.2f}%;top:{hy:.2f}%"><span class="bd-mk-radar"></span><span class="bd-mk-pin"></span><span class="bd-mk-lab bd-mono">Dhaka · HQ</span></div>
<div class="bd-mtip" aria-live="polite"><span class="bd-mono bd-mtip-k"></span><b class="bd-mtip-n"></b><span class="bd-mtip-m"></span></div>
</div>
<div class="bd-board-foot bd-mono"><span>14 countries · 5 continents · hover a dot</span><a href="Audit.dc.html">Your country next? →</a></div>
</div>
<div class="bd-mchips">{chips}</div>
</div>
</section>'''

def world_html(theme='navy', label='Worldwide', sid='bd-world'):
  hx, hy = proj(*DHAKA)
  arcs, pkts, mks, chips, cls = [], [], [], [], []
  order = sorted(range(len(COUNTRIES)), key=lambda i: -WREVIEWS.get(COUNTRIES[i][1], 0))
  for i, (name, code, la, lo, cont) in enumerate(COUNTRIES):
    x, y = proj(la, lo)
    L = math.hypot(x - hx, y - hy)
    cx, cy = (hx + x) / 2, (hy + y) / 2 - L * 0.32
    d = 'M%.1f %.1fQ%.1f %.1f %.1f %.1f' % (hx, hy, cx, cy, x, y)
    arcs.append('<path id="bd-arc-%d" class="bd-arc" data-i="%d" pathLength="1" d="%s" style="--d:%.2fs"></path>' % (i, i, d, 0.25 + i * 0.09))
    pkts.append('<circle class="bd-pkt" data-i="%d" r="2.6"><animateMotion dur="%.1fs" begin="-%.2fs" repeatCount="indefinite"><mpath href="#bd-arc-%d"></mpath></animateMotion></circle>'
      % (i, 2.6 + L / 400.0, (i * 0.53) % 3, i))
    n = WREVIEWS.get(code, 0)
    km = int(round(dist_km(DHAKA[0], DHAKA[1], la, lo) / 100.0) * 100)
    meta = ('%d Fiverr review%s' % (n, '' if n == 1 else 's')) if n else 'Direct client'
    size = 8 + min(math.sqrt(n), 6) * 1.1
    mks.append('<button type="button" class="bd-mk" data-i="%d" data-name="%s" data-k="%s · %s" data-meta="%s · %s km from Dhaka" style="left:%.2f%%;top:%.2f%%;--s:%.1fpx;--rd:%.2fs" aria-label="%s, %s"><span class="bd-mk-ring"></span><span class="bd-mk-dot"></span></button>'
      % (i, html.escape(name), code, html.escape(cont), meta, '{:,}'.format(km), x / MW * 100, y / MH * 100, size, (i * 0.37) % 2.4, html.escape(name), meta))
    if code in _MD['client']:
      cls.append('<path class="bd-map-cl" data-i="%d" d="%s"></path>' % (i, _MD['client'][code]))
  for i in order:
    name, code = COUNTRIES[i][0], COUNTRIES[i][1]
    n = WREVIEWS.get(code, 0)
    chips.append('<button type="button" class="bd-mchip bd-mono" data-i="%d"><span class="bd-mchip-c">%s</span>%s<span class="bd-mchip-n">%s</span></button>'
      % (i, code, html.escape(name), n if n else 'Direct'))
  return SECTION.format(sid=sid, theme=theme, label=label, cont=CONTINENTS, mw=MW, mh=MH, base=_MD['base'], cls=''.join(cls), home=_MD['home'],
    arcs=''.join(arcs), pkts=''.join(pkts), mks=''.join(mks), hx=hx / MW * 100, hy=hy / MH * 100, chips=''.join(chips))

WORLD_CSS = r'''
/* ---------- worldwide live map ---------- */
@keyframes bd-pulse2{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--rc) 60%,transparent)}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
@keyframes bd-ring{0%{transform:scale(1);opacity:.7}100%{transform:scale(3.2);opacity:0}}
@keyframes bd-radar{0%{transform:translate(-50%,-50%) scale(.3);opacity:.8}100%{transform:translate(-50%,-50%) scale(1);opacity:0}}
.bd-world{padding:120px 0;overflow:hidden}
.bd-world-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:32px;margin-bottom:44px}
.bd-world-k{display:flex;align-items:center;gap:10px;color:var(--muted);margin-bottom:20px}
.bd-world-live{width:8px;height:8px;border-radius:50%;background:var(--accent);--rc:var(--accent);animation:bd-pulse2 1.8s infinite}
.bd-world-h{margin:0;font-size:clamp(40px,5vw,80px);font-weight:200;line-height:1;letter-spacing:-0.05em}
.bd-world-h span{color:var(--accent)}
.bd-world-stats{display:grid;grid-template-columns:repeat(4,auto);gap:10px 36px}
.bd-world-stats b{display:block;font-size:clamp(30px,3.2vw,50px);font-weight:200;letter-spacing:-0.045em;line-height:1;font-variant-numeric:tabular-nums}
.bd-world-stats .bd-mono{display:block;margin-top:8px;color:var(--muted);font-size:10px}
.bd-mapcard{position:relative;display:block;width:100%;box-sizing:border-box;border-radius:22px;padding:18px 22px 14px;background:#08090C;border:1px solid #1F2433;box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 40px 80px -30px rgba(0,0,0,.7);color:#F2E9D8}

.bd-board-head{position:relative;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;padding:2px 2px 10px;color:#F2E9D8;font-size:11px}
.bd-board-title{display:inline-flex;align-items:center;gap:10px}
.bd-board-clock,.bd-board-page{color:#9AA0AE}
.bd-board-clock span,.bd-board-page span{color:#FF5A1F;font-variant-numeric:tabular-nums}
.bd-board-dot{width:7px;height:7px;border-radius:50%;background:#4ADE80;animation:bd-pulse 2s infinite}
.bd-map{position:relative;display:block;width:100%;height:0;padding-bottom:38.6%;margin:10px 0 6px}
.bd-map-svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.bd-map-base,.bd-map-cl,.bd-map-home{fill:none;stroke-linecap:round;stroke-width:2.7}
.bd-map-base{stroke:#22262F}
.bd-map-cl{stroke:#4A3127;transition:stroke .4s}
.bd-map-cl.bd-on{stroke:#FF5A1F}
.bd-map-home{stroke:#F2E9D8}
.bd-arc{fill:none;stroke:#FF5A1F;stroke-width:1;vector-effect:non-scaling-stroke;opacity:0;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 1.6s cubic-bezier(.6,0,.2,1) var(--d),opacity .4s,stroke-width .4s}
.bd-map.bd-in .bd-arc{stroke-dashoffset:0}
.bd-arc.bd-on{opacity:.9;stroke-width:1.2;filter:drop-shadow(0 0 4px rgba(255,90,31,.8))}
.bd-pkt{fill:#FFB38F;opacity:0;transition:opacity .6s}
.bd-map.bd-in .bd-pkt{opacity:0}
.bd-map.bd-in .bd-pkt.bd-on{opacity:1;fill:#fff;transition-delay:0s}
.bd-mk{position:absolute;width:9px;height:9px;padding:0;border:0;background:none;transform:translate(-50%,-50%);cursor:pointer;z-index:2;opacity:0;transition:opacity .5s,transform .35s cubic-bezier(.2,.8,.2,1)}
.bd-map.bd-in .bd-mk{opacity:1;transition-delay:calc(var(--rd) * .3 + 1s),0s}
.bd-mk::before{content:'';position:absolute;inset:-10px}
.bd-mk-dot{position:absolute;inset:0;border-radius:50%;background:#FF5A1F;box-shadow:0 0 10px 2px rgba(255,90,31,.55);transition:background .3s,box-shadow .3s}
.bd-mk-ring{position:absolute;inset:0;border-radius:50%;border:1px solid rgba(255,90,31,.6);animation:bd-ring 3.2s cubic-bezier(.2,.6,.3,1) infinite;animation-delay:var(--rd)}
.bd-mk.bd-on{transform:translate(-50%,-50%) scale(1.5);z-index:3}
.bd-mk.bd-on .bd-mk-dot{background:#FFF4EC;box-shadow:0 0 0 3px rgba(255,90,31,.35),0 0 22px 6px rgba(255,90,31,.7)}
.bd-mk:focus-visible{outline:none}
.bd-mk:focus-visible .bd-mk-dot{box-shadow:0 0 0 3px #08090C,0 0 0 5px #fff}
.bd-mk-home{position:absolute;z-index:2;width:0;height:0}
.bd-mk-pin{position:absolute;left:-5px;top:-5px;width:10px;height:10px;border-radius:50%;background:#F2E9D8;box-shadow:0 0 16px 3px rgba(242,233,216,.45)}
.bd-mk-radar{position:absolute;left:0;top:0;width:44px;height:44px;border-radius:50%;border:1px solid rgba(242,233,216,.35);animation:bd-radar 3s ease-out infinite;pointer-events:none}
.bd-mk-radar2{animation-delay:1.5s}
.bd-mk-lab{position:absolute;left:10px;top:6px;white-space:nowrap;font-size:9.5px;color:#9A958C}
.bd-mtip{position:absolute;z-index:4;pointer-events:none;display:flex;flex-direction:column;gap:2px;width:max-content;max-width:220px;padding:9px 13px 10px;border-radius:12px;background:rgba(12,12,14,.88);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);color:#F2E9D8;border:1px solid rgba(255,90,31,.55);box-shadow:0 0 0 1px rgba(255,90,31,.15),0 0 28px -2px rgba(255,90,31,.45),0 14px 30px -12px rgba(0,0,0,.8);transform:translate(-50%,calc(-100% - 18px));opacity:0;transition:opacity .3s,left .5s cubic-bezier(.2,.8,.2,1),top .5s cubic-bezier(.2,.8,.2,1)}
.bd-mtip::after{content:'';position:absolute;left:50%;bottom:-5px;width:9px;height:9px;margin-left:-4.5px;background:#0E0E10;border-right:1px solid rgba(255,90,31,.55);border-bottom:1px solid rgba(255,90,31,.55);transform:rotate(45deg)}
.bd-mtip.bd-show{opacity:1}
.bd-mtip.bd-tl{transform:translate(-24px,calc(-100% - 18px))}
.bd-mtip.bd-tl::after{left:24px}
.bd-mtip.bd-tr{transform:translate(calc(-100% + 24px),calc(-100% - 18px))}
.bd-mtip.bd-tr::after{left:auto;right:19px;margin-left:0}
.bd-mtip.bd-below{transform:translate(-50%,18px)}
.bd-mtip.bd-below.bd-tl{transform:translate(-24px,18px)}
.bd-mtip.bd-below.bd-tr{transform:translate(calc(-100% + 24px),18px)}
.bd-mtip.bd-below::after{bottom:auto;top:-5px;transform:rotate(225deg)}
.bd-mtip-k{font-size:9px;color:#FF5A1F;letter-spacing:.12em}
.bd-mtip-n{font-size:17px;font-weight:300;letter-spacing:-.02em;line-height:1.15}
.bd-mtip-m{font-size:11.5px;color:#9A958C}
.bd-board-foot{position:relative;display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin-top:10px;padding-top:12px;border-top:1px solid #1A1E29;color:#9AA0AE;font-size:10.5px}
.bd-board-foot a{margin-left:auto;color:#FF5A1F}
.bd-mleg{display:inline-flex;align-items:center;gap:7px}
.bd-mleg-a,.bd-mleg-h{width:8px;height:8px;border-radius:50%}
.bd-mleg-a{background:#FF5A1F}
.bd-mleg-h{background:#F2E9D8}
.bd-mchips{display:flex;flex-wrap:wrap;gap:4px;margin-top:14px}
.bd-mchip{display:inline-flex;align-items:center;gap:7px;padding:6px 12px;border-radius:999px;border:1px solid transparent;background:transparent;color:var(--muted);font-size:10.5px;cursor:pointer;transition:color .3s,border-color .3s,box-shadow .3s}
.bd-mchip-c{display:none}
.bd-mchip-n{color:var(--muted)}
.bd-mchip.bd-on,.bd-mchip:hover{color:var(--fg);border-color:rgba(255,90,31,.55);box-shadow:0 0 18px -4px rgba(255,90,31,.6)}

.bd-mchip.bd-on .bd-mchip-n,.bd-mchip:hover .bd-mchip-n{color:var(--accent)}
@media (max-width: 760px){
 .bd-world{padding:72px 0}
 .bd-world-stats{grid-template-columns:repeat(2,auto)}
 .bd-mapcard{padding:12px 10px;border-radius:16px}
 .bd-map-base,.bd-map-cl,.bd-map-home{stroke-width:3.3}
 .bd-mk-lab{display:none}
 .bd-mk-radar{width:50px;height:50px}
 .bd-mtip{min-width:136px;padding:8px 11px 9px}
 .bd-mtip-n{font-size:16px}
 .bd-mtip-m{font-size:10.5px}
 .bd-board-foot a{margin-left:0}
 .bd-mchip{font-size:10px;padding:6px 10px 6px 6px}
}
@media (prefers-reduced-motion: reduce){.bd-mk-ring,.bd-mk-radar,.bd-pkt{animation:none;display:none}.bd-arc{transition:none}}
'''

WORLD_JS = r'''
    // ---------- Worldwide live map: arcs draw in, auto tour, hover/focus tooltips, count-ups ----------
    all('.bd-world').forEach(function (sec) {
      var map = sec.querySelector('.bd-map');
      var clock = function () {
        var now = new Date(), dk = new Date(now.getTime() + now.getTimezoneOffset() * 60000 + 6 * 3600000);
        var el = sec.querySelector('#bd-board-time');
        if (el) el.textContent = (dk.getHours() < 10 ? '0' : '') + dk.getHours() + ':' + (dk.getMinutes() < 10 ? '0' : '') + dk.getMinutes();
      };
      clock();
      var ct = setInterval(clock, 20000); self._off.push(function () { clearInterval(ct); });
      if (map) {
        var mks = map.querySelectorAll('.bd-mk'), tip = map.querySelector('.bd-mtip');
        var linked = sec.querySelectorAll('[data-i]'), chips = sec.querySelectorAll('.bd-mchip');
        var cur = -1, hold = false, vis = false, tourIx = 0, order = [];
        for (var c = 0; c < chips.length; c++) order.push(+chips[c].getAttribute('data-i'));
        var act = function (i) {
          cur = i;
          for (var k = 0; k < linked.length; k++) linked[k].classList.toggle('bd-on', +linked[k].getAttribute('data-i') === i);
          var mk = mks[i]; if (!mk || !tip) return;
          var x = parseFloat(mk.style.left), y = parseFloat(mk.style.top);
          tip.querySelector('.bd-mtip-k').textContent = mk.getAttribute('data-k');
          tip.querySelector('.bd-mtip-n').textContent = mk.getAttribute('data-name');
          tip.querySelector('.bd-mtip-m').textContent = mk.getAttribute('data-meta');
          tip.style.left = x + '%'; tip.style.top = y + '%';
          tip.classList.toggle('bd-tl', x < 18); tip.classList.toggle('bd-tr', x > 82); tip.classList.toggle('bd-below', y < 32);
          tip.classList.add('bd-show');
          var n = sec.querySelector('#bd-map-n'); if (n) { var p = order.indexOf(i) + 1; n.textContent = (p < 10 ? '0' : '') + p; }
        };
        var bind = function (el) {
          var i = +el.getAttribute('data-i');
          on(el, 'mouseenter', function () { hold = true; act(i); });
          on(el, 'focus', function () { hold = true; act(i); });
          on(el, 'mouseleave', function () { hold = false; tourIx = order.indexOf(i); });
          on(el, 'blur', function () { hold = false; });
          on(el, 'click', function () { act(i); tourIx = order.indexOf(i); });
        };
        for (var m = 0; m < mks.length; m++) bind(mks[m]);
        for (var c2 = 0; c2 < chips.length; c2++) bind(chips[c2]);
        if ('IntersectionObserver' in window) {
          var mio = new IntersectionObserver(function (es) {
            vis = es[0].isIntersecting;
            if (vis && !map.classList.contains('bd-in')) {
              map.classList.add('bd-in');
              setTimeout(function () { if (self._alive && cur < 0) act(order[0]); }, 2200);
            }
          }, { threshold: 0.3 });
          mio.observe(map); self._off.push(function () { mio.disconnect(); });
        } else { map.classList.add('bd-in'); act(order[0]); }
        var tt = setInterval(function () {
          if (!vis || hold || cur < 0 || reduced) return;
          tourIx = (tourIx + 1) % order.length; act(order[tourIx]);
        }, 2800);
        self._off.push(function () { clearInterval(tt); });
      }
      var counted = false, counters = sec.querySelectorAll('[data-count]');
      var runCount = function () {
        if (counted) return;
        var rr = sec.getBoundingClientRect();
        if (rr.top > window.innerHeight * 0.8 || rr.bottom < 0) return;
        counted = true;
        for (var c = 0; c < counters.length; c++) (function (el) {
          var to = parseInt(el.getAttribute('data-count'), 10), suf = el.getAttribute('data-suffix') || '', t0 = performance.now();
          if (reduced) { el.textContent = to + suf; return; }
          var step = function (now) { var p = Math.min(1, (now - t0) / 1600), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(to * e) + (p === 1 ? suf : ''); if (p < 1 && self._alive) requestAnimationFrame(step); };
          requestAnimationFrame(step);
        })(counters[c]);
      };
      on(window, 'scroll', runCount, { passive: true }); runCount();
    });
'''
