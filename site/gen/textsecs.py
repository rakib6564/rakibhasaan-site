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
      variants[i %% len(variants)] if False else variants[i % len(variants)], num, svg(icon_for(s['title'])), html.escape(clean(s['title'])), render_blocks(bl), num))
  return '''<section data-theme="%s" class="bd-sec"><div class="bd-wrap"><div class="bd-bento bd-bento-%d">%s</div></div></section>''' % (theme, min(len(run), 4), ''.join(cards))

def statement(s, n, theme):
  bl = parse_blocks(s['lines'])
  first = next(i for i, b in enumerate(bl) if b[0] == 'p')
  text = bl[first][1]
  m = re.match(r'^(.+?[.!?])\s+(.*)$', text)
  lead, rest = (m.group(1), m.group(2)) if m else (text, '')
  rest_blocks = bl[:first] + ([('p', rest)] if rest else []) + bl[first + 1:]
  words = ''.join('<span data-w="1">%s </span>' % w for w in inl(lead).split(' '))
  return '''<section data-theme="%s" class="bd-sec bd-stmt"><div class="bd-wrap">
<div class="bd-stmt-head"><span class="bd-mono">%02d</span><h2 class="bd-stmt-h">%s</h2><span class="bd-stmt-line" aria-hidden="true"></span><span class="bd-stmt-ic">%s</span></div>
<div class="bd-stmt-grid"><p class="bd-stmt-lead">%s</p><div class="bd-stmt-rest">%s</div></div>
</div></section>''' % (theme, n, html.escape(clean(s['title'])), svg(icon_for(s['title'])), words, render_blocks(rest_blocks))
