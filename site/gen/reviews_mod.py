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
<div class="bd-rwall">%s</div>
</div>
</section>''' % (bars(countries, 101), bars(gigs, 101),
       ''.join('<span><b>%s</b> ×%d</span>' % (html.escape(a), b) for a, b in repeat),
       row(uniq[:half]), row(uniq[:half]), row(uniq[half:]), row(uniq[half:]), ''.join(cards))
