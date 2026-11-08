# Puts the shared header, footer and message widget onto the Home board (Creative.dc.html).
import os, re
BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(os.path.dirname(BASE), 'project', 'Creative.dc.html')
s = open(P, encoding='utf-8').read()
if '/* shared-shell */' in s:
    print('already patched'); raise SystemExit
header, footer, widget = open(os.path.join(BASE, 'shell.html'), encoding='utf-8').read().split('<!--SPLIT-->')
shared_vals = open(os.path.join(BASE, 'shared_vals.js'), encoding='utf-8').read()
widget_mount = open(os.path.join(BASE, 'widget_mount.js'), encoding='utf-8').read()
css = open(os.path.join(BASE, 'widget.css'), encoding='utf-8').read()
pcss = open(os.path.join(BASE, 'pages.css'), encoding='utf-8').read()
# only the footer + fill rules from pages.css are needed on Home
keep = [l for l in pcss.split('\n') if l.startswith(('.bd-wrap{', '.bd-foot', '.bd-fill{', '.bd-ln', '.bd-nl[aria-current'))]

# 1. header + full menu
a = s.index('<sc-if value="{{mega}}" hint-placeholder-val="{{false}}">\n<div class="bd-scrim"')
b = s.index('<section id="bd-hero"')
s = s[:a] + header.strip() + '\n\n' + s[b:]
s = s.replace('<a href="Creative.dc.html" class="bd-logo">', '<a href="#bd-hero" class="bd-logo">', 1)

# 2. footer + widget
a = s.index('<footer class="bd-pad"'); b = s.index('</footer>', a) + len('</footer>')
s = s[:a] + footer.strip() + '\n' + widget.strip() + s[b:]

# 3. css
s = s.replace('</style>\n</helmet>', '/* shared-shell */\n' + '\n'.join(keep) + '\n' + css + '\n</style>\n</helmet>', 1)

# 4. state + mount
s = s.replace("this.state = { sent: false, mega: false, full: false, fsIdx: 0 };",
              "this.state = { sent: false, mega: false, full: false, fsIdx: 0, chatShown: false, chatHidden: false, chatOpen: false, chatSent: false, chatTopic: '', chatMsg: '', tick: 0 };")
assert 'chatShown: false' in s
anchor = '    // ---------- WebGL hero ----------'
s = s.replace(anchor, widget_mount + '\n' + anchor, 1)

# 5. renderVals: merge shared values over Home's own
rv = s.index('  renderVals() {')
ret = s.index('\n    return {\n', rv) + 1
s = s[:ret] + '    var __H = {' + s[ret + len('    return {'):]
end = s.index('      _end: true\n    };', ret)
s = s[:end] + '      _end: true\n    };\n    var X = {};\n' + shared_vals + '\n    for (var __k in __H) if (!(__k in X)) X[__k] = __H[__k];\n    return X;' + s[end + len('      _end: true\n    };'):]
open(P, 'w', encoding='utf-8').write(s)
print('home patched')
