# Turns the design pages (project/*.dc.html) into a plain static website in dist/.
# Usage: python3 export.py [out_dir]
import os, re, sys, json, shutil, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PROJ = os.path.join(SITE, 'project')
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(SITE, 'dist')
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

def main():
  if os.path.isdir(OUT): shutil.rmtree(OUT)
  os.makedirs(os.path.join(OUT, 'assets', 'img'))
  used = set()
  for a, b in PAGES.items():
    src = open(os.path.join(PROJ, a), encoding='utf-8').read()
    open(os.path.join(OUT, b), 'w', encoding='utf-8').write(fix_refs(convert(src), used))
  for f in used: shutil.copy(os.path.join(IMAGES, f), os.path.join(OUT, 'assets', 'img', f))
  shutil.copy(os.path.join(HERE, 'dc-static.js'), os.path.join(OUT, 'assets', 'dc-static.js'))
  shutil.copy(os.path.join(HERE, 'lenis.min.js'), os.path.join(OUT, 'assets', 'lenis.min.js'))
  open(os.path.join(OUT, '.htaccess'), 'w').write('DirectoryIndex index.html\nOptions -Indexes\nHeader set X-Robots-Tag "noindex, nofollow"\n<FilesMatch "\\.(jpg|jpeg|png|webp)$">\nHeader set Cache-Control "public, max-age=2592000"\n</FilesMatch>\n')
  print('exported %d pages, %d images -> %s' % (len(PAGES), len(used), OUT))

if __name__ == '__main__':
  main()
