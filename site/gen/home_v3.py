import os, re
BASE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(BASE, 'world.py'), encoding='utf-8').read())
P = os.path.join(os.path.dirname(BASE), 'project', 'Creative.dc.html')
s = open(P, encoding='utf-8').read()
header, footer, widget = open(os.path.join(BASE, 'shell.html'), encoding='utf-8').read().split('<!--SPLIT-->')
# world section
a = s.index('<section id="bd-world"'); b = s.index('</section>', a) + len('</section>')
s = s[:a] + world_html('navy', '06 — Worldwide') + s[b:]
# world css (old orbit or board block sits right before the shared-shell marker)
for mk in ('/* ---------- worldwide orbit ---------- */', '/* ---------- worldwide board ---------- */', '/* ---------- worldwide live map ---------- */'):
  if mk in s:
    a = s.index(mk); b = s.index('/* shared-shell */', a)
    s = s[:a] + s[b:]
s = s.replace('/* shared-shell */', WORLD_CSS.strip() + '\n/* shared-shell */', 1)
# world js
for mk in ('    // ---------- Worldwide orbit', '    // ---------- Worldwide board', '    // ---------- Worldwide live map'):
  if mk in s:
    a = s.index(mk); b = s.index('    // ---------- WebGL hero ----------', a)
    s = s[:a] + s[b:]
fx = open(os.path.join(BASE, 'fx_mount.js'), encoding='utf-8').read()
if '// ---------- Footer name: variable-weight wave' in s:
  a = s.index('    // ---------- Footer name: variable-weight wave'); b = s.index('    // ---------- WebGL hero ----------', a)
  s = s[:a] + s[b:]
s = s.replace('    // ---------- WebGL hero ----------', WORLD_JS + '\n' + fx + '\n    // ---------- WebGL hero ----------', 1)
# full-screen menu block from the shared shell
a = s.index('<sc-if value="{{full}}"'); b = s.index('</sc-if>', a) + len('</sc-if>')
fa = header.index('<sc-if value="{{full}}"'); fb = header.index('</sc-if>', fa) + len('</sc-if>')
assert '<sc-if' not in s[a + 5:b - 8]
s = s[:a] + header[fa:fb] + s[b:]
# widget block
a = s.index('<sc-if value="{{chatVisible}}"'); z = s.index('</x-dc>'); b = s.rindex('</div>', a, z)
s = s[:a] + widget.strip() + '\n' + s[b:]
s = s.replace('family=Geist:wght@200;300;400;500;600', 'family=Geist:wght@200..600')
s = s.replace('if (this._raf2) cancelAnimationFrame(this._raf2);', 'if (this._raf2) cancelAnimationFrame(this._raf2);\n    if (this._fraf) cancelAnimationFrame(this._fraf);', 1)
open(P, 'w', encoding='utf-8').write(s); print('home v3 ok')
