# "Products I build" showcase for the Custom development page, from Rakib's public GitHub repos.
GH = 'https://github.com/rakib6564/'

def products_html(n):
  mods = ['Booking', 'Membership', 'Forms', 'Coaching', 'Stripe', 'Multilang', 'Media', 'Backups', 'MCP Gateway']
  tiles = ''.join('<span class="bd-pr-mod" style="--i:%d">%s</span>' % (i, m) for i, m in enumerate(mods))
  chip = lambda xs: ''.join('<span class="bd-pr-chip bd-mono">%s</span>' % x for x in xs)
  return '''<section id="bd-s%d" data-theme="ink" class="bd-sec bd-products"><div class="bd-wrap">
<div class="bd-pr-head"><div><div class="bd-mono bd-lab">%02d — Products I build</div>
<h2 class="bd-h2">I don't only build for clients.<br><span>I ship my own software.</span></h2></div>
<p class="bd-p bd-pr-intro">The same standards I bring to client plugins, proven on products I design, release and maintain myself: versioned releases, automated checks, documentation and real customers.</p></div>
<div class="bd-pr-stats bd-mono"><div><b>641</b>commits on Kohevo</div><div><b>18</b>active branches</div><div><b>v1.6.2</b>current release</div><div><b>EN · FR</b>3,358 translated strings</div></div>
<div class="bd-pr-grid">
<article class="bd-pr bd-pr-a">
<div class="bd-pr-top"><span class="bd-pr-tag bd-mono"><span class="bd-pr-dot"></span>Platform · PHP 8.2</span><a class="bd-pr-gh bd-mono" href="%skohevo" target="_blank" rel="noopener">GitHub ↗</a></div>
<h3 class="bd-pr-h">Kohevo</h3>
<p class="bd-pr-p">A white-label business platform. Website, customer portal, bookings, memberships, forms, coaching programmes and Stripe payments run in one branded system instead of five disconnected tools.</p>
<div class="bd-pr-mods" aria-hidden="true">%s</div>
<div class="bd-pr-chips">%s</div>
</article>
<article class="bd-pr bd-pr-b">
<div class="bd-pr-top"><span class="bd-pr-tag bd-mono"><span class="bd-pr-dot"></span>Licensing server · v1.6.2</span><a class="bd-pr-gh bd-mono" href="%sKohevo-Licensing-Rebuild" target="_blank" rel="noopener">GitHub ↗</a></div>
<h3 class="bd-pr-h">Kohevo Licensing</h3>
<p class="bd-pr-p">The central authority behind every Kohevo install: products, plans, licences and module entitlements, with Ed25519-signed check-ins, a 7-day expiry warning and a 7-day grace period.</p>
<div class="bd-pr-term bd-mono" aria-hidden="true"><div><span>$</span> POST /licensing/check</div><div class="bd-pr-l2">→ 200 · signature verified <i>✓</i></div><div class="bd-pr-l3">→ modules: booking, forms, coaching</div></div>
</article>
<article class="bd-pr bd-pr-c">
<div class="bd-pr-top"><span class="bd-pr-tag bd-mono"><span class="bd-pr-dot"></span>WordPress plugin · React</span><a class="bd-pr-gh bd-mono" href="%sRK-React-Builder" target="_blank" rel="noopener">GitHub ↗</a></div>
<h3 class="bd-pr-h">RK React Builder</h3>
<p class="bd-pr-p">A focused visual page builder for WordPress, shipped as one installable plugin. A React and TypeScript editor with reusable blocks, drafts, revisions and undo, rendered by PHP on the live site, with an optional headless mode.</p>
<div class="bd-pr-blocks" aria-hidden="true"><span>Hero</span><span>Heading</span><span class="bd-pr-drag">Services grid</span><span>Call to action</span></div>
<div class="bd-pr-chips">%s</div>
</article>
<article class="bd-pr bd-pr-d">
<div class="bd-pr-top"><span class="bd-pr-tag bd-mono"><span class="bd-pr-dot bd-pr-dot-w"></span>Private · in development</span></div>
<h3 class="bd-pr-h">Elementor Forge</h3>
<p class="bd-pr-p">Tooling for faster, cleaner Elementor builds, in active private development.</p>
</article>
</div>
<div class="bd-pr-foot"><span class="bd-p">Need a plugin, a licensing system or a custom builder of your own?</span><a href="Contact.dc.html" class="bd-btn bd-btn-p">Talk about your product<span aria-hidden="true">→</span></a></div>
</div></section>''' % (n, n, GH, tiles, chip(['PHP 8.2', 'MySQL', 'No build step', 'Multi-tenant', 'EN · FR']),
     GH, GH, chip(['React', 'TypeScript', 'Vite', 'REST API', 'Headless mode']))

PRODUCTS_CSS = r'''
/* ---------- products showcase ---------- */
@keyframes bd-pr-lit{0%,100%{background:transparent;color:var(--muted);border-color:var(--line)}8%,22%{background:#FF5A1F;color:#0B0B0C;border-color:#FF5A1F}}
@keyframes bd-pr-type{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes bd-pr-drag{0%,20%{transform:translate(0,0);box-shadow:none}35%,60%{transform:translate(14px,-46px) rotate(-2deg);box-shadow:0 18px 30px -12px rgba(0,0,0,.6)}75%,100%{transform:translate(0,0);box-shadow:none}}
.bd-pr-head{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:32px;align-items:end;margin-bottom:28px}
.bd-pr-head .bd-h2 span{color:var(--accent)}
.bd-pr-intro{margin:0;color:var(--muted)}
.bd-pr-stats{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:22px;font-size:10.5px;color:var(--muted)}
.bd-pr-stats div{padding:16px 16px 16px 0}
.bd-pr-stats div+div{padding-left:16px;border-left:1px solid var(--line)}
.bd-pr-stats b{display:block;font-family:'Geist',sans-serif;font-weight:200;font-size:clamp(24px,2.6vw,38px);letter-spacing:-.04em;color:var(--fg);margin-bottom:4px}
.bd-pr-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px}
.bd-pr{position:relative;display:flex;flex-direction:column;gap:14px;padding:24px;border-radius:22px;border:1px solid var(--line);background:color-mix(in srgb,var(--fg) 3%,transparent);overflow:hidden;transition:border-color .4s,transform .5s cubic-bezier(.2,.8,.2,1)}
.bd-pr:hover{border-color:color-mix(in srgb,var(--accent) 60%,var(--line));transform:translateY(-4px)}
.bd-pr::after{content:'';position:absolute;inset:auto -30% -60% auto;width:70%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(255,90,31,.16),transparent 65%);pointer-events:none}
.bd-pr-a{grid-column:span 4;grid-row:span 2}
.bd-pr-b,.bd-pr-c{grid-column:span 2}
.bd-pr-d{grid-column:span 6;flex-direction:row;flex-wrap:wrap;align-items:center;gap:10px 24px}
.bd-pr-d .bd-pr-h{font-size:clamp(22px,2vw,30px)}
.bd-pr-top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.bd-pr-tag{display:inline-flex;align-items:center;gap:8px;font-size:10px;color:var(--muted)}
.bd-pr-dot{width:7px;height:7px;border-radius:50%;background:#4ADE80;animation:bd-pulse 2s infinite}
.bd-pr-dot-w{background:#FFB020;animation:none}
.bd-pr-gh{font-size:10px;padding:6px 10px;border:1px solid var(--line);border-radius:999px;transition:background .3s,color .3s,border-color .3s}
.bd-pr-gh:hover{background:var(--accent);border-color:var(--accent);color:#0B0B0C}
.bd-pr-h{margin:0;font-size:clamp(28px,3vw,46px);font-weight:200;letter-spacing:-.045em;line-height:1}
.bd-pr-a .bd-pr-h{font-size:clamp(40px,5vw,76px)}
.bd-pr-p{margin:0;max-width:560px;font-size:15.5px;line-height:1.55;font-weight:300;color:color-mix(in srgb,var(--fg) 78%,var(--bg))}
.bd-pr-mods{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:auto}
.bd-pr-mod{padding:14px 12px;border-radius:12px;border:1px solid var(--line);font-family:'Geist Mono',monospace;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);animation:bd-pr-lit 9s infinite;animation-delay:calc(var(--i) * 1s)}
.bd-pr-chips{display:flex;flex-wrap:wrap;gap:6px}
.bd-pr-chip{font-size:9.5px;padding:5px 9px;border-radius:999px;background:color-mix(in srgb,var(--fg) 7%,transparent);color:var(--muted)}
.bd-pr-term{margin-top:auto;padding:14px 16px;border-radius:12px;background:#050506;border:1px solid #1F2433;color:#C9C3B8;font-size:11px;line-height:1.9}
.bd-pr-term span{color:#FF5A1F}
.bd-pr-term i{font-style:normal;color:#4ADE80}
.bd-pr-term div{animation:bd-pr-type 1.2s steps(28) both}
.bd-pr-term .bd-pr-l2{animation-delay:1.3s;color:#9AA0AE}
.bd-pr-term .bd-pr-l3{animation-delay:2.6s;color:#9AA0AE}
.bd-pr-blocks{display:flex;flex-direction:column;gap:6px;margin-top:auto;padding:12px;border-radius:12px;border:1px dashed var(--line)}
.bd-pr-blocks span{padding:9px 12px;border-radius:8px;background:color-mix(in srgb,var(--fg) 6%,transparent);font-family:'Geist Mono',monospace;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.bd-pr-blocks .bd-pr-drag{background:#FF5A1F;color:#0B0B0C;animation:bd-pr-drag 4.5s cubic-bezier(.6,0,.2,1) infinite}
.bd-pr-foot{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px;margin-top:22px;padding-top:22px;border-top:1px solid var(--line)}
.bd-pr-foot .bd-p{margin:0}
@media (max-width: 1000px){.bd-pr-a,.bd-pr-b,.bd-pr-c,.bd-pr-d{grid-column:span 6;grid-row:auto}.bd-pr-head{grid-template-columns:1fr}}
@media (max-width: 760px){.bd-pr-stats{grid-template-columns:repeat(2,1fr)}.bd-pr-stats div:nth-child(3){border-left:0;padding-left:0}.bd-pr-stats div:nth-child(n+3){border-top:1px solid var(--line)}.bd-pr{padding:18px}.bd-pr-mods{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (prefers-reduced-motion: reduce){.bd-pr-mod,.bd-pr-term div,.bd-pr-blocks .bd-pr-drag,.bd-pr-dot{animation:none}}
'''
