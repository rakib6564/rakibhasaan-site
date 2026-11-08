CHECK_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
EDITORIAL_TABLES = ('New filter', 'Field', 'Rule')

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
        out.append('<ul class="bd-checks">' + ''.join('<li><span class="bd-check">%s</span><span>%s</span></li>' % (CHECK_SVG, inl(it)) for it in v) + '</ul>')
    elif kind == 'ol':
      rows = []
      for n, it in enumerate(v):
        m = re.match(r'^\*\*(.+?)\*\*\s*(.*)$', it)
        head, body = (m.group(1), m.group(2)) if m else ('', it)
        rows.append('<li class="bd-tl"><span class="bd-tl-n">%02d</span><div class="bd-tl-card">%s<p>%s</p></div></li>' % (
          n + 1, ('<div class="bd-tl-h">%s</div>' % inl(head.rstrip('.'))) if head else '', inl(body)))
      out.append('<ol class="bd-timeline">' + ''.join(rows) + '</ol>')
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
      else:
        th = ''.join('<th>%s</th>' % inl(c) for c in head)
        trs = ''.join('<tr>' + ''.join('<td>%s</td>' % inl(c) for c in r) + '</tr>' for r in body)
        out.append('<div class="bd-tablewrap"><table class="bd-table"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs))
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

