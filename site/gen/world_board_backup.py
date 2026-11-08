# "Worldwide" section as an airport departures board: split-flap letters that flip through every client country.
import math, html, json

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
ROWS = 7
W = {'code': 2, 'country': 14, 'cont': 10, 'dist': 9, 'status': 9}

def dist_km(lat1, lon1, lat2, lon2):
  p1, p2, dl = math.radians(lat1), math.radians(lat2), math.radians(lon2 - lon1)
  return 2 * 6371 * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))

def board_rows():
  rows = []
  for i, (name, code, la, lo, cont) in enumerate(COUNTRIES):
    d = int(round(dist_km(DHAKA[0], DHAKA[1], la, lo) / 100.0) * 100)
    rows.append({'code': code, 'country': name.upper(), 'cont': cont.upper(), 'dist': '{:,}KM'.format(d), 'status': 'DELIVERED'})
  return rows

def cells(text, n, cls):
  t = text[:n].ljust(n)
  return '<span class="bd-fcol %s">%s</span>' % (cls, ''.join('<span class="bd-fc">%s</span>' % ('&nbsp;' if ch == ' ' else html.escape(ch)) for ch in t))

def world_html(theme='navy', label='Worldwide', sid='bd-world'):
  rows = board_rows()
  body = []
  for r in rows[:ROWS]:
    body.append('<div class="bd-frow">%s%s%s%s%s</div>' % (cells(r['code'], W['code'], 'bd-fc-code'), cells(r['country'], W['country'], 'bd-fc-country'),
      cells(r['cont'], W['cont'], 'bd-fc-cont'), cells(r['dist'], W['dist'], 'bd-fc-dist'), cells(r['status'], W['status'], 'bd-fc-status')))
  sr = ''.join('<li>%s</li>' % html.escape(c[0]) for c in COUNTRIES)
  return '''<section id="%s" data-theme="%s" class="bd-world">
<div class="bd-wrap">
<div class="bd-world-top">
<div>
<div class="bd-mono bd-world-k"><span class="bd-world-live"></span>%s</div>
<h2 class="bd-world-h">250+ websites,<br>shipped from <span>one desk in Dhaka.</span></h2>
</div>
<div class="bd-world-stats">
<div><b data-count="250" data-suffix="+">250+</b><span class="bd-mono">Websites shipped</span></div>
<div><b data-count="14">14</b><span class="bd-mono">Countries</span></div>
<div><b data-count="%d">%d</b><span class="bd-mono">Continents</span></div>
<div><b data-count="101">101</b><span class="bd-mono">Fiverr reviews</span></div>
</div>
</div>
<div class="bd-board" data-rows='%s'>
<div class="bd-board-head bd-mono"><span class="bd-board-title"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 16l20-6-4-2-6 2-6-6-2 1 4 6-4 1-2-2-2 1z"></path></svg>Departures · Dhaka DAC</span><span class="bd-board-clock"><span id="bd-board-time">--:--</span> local</span><span class="bd-board-page">Page <span id="bd-board-pg">1</span> / 2</span></div>
<div class="bd-frow bd-frow-h" aria-hidden="true"><span class="bd-fh bd-fc-code" style="--n:2"><em>Code</em></span><span class="bd-fh bd-fc-country" style="--n:14"><em>Destination</em></span><span class="bd-fh bd-fc-cont" style="--n:10"><em>Region</em></span><span class="bd-fh bd-fc-dist" style="--n:9"><em>Distance</em></span><span class="bd-fh bd-fc-status" style="--n:9"><em>Status</em></span></div>
<div class="bd-board-body" aria-hidden="true">%s</div>
<div class="bd-board-foot bd-mono"><span>All 14 countries · Fiverr and direct clients</span><span class="bd-board-dot"></span><span>Next flight: yours?</span><a href="Audit.dc.html">Book a free audit →</a></div>
<ul class="bd-sr">%s</ul>
</div>
</div>
</section>''' % (sid, theme, label, CONTINENTS, CONTINENTS, html.escape(json.dumps(rows), quote=True), ''.join(body), sr)

WORLD_CSS = r'''
/* ---------- worldwide board ---------- */
@keyframes bd-pulse2{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--rc) 60%,transparent)}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
.bd-world{padding:120px 0;overflow:hidden}
.bd-world-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:32px;margin-bottom:44px}
.bd-world-k{display:flex;align-items:center;gap:10px;color:var(--muted);margin-bottom:20px}
.bd-world-live{width:8px;height:8px;border-radius:50%;background:var(--accent);--rc:var(--accent);animation:bd-pulse2 1.8s infinite}
.bd-world-h{margin:0;font-size:clamp(40px,5vw,80px);font-weight:200;line-height:1;letter-spacing:-0.05em}
.bd-world-h span{color:var(--accent)}
.bd-world-stats{display:grid;grid-template-columns:repeat(4,auto);gap:10px 36px}
.bd-world-stats b{display:block;font-size:clamp(30px,3.2vw,50px);font-weight:200;letter-spacing:-0.045em;line-height:1;font-variant-numeric:tabular-nums}
.bd-world-stats .bd-mono{display:block;margin-top:8px;color:var(--muted);font-size:10px}
.bd-board{position:relative;border-radius:22px;padding:18px 20px 16px;background:#08090C;border:1px solid #1F2433;box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 40px 80px -30px rgba(0,0,0,.7);color:#F2E9D8;overflow:hidden}
.bd-board::after{content:'';position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.015) 0 1px,transparent 1px 3px)}
.bd-board-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;padding:2px 2px 14px;color:#FFB020;font-size:11px}
.bd-board-title{display:inline-flex;align-items:center;gap:10px}
.bd-board-clock,.bd-board-page{color:#9AA0AE}
.bd-board-clock span{color:#F2E9D8}
.bd-frow{display:flex;justify-content:space-between;gap:14px;align-items:center;padding:5px 0}
.bd-frow-h{color:#6B7183;font-size:9.5px;padding:0 0 6px;border-bottom:1px solid #1A1E29;margin-bottom:6px}
.bd-fh{flex:none;font-size:clamp(12px,1.3vw,20px);width:calc(var(--n) * 1.32em + (var(--n) - 1) * 2px)}
.bd-fh em{font-style:normal;font-family:'Geist Mono',monospace;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:#6B7183}
.bd-fc-code .bd-fc{color:#FFB020}
.bd-fc-status .bd-fc{color:#4ADE80}
.bd-board-foot{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin-top:12px;padding-top:12px;border-top:1px solid #1A1E29;color:#9AA0AE;font-size:10.5px}
.bd-board-foot a{margin-left:auto;color:#FFB020}
.bd-board-dot{width:6px;height:6px;border-radius:50%;background:#4ADE80;animation:bd-pulse 2s infinite}
.bd-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;margin:0;padding:0}
@media (max-width: 1100px){.bd-fc-cont{display:none !important}}
@media (max-width: 760px){
 .bd-world{padding:72px 0}
 .bd-world-stats{grid-template-columns:repeat(2,auto)}
 .bd-fc-dist{display:none !important}
 .bd-fcol .bd-fc{font-size:12px}
 .bd-board{padding:14px 12px}
 .bd-frow{gap:8px}
 .bd-board-foot a{margin-left:0}
}
@media (max-width: 420px){.bd-fc-status{display:none !important}}
@media (prefers-reduced-motion: reduce){.bd-fcol .bd-fc.bd-flip{animation:none}}
'''

WORLD_JS = r'''
    // ---------- Worldwide board: split-flap pages + count-up stats ----------
    all('.bd-world').forEach(function (sec) {
      var board = sec.querySelector('.bd-board');
      var rows = []; try { rows = JSON.parse(board.getAttribute('data-rows')); } catch (e) {}
      var rowEls = sec.querySelectorAll('.bd-board-body .bd-frow');
      var cols = ['code', 'country', 'cont', 'dist', 'status'];
      var CH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.';
      var page = 0, vis = false;
      var flipTo = function (cell, ch, delay) {
        if (cell.textContent === ch || (ch === ' ' && cell.textContent === ' ')) return;
        if (reduced) { cell.textContent = ch === ' ' ? ' ' : ch; return; }
        var n = 3 + Math.floor(Math.random() * 6);
        setTimeout(function tick() {
          if (!self._alive) return;
          cell.classList.remove('bd-flip'); void cell.offsetWidth; cell.classList.add('bd-flip');
          if (n-- > 0) { cell.textContent = CH.charAt(Math.floor(Math.random() * CH.length)); setTimeout(tick, 70); }
          else cell.textContent = ch === ' ' ? ' ' : ch;
        }, delay);
      };
      var show = function (p) {
        var start = p * rowEls.length;
        for (var r = 0; r < rowEls.length; r++) {
          var data = rows[(start + r) % rows.length] || {};
          var colEls = rowEls[r].querySelectorAll('.bd-fcol');
          for (var c = 0; c < colEls.length; c++) {
            var cellEls = colEls[c].querySelectorAll('.bd-fc'), txt = String(data[cols[c]] || '');
            for (var k = 0; k < cellEls.length; k++) flipTo(cellEls[k], (txt.charAt(k) || ' '), r * 90 + k * 25);
          }
        }
        var pg = sec.querySelector('#bd-board-pg'); if (pg) pg.textContent = String(p + 1);
      };
      var clock = function () {
        var now = new Date(), dk = new Date(now.getTime() + now.getTimezoneOffset() * 60000 + 6 * 3600000);
        var el = sec.querySelector('#bd-board-time');
        if (el) el.textContent = (dk.getHours() < 10 ? '0' : '') + dk.getHours() + ':' + (dk.getMinutes() < 10 ? '0' : '') + dk.getMinutes();
      };
      clock();
      var ct = setInterval(clock, 20000); self._off.push(function () { clearInterval(ct); });
      if ('IntersectionObserver' in window) {
        var bio = new IntersectionObserver(function (es) {
          var was = vis; vis = es[0].isIntersecting;
          if (vis && !was) { page = 1 - page; show(page); }
        }, { threshold: 0.25 });
        bio.observe(board); self._off.push(function () { bio.disconnect(); });
      }
      if (!reduced) {
        var bt = setInterval(function () { if (vis) { page = (page + 1) % 2; show(page); } }, 6500);
        self._off.push(function () { clearInterval(bt); });
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
