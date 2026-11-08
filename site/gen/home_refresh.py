# Refreshes the shared parts on Home (footer, CSS, shared values) and installs the interactive "Three rules" block.
import os, re
BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(os.path.dirname(BASE), 'project', 'Creative.dc.html')
s = open(P, encoding='utf-8').read()
header, footer, widget = open(os.path.join(BASE, 'shell.html'), encoding='utf-8').read().split('<!--SPLIT-->')
shared_vals = open(os.path.join(BASE, 'shared_vals.js'), encoding='utf-8').read()
pcss = open(os.path.join(BASE, 'pages.css'), encoding='utf-8').read()
wcss = open(os.path.join(BASE, 'widget.css'), encoding='utf-8').read()
rcss = open(os.path.join(BASE, 'rules.css'), encoding='utf-8').read()
keep = [l for l in pcss.split('\n') if l.startswith(('.bd-wrap{', '.bd-fill{', '.bd-ln', '.bd-nl[aria-current'))]

# footer
a = s.index('<footer data-theme="ink" class="bd-foot">'); b = s.index('</footer>', a) + len('</footer>')
s = s[:a] + footer.strip() + s[b:]

# css
a = s.index('/* shared-shell */'); b = s.index('</style>', a)
s = s[:a] + '/* shared-shell */\n' + '\n'.join(keep) + '\n' + wcss + '\n' + rcss + '\n' + s[b:]

# shared values
a = s.index('    var X = {};\n') + len('    var X = {};\n'); b = s.index('    for (var __k in __H)', a)
s = s[:a] + shared_vals + '\n' + s[b:]

# rules section
if 'id="bd-rules"' not in s:
    a = s.index('<section id="bd-process"'); b = s.index('</section>', a) + len('</section>')
    s = s[:a] + open(os.path.join(BASE, 'rules.html'), encoding='utf-8').read().strip() + s[b:]
    s = s.replace("this.state = { sent: false, mega: false, full: false, fsIdx: 0,", "this.state = { rule: 0, sent: false, mega: false, full: false, fsIdx: 0,", 1)
    assert 'rule: 0,' in s
    anchor = '    // ---------- WebGL hero ----------'
    s = s.replace(anchor, open(os.path.join(BASE, 'rules_mount.js'), encoding='utf-8').read() + '\n' + anchor, 1)
    rv = s.index('    var __H = {')
    s = s[:rv] + open(os.path.join(BASE, 'rules_vals.js'), encoding='utf-8').read() + '\n' + s[rv:]
    s = s.replace('    var __H = {', '    var __H = {\n      rulesList: rulesList, rule0: ri === 0, rule1: ri === 1, rule2: ri === 2, stageStyle: stageStyle, ruleNum: RULES[ri].n,', 1)
open(P, 'w', encoding='utf-8').write(s)
print('home refreshed')
