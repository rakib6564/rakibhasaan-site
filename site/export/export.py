# Turns the design pages (project/*.dc.html) into a plain static website in dist/.
# Usage: python3 export.py [out_dir]
import os, re, sys, json, shutil, html, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PROJ = os.path.join(SITE, 'project')
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
V2 = '--v2' in sys.argv
OUT = os.path.abspath(ARGS[0]) if ARGS else os.path.join(SITE, 'dist')
IMAGES = os.path.join(HERE, 'images')  # <blob id>.<ext>

PAGES = {
  'Creative.dc.html': 'index.html', 'Work.dc.html': 'work.html', 'Case.dc.html': 'case.html', 'Services.dc.html': 'services.html',
  'SvcWordPress.dc.html': 'wordpress-websites.html', 'SvcCustom.dc.html': 'custom-development.html', 'SvcSEO.dc.html': 'seo.html',
  'SvcApps.dc.html': 'apps.html', 'SvcPlatforms.dc.html': 'platforms.html', 'SvcBrand.dc.html': 'branding.html',
  'Construction.dc.html': 'construction.html', 'Process.dc.html': 'process.html', 'About.dc.html': 'about.html',
  'Reviews.dc.html': 'reviews.html', 'FAQ.dc.html': 'faq.html', 'Contact.dc.html': 'contact.html', 'Audit.dc.html': 'audit.html',
}

def between(s, a, b):
  i = s.index(a) + len(a); j = s.index(b, i)
  return s[i:j]

def convert(src):
  title = between(src, '<title>', '</title>')
  helmet = between(src, '<helmet>', '</helmet>')
  body = between(src, '<x-dc>', '</x-dc>')
  body = body.replace(helmet, '', 1).replace('<helmet>', '', 1).replace('</helmet>', '', 1)
  m = re.search(r'<script type="text/x-dc" data-dc-script data-props=\'([^\']*)\'>(.*?)</script>', src, re.S)
  props, code = m.group(1), m.group(2)
  # Tags whose children the HTML parser would rearrange get a dc- prefix; the runtime maps them back.
  for t in ('select', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th'):
    body = re.sub(r'<(/?)%s(?=[\s>])' % t, r'<\1dc-%s' % t, body)
  out = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Ccircle cx='16' cy='16' r='10' fill='%%23FF5A1F'/%%3E%%3C/svg%%3E">
%s
<style>html,body{margin:0;background:#0B0B0C}html.lenis,html.lenis body{height:auto}.lenis.lenis-smooth{scroll-behavior:auto!important}.lenis.lenis-stopped{overflow:hidden}</style>
</head>
<body>
<div id="dc-root"></div>
<template id="dc-tpl">%s</template>
<script type="text/plain" id="dc-src" data-props='%s'>%s</script>
<script src="assets/dc-static.js"></script>
<script src="assets/lenis.min.js"></script>
<script>(function(){if(!window.Lenis||matchMedia("(prefers-reduced-motion: reduce)").matches)return;var l=new Lenis({lerp:0.11,smoothWheel:true,anchors:true});window.__lenis=l;function f(t){l.raf(t);requestAnimationFrame(f)}requestAnimationFrame(f);})();</script>
</body>
</html>
''' % (title, helmet.strip(), body, props, code)
  return out

def fix_refs(s, used):
  def blob(m):
    bid = m.group(1)
    f = [x for x in os.listdir(IMAGES) if x.startswith(bid + '.')]
    if not f: raise SystemExit('missing image ' + bid)
    used.add(f[0]); return 'assets/img/' + f[0]
  s = re.sub(r'/_blob/([0-9a-f]{32})', blob, s)
  for a, b in PAGES.items():
    s = s.replace(a, b)
  s = s.replace('href="index.html#', 'href="./#').replace("href='index.html'", "href='./'").replace('href="index.html"', 'href="./"')
  return s

# v2: GSAP takes over reveals, theme colours, the Home marquee and the Home horizontal scroll.
V2_PATCHES = [
  ("if (pt !== pageTheme && themes[pt] && root)", "if (!window.__V2 && pt !== pageTheme && themes[pt] && root)"),
  ("var ups = all('[data-up]');", "var ups = window.__V2 ? [] : all('[data-up]');"),
  ("var rise = all(", "var rise = window.__V2 ? [] : all("),
  ("var clips = all('[data-clip]');", "var clips = window.__V2 ? [] : all('[data-clip]');"),
  ("var leads = all('.bd-stmt-lead');", "var leads = window.__V2 ? [] : all('.bd-stmt-lead');"),
  ("applyTheme(pick);", "if (!window.__V2) applyTheme(pick);"),
  ("var words = all('[data-w]'), man", "var words = window.__V2 ? [] : all('[data-w]'), man"),
  ("if (m1 && m2 && !reduced) {", "if (m1 && m2 && !reduced && !window.__V2) {"),
  ("if (horizontal) {", "if (horizontal && !window.__V2) {"),
]
V2_CSS = '<style>.v2-w{display:inline-block;white-space:nowrap}.v2-c{display:inline-block;will-change:transform}.v2-m{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.1em;margin-bottom:-.1em}.v2-mi{display:inline-block}</style>'
GSAP = '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'

def to_v2(t, name):
  hits = 0
  for a, b in V2_PATCHES:
    n = t.count(a); hits += n
    t = t.replace(a, b)
  if hits < 4: raise SystemExit('v2 patches did not apply to ' + name)
  t = re.sub(r'<script>\(function\(\)\{if\(!window.Lenis.*?</script>\n', '', t, flags=re.S)
  t = t.replace('<script src="assets/dc-static.js"></script>', '<script>window.__V2=1</script>\n' + GSAP + '<script src="assets/lenis.min.js"></script>\n<script src="assets/dc-static.js"></script>\n<script src="assets/v2.js"></script>', 1)
  t = t.replace('<script src="assets/lenis.min.js"></script>\n</body>', '</body>')
  t = t.replace('</head>', V2_CSS + '\n</head>', 1)
  return t

def main():
  if os.path.isdir(OUT): shutil.rmtree(OUT)
  os.makedirs(os.path.join(OUT, 'assets', 'img'))
  used = set()
  for a, b in PAGES.items():
    src = open(os.path.join(PROJ, a), encoding='utf-8').read()
    t = fix_refs(convert(src), used)
    if V2: t = to_v2(t, b)
    open(os.path.join(OUT, b), 'w', encoding='utf-8').write(t)
  for f in used:
    shutil.copy(os.path.join(IMAGES, f), os.path.join(OUT, 'assets', 'img', f))
    os.chmod(os.path.join(OUT, 'assets', 'img', f), 0o644)  # web server must be able to read every image
  shutil.copy(os.path.join(HERE, 'dc-static.js'), os.path.join(OUT, 'assets', 'dc-static.js'))
  shutil.copy(os.path.join(HERE, 'lenis.min.js'), os.path.join(OUT, 'assets', 'lenis.min.js'))
  if V2: shutil.copy(os.path.join(HERE, 'v2.js'), os.path.join(OUT, 'assets', 'v2.js'))
  ver = hashlib.sha1(open(os.path.join(HERE, 'dc-static.js'), 'rb').read() + open(os.path.join(HERE, 'lenis.min.js'), 'rb').read() + (open(os.path.join(HERE, 'v2.js'), 'rb').read() if V2 else b'')).hexdigest()[:10]
  for b in PAGES.values():
    fp = os.path.join(OUT, b); t = open(fp, encoding='utf-8').read()
    t = t.replace('src="assets/dc-static.js"', 'src="assets/dc-static.js?v=' + ver + '"').replace('src="assets/lenis.min.js"', 'src="assets/lenis.min.js?v=' + ver + '"').replace('src="assets/v2.js"', 'src="assets/v2.js?v=' + ver + '"')
    open(fp, 'w', encoding='utf-8').write(t)
  open(os.path.join(OUT, '.htaccess'), 'w').write('<FilesMatch "\\.(html|js)$">\nHeader set Cache-Control "no-cache, must-revalidate"\n</FilesMatch>\n' + 'DirectoryIndex index.html\nOptions -Indexes\nHeader set X-Robots-Tag "noindex, nofollow"\n<FilesMatch "\\.(jpg|jpeg|png|webp)$">\nHeader set Cache-Control "public, max-age=2592000"\n</FilesMatch>\n')
  print('exported %d pages, %d images -> %s' % (len(PAGES), len(used), OUT))

if __name__ == '__main__':
  main()
