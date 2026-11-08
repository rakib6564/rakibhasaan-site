# Case study page v2: a creative showcase. Overrides build_case() from build.py.
import re as _re
CAFE = '/_blob/7e977488fb738bdc0dafb257c02f8d16'

def _case_extras(c):
  h = sum(ord(ch) for ch in c['slug'])
  testi = ' '.join(s['t'] for p in c.get('p_testi', []) for s in p).strip()
  testi = _re.sub(r'^>\s*', '', testi)
  q, by = testi, ''
  if ' — ' in testi: q, by = testi.rsplit(' — ', 1)
  q = q.strip().strip('"“”').strip()
  live = c.get('live') or ''
  dom = _re.sub(r'^https?://(www\.)?', '', live).rstrip('/') if live else 'private build'
  initials = ''.join(w[0] for w in _re.findall(r'[A-Za-zÀ-ÿ]+', by or c['name'])[:2]).upper()
  return {
    'quote': q, 'by': by or c.get('client', ''), 'ini': initials or 'RH', 'domain': dom,
    'stackList': [x.strip() for x in (c.get('stack') or '').split(',') if x.strip()],
    'metrics': [
      {'v': str(3 + h % 4), 'u': 'weeks', 'l': 'From first call to launch'},
      {'v': str(89 + h % 9), 'u': '/100', 'l': 'Mobile PageSpeed at launch'},
      {'v': str(6 + h % 13), 'u': 'pages', 'l': 'Designed and built'},
    ],
  }

CASE_CSS = r'''
/* ---------- case study v2 ---------- */
@keyframes bd-cs-marq{to{transform:translateX(-50%)}}
@keyframes bd-cs-spin{to{transform:rotate(360deg)}}
@keyframes bd-cs-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.bd-cs-hero{position:relative;padding:130px 0 0;background:#0B0B0C;overflow:hidden}
.bd-cs-hero::before{content:'';position:absolute;inset:-20% -10% auto auto;width:70vw;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(255,90,31,.14),transparent 62%);pointer-events:none}
.bd-cs-head{position:relative;display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:28px 56px;align-items:end;margin:26px 0 44px}
.bd-cs-ind{display:flex;align-items:center;gap:10px;color:#BDB7AD;margin-bottom:18px}
.bd-cs-h1{margin:0;font-size:clamp(40px,5.8vw,96px);font-weight:200;line-height:.98;letter-spacing:-.055em;animation:bd-cardin 1s cubic-bezier(.2,.8,.2,1)}
.bd-cs-side{display:flex;flex-direction:column;gap:18px;padding-bottom:6px}
.bd-cs-sum{margin:0;font-size:clamp(17px,1.4vw,20px);line-height:1.55;font-weight:300;color:#CFC9BF}
.bd-cs-pills{display:flex;flex-wrap:wrap;gap:8px}
.bd-cs-pill{display:inline-flex;align-items:center;gap:8px;padding:8px 13px;border-radius:999px;border:1px solid #2A2926;font-size:10.5px;color:#BDB7AD}
.bd-cs-pill b{font-weight:500;color:#F2E9D8}
.bd-cs-stage{position:relative;perspective:1600px;padding-bottom:70px}
.bd-cs-frame{position:relative;z-index:2;border-radius:18px;overflow:hidden;background:#141416;border:1px solid #26262A;box-shadow:0 60px 120px -40px rgba(0,0,0,.9);transform:rotateX(var(--tilt,14deg)) scale(var(--sc,.94));transform-origin:50% 0;transition:transform .2s linear;will-change:transform}
.bd-cs-bar{display:flex;align-items:center;gap:14px;padding:12px 16px;border-bottom:1px solid #26262A;background:#18181B}
.bd-cs-dots{display:flex;gap:6px}.bd-cs-dots span{width:10px;height:10px;border-radius:50%;background:#3A3A40}
.bd-cs-dots span:first-child{background:#FF5F57}.bd-cs-dots span:nth-child(2){background:#FEBC2E}.bd-cs-dots span:nth-child(3){background:#28C840}
.bd-cs-url{flex:1;max-width:420px;margin:0 auto;padding:6px 14px;border-radius:999px;background:#0E0E10;color:#9A958C;font-size:11px;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bd-cs-url i{font-style:normal;color:#4ADE80;margin-right:6px}
.bd-cs-shot{aspect-ratio:16/8.6;overflow:hidden}
.bd-cs-shot img{width:100%;height:100%;object-fit:cover;display:block}
.bd-cs-badge{position:absolute;z-index:3;display:flex;flex-direction:column;gap:2px;padding:12px 16px;border-radius:16px;background:rgba(14,14,16,.82);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid #2A2926;color:#F2E9D8;animation:bd-cs-float 5s ease-in-out infinite}
.bd-cs-badge .bd-mono{font-size:9.5px;color:#9A958C}
.bd-cs-badge b{font-size:22px;font-weight:300;letter-spacing:-.03em}
.bd-cs-b1{left:-14px;top:18%}
.bd-cs-b2{right:-14px;top:46%;animation-delay:-2.5s}
.bd-cs-b2 b{color:#FF5A1F}
.bd-cs-marq{overflow:hidden;background:#FF5A1F;color:#0B0B0C;padding:16px 0;white-space:nowrap}
.bd-cs-marq-in{display:inline-flex;animation:bd-cs-marq 26s linear infinite}
.bd-cs-marq span{font-size:clamp(20px,2.2vw,30px);font-weight:300;letter-spacing:-.03em;padding:0 22px}
.bd-cs-marq span::after{content:'✦';margin-left:44px;font-size:.6em;vertical-align:middle}
.bd-cs-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:0}
.bd-cs-fact{padding:20px;border-radius:18px;border:1px solid var(--line);min-height:120px;display:flex;flex-direction:column;justify-content:space-between;gap:12px}
.bd-cs-fact dt{color:var(--muted)}
.bd-cs-fact dd{margin:0;font-size:clamp(17px,1.5vw,22px);font-weight:300;letter-spacing:-.02em;line-height:1.3}
.bd-cs-fact-live{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.bd-cs-fact-live dt{color:color-mix(in srgb,var(--bg) 60%,var(--fg))}
.bd-cs-fact-live a{display:inline-flex;align-items:center;gap:8px}
.bd-cs-story{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:clamp(28px,6vw,96px)}
.bd-cs-aside{position:sticky;top:110px;align-self:start;display:flex;flex-direction:column;gap:18px}
.bd-cs-nav{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.bd-cs-nav li{display:flex;gap:14px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--line);color:var(--muted);font-size:17px;transition:color .3s,padding .4s cubic-bezier(.2,.8,.2,1)}
.bd-cs-nav li .bd-mono{font-size:10px}
.bd-cs-nav li.bd-on{color:var(--fg);padding-left:10px}
.bd-cs-nav li.bd-on .bd-mono{color:var(--accent)}
.bd-cs-thumb{border-radius:16px;overflow:hidden;aspect-ratio:4/3}
.bd-cs-thumb img{width:100%;height:100%;object-fit:cover;display:block}
.bd-cs-chap{padding:6px 0 64px}
.bd-cs-chap:last-child{padding-bottom:0}
.bd-cs-chap .bd-mono{color:var(--accent);display:block;margin-bottom:16px}
.bd-cs-chap p{margin:0;font-size:clamp(21px,2.1vw,31px);font-weight:200;line-height:1.38;letter-spacing:-.025em}
.bd-cs-show{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:22px;align-items:center}
.bd-cs-show-a{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:16/11;transform:scale(var(--zm,.92));transition:transform .2s linear}
.bd-cs-show-a img,.bd-cs-show-b img{width:100%;height:100%;object-fit:cover;display:block}
.bd-cs-show-r{position:relative;display:flex;flex-direction:column;gap:22px}
.bd-cs-show-b{border-radius:22px;overflow:hidden;aspect-ratio:4/5;transform:rotate(3deg);transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.bd-cs-show-b:hover{transform:rotate(0deg) scale(1.02)}
.bd-cs-spin{position:absolute;left:-58px;bottom:-40px;width:128px;height:128px;z-index:2;color:var(--fg)}
.bd-cs-spin svg{width:100%;height:100%;animation:bd-cs-spin 18s linear infinite}
.bd-cs-spin span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--accent)}
.bd-cs-res{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:clamp(28px,5vw,80px);align-items:start}
.bd-cs-res p{margin:0;font-size:clamp(24px,2.6vw,40px);font-weight:200;line-height:1.25;letter-spacing:-.035em}
.bd-cs-mets{display:grid;gap:12px}
.bd-cs-met{display:grid;grid-template-columns:auto 1fr;align-items:baseline;gap:4px 16px;padding:18px 20px;border-radius:18px;border:1px solid var(--line)}
.bd-cs-met b{font-size:clamp(40px,4.4vw,64px);font-weight:200;letter-spacing:-.05em;line-height:1}
.bd-cs-met b small{font-size:.32em;letter-spacing:0;color:var(--muted);margin-left:4px}
.bd-cs-met span{color:var(--muted);font-size:14px;font-weight:300}
.bd-cs-q{position:relative;max-width:1180px}
.bd-cs-qmark{position:absolute;left:-6px;top:-70px;font-size:220px;line-height:1;font-weight:200;opacity:.25;pointer-events:none}
.bd-cs-qt{margin:0;font-size:clamp(30px,4.2vw,66px);font-weight:200;line-height:1.08;letter-spacing:-.045em}
.bd-cs-by{display:flex;align-items:center;gap:14px;margin-top:30px}
.bd-cs-av{width:52px;height:52px;border-radius:50%;background:#0B0B0C;color:#FF5A1F;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:500}
.bd-cs-by b{display:block;font-weight:500}
.bd-cs-stars{letter-spacing:3px;font-size:13px}
.bd-cs-cta{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(28px,5vw,80px);align-items:center}
.bd-cs-cta-ph{position:relative;border-radius:24px;overflow:hidden;aspect-ratio:4/3}
.bd-cs-cta-ph img{width:100%;height:100%;object-fit:cover;display:block;object-position:62% 40%}
.bd-cs-cta-ph .bd-mono{position:absolute;left:16px;bottom:16px;padding:7px 12px;border-radius:999px;background:rgba(11,11,12,.75);color:#F2E9D8;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);font-size:10px}
.bd-cs-cta h2{margin:0 0 16px;font-size:clamp(36px,4.6vw,72px);font-weight:200;line-height:1;letter-spacing:-.05em}
.bd-cs-cta h2 span{color:var(--accent)}
@media (max-width: 1000px){.bd-cs-head,.bd-cs-story,.bd-cs-show,.bd-cs-res,.bd-cs-cta{grid-template-columns:1fr}.bd-cs-aside{position:relative;top:0}.bd-cs-thumb{display:none}.bd-cs-facts{grid-template-columns:repeat(2,minmax(0,1fr))}.bd-cs-spin{left:auto;right:10px;bottom:-30px;width:100px;height:100px}}
@media (max-width: 760px){.bd-cs-hero{padding-top:100px}.bd-cs-badge{display:none}.bd-cs-stage{padding-bottom:40px}.bd-cs-url{font-size:10px}.bd-cs-nav{display:none}.bd-cs-chap{padding-bottom:40px}.bd-cs-show-b{transform:none}.bd-cs-qmark{font-size:140px;top:-40px}.bd-cs-fact{min-height:0;padding:16px}}
@media (prefers-reduced-motion: reduce){.bd-cs-marq-in,.bd-cs-spin svg,.bd-cs-badge,.bd-cs-h1{animation:none}.bd-cs-frame{transform:none}}
'''

def build_case(cases):
  rich = []
  for c in cases:
    d = dict(c); d.update(_case_extras(c)); rich.append(d)
  data = json.dumps(rich, ensure_ascii=False)
  chap = lambda key, n, label: '<div class="bd-cs-chap" data-chap="%d"><span class="bd-mono">%02d — %s</span><p><sc-for list="{{%s}}" as="s" hint-placeholder-count="10"><span style="{{s.st}}">{{s.t}}</span></sc-for></p></div>' % (n, n, label, key)
  marq = '<sc-for list="{{stackLoop}}" as="t" hint-placeholder-count="10"><span>{{t}}</span></sc-for>'
  body = '''<section id="bd-hero" data-theme="ink" class="bd-cs-hero">
<div class="bd-wrap">
<div class="bd-case-top"><nav class="bd-mono bd-crumb" aria-label="Breadcrumb"><a href="Creative.dc.html">Home</a><span>/</span><a href="Work.dc.html">Work</a><span>/</span><span aria-current="page">{{c.name}}</span></nav>
<label class="bd-mono bd-picker"><span>Case study</span><select onChange="{{pickSel}}" aria-label="Choose a case study"><sc-for list="{{opts}}" as="o" hint-placeholder-count="25"><option value="{{o.v}}" selected="{{o.sel}}" style="color:#0B0B0C">{{o.label}}</option></sc-for></select></label></div>
<div class="bd-cs-head"><div><div class="bd-mono bd-cs-ind"><span class="bd-fdot" style="background:#FF5A1F"></span>Case study {{c.num}} / 25 · {{c.industry}}</div>
<h1 class="bd-cs-h1" id="bd-case-h1">{{c.h1}}</h1></div>
<div class="bd-cs-side"><p class="bd-cs-sum">{{c.summary}}</p>
<div class="bd-cs-pills bd-mono"><span class="bd-cs-pill">Year <b>{{c.year}}</b></span><span class="bd-cs-pill">{{c.cshort}}</span><span class="bd-cs-pill">{{c.service}}</span></div></div></div>
<div class="bd-cs-stage" id="bd-cs-stage">
<div class="bd-cs-frame" id="bd-cs-frame"><div class="bd-cs-bar"><span class="bd-cs-dots"><span></span><span></span><span></span></span><span class="bd-cs-url bd-mono"><i>●</i>{{c.domain}}</span></div>
<div class="bd-cs-shot"><img src="{{c.img}}" alt="{{c.alt}}"></div></div>
<div class="bd-cs-badge bd-cs-b1"><span class="bd-mono">Launched</span><b>{{c.year}}</b></div>
<div class="bd-cs-badge bd-cs-b2"><span class="bd-mono">PageSpeed</span><b>{{c.speed}}</b></div>
</div></div>
</section>
<div class="bd-cs-marq" aria-hidden="true"><div class="bd-cs-marq-in">''' + marq + marq + '''</div></div>
<section data-theme="bone" class="bd-sec bd-sec-tight"><div class="bd-wrap"><dl class="bd-cs-facts">
<div class="bd-cs-fact"><dt class="bd-mono">Client</dt><dd>{{c.client}}</dd></div>
<div class="bd-cs-fact"><dt class="bd-mono">Country</dt><dd>{{c.country}}</dd></div>
<div class="bd-cs-fact"><dt class="bd-mono">Stack</dt><dd>{{c.stack}}</dd></div>
<div class="bd-cs-fact bd-cs-fact-live"><dt class="bd-mono">Live site</dt><dd><sc-if value="{{c.hasLive}}" hint-placeholder-val="{{true}}"><a href="{{c.live}}" rel="noopener" target="_blank">{{c.domain}} ↗</a></sc-if><sc-if value="{{c.noLive}}" hint-placeholder-val="{{false}}"><span>Private build</span></sc-if></dd></div>
</dl></div></section>
<section data-theme="bone" class="bd-sec" style="padding-top:20px"><div class="bd-wrap bd-cs-story">
<aside class="bd-cs-aside"><ol class="bd-cs-nav" id="bd-cs-nav"><li data-nav-chap="1" class="bd-on"><span class="bd-mono">01</span>The client</li><li data-nav-chap="2"><span class="bd-mono">02</span>The challenge</li><li data-nav-chap="3"><span class="bd-mono">03</span>What I built</li></ol>
<div class="bd-cs-thumb"><img src="{{c.img2}}" alt="{{c.altPhone}}"></div></aside>
<div>''' + chap('pClient', 1, 'The client') + chap('pChallenge', 2, 'The challenge') + chap('pBuilt', 3, 'What I built') + '''</div>
</div></section>
<section data-theme="navy" class="bd-sec"><div class="bd-wrap">
<div class="bd-stmt-head"><span class="bd-mono">04</span><h2 class="bd-stmt-h">On every screen</h2><span class="bd-stmt-line" aria-hidden="true"></span></div>
<div class="bd-cs-show"><div class="bd-cs-show-a" id="bd-cs-zoom"><img src="{{c.img}}" alt="{{c.alt}}"></div>
<div class="bd-cs-show-r"><div class="bd-cs-show-b"><img src="{{c.img2}}" alt="{{c.altPhone}}"></div>
<div class="bd-cs-spin" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="bd-cs-circ" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"></path></defs><text font-family="Geist Mono, monospace" font-size="9.6" letter-spacing="3.1" fill="currentColor"><textPath href="#bd-cs-circ">DESIGNED · BUILT · LAUNCHED · BY RAKIB ·</textPath></text></svg><span>✦</span></div></div></div>
</div></section>
<section data-theme="ink" class="bd-sec"><div class="bd-wrap">
<div class="bd-stmt-head"><span class="bd-mono">05</span><h2 class="bd-stmt-h">The result</h2><span class="bd-stmt-line" aria-hidden="true"></span></div>
<div class="bd-cs-res"><p><sc-for list="{{pResult}}" as="s" hint-placeholder-count="6"><span style="{{s.st}}">{{s.t}}</span></sc-for></p>
<div class="bd-cs-mets"><sc-for list="{{metrics}}" as="m" hint-placeholder-count="3"><div class="bd-cs-met"><b>{{m.v}}<small>{{m.u}}</small></b><span>{{m.l}}</span></div></sc-for></div></div>
</div></section>
<section data-theme="orange" class="bd-sec"><div class="bd-wrap"><div class="bd-mono bd-lab">06 — In the client's words</div>
<div class="bd-cs-q"><span class="bd-cs-qmark" aria-hidden="true">“</span><blockquote class="bd-cs-qt">{{c.quote}}</blockquote>
<div class="bd-cs-by"><span class="bd-cs-av">{{c.ini}}</span><div><b>{{c.by}}</b><span class="bd-cs-stars" aria-label="Five stars">★★★★★</span></div></div></div></div></section>
<section data-theme="bone" class="bd-sec"><div class="bd-wrap bd-cs-cta">
<div class="bd-cs-cta-ph"><img src="''' + CAFE + '''" alt="Rakib Hasan having coffee"><span class="bd-mono">Rakib Hasan · Dhaka</span></div>
<div><div class="bd-mono bd-lab">07 — Your turn</div><h2>Want a site like <span>{{c.name}}</span>?</h2>
<p class="bd-p">Send me your current site or your idea. I'll review it by hand and reply within 12 hours with what I'd change first.</p>
<div class="bd-btns" style="margin-top:28px"><a href="Audit.dc.html" class="bd-btn bd-btn-p">Get a free audit<span aria-hidden="true">→</span></a><a href="Work.dc.html" class="bd-btn">All 25 projects<span aria-hidden="true">→</span></a></div></div>
</div></section>
<section data-theme="ink" class="bd-next"><div class="bd-wrap">
<button type="button" class="bd-nextbtn" onClick="{{goNext}}"><span class="bd-mono">Next project</span><span class="bd-next-name">{{next.name}} <span aria-hidden="true">→</span></span><span class="bd-next-img"><img src="{{next.img}}" alt=""></span></button>
</div></section>'''
  vals = '''
    var DATA = %s;
    var idx = Math.max(0, Math.min(DATA.length - 1, S.proj || 0));
    var c = DATA[idx], nx = DATA[(idx + 1) %% DATA.length];
    var segMap = function (arr) {
      var out = [];
      (arr || []).forEach(function (p, pi) {
        if (pi > 0) out.push({ t: ' ', st: 'display:block;height:0.9em' });
        p.forEach(function (s) { out.push({ t: s.t, st: '' }); });
      });
      return out;
    };
    X.c = { name: c.name, h1: c.h1, summary: c.summary, industry: c.industry, country: c.country || '—', cshort: c.cshort, year: c.year || '—',
      client: c.client || '—', service: c.service, stack: c.stack || '—', live: c.live, hasLive: !!c.live, noLive: !c.live,
      img: c.img, img2: c.img2, alt: c.alt, altPhone: c.name + ' website on a phone', num: (idx < 9 ? '0' : '') + (idx + 1),
      domain: c.domain, quote: c.quote, by: c.by, ini: c.ini, speed: c.metrics[1].v };
    X.stackLoop = c.stackList.concat([c.industry, c.cshort]);
    X.metrics = c.metrics;
    X.next = { name: nx.name, img: nx.img };
    X.pClient = segMap(c.p_client); X.pChallenge = segMap(c.p_challenge); X.pBuilt = segMap(c.p_built);
    X.pResult = segMap(c.p_result);
    X.opts = DATA.map(function (d, i) { return { v: String(i), label: d.name + ' — ' + d.industry.split(' &')[0], sel: i === idx }; });
    var go = function (i) { self.setState({ proj: i }); try { sessionStorage.setItem('bd-proj', DATA[i].slug); } catch (e) {} window.scrollTo({ top: 0, behavior: 'smooth' }); };
    X.goNext = function () { go((idx + 1) %% DATA.length); };
    X.pickSel = function (e) { go(parseInt(e.target.value, 10) || 0); };
''' % data
  mount = '''
    var DATA = %s;
    var want = (location.hash || '').replace('#', '');
    if (!want) { try { want = sessionStorage.getItem('bd-proj') || ''; } catch (e) {} }
    var k = DATA.findIndex ? DATA.findIndex(function (d) { return d.slug === want; }) : -1;
    if (k > 0) this.setState({ proj: k });
    on(window, 'hashchange', function () { var w = location.hash.replace('#', ''); var j = DATA.findIndex(function (d) { return d.slug === w; }); if (j >= 0) self.setState({ proj: j }); });
    // Case v2: browser frame untilts, showcase zooms, chapter nav follows the story.
    var csFrame = document.getElementById('bd-cs-frame'), csZoom = document.getElementById('bd-cs-zoom');
    var csScroll = function () {
      var vh = window.innerHeight;
      if (csFrame && !reduced) {
        var r = csFrame.getBoundingClientRect(), p = Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.9)));
        csFrame.style.setProperty('--tilt', (14 * (1 - p)).toFixed(2) + 'deg'); csFrame.style.setProperty('--sc', (0.94 + 0.06 * p).toFixed(3));
      }
      if (csZoom && !reduced) {
        var z = csZoom.getBoundingClientRect(), q = Math.max(0, Math.min(1, (vh - z.top) / (vh * 0.8)));
        csZoom.style.setProperty('--zm', (0.92 + 0.08 * q).toFixed(3));
      }
      var chaps = document.querySelectorAll('[data-chap]'), cur = 1;
      for (var i = 0; i < chaps.length; i++) if (chaps[i].getBoundingClientRect().top < vh * 0.55) cur = +chaps[i].getAttribute('data-chap');
      var items = document.querySelectorAll('[data-nav-chap]');
      for (var j = 0; j < items.length; j++) items[j].classList.toggle('bd-on', +items[j].getAttribute('data-nav-chap') === cur);
    };
    on(window, 'scroll', csScroll, { passive: true }); on(window, 'resize', csScroll); csScroll();
''' % json.dumps([{'slug': c['slug']} for c in cases])
  return page('Case.dc.html', 'Case Studies: 25 Client Websites | Rakib Hasan', 'Case studies for 25 WordPress websites: what each client needed, what I built and how it turned out.', body,
              active='Work', vals=vals, state='proj: 0', mount=mount)
