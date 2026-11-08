import os
BASE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(BASE, 'world.py'), encoding='utf-8').read())
P = os.path.join(os.path.dirname(BASE), 'project', 'Creative.dc.html')
s = open(P, encoding='utf-8').read()
R = [
 ('Six industries · 25 sites', 'Six industries · 250+ sites'),
 ('Twenty-five times so far.', 'More than 250 times so far.'),
 ('>25 websites for real businesses in the US, Belgium and Hungary,', '>250+ websites for real businesses in 14 countries,'),
 ('line-height: 1">25</div>', 'line-height: 1">250+</div>'),
 ('<dd>USA, Belgium, Hungary</dd>', '<dd>14 countries, 5 continents</dd>'),
]
for a, b in R:
  if a in s: s = s.replace(a, b)
  else: print('not found:', a)
if 'id="bd-world"' not in s:
  a = s.index('<section id="bd-reviews"'); b = s.index('</section>', a) + len('</section>')
  s = s[:b] + '\n\n' + world_html('navy', '06 — Worldwide') + s[b:]
  s = s.replace('/* shared-shell */', WORLD_CSS + '\n/* shared-shell */', 1)
  anchor = '    // ---------- WebGL hero ----------'
  s = s.replace(anchor, WORLD_JS + '\n' + anchor, 1)
open(P, 'w', encoding='utf-8').write(s); print('home world ok')
