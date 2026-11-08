# Equal-height, paginated review grid for the Reviews page.
def reviews_grid_html():
  byn = {r['n']: r for r in REVIEWS}
  order = [byn[n] for n in FEATURED if n in byn]
  rest = sorted([r for r in REVIEWS if r['n'] not in FEATURED and len(r['text'].strip()) >= 48], key=lambda r: -len(r['text']))
  items = order + rest
  cards = []
  for i, r in enumerate(items):
    t = r['text'].strip()
    meta = [r['country']] + ([r['price']] if r.get('price') else [])
    dur = r.get('dur') or ''
    cards.append('''<figure class="bd-rx" data-ix="%d"%s>
<div class="bd-rx-top"><span class="bd-rx-q" aria-hidden="true">“</span><span class="bd-rx-stars" aria-label="%s out of 5">★★★★★</span></div>
<blockquote class="bd-rx-t">%s</blockquote>
<button type="button" class="bd-rx-more bd-mono" data-full="%s" data-who="%s">Read full review</button>
<figcaption class="bd-rx-by"><span class="bd-rx-av" aria-hidden="true">%s</span><span class="bd-rx-who"><b>%s</b><span class="bd-mono">%s</span></span><span class="bd-rx-when bd-mono">%s%s</span></figcaption>
</figure>''' % (i, '' if i < 6 else ' hidden', r['rating'], html.escape(t), html.escape(t, quote=True), html.escape(r['who'], quote=True),
      initials2(r['who']), html.escape(r['who']), html.escape(' · '.join(meta)), html.escape(r['when']), (' · ' + html.escape(dur)) if dur else ''))
  return '''<div class="bd-rx-wrap" data-total="%d">
<div class="bd-rx-bar"><div class="bd-rx-count bd-mono"><span class="bd-rx-from">01</span>–<span class="bd-rx-to">06</span> of %d reviews</div>
<div class="bd-rx-nav"><button type="button" class="bd-rx-btn bd-rx-prev" aria-label="Previous reviews">←</button><div class="bd-rx-pages bd-mono"></div><button type="button" class="bd-rx-btn bd-rx-next" aria-label="Next reviews">→</button></div></div>
<div class="bd-rx-grid">%s</div>
<div class="bd-rx-prog" aria-hidden="true"><i></i></div>
<div class="bd-rx-modal" hidden><div class="bd-rx-dlg" role="dialog" aria-modal="true" aria-label="Full review"><button type="button" class="bd-rx-x" aria-label="Close">×</button><div class="bd-rx-stars">★★★★★</div><p class="bd-rx-full"></p><div class="bd-rx-mwho bd-mono"></div></div></div>
</div>''' % (len(items), len(items), ''.join(cards))

REV_CSS = r'''
/* ---------- reviews grid ---------- */
@keyframes bd-rx-in{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.bd-rx-bar{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:14px;margin-bottom:18px}
.bd-rx-count{color:var(--muted);font-size:11px}
.bd-rx-count span{color:var(--fg)}
.bd-rx-nav{display:flex;align-items:center;gap:8px}
.bd-rx-btn{width:44px;height:44px;border-radius:50%;border:1px solid color-mix(in srgb,var(--fg) 16%,transparent);background:transparent;color:var(--fg);font-size:16px;cursor:pointer;transition:background .3s,color .3s,border-color .3s,opacity .3s}
.bd-rx-btn:hover:not(:disabled){background:var(--fg);color:var(--bg);border-color:var(--fg)}
.bd-rx-btn:disabled{opacity:.3;cursor:default}
.bd-rx-pages{display:flex;gap:4px}
.bd-rx-pg{min-width:34px;height:34px;padding:0 8px;border-radius:999px;border:0;background:transparent;color:var(--muted);font:inherit;font-size:11px;cursor:pointer;transition:background .3s,color .3s}
.bd-rx-pg:hover{color:var(--fg)}
.bd-rx-pg[aria-current="true"]{background:var(--accent);color:#0B0B0C}
.bd-rx-gap{align-self:center;color:var(--muted);padding:0 2px}
.bd-rx-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-auto-rows:1fr;gap:16px}
.bd-rx{position:relative;display:flex;flex-direction:column;gap:16px;margin:0;padding:26px 26px 22px;border-radius:24px;background:linear-gradient(180deg,color-mix(in srgb,#fff 55%,transparent),color-mix(in srgb,#fff 25%,transparent));border:1px solid color-mix(in srgb,var(--fg) 9%,transparent);box-shadow:0 1px 0 rgba(255,255,255,.7) inset,0 24px 40px -32px rgba(40,30,20,.45);overflow:hidden;transition:transform .5s cubic-bezier(.2,.8,.2,1),box-shadow .5s,border-color .4s;animation:bd-rx-in .7s cubic-bezier(.2,.8,.2,1) both}
.bd-rx:hover{transform:translateY(-4px);border-color:color-mix(in srgb,var(--accent) 45%,transparent);box-shadow:0 1px 0 rgba(255,255,255,.7) inset,0 30px 50px -30px rgba(255,90,31,.45)}
.bd-rx[hidden]{display:none}
.bd-rx-top{display:flex;justify-content:space-between;align-items:flex-start}
.bd-rx-q{font-size:64px;line-height:.7;font-weight:200;color:var(--accent);height:30px}
.bd-rx-stars{color:var(--accent);font-size:12px;letter-spacing:2px}
.bd-rx-t{margin:0;font-size:16.5px;line-height:1.6;font-weight:300;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:6;line-clamp:6;overflow:hidden}
.bd-rx-more{align-self:flex-start;margin-top:-6px;padding:0;border:0;background:none;color:var(--accent);font-size:10.5px;cursor:pointer;visibility:hidden}
.bd-rx.bd-long .bd-rx-more{visibility:visible}
.bd-rx-by{display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-areas:"av who" "av when";column-gap:12px;align-items:center;margin-top:auto;padding-top:16px;border-top:1px solid color-mix(in srgb,var(--fg) 9%,transparent)}
.bd-rx-av{grid-area:av;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#0B0B0C;color:#FF5A1F;font-size:13px;font-weight:500;letter-spacing:.02em}
.bd-rx-who{grid-area:who;min-width:0}
.bd-rx-who b{display:block;font-weight:500;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bd-rx-who .bd-mono,.bd-rx-when{display:block;color:var(--muted);font-size:9.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bd-rx-when{grid-area:when;margin-top:2px}
.bd-rx:nth-child(6n+1){background:#0B0B0C;color:#EDE8DF;border-color:#0B0B0C}
.bd-rx:nth-child(6n+1) .bd-rx-av{background:#FF5A1F;color:#0B0B0C}
.bd-rx:nth-child(6n+1) .bd-rx-by{border-color:#26241F}
.bd-rx:nth-child(6n+1) .bd-rx-who .bd-mono,.bd-rx:nth-child(6n+1) .bd-rx-when{color:#8F8A82}
.bd-rx-prog{height:2px;margin-top:22px;border-radius:2px;background:color-mix(in srgb,var(--fg) 10%,transparent);overflow:hidden}
.bd-rx-prog i{display:block;height:100%;width:var(--p,10%);background:var(--accent);transition:width .6s cubic-bezier(.2,.8,.2,1)}
.bd-rx-modal{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;background:rgba(11,11,12,.55);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.bd-rx-modal[hidden]{display:none}
.bd-rx-dlg{position:relative;max-width:620px;width:100%;max-height:85vh;overflow:auto;padding:34px;border-radius:24px;background:#F4EFE6;color:#0B0B0C;box-shadow:0 40px 80px -30px rgba(0,0,0,.6);animation:bd-rx-in .4s cubic-bezier(.2,.8,.2,1)}
.bd-rx-full{margin:16px 0 18px;font-size:clamp(18px,1.8vw,22px);line-height:1.5;font-weight:300}
.bd-rx-mwho{color:#6B665E;font-size:11px}
.bd-rx-x{position:absolute;right:14px;top:14px;width:38px;height:38px;border-radius:50%;border:1px solid rgba(0,0,0,.12);background:transparent;font-size:20px;cursor:pointer;color:#0B0B0C}
@media (max-width: 1000px){.bd-rx-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width: 640px){.bd-rx-grid{grid-template-columns:1fr;grid-auto-rows:auto}.bd-rx{padding:22px 20px 18px}.bd-rx-bar{flex-direction:column;align-items:flex-start}.bd-rx-pg{min-width:30px;height:30px}}
@media (prefers-reduced-motion: reduce){.bd-rx,.bd-rx-dlg{animation:none}}
'''

REV_JS = r'''
    // ---------- Reviews grid: pagination + full-review dialog ----------
    all('.bd-rx-wrap').forEach(function (wrap) {
      var cards = Array.prototype.slice.call(wrap.querySelectorAll('.bd-rx')), total = cards.length;
      var pagesEl = wrap.querySelector('.bd-rx-pages'), prev = wrap.querySelector('.bd-rx-prev'), next = wrap.querySelector('.bd-rx-next');
      var page = 0;
      var per = function () { return window.innerWidth <= 640 ? 3 : window.innerWidth <= 1000 ? 4 : 6; };
      var count = function () { return Math.ceil(total / per()); };
      var pad = function (n) { return (n < 10 ? '0' : '') + n; };
      var render = function (scroll) {
        var p = per(), n = count(); page = Math.max(0, Math.min(page, n - 1));
        cards.forEach(function (c, i) {
          var show = i >= page * p && i < (page + 1) * p;
          c.hidden = !show;
          if (show) { c.style.animationDelay = ((i - page * p) * 0.06).toFixed(2) + 's'; c.style.animationName = 'none'; void c.offsetWidth; c.style.animationName = '';
            var t = c.querySelector('.bd-rx-t'); c.classList.toggle('bd-long', t.scrollHeight > t.clientHeight + 2); }
        });
        wrap.querySelector('.bd-rx-from').textContent = pad(page * p + 1);
        wrap.querySelector('.bd-rx-to').textContent = pad(Math.min(total, (page + 1) * p));
        prev.disabled = page === 0; next.disabled = page >= n - 1;
        var nums = [], k;
        for (k = 0; k < n; k++) if (k === 0 || k === n - 1 || Math.abs(k - page) <= 1) nums.push(k); else if (nums[nums.length - 1] !== -1) nums.push(-1);
        pagesEl.innerHTML = nums.map(function (x) { return x < 0 ? '<span class="bd-rx-gap">…</span>' : '<button type="button" class="bd-rx-pg" data-pg="' + x + '" aria-current="' + (x === page) + '">' + pad(x + 1) + '</button>'; }).join('');
        wrap.querySelector('.bd-rx-prog').style.setProperty('--p', ((page + 1) / n * 100).toFixed(1) + '%');
        if (scroll) { var r = wrap.getBoundingClientRect(); if (r.top < 60) window.scrollBy({ top: r.top - 110, behavior: 'smooth' }); }
      };
      on(prev, 'click', function () { page--; render(true); });
      on(next, 'click', function () { page++; render(true); });
      on(pagesEl, 'click', function (e) { var b = e.target.closest('[data-pg]'); if (b) { page = +b.getAttribute('data-pg'); render(true); } });
      var lastPer = per();
      on(window, 'resize', function () { if (per() !== lastPer) { var first = page * lastPer; lastPer = per(); page = Math.floor(first / lastPer); render(false); } });
      var modal = wrap.querySelector('.bd-rx-modal');
      var close = function () { modal.hidden = true; };
      on(wrap, 'click', function (e) {
        var m = e.target.closest('.bd-rx-more');
        if (m) { modal.querySelector('.bd-rx-full').textContent = m.getAttribute('data-full'); modal.querySelector('.bd-rx-mwho').textContent = '— ' + m.getAttribute('data-who') + ' · on Fiverr'; modal.hidden = false; modal.querySelector('.bd-rx-x').focus(); return; }
        if (e.target === modal || e.target.closest('.bd-rx-x')) close();
      });
      on(document, 'keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });
      render(false);
    });
'''
