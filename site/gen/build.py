# Builds the inner pages of the "Built Different" site from the Phase 1 copy doc.
import re, html, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
NICHE = os.path.dirname(BASE)
PROJ = os.path.join(NICHE, 'project')
COPY = open(os.path.join(os.path.dirname(NICHE), 'copy.md'), encoding='utf-8').read()
for _a, _b in [("I've built 25 sites this way", "I've built more than 250 sites this way"), ("I've built 25 sites for clients in the US, Belgium and Hungary", "I've shipped more than 250 sites for clients in 14 countries"), ("I've shipped 25 sites for clients in the US, Belgium and Hungary", "I've shipped more than 250 sites for clients in 14 countries"), ('Twenty-five websites built for small businesses in the US, Belgium and Hungary.', 'More than 250 websites built for small businesses in 14 countries. The 25 below are written up in full.'), ('across the US, Belgium and Hungary', 'across 14 countries'), ('in the US, Belgium and Hungary', 'in 14 countries across five continents'), ('25 client websites', '250+ client websites'), ('25 sites shipped', '250+ sites shipped'), ('See all 25 projects', 'See all 25 case studies'), ('View all 25 projects', 'View all 25 case studies')]:
  COPY = COPY.replace(_a, _b)
exec(open(os.path.join(BASE, 'fill.py'), encoding='utf-8').read())
COPY = fill_copy(COPY)
exec(open(os.path.join(BASE, 'world.py'), encoding='utf-8').read())
exec(open(os.path.join(BASE, 'products.py'), encoding='utf-8').read())
exec(open(os.path.join(BASE, 'reviews_grid.py'), encoding='utf-8').read())
exec(open(os.path.join(BASE, 'imgq.py'), encoding='utf-8').read())
FX_JS = open(os.path.join(BASE, 'fx_mount.js'), encoding='utf-8').read()
BLOBS = json.load(open(os.path.join(NICHE, 'assets', 'blobs.json')))
CREATIVE = open(os.path.join(PROJ, 'Creative.dc.html'), encoding='utf-8').read()
PORTRAIT = '/_blob/6fbbcd188e6864012d87c634f944c25d'
AVATAR = '/_blob/dc5af924d95ea0c65e0bccbd61ccba59'
BANDS = {
  'About.dc.html': ('/_blob/fbba8323ce2532684276bba580d15600', 'Rakib Hasan at work', 'One person plans, designs and builds your site'),
  'Process.dc.html': ('/_blob/3f8022fe20f01f0732100bca0089e37c', 'Rakib Hasan building a website on a laptop', 'From first audit to a verified launch'),
  'Contact.dc.html': ('/_blob/7e977488fb738bdc0dafb257c02f8d16', 'Rakib Hasan with a coffee, between client calls', 'Every message is read and answered by me'),
  'Audit.dc.html': ('/_blob/7f3bcf262879b443e5a37433f5a899ee', 'Rakib Hasan reviewing a website by hand', 'Every audit is done by hand, not by a bot'),
  'Services.dc.html': ('/_blob/3b151369cc032d5100fef8a6c0373841', 'Rakib Hasan at his desk', 'Design, development and SEO from one person'),
}

def band(fname):
  src, alt, cap = BANDS[fname]
  return '''<section data-theme="ink" class="bd-band"><div class="bd-wrap"><figure class="bd-band-fig"><div class="bd-band-img" data-clip="1"><img src="%s" alt="%s" loading="lazy"></div><figcaption class="bd-band-cap"><span class="bd-mono">%s</span><span class="bd-band-who"><img src="%s" alt="">Rakib Hasan</span></figcaption></figure></div></section>''' % (src, alt, html.escape(cap), AVATAR)
B = lambda h: '/_blob/' + h

# ---------------------------------------------------------------- pages
PAGES = {
  'Services.dc.html':     ('## Services hub', 'Services'),
  'SvcWordPress.dc.html': ('## Service: WordPress & Elementor websites', 'Services'),
  'SvcCustom.dc.html':    ('## Service: Custom WordPress development', 'Services'),
  'SvcSEO.dc.html':       ('## Service: SEO audit & fixes', 'Services'),
  'SvcApps.dc.html':      ('## Service: Web & mobile apps', 'Services'),
  'SvcPlatforms.dc.html': ('## Service: Shopify, Wix & Squarespace', 'Services'),
  'SvcBrand.dc.html':     ('## Service: Branding, social media & video', 'Services'),
  'Audit.dc.html':        ('## Free website audit', None),
  'About.dc.html':        ('## About', None),
  'Process.dc.html':      ('## Process', None),
  'Reviews.dc.html':      ('## Reviews', None),
  'FAQ.dc.html':          ('## FAQ', None),
  'Contact.dc.html':      ('## Contact', None),
}

def link_for(text):
  t = text.lower()
  if 'audit' in t and 'seo audit' not in t and 'wordpress seo' not in t: return 'Audit.dc.html'
  if 'custom wordpress' in t: return 'SvcCustom.dc.html'
  if 'seo' in t: return 'SvcSEO.dc.html'
  if 'web app' in t or 'mobile app' in t or 'app ' in t: return 'SvcApps.dc.html'
  if 'shopify' in t or 'wix' in t or 'squarespace' in t: return 'SvcPlatforms.dc.html'
  if 'brand' in t or 'video' in t: return 'SvcBrand.dc.html'
  if 'wordpress website' in t: return 'SvcWordPress.dc.html'
  if 'case study' in t: return 'Case.dc.html'
  if 'project' in t or 'work' in t: return 'Work.dc.html'
  if 'review' in t: return 'Reviews.dc.html'
  if 'process' in t: return 'Process.dc.html'
  if 'service' in t: return 'Services.dc.html'
  return 'Contact.dc.html'

def chunk(start):
  i = COPY.index(start + '\n')
  j = COPY.find('\n## ', i + 3)
  return COPY[i:j if j > 0 else len(COPY)]

# ---------------------------------------------------------------- inline markdown
def clean(t):
  return (t.replace('\\[', '[').replace('\\]', ']').replace('&#91;', '[').replace('\\|', '|')
           .replace('\\<', '<').replace('\\_', '_').replace('\\*', '*').replace('\\-', '-'))

def inl(t):
  t = html.escape(clean(t), quote=False)
  t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" class="bd-ln">\1</a>', t)
  t = re.sub(r'\[([^\]]+)\]', r'<span class="bd-fill">[\1]</span>', t)
  t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
  t = re.sub(r'`([^`]+)`', r'<code class="bd-code">\1</code>', t)
  t = t.replace('Read the case study.', '<a href="Case.dc.html" class="bd-ln">Read the case study</a>.')
  return t

def plain(t):
  t = clean(t)
  t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', t)
  return re.sub(r'\*\*(.+?)\*\*', r'\1', t).replace('`', '')

SKIP = ('**Internal links:**', '**Rule:**', 'Photo:', 'Each quote links', '**Form', '**Setup note', 'Success message:',
        '**Filters', '**Card copy', '**New JetEngine', 'H1:', '**Form fields:**', '**Sections, in order')

def parse_blocks(lines):
  blocks, para = [], []
  def flush():
    if para: blocks.append(('p', ' '.join(para))); para.clear()
  i = 0
  while i < len(lines):
    l = lines[i].rstrip(); s = l.strip()
    if not s: flush(); i += 1; continue
    if s.startswith(SKIP): flush(); i += 1; continue
    if s.startswith('|'):
      flush(); rows = []
      while i < len(lines) and lines[i].strip().startswith('|'):
        r = [c.strip() for c in re.split(r'(?<!\\)\|', lines[i].strip())[1:-1]]
        if not all(set(c) <= set('- :') for c in r): rows.append(r)
        i += 1
      blocks.append(('table', rows)); continue
    m = re.match(r'^[-*] (.*)', s)
    if m:
      flush(); items = []
      while i < len(lines) and re.match(r'^\s*[-*] ', lines[i]):
        items.append(re.sub(r'^\s*[-*] ', '', lines[i].strip())); i += 1
      blocks.append(('ul', items)); continue
    m = re.match(r'^\d+\. (.*)', s)
    if m:
      flush(); items = []
      while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()):
        items.append(re.sub(r'^\d+\. ', '', lines[i].strip())); i += 1
      blocks.append(('ol', items)); continue
    if s.startswith('> '): flush(); blocks.append(('quote', s[2:])); i += 1; continue
    if re.match(r'^Buttons?( \([^)]*\))?:', s): flush(); blocks.append(('btns', s.split(':', 1)[1])); i += 1; continue
    if s.startswith('Link:'): flush(); blocks.append(('link', s[5:].strip())); i += 1; continue
    if s.startswith(('Badge:', 'Trust line:')): flush(); blocks.append(('badge', s.split(':', 1)[1].strip())); i += 1; continue
    if s.startswith('Under the button:'): flush(); blocks.append(('note', s.split(':', 1)[1].strip())); i += 1; continue
    para.append(s); i += 1
  flush()
  merged = []
  for b in blocks:
    if merged and b[0] == 'ul' and merged[-1][0] == 'ul':
      merged[-1] = ('ul', merged[-1][1] + b[1])
    else:
      merged.append(b)
  return merged

def parse_page(md):
  lines = md.split('\n')
  spec = {}
  # spec table
  k = 1
  while k < len(lines) and not lines[k].startswith('|'): k += 1
  while k < len(lines) and lines[k].startswith('|'):
    r = [c.strip() for c in re.split(r'(?<!\\)\|', lines[k])[1:-1]]
    if len(r) >= 2: spec[re.sub(r' \(\d+\)', '', r[0])] = r[1]
    k += 1
  intro, sections, cur = [], [], None
  for l in lines[k:]:
    if l.startswith('### '):
      cur = {'title': l[4:].strip(), 'lines': [], 'subs': []}; sections.append(cur); continue
    if l.startswith('#### ') and cur is not None:
      cur['subs'].append({'title': l[5:].strip(), 'lines': []}); continue
    if cur is None: intro.append(l)
    elif cur['subs']: cur['subs'][-1]['lines'].append(l)
    else: cur['lines'].append(l)
  return spec, parse_blocks(intro), sections

# ---------------------------------------------------------------- block renderers
def btn(label, href, primary):
  cls = 'bd-btn bd-btn-p' if primary else 'bd-btn'
  return '<a href="%s" class="%s">%s<span aria-hidden="true">→</span></a>' % (href, cls, inl(label))

def render_btns(spec_text):
  parts = [p.strip() for p in spec_text.split(' · ') if p.strip()]
  out = []
  for n, p in enumerate(parts):
    primary = p.startswith('**')
    label = plain(p).strip()
    out.append(btn(label, link_for(label), primary or n == 0))
  return '<div class="bd-btns">' + ''.join(out) + '</div>'

def is_faq(b): return b[0] == 'p' and re.match(r'^\*\*[^*]+\?\*\*', b[1])

CHECK_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
EDITORIAL_TABLES = ('New filter', 'Field', 'Rule')
PICK_N = 0

def initials(who):
  name = re.split(r'[,·]', plain(who))[0].strip()
  parts = [p for p in re.split(r'\s+', name) if p and p[0].isalpha()]
  return ''.join(p[0] for p in parts[:2]).upper() or '★'

def render_blocks(blocks, lead=False):
  out, i, first_p = [], 0, True
  while i < len(blocks):
    kind, v = blocks[i]
    if is_faq(blocks[i]):
      items = []
      while i < len(blocks) and is_faq(blocks[i]):
        m = re.match(r'^\*\*([^*]+\?)\*\*\s*(.*)$', blocks[i][1])
        items.append('<details class="bd-faq"><summary><span>%s</span><span class="bd-plus" aria-hidden="true"></span></summary><p>%s</p></details>' % (inl(m.group(1)), inl(m.group(2))))
        i += 1
      out.append('<div class="bd-faqs">' + ''.join(items) + '</div>'); continue
    if kind == 'p':
      if v.startswith('Summary:'): v = v[8:].strip()
      cls = 'bd-p bd-p-lg' if (lead and first_p) else 'bd-p'
      first_p = False
      out.append('<p class="%s">%s</p>' % (cls, inl(v)))
    elif kind == 'ul':
      leads = [re.match(r'^\*\*(.+?)\*\*:?\s*(.+)$', it) for it in v]
      if all(leads):
        tiles = []
        for n, m in enumerate(leads):
          tiles.append('<div class="bd-tile"><span class="bd-mono bd-tile-n">%02d</span><div class="bd-tile-h">%s</div><p>%s</p></div>' % (n + 1, inl(m.group(1).rstrip(':')), inl(m.group(2).lstrip(': '))))
        out.append('<div class="bd-tiles">' + ''.join(tiles) + '</div>')
      else:
        out.append('<ul class="bd-checks">' + ''.join('<li><span class="bd-check"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path pathLength="1" d="M5 12.5l4.5 4.5L19 7.5"></path></svg></span><span class="bd-check-t">%s</span><span class="bd-mono bd-check-n">%02d</span></li>' % (inl(it), k + 1) for k, it in enumerate(v)) + '</ul>')
    elif kind == 'ol':
      rows = []
      for n, it in enumerate(v):
        m = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', it)
        head, body = (m.group(1), m.group(2)) if m else ('', it)
        rows.append('<li class="bd-tl"><span class="bd-tl-n">%02d</span><div class="bd-tl-card">%s<p>%s</p></div></li>' % (
          n + 1, ('<div class="bd-tl-h">%s</div>' % inl(head.rstrip('.'))) if head else '', inl(body)))
      out.append('<ol class="bd-timeline"><li class="bd-tl-rail" aria-hidden="true" role="presentation"><i></i></li>' + ''.join(rows) + '</ol>')
    elif kind == 'table':
      head, *body = v
      if plain(head[0]) in EDITORIAL_TABLES:
        i += 1; continue
      if 'price' in plain(head[-1]).lower() and len(head) >= 3:
        cards = []
        for n, r in enumerate(body):
          name = plain(r[0])
          feat = 'most chosen' in name.lower() or (len(body) >= 3 and n == 1) or (len(body) == 2 and n == 1)
          name = re.sub(r'\s*\(most chosen\)', '', name, flags=re.I)
          cards.append('<div class="bd-price%s">%s<div class="bd-mono bd-price-k">%s</div><h3 class="bd-price-h">%s</h3><p>%s</p><div class="bd-price-v">%s</div><a class="bd-btn%s" href="Audit.dc.html">%s<span aria-hidden="true">→</span></a></div>' % (
            ' bd-price-feat' if feat else '', '<span class="bd-mono bd-price-badge">Most chosen</span>' if feat else '',
            'Package %02d' % (n + 1), html.escape(name), inl(r[1]), inl(r[-1]), ' bd-btn-p' if feat else '',
            'Start with an audit' if 'quoted' in plain(r[-1]).lower() else 'Get a quote'))
        out.append('<div class="bd-prices">' + ''.join(cards) + '</div>')
      elif len(head) == 2 and 'price' in plain(head[1]).lower():
        rows = ''.join('<li class="bd-plist-row"><span class="bd-plist-n">%s</span><span class="bd-plist-dots" aria-hidden="true"></span><span class="bd-plist-v">%s</span></li>' % (inl(r[0]), inl(r[1])) for r in body)
        out.append('<div class="bd-plist"><div class="bd-plist-head bd-mono"><span>%s</span><span>%s</span></div><ul>%s</ul><a class="bd-arrow" href="Audit.dc.html">Get an exact quote after a free audit <span aria-hidden="true">→</span></a></div>' % (inl(head[0]), inl(head[1]), rows))
      elif len(head) == 2:
        global PICK_N
        PICK_N += 1
        pid = 'bdpk%d' % PICK_N
        opts, res = [], []
        for n, r in enumerate(body):
          ans = plain(r[1])
          opts.append('<label class="bd-pick-o" for="%s-%d"><input type="radio" name="%s" id="%s-%d"%s><span class="bd-mono bd-pick-n">%02d</span><span class="bd-pick-q">%s</span><span class="bd-pick-a">%s</span><span class="bd-pick-ic" aria-hidden="true">→</span></label>' % (pid, n, pid, pid, n, ' checked' if n == 0 else '', n + 1, inl(r[0]), inl(r[1])))
          res.append('<div class="bd-pick-r" data-i="%d"><span class="bd-mono">%s</span><div class="bd-pick-big">%s</div><p>%s</p><a class="bd-btn bd-btn-p" href="%s">See %s work<span aria-hidden="true">→</span></a></div>' % (n, inl(head[1]), inl(r[1]), inl(r[0]), link_for(ans), html.escape(ans.split(' or ')[0])))
        css = ''
        out.append('<div class="bd-pick" id="%s">%s<div class="bd-pick-l"><div class="bd-mono bd-pick-h">%s</div>%s</div><div class="bd-pick-panel" aria-live="polite">%s</div></div>' % (pid, css, inl(head[0]), ''.join(opts), ''.join(res)))
      else:
        cards = []
        for r in body:
          dl = ''.join('<div><dt class="bd-mono">%s</dt><dd>%s</dd></div>' % (inl(h), inl(c)) for h, c in zip(head[1:], r[1:]))
          cards.append('<div class="bd-spec"><div class="bd-spec-h">%s</div><dl>%s</dl></div>' % (inl(r[0]), dl))
        out.append('<div class="bd-specs">' + ''.join(cards) + '</div>')
    elif kind == 'quote':
      q = clean(v)
      m = re.match(r'^(.*?)\s+—\s+(.*)$', q)
      text, who = (m.group(1), m.group(2)) if m else (q, '')
      text = text.strip().strip('"“”')
      out.append('<figure class="bd-quote"><span class="bd-qmark" aria-hidden="true">“</span><blockquote>%s</blockquote><figcaption><span class="bd-qav" aria-hidden="true">%s</span><span class="bd-mono">%s</span></figcaption></figure>' % (inl(text), initials(who), inl(who)))
    elif kind == 'btns':
      out.append(render_btns(v))
    elif kind == 'link':
      label = plain(v).strip().rstrip('→').strip()
      out.append('<a class="bd-arrow" href="%s">%s <span aria-hidden="true">→</span></a>' % (link_for(label), inl(label)))
    elif kind == 'badge':
      out.append('<div class="bd-badgeline">' + ''.join('<span>%s</span>' % inl(p) for p in v.split(' · ')) + '</div>')
    elif kind == 'note':
      out.append('<p class="bd-note">%s</p>' % inl(v))
    i += 1
  return '\n'.join(out)

ICONS = {
  'mail': '<path d="M4 6h16v12H4z"></path><path d="M4 7l8 6 8-6"></path>',
  'tag': '<path d="M3 12V4h8l10 10-8 8z"></path><circle cx="7.5" cy="7.5" r="1.5"></circle>',
  'arrow': '<path d="M5 12h14M13 6l6 6-6 6"></path>',
  'chat': '<path d="M4 5h16v11H9l-5 4z"></path>',
  'people': '<circle cx="9" cy="8" r="3"></circle><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"></path><path d="M16 4.5a3 3 0 010 6M21 20c0-2.6-1.6-4.8-4-5.6"></path>',
  'tool': '<path d="M14.5 5.5a4 4 0 00-5 5L4 16l4 4 5.5-5.5a4 4 0 005-5l-2.5 2.5-3-1-1-3z"></path>',
  'spark': '<path d="M12 3v6M12 15v6M3 12h6M15 12h6"></path>',
  'shield': '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"></path>',
}
def icon_for(title):
  t = title.lower()
  for keys, ic in ((('get', 'deliver', 'receive'), 'mail'), (('free', 'price', 'cost'), 'tag'), (('next', 'happens', 'after'), 'arrow'),
                   (('touch', 'talk', 'reach', 'question'), 'chat'), (('who', 'clients', 'with'), 'people'), (('tool', 'stack', 'build'), 'tool'),
                   (('safe', 'secur', 'redesign', 'ranking'), 'shield')):
    if any(k in t for k in keys): return ic
  return 'spark'

def svg(name):
  return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICONS[name]

def is_simple(s):
  if s['subs']: return False
  bl = parse_blocks(s['lines'])
  if not bl or not any(b[0] == 'p' for b in bl): return False
  if any(is_faq(b) for b in bl): return False
  if not all(b[0] in ('p', 'link', 'btns', 'note', 'badge') for b in bl): return False
  return sum(len(b[1]) for b in bl if b[0] == 'p') < 900

def bento(run, n0, theme):
  variants = ['bd-bc-a', 'bd-bc-b', 'bd-bc-c', 'bd-bc-b']
  cards = []
  for i, s in enumerate(run):
    num = n0 + i
    bl = parse_blocks(s['lines'])
    cards.append('''<article class="bd-bc %s"><div class="bd-bc-top"><span class="bd-mono">%02d</span><span class="bd-bc-ic">%s</span></div><h2 class="bd-bc-h">%s</h2><div class="bd-bc-body">%s</div><span class="bd-bc-num" aria-hidden="true">%02d</span></article>''' % (
      variants[i % len(variants)], num, svg(icon_for(s['title'])), html.escape(clean(s['title'])), render_blocks(bl), num))
  return '''<section data-theme="%s" class="bd-sec"><div class="bd-wrap"><div class="bd-bento bd-bento-%d">%s</div></div></section>''' % (theme, min(len(run), 4), ''.join(cards))

def statement(s, n, theme):
  bl = parse_blocks(s['lines'])
  first = next(i for i, b in enumerate(bl) if b[0] == 'p')
  text = bl[first][1]
  m = re.match(r'^(.+?[.!?])\s+(.*)$', text)
  lead, rest = (m.group(1), m.group(2)) if m else (text, '')
  rest_blocks = bl[:first] + ([('p', rest)] if rest else []) + bl[first + 1:]
  parts = []
  for chunk_ in re.split(r'(\[[^\]]+\])', plain(lead)):
    if not chunk_: continue
    if chunk_.startswith('['):
      parts.append('<span data-w="1"><span class="bd-fill">%s</span> </span>' % html.escape(chunk_))
    else:
      parts += ['<span data-w="1">%s </span>' % html.escape(w) for w in chunk_.split()]
  words = ''.join(parts)
  return '''<section data-theme="%s" class="bd-sec bd-stmt"><div class="bd-wrap">
<div class="bd-stmt-head"><span class="bd-mono">%02d</span><h2 class="bd-stmt-h">%s</h2><span class="bd-stmt-line" aria-hidden="true"></span><span class="bd-stmt-ic">%s</span></div>
<div class="bd-stmt-grid"><p class="bd-stmt-lead">%s</p><div class="bd-stmt-rest">%s</div></div>
</div></section>''' % (theme, n, html.escape(clean(s['title'])), svg(icon_for(s['title'])), words, render_blocks(rest_blocks))


REVIEWS = json.load(open(os.path.join(BASE, 'reviews.json'), encoding='utf-8'))
FEATURED = ['46', '48', '66', '67', '7', '3', '42', '83', '9', '70', '97', '61', '12', '68', '81', '92']

def stars(r):
  try: v = float(r)
  except ValueError: v = 5
  full = int(v)
  return '★' * full + ('½' if v - full >= 0.5 else '') + ' %s' % (('%.1f' % v) if v != int(v) else '%d.0' % v)

def initials2(who):
  w = re.sub(r'[^a-zA-Z]', '', who)
  return (w[:2] or 'RH').upper()

def reviews_html():
  byn = {r['n']: r for r in REVIEWS}
  cards = []
  for i, n in enumerate(FEATURED):
    r = byn.get(n)
    if not r: continue
    t = r['text'].strip()
    if len(t) > 360: t = t[:340].rsplit(' ', 1)[0] + '…'
    big = ' bd-rv-big' if i in (0, 5, 10) else ''
    cards.append('''<figure class="bd-rv%s"><div class="bd-rv-top"><span class="bd-rv-stars" aria-label="%s out of 5">%s</span><span class="bd-mono">%s</span></div>
<blockquote>%s</blockquote>
<figcaption><span class="bd-qav" aria-hidden="true">%s</span><span><b>%s</b><span class="bd-mono">%s · %s</span></span></figcaption></figure>''' % (
      big, r['rating'], stars(r['rating']), html.escape(r['when']), html.escape(t), initials2(r['who']), html.escape(r['who']), html.escape(r['country']), html.escape(r['price'])))
  shorts = [r['text'].strip() for r in REVIEWS if len(r['text'].strip()) < 48]
  seen, uniq = set(), []
  for x in shorts:
    k = x.lower().strip('.! ')
    if k not in seen: seen.add(k); uniq.append(x)
  row = lambda items: ''.join('<span class="bd-mq-chip"><i aria-hidden="true">★</i>%s</span>' % html.escape(x) for x in items)
  half = len(uniq) // 2
  countries = [('United States', 72), ('Belgium', 10), ('United Kingdom', 4), ('Azerbaijan', 3), ('Germany', 2), ('Nigeria', 2), ('New Zealand', 2), ('8 more countries', 6)]
  gigs = [('Construction websites', 39), ('Ecommerce websites', 33), ('Portfolio & resume', 20), ('Consulting & coaching', 4), ('Transport & logistics', 3), ('Restaurants', 2)]
  bars = lambda items, total: ''.join('<div class="bd-rbar"><span class="bd-rbar-l">%s</span><span class="bd-rbar-t"><i data-grow="%.1f%%"></i></span><span class="bd-mono">%d</span></div>' % (html.escape(a), b * 100.0 / total, b) for a, b in items)
  repeat = [('evburgessjr_01', 20), ('stelaire', 10), ('chefgregorys', 7), ('muzteng309', 4), ('creditdude', 4), ('rtjrentals', 4)]
  return '''<section data-theme="ink" class="bd-sec bd-rstats">
<div class="bd-wrap">
<div class="bd-rs-grid">
<div class="bd-rs-score">
<div class="bd-mono" style="color:var(--muted)">Fiverr · rakib_64 · Level 2</div>
<div class="bd-rs-big">4.99</div>
<div class="bd-rs-stars" aria-hidden="true">★★★★★</div>
<p>Average of all <b>101 reviews</b>. 98 are five stars. Every category on the profile is rated 5: communication, quality and value.</p>
<div class="bd-rs-kpis"><div><b>101</b><span class="bd-mono">Reviews</span></div><div><b>13</b><span class="bd-mono">Countries</span></div><div><b>1 hr</b><span class="bd-mono">Avg. response</span></div><div><b>89</b><span class="bd-mono">Replied to</span></div></div>
</div>
<div class="bd-rs-card"><div class="bd-mono bd-rs-h">Where clients are</div>%s</div>
<div class="bd-rs-card"><div class="bd-mono bd-rs-h">What they hired me for</div>%s</div>
<div class="bd-rs-card bd-rs-repeat"><div class="bd-mono bd-rs-h">Clients who came back</div><div class="bd-rs-chips">%s</div><p>evburgessjr_01 has hired me 20 times.</p></div>
</div>
</div>
</section>
<section data-theme="bone" class="bd-mqsec" aria-label="Short reviews">
<div class="bd-mqrow"><div class="bd-mqtrack">%s%s</div></div>
<div class="bd-mqrow bd-mqrow-r"><div class="bd-mqtrack">%s%s</div></div>
</section>
<section data-theme="bone" class="bd-sec">
<div class="bd-wrap">
<div class="bd-sechead"><div class="bd-mono bd-lab">Client reviews</div><h2 class="bd-h2">In their own words</h2><div class="bd-sechead-b"><p class="bd-p">Copied exactly as they appear on Fiverr, typos and all. <a class="bd-ln" href="https://fiverr.com/rakib_64/">Read all 101 on Fiverr</a>.</p></div></div>
%s
</div>
</section>''' % (bars(countries, 101), bars(gigs, 101),
       ''.join('<span><b>%s</b> ×%d</span>' % (html.escape(a), b) for a, b in repeat),
       row(uniq[:half]), row(uniq[:half]), row(uniq[half:]), row(uniq[half:]), reviews_grid_html())


def lines_html(h1):
  words = clean(h1).split()
  n = len(words)
  per = 3 if n <= 7 else 4 if n <= 10 else 5
  chunks = [' '.join(words[k:k + per]) for k in range(0, n, per)]
  if len(chunks) > 1 and len(chunks[-1].split()) == 1:
    tail = chunks.pop(); chunks[-1] += ' ' + tail
  return ''.join('<span class="bd-line"><span data-up="1">%s</span></span>' % html.escape(c) for c in chunks)

THEMES = ['bone', 'ink', 'bone', 'navy', 'bone', 'ink']

def render_section(sec, n, theme, last):
  title = clean(sec['title'])
  blocks = parse_blocks(sec['lines'])
  sid = 'bd-s%d' % n
  label = '<div class="bd-mono bd-lab">%02d</div>' % n
  if last:
    return '''<section id="%s" data-theme="orange" class="bd-ctasec">
<div class="bd-wrap">
<h2 class="bd-cta-h">%s</h2>
<div class="bd-cta-row">
<div class="bd-cta-body">%s</div>
<div class="bd-hide-sm bd-magwrap"><a class="bd-magnet" href="Audit.dc.html">Start here</a></div>
</div>
</div>
</section>''' % (sid, lines_html(title), render_blocks(blocks) or render_btns('**Get a free audit**'))
  if sec['subs']:
    cards = []
    for k, sub in enumerate(sec['subs']):
      sb = parse_blocks(sub['lines'])
      link = next((b for b in sb if b[0] == 'link'), None)
      sb = [b for b in sb if b[0] != 'link']
      st = re.sub(r'^\d+\.\s*', '', clean(sub['title']))
      inner = '<span class="bd-mono bd-card-n">%02d</span><h3 class="bd-card-h">%s</h3>%s' % (k + 1, html.escape(st), render_blocks(sb))
      if link:
        lab = plain(link[1]).rstrip('→').strip()
        cards.append('<a class="bd-cardx bd-cardlink" href="%s">%s<span class="bd-arrow">%s <span aria-hidden="true">→</span></span></a>' % (link_for(lab), inner, html.escape(lab)))
      else:
        cards.append('<div class="bd-cardx">%s</div>' % inner)
    return '''<section id="%s" data-theme="%s" class="bd-sec">
<div class="bd-wrap">
<div class="bd-sechead">%s<h2 class="bd-h2">%s</h2>%s</div>
<div class="bd-cards">%s</div>
</div>
</section>''' % (sid, theme, label, html.escape(title), ('<div class="bd-sechead-b">' + render_blocks(blocks) + '</div>') if blocks else '', ''.join(cards))
  quotes = [b for b in blocks if b[0] == 'quote']
  if len(quotes) >= 3:
    rest = [b for b in blocks if b[0] != 'quote']
    qs = render_blocks(quotes)
    return '''<section id="%s" data-theme="%s" class="bd-sec">
<div class="bd-wrap">
<div class="bd-sechead">%s<h2 class="bd-h2">%s</h2></div>
<div class="bd-quotes">%s</div>%s
</div>
</section>''' % (sid, theme, label, html.escape(title), qs, render_blocks(rest))
  return '''<section id="%s" data-theme="%s" class="bd-sec">
<div class="bd-wrap bd-split">
<div class="bd-split-l">%s<h2 class="bd-h2">%s</h2></div>
<div class="bd-split-r">%s</div>
</div>
</section>''' % (sid, theme, label, html.escape(title), render_blocks(blocks, lead=all(b[0] == 'p' for b in blocks)))

def hero(crumb, h1, intro_html, side=''):
  return '''<section id="bd-hero" data-theme="ink" class="bd-hero">
<canvas id="bd-gl" aria-hidden="true"></canvas>
<div class="bd-wrap bd-hero-in">
<nav class="bd-mono bd-crumb" aria-label="Breadcrumb"><a href="Creative.dc.html">Home</a><span>/</span>%s</nav>
<h1 class="bd-h1">%s</h1>
<div class="bd-hero-row"><div class="bd-hero-intro">%s</div>%s</div>
<div class="bd-hero-meta bd-mono"><span><b>5.0</b> from 101 reviews</span><span><b>250+</b> sites shipped</span><span><b>~1 hr</b> average reply</span><span class="bd-hide-sm"><b>14</b> countries</span></div>
</div>
</section>''' % (crumb, lines_html(h1), intro_html, side)

FORM_FIELD = 'class="bd-in"'
def audit_form(note):
  return '''<form class="bd-form" id="bd-form" onSubmit="{{noop}}">
<label class="bd-mono">Your name<input type="text" name="name" autocomplete="name" %s></label>
<label class="bd-mono">Email<input type="email" name="email" autocomplete="email" %s></label>
<label class="bd-mono">Website address<input type="url" name="website" placeholder="https://" %s></label>
<label class="bd-mono">What would you most like your website to do better? (optional)<textarea name="goal" rows="2" %s></textarea></label>
<button type="button" class="bd-btn bd-btn-p bd-btn-lg" onClick="{{send}}">Send me my audit<span aria-hidden="true">→</span></button>
<p class="bd-note">%s</p>
<sc-if value="{{sent}}" hint-placeholder-val="{{false}}"><p role="status" class="bd-ok">Got it. I'll review your site by hand and email your top five fixes within 48 hours.</p></sc-if>
</form>''' % (FORM_FIELD, FORM_FIELD, FORM_FIELD, FORM_FIELD, note)

def contact_form():
  opts = ['New website', 'Redesign', 'Custom plugin or app', 'SEO audit or fixes', 'Shopify, Wix or Squarespace', 'Branding or content', 'Something else']
  o = ''.join('<option style="color:#0B0B0C">%s</option>' % html.escape(x) for x in opts)
  return '''<form class="bd-form" id="bd-form">
<div class="bd-form2"><label class="bd-mono">Your name *<input type="text" name="name" autocomplete="name" required %s></label>
<label class="bd-mono">Email *<input type="email" name="email" autocomplete="email" required %s></label></div>
<label class="bd-mono">Website address, if you have one<input type="url" name="website" placeholder="https://" %s></label>
<div class="bd-form2"><label class="bd-mono">What do you need?<select name="need" %s>%s</select></label>
<label class="bd-mono">Budget<select name="budget" %s><option style="color:#0B0B0C">Under $1,000</option><option style="color:#0B0B0C">$1,000–$3,000</option><option style="color:#0B0B0C">$3,000–$7,500</option><option style="color:#0B0B0C">$7,500+</option><option style="color:#0B0B0C">Not sure yet</option></select></label></div>
<label class="bd-mono">Tell me about the project *<textarea name="msg" rows="4" required %s></textarea></label>
<button type="button" class="bd-btn bd-btn-p bd-btn-lg" onClick="{{send}}">Send message<span aria-hidden="true">→</span></button>
<p class="bd-note">I'll only use your details to reply to you.</p>
<sc-if value="{{sent}}" hint-placeholder-val="{{false}}"><p role="status" class="bd-ok">Thanks, your message is on its way. I'll reply within 12 hours. While you wait, have a look at <a class="bd-ln" href="Work.dc.html">recent projects</a>.</p></sc-if>
</form>''' % (FORM_FIELD, FORM_FIELD, FORM_FIELD, FORM_FIELD, o, FORM_FIELD, FORM_FIELD)

def build_generic(fname, start, crumb2):
  spec, intro, sections = parse_page(chunk(start))
  h1 = clean(spec.get('H1', ''))
  name = start[3:].replace('Service: ', '')
  crumb = ('<a href="Services.dc.html">Services</a><span>/</span>' if crumb2 else '') + '<span aria-current="page">%s</span>' % html.escape(clean(name))
  intro_html = render_blocks(intro)
  side = ''
  body = []
  if fname == 'Audit.dc.html':
    side = '<div class="bd-hero-form">' + audit_form('I reply within 12 hours. Your details are only used to send your audit.') + '</div>'
    intro_html = render_blocks([b for b in intro if b[0] != 'note'])
  if fname == 'About.dc.html':
    side = '''<div class="bd-ph-wrap bd-hero-ph"><div class="bd-ph" data-clip="1"><img id="bd-portrait" src="%s" alt="Rakib Hasan, freelance web designer and developer"></div></div>''' % PORTRAIT
  secs = [s for s in sections if s['title'] not in ('Add more reviews', 'Case study template (every project page)')]
  if fname in BANDS: body.append(band(fname))
  if fname == 'About.dc.html': body.append(world_html('navy', 'Where my clients are'))
  n = 0
  done = set()
  for k, s in enumerate(secs):
    last = k == len(secs) - 1
    if s['title'] == 'Send a message':
      n += 1
      body.append('''<section id="bd-s%d" data-theme="bone" class="bd-sec"><div class="bd-wrap bd-split"><div class="bd-split-l"><div class="bd-mono bd-lab">%02d</div><h2 class="bd-h2">Send a message</h2>
<div class="bd-me"><img src="%s" alt=""><div><div>Rakib Hasan</div><div class="bd-mono" style="color:var(--muted)">Replies within about an hour</div></div></div></div>
<div class="bd-split-r">%s</div></div></section>''' % (n, n, AVATAR, contact_form()))
      continue
    if k in done: continue
    if s['title'].startswith('Case in point: the Kohevo'):
      n += 1; body.append(products_html(n)); continue
    if fname == 'Reviews.dc.html' and s['title'] == 'Client reviews':
      body.append(reviews_html()); body.append(world_html('navy', 'Clients in 14 countries')); n += 1; continue
    if not last and is_simple(s):
      run = [s]; j = k + 1
      while j < len(secs) - 1 and is_simple(secs[j]) and secs[j]['title'] != 'Send a message' and len(run) < 4:
        run.append(secs[j]); j += 1
      for x in range(k + 1, j): done.add(x)
      theme = THEMES[n % len(THEMES)]
      if len(run) >= 2: body.append(bento(run, n + 1, theme))
      else: body.append(statement(s, n + 1, theme))
      n += len(run)
      continue
    n += 1
    body.append(render_section(s, n, THEMES[(n - 1) % len(THEMES)], last))
  if fname in IMGQ_PAGES and body:
    body.insert(len(body) - 1, imgq_html(cases))
  title = plain(spec.get('SEO title', h1))
  meta = plain(spec.get('Meta description', ''))
  return page(fname, title, meta, hero(crumb, h1, intro_html, side) + '\n' + '\n'.join(body), active=crumb2 and 'Services' or name)

# ---------------------------------------------------------------- case studies
NAME2SLUG = {
 'RTJ Rentals': 'rtj-rentals', 'Villa Lapierrot': 'villa-lapierrot', 'Redkey Logistics': 'redkey-logistics',
 'CDG Maui': 'cdg-maui', 'CGP Construction Corp': 'cgp-construction-corp', 'JOAB Construction': 'joab-construction',
 'RF Home Remodeling': 'remodeling-rf', 'Palm Flooring': 'palm-tile', 'Carolina Custom Glass Works': 'carolina-custom-glass-works',
 'Mendozaa Electric': 'mendozaa-electric', 'Restyling Solutions NC': 'restyling-solutions-nc', '4Eleven Logistics': 'fourelevenlogistics',
 'Anytime Pilot Car': 'anytime-pilot-car', 'Anytime Brokerage': 'anytime-brokerage', 'Safi Cleaners': 'safi-cleaners',
 'Steri Clean': 'steri-clean', 'SteriLab': 'steri-lab', 'La Côte de Beaune': 'la-cote-de-beaune', 'Domaine de La Haye': 'domaine-de-la-haye',
 'Sergio Ardila Law': 'sergio-ardila-law', 'Courageous & Free Collective': 'crenee-salone', 'Sabiha Ozbay': 'sabiha-ozbay',
 'Tatiana Megard': 'tatiana-megard', '(in)extenso': 'inextenso', 'Tündérkehely': 'tunderkehely'}
IND_COLOR = {'Construction & trades': '#FF5A1F', 'Logistics & transport': '#8EA2FF', 'Cleaning & sterilisation': '#19C7B0',
             'Hospitality & rentals': '#FF6FA5', 'Professional services': '#E8B931', 'Creative & wellness': '#B49BFF'}

def segs(text):
  """Split text into [{t, s}] segments so placeholders can be highlighted inside holes."""
  text = plain(text)
  out = []
  for part in re.split(r'(\[[^\]]+\])', text):
    if not part: continue
    out.append({'t': part, 'f': part.startswith('[')})
  return out

def parse_cases():
  md = chunk('## Case studies')
  lines = md.split('\n')
  cases, cur, sub = [], None, None
  for l in lines:
    m1 = re.match(r'^### Case study: (.+)$', l)
    m2 = re.match(r'^#### (.+)$', l)
    if m1 or (m2 and m2.group(1).strip() in NAME2SLUG):
      name = (m1 or m2).group(1).strip()
      cur = {'name': name, 'spec': {}, 'secs': {}, 'order': []}; cases.append(cur); sub = None; continue
    if l.startswith('### '): cur = None; continue
    if cur is None: continue
    if l.startswith('|'):
      r = [c.strip() for c in re.split(r'(?<!\\)\|', l)[1:-1]]
      if len(r) >= 2 and not set(r[0]) <= set('- :'): cur['spec'][re.sub(r' \(\d+\)', '', r[0])] = r[1]
      continue
    if m2: sub = m2.group(1).strip(); cur['secs'].setdefault(sub, []); continue
    s = l.strip()
    if not s or s.startswith('H1:'): continue
    m = re.match(r'^\*\*(Summary|The client|The challenge|What I built|The result|Testimonial):\*\*\s*(.*)$', s)
    if m: sub = m.group(1); cur['secs'].setdefault(sub, []).append(m.group(2)); continue
    if s.startswith('Summary:'): cur['secs'].setdefault('Summary', []).append(s[8:].strip()); continue
    if s.startswith('Next project:'): continue
    if sub: cur['secs'][sub].append(s)
  out = []
  for c in cases:
    slug = NAME2SLUG[c['name']]
    facts = {}
    for p in clean(c['spec'].get('Fact panel', '')).split(' · '):
      if ':' in p and not p.startswith('['): k, v = p.split(':', 1); facts[k.strip()] = v.strip()
      m = re.search(r'\[Live site\]\((https?://[^)]+)\)', p)
      if m: facts['Live'] = m.group(1)
    ind = facts.get('Industry', '')
    ind = next((k for k in IND_COLOR if k.lower().split(' ')[0] in ind.lower()), 'Construction & trades')
    def para(key):
      v = c['secs'].get(key, [])
      return [segs(x) for x in v if x and not x.startswith('- ')]
    gallery = [x[2:] for x in c['secs'].get('Gallery', []) if x.startswith('- ')]
    f, g = BLOBS[slug]
    year = re.sub(r'[^0-9]', '', facts.get('Year', ''))[:4]
    country = facts.get('Country', '')
    sumtxt = plain(' '.join(c['secs'].get('Summary', [])))
    out.append({
      'slug': slug, 'name': c['name'], 'industry': ind, 'color': IND_COLOR[ind],
      'country': country, 'cshort': re.sub(r'\s*\(.*\)', '', country), 'year': year,
      'client': facts.get('Client', ''), 'stack': facts.get('Stack', ''), 'service': facts.get('Service', 'Design & development'),
      'live': facts.get('Live', ''), 'h1': plain(c['spec'].get('H1', c['name'])), 'title': plain(c['spec'].get('SEO title', '')),
      'summary': sumtxt, 'img': B(f), 'img2': B(g),
      'alt': gallery[0].split(' Alt: ')[0] if gallery else c['name'] + ' website on a laptop',
      'p_client': para('The client'), 'p_challenge': para('The challenge'), 'p_built': para('What I built'),
      'p_result': para('The result'), 'p_testi': para('Testimonial')})
  return out

# ---------------------------------------------------------------- construction (from the niche prototype copy)
CONSTRUCTION = '''## Construction

| Field | Value |
| --- | --- |
| SEO title (58) | Websites for Construction Companies & Trades \\| Rakib Hasan |
| Meta description (144) | Websites for contractors, remodelers and trades: service and area pages, project galleries and quote forms that win local work. Free site audit. |
| H1 | Websites for construction companies that win more quote requests |

I build WordPress websites for contractors, remodelers and trades: service pages that rank in your area, project galleries that prove your work, and quote forms on every page. I've built eight in the US and Uganda so far.

Buttons: **Get a free contractor site audit** · See construction projects

### Why most contractor websites don't bring in work

#### Invisible in local search

One "Services" page can't rank for "kitchen remodel in Charlotte". Each trade and each area needs its own page.

#### No proof of the work

Homeowners hire on finished jobs they can see. Stock photos tell them nothing about you.

#### The quote form is buried

If asking for a price takes more than one tap, visitors call the next contractor instead.

#### Slow on a phone

Most people searching for a contractor are on mobile. Heavy galleries that load slowly lose them.

### What every contractor site gets

Built on WordPress and Elementor, so you can add projects and update prices yourself.

- **A page for every service:** Foundation repair, kitchens, flooring: each one written to rank on its own.
- **Service area pages:** The towns you cover, each with its own page and local details.
- **Project gallery:** Before-and-after photos, filtered by job type, that load fast on phones.
- **Quote form + click-to-call:** On every page, sending requests straight to your inbox.
- **Reviews that build trust:** Your Google reviews and testimonials placed next to the jobs they describe.
- **Local SEO setup:** LocalBusiness schema, Search Console, and details that match your Google Business Profile.

### Construction sites I've built

PROJECTS

### What contractors say

> "Always great to work with. He has done several sites for me, and all have been fantastic!" — Thiago Fernan · Palm Flooring, New England

> "Go ahead, this guy is really good." — Rafael · RF Home Remodeling, Philadelphia

> "As a General Contractor, I've hired over 300 independent contractors over the course of my career and I can say with confidence I've never had an experience like this. He's the MVP!" — muzteng309 · General contractor, United States · via Fiverr

### Contractor website packages

| Package | What's included | Price |
| --- | --- | --- |
| Local Trade | Up to 6 service pages, project gallery, quote form and click-to-call, local SEO setup | From $990 |
| Growing Contractor (most chosen) | Everything in Local Trade, up to 10 service area pages, filterable before-and-after gallery, reviews section and blog setup | From $1,890 |

### Contractor website FAQ

**Can I add new projects myself?** Yes. You upload photos and a short description, and the project appears in your gallery under the right job type. Every site comes with video tutorials.

**How do service area pages help?** People search for a trade plus a place. A page for each town you cover, with real local details, gives Google a page to show for those searches.

**Will it match my Google Business Profile?** Yes. I make sure your name, address, phone, hours and service areas match everywhere, which Google uses to judge local businesses.

**How long does a contractor site take?** Usually 3–5 weeks from the first call to launch. Having your project photos ready is the biggest time saver.

### Free audit for contractor websites

I'll check how your site shows up for your trade in your area, how fast it loads on a phone, and how easy it is to ask for a quote. You get the top five fixes, free.

Button: **Send me my free audit**
'''

def project_cards(cases, flt=None):
  cs = [c for c in cases if not flt or c['industry'] == flt]
  out = []
  for c in cs:
    out.append('''<a class="bd-pcard" href="Case.dc.html#%s" data-slug="%s"><div class="bd-pcard-img" data-clip="1"><img src="%s" alt="%s" loading="lazy"><span class="bd-mono bd-tag" style="background:%s">%s</span></div>
<div class="bd-pcard-t"><span>%s</span><span class="bd-mono">%s · %s</span></div><p>%s</p></a>''' % (
      c['slug'], c['slug'], c['img'], html.escape(c['alt']), c['color'], html.escape(c['industry'].split(' &')[0]),
      html.escape(c['name']), html.escape(c['cshort']), c['year'] or '—', html.escape(c['summary'])))
  return '<div class="bd-pgrid">' + ''.join(out) + '</div>'

def build_construction(cases):
  md = CONSTRUCTION
  spec, intro, sections = parse_page(md)
  h1 = spec['H1']
  crumb = '<a href="Work.dc.html">Industries</a><span>/</span><span aria-current="page">Construction &amp; trades</span>'
  side = '<div class="bd-chips bd-hide-sm"><span class="bd-mono" style="color:#8F8A82">Built for</span>' + ''.join('<span class="bd-chip">%s</span>' % x for x in ['General contractors', 'Design-build firms', 'Remodelers', 'Flooring &amp; tile', 'Glass &amp; glazing', 'Electricians']) + '</div>'
  body, n = [], 0
  for k, s in enumerate(sections):
    n += 1
    if s['title'] == "Construction sites I've built":
      body.append('''<section id="bd-s%d" data-theme="navy" class="bd-sec"><div class="bd-wrap"><div class="bd-sechead"><div class="bd-mono bd-lab">%02d</div><h2 class="bd-h2">%s</h2></div>%s</div></section>''' % (n, n, html.escape(s['title']), project_cards(cases, 'Construction & trades')))
      continue
    if k == len(sections) - 1:
      body.append('''<section id="bd-s%d" data-theme="orange" class="bd-ctasec"><div class="bd-wrap"><h2 class="bd-cta-h">%s</h2><div class="bd-cta-row"><div class="bd-cta-body">%s</div><div class="bd-hero-form bd-form-on-orange">%s</div></div></div></section>''' % (n, lines_html(s['title']), render_blocks([b for b in parse_blocks(s['lines']) if b[0] == 'p']), audit_form('Your trade, your area, your top five fixes.')))
      continue
    body.append(render_section(s, n, THEMES[(n - 1) % len(THEMES)], False))
  return page('Construction.dc.html', plain(spec['SEO title']), plain(spec['Meta description']),
              hero(crumb, h1, render_blocks(intro), side) + '\n' + '\n'.join(body), active='Industries')

def build_work(cases):
  spec, intro, sections = parse_page(chunk('## Work archive + case study template'))
  crumb = '<span aria-current="page">Work</span>'
  filters = ['All'] + list(IND_COLOR.keys())
  body = '''<section id="bd-grid" data-theme="bone" class="bd-sec" style="padding-top:90px">
<div class="bd-wrap">
<div class="bd-fx" role="toolbar" aria-label="Filter by industry"><span class="bd-mono bd-fx-k">Filter</span>
<div class="bd-fx-list"><sc-for list="{{filters}}" as="f" hint-placeholder-count="7"><button type="button" class="bd-fx-b" aria-pressed="{{f.on}}" onClick="{{f.pick}}">{{f.label}}<span class="bd-mono">{{f.count}}</span></button></sc-for></div>
<span class="bd-mono bd-fx-n">{{shownCount}} projects</span></div>
<div class="bd-pgrid">
<sc-for list="{{shown}}" as="c" hint-placeholder-count="9"><a class="bd-pcard bd-pcard-in" href="{{c.href}}" onClick="{{c.pick}}" style="{{c.delay}}"><div class="bd-pcard-img"><img src="{{c.img}}" alt="{{c.alt}}" loading="lazy"><span class="bd-mono bd-tag" style="{{c.tag}}">{{c.ind}}</span></div>
<div class="bd-pcard-t"><span>{{c.name}}</span><span class="bd-mono">{{c.meta}}</span></div><p>{{c.summary}}</p></a></sc-for>
</div>
</div>
</section>
'''
  sec = [s for s in sections if s['title'].startswith('Not sure')][0]
  body += render_section(sec, 2, 'orange', True)
  data = [{'slug': c['slug'], 'name': c['name'], 'ind': c['industry'], 'color': c['color'], 'img': c['img'], 'alt': c['alt'],
           'meta': '%s · %s' % (c['cshort'], c['year'] or '—'), 'summary': c['summary']} for c in cases]
  vals = '''
    var DATA = %s, FL = %s, COL = %s;
    var flt = S.filter || 'All';
    var filters = FL.map(function (f) {
      return { label: f === 'All' ? 'All' : ({ 'Professional services': 'Professional' }[f] || f.split(' &')[0]), on: f === flt ? 'true' : 'false', count: f === 'All' ? DATA.length : DATA.filter(function (d) { return d.ind === f; }).length,
        dot: 'background:' + (COL[f] || 'currentColor'), pick: function () { self.setState({ filter: f }); } };
    });
    var shown = DATA.filter(function (d) { return flt === 'All' || d.ind === flt; }).map(function (d, i) {
      return { name: d.name, img: d.img, alt: d.alt, meta: d.meta, summary: d.summary, ind: d.ind.split(' &')[0], href: 'Case.dc.html#' + d.slug,
        tag: 'background:' + d.color, delay: 'animation-delay:' + (Math.min(i, 8) * 0.05).toFixed(2) + 's',
        pick: function () { try { sessionStorage.setItem('bd-proj', d.slug); } catch (e) {} } };
    });
    X.filters = filters; X.shown = shown; X.shownCount = shown.length;
''' % (json.dumps(data, ensure_ascii=False), json.dumps(filters), json.dumps(IND_COLOR))
  return page('Work.dc.html', plain(spec['SEO title']), plain(spec['Meta description']),
              hero(crumb, clean(spec['H1']), render_blocks(intro), '<div class="bd-hero-stats"><div><b>250+</b><span class="bd-mono">Websites shipped</span></div><div><b>25</b><span class="bd-mono">Case studies</span></div><div><b>14</b><span class="bd-mono">Countries</span></div></div>') + '\n' + body,
              active='Work', vals=vals, state="filter: 'All'")

def build_case(cases):
  data = json.dumps(cases, ensure_ascii=False)
  para_block = lambda key, label, theme, n: '''<section data-theme="%s" class="bd-sec bd-sec-tight bd-stmt"><div class="bd-wrap"><div class="bd-stmt-head"><span class="bd-mono">%02d</span><h2 class="bd-stmt-h">%s</h2><span class="bd-stmt-line" aria-hidden="true"></span></div>
<p class="bd-case-txt"><sc-for list="{{%s}}" as="s" hint-placeholder-count="12"><span style="{{s.st}}">{{s.t}}</span></sc-for></p></div></section>''' % (theme, n, label, key)
  body = '''<section id="bd-hero" data-theme="ink" class="bd-hero bd-case-hero">
<div class="bd-wrap bd-hero-in" style="padding-top:130px">
<div class="bd-case-top"><nav class="bd-mono bd-crumb" aria-label="Breadcrumb"><a href="Creative.dc.html">Home</a><span>/</span><a href="Work.dc.html">Work</a><span>/</span><span aria-current="page">{{c.name}}</span></nav>
<label class="bd-mono bd-picker"><span>Case study</span><select onChange="{{pickSel}}" aria-label="Choose a case study"><sc-for list="{{opts}}" as="o" hint-placeholder-count="25"><option value="{{o.v}}" selected="{{o.sel}}" style="color:#0B0B0C">{{o.label}}</option></sc-for></select></label></div>
<div class="bd-mono bd-case-ind"><span class="bd-fdot" style="{{c.dot}}"></span>{{c.industry}} · {{c.cshort}} · {{c.year}}</div>
<h1 class="bd-h1 bd-case-h1" id="bd-case-h1">{{c.h1}}</h1>
<p class="bd-case-sum">{{c.summary}}</p>
</div>
<div class="bd-wrap"><div class="bd-case-img" id="bd-case-img"><img src="{{c.img}}" alt="{{c.alt}}"></div></div>
</section>
<section data-theme="ink" class="bd-facts-band"><div class="bd-wrap"><dl class="bd-factrow">
<div><dt class="bd-mono">Client</dt><dd>{{c.client}}</dd></div>
<div><dt class="bd-mono">Industry</dt><dd>{{c.industry}}</dd></div>
<div><dt class="bd-mono">Country</dt><dd>{{c.country}}</dd></div>
<div><dt class="bd-mono">Service</dt><dd>{{c.service}}</dd></div>
<div class="bd-fact-wide"><dt class="bd-mono">Stack</dt><dd>{{c.stack}}</dd></div>
<div><dt class="bd-mono">Live site</dt><dd><sc-if value="{{c.hasLive}}" hint-placeholder-val="{{true}}"><a class="bd-ln" href="{{c.live}}" rel="noopener" target="_blank">Visit ↗</a></sc-if><sc-if value="{{c.noLive}}" hint-placeholder-val="{{false}}"><span>Private build</span></sc-if></dd></div>
</dl></div></section>
''' + para_block('pClient', 'The client', 'bone', 1) + para_block('pChallenge', 'The challenge', 'bone', 2) + para_block('pBuilt', 'What I built', 'ink', 3) + '''
<section data-theme="navy" class="bd-sec"><div class="bd-wrap"><div class="bd-sechead"><div class="bd-mono bd-lab">04</div><h2 class="bd-h2">On every screen</h2></div>
<div class="bd-gal"><div class="bd-gal-a"><img src="{{c.img}}" alt="{{c.alt}}"></div><div class="bd-gal-b"><img src="{{c.img2}}" alt="{{c.altPhone}}"></div></div></div></section>
''' + para_block('pResult', 'The result', 'bone', 5) + '''
<section data-theme="orange" class="bd-sec"><div class="bd-wrap"><div class="bd-mono bd-lab">06 — In the client's words</div>
<blockquote class="bd-bigq"><sc-for list="{{pTesti}}" as="s" hint-placeholder-count="8"><span style="{{s.st}}">{{s.t}}</span></sc-for></blockquote>
<div class="bd-mono" style="margin-top:22px">{{c.client}}</div></div></section>
<section data-theme="ink" class="bd-next"><div class="bd-wrap">
<button type="button" class="bd-nextbtn" onClick="{{goNext}}"><span class="bd-mono">Next project</span><span class="bd-next-name">{{next.name}} <span aria-hidden="true">→</span></span><span class="bd-next-img"><img src="{{next.img}}" alt=""></span></button>
<div class="bd-btns" style="margin-top:36px"><a href="Audit.dc.html" class="bd-btn bd-btn-p">Start a project like this<span aria-hidden="true">→</span></a><a href="Work.dc.html" class="bd-btn">All 25 projects<span aria-hidden="true">→</span></a></div>
</div></section>'''
  vals = '''
    var DATA = %s;
    var idx = Math.max(0, Math.min(DATA.length - 1, S.proj || 0));
    var c = DATA[idx], nx = DATA[(idx + 1) %% DATA.length];
    var segMap = function (arr) {
      var out = [];
      (arr || []).forEach(function (p, pi) {
        if (pi > 0) out.push({ t: ' ', st: 'display:block;height:0.9em' });
        p.forEach(function (s) { out.push({ t: s.t, st: s.f ? 'background:color-mix(in srgb,var(--accent) 16%%,transparent);outline:1px dashed var(--accent);outline-offset:1px;border-radius:4px;padding:0 4px' : '' }); });
      });
      if (!out.length) out.push({ t: '[ADD]', st: 'outline:1px dashed var(--accent);border-radius:4px;padding:0 4px' });
      return out;
    };
    X.c = { name: c.name, h1: c.h1, summary: c.summary, industry: c.industry, country: c.country || '—', cshort: c.cshort, year: c.year || '—',
      client: c.client || '—', service: c.service, stack: c.stack || '—', live: c.live, hasLive: !!c.live, noLive: !c.live,
      img: c.img, img2: c.img2, alt: c.alt, altPhone: c.name + ' website on a phone', dot: 'background:' + c.color };
    X.next = { name: nx.name, img: nx.img };
    X.pClient = segMap(c.p_client); X.pChallenge = segMap(c.p_challenge); X.pBuilt = segMap(c.p_built);
    X.pResult = segMap(c.p_result); X.pTesti = segMap(c.p_testi);
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
''' % json.dumps([{'slug': c['slug']} for c in cases])
  return page('Case.dc.html', 'Case Studies: 25 Client Websites | Rakib Hasan', 'Case studies for 25 WordPress websites: what each client needed, what I built and how it turned out.', body,
              active='Work', vals=vals, state='proj: 0', mount=mount)

# ---------------------------------------------------------------- shared shell
def extract_style():
  a = CREATIVE.index('<style>') + 7; b = CREATIVE.index('/* shared-shell */') if '/* shared-shell */' in CREATIVE else CREATIVE.index('</style>')
  return CREATIVE[a:b]

def extract_gl():
  a = CREATIVE.index('  _startGL(st, reduced) {'); b = CREATIVE.index('  componentDidUpdate(')
  return CREATIVE[a:b]

exec(open(os.path.join(BASE, 'case_page.py'), encoding='utf-8').read())
PAGE_CSS = open(os.path.join(BASE, 'pages.css'), encoding='utf-8').read() + PRODUCTS_CSS + CASE_CSS + REV_CSS + IMGQ_CSS
WIDGET_CSS = open(os.path.join(BASE, 'widget.css'), encoding='utf-8').read()
SHELL = open(os.path.join(BASE, 'shell.html'), encoding='utf-8').read()
RUNTIME = open(os.path.join(BASE, 'runtime.js'), encoding='utf-8').read()
SHARED_VALS = open(os.path.join(BASE, 'shared_vals.js'), encoding='utf-8').read()
WIDGET_MOUNT = open(os.path.join(BASE, 'widget_mount.js'), encoding='utf-8').read()

def page(fname, title, meta, body, active='', vals='', state='', mount=''):
  header, footer, widget = SHELL.split('<!--SPLIT-->')
  doc = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%s</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<meta name="description" content="%s">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@200..600&amp;family=Geist+Mono:wght@400;500&amp;display=swap">
<style>
%s
%s
%s
%s
</style>
</helmet>
<div id="bd-root" style="position: relative; background: var(--bg); color: var(--fg); font-family: 'Geist', system-ui, sans-serif; font-weight: 400; overflow-x: clip">
%s
<main>
%s
</main>
%s
%s
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1440,"height":6000}}'>
%s
</script>
</body>
</html>
''' % (html.escape(title), html.escape(meta, quote=True), extract_style(), PAGE_CSS, WIDGET_CSS, WORLD_CSS,
       header.replace('data-nav="%s"' % active, 'data-nav="%s" aria-current="page"' % active), body, footer, widget,
       RUNTIME.replace('/*PAGE_STATE*/', (state + ',') if state else '')
              .replace('/*PAGE_MOUNT*/', mount + '\n' + WIDGET_MOUNT + WORLD_JS + REV_JS + IMGQ_JS + FX_JS)
              .replace('/*PAGE_VALS*/', vals)
              .replace('/*SHARED_VALS*/', SHARED_VALS)
              .replace('/*GL*/', extract_gl()))
  open(os.path.join(PROJ, fname), 'w', encoding='utf-8').write(doc)
  return fname

if __name__ == '__main__':
  cases = parse_cases()
  assert len(cases) == 25, len(cases)
  json.dump(cases, open(os.path.join(BASE, 'cases.json'), 'w'), ensure_ascii=False, indent=1)
  built = [build_generic(f, s, c) for f, (s, c) in PAGES.items()]
  built += [build_construction(cases), build_work(cases), build_case(cases)]
  print('\n'.join(built))
