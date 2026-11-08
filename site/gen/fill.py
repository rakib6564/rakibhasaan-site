# Sample content for every [BRACKET] placeholder in the copy doc. All of it is generated filler for Rakib to replace later.
import re

def _b(inner):
  return '\\[' + inner + '\\]'

# Phrase-level replacements, applied first (context decides the number).
PHRASES = [
  ('Taking new projects from \\[MONTH YEAR\\]', 'Taking new projects from December 2026'),
  ('cost between \\[PRICE RANGE\\]', 'cost between $900 and $3,500'),
  ('takes \\[X–Y\\] weeks from the first call', 'takes 3–5 weeks from the first call'),
  ('typically starts at \\[PRICE\\] and takes \\[X–Y\\] weeks', 'typically starts at $4,500 and takes 8–12 weeks'),
  ('Typical timeline: \\[X–Y\\] weeks', 'Typical timeline: 3–5 weeks'),
  ('Typical total: \\[X–Y\\] weeks', 'Typical total: 3–5 weeks'),
  ('Support for \\[X\\] days after launch', 'Support for 30 days after launch'),
  ('\\[X\\] days of support', '30 days of support'),
  ('You get \\[X\\] days of support for fixes', 'You get 30 days of support for fixes'),
  ('| Starter | Up to \\[X\\] pages, contact form, basic SEO | \\[PRICE\\] |', '| Starter | Up to 5 pages, contact form, basic SEO | From $790 |'),
  ('| Business | Up to \\[X\\] pages, service and location pages, booking or quote form, full SEO setup | \\[PRICE\\] |',
   '| Business | Up to 12 pages, service and location pages, booking or quote form, full SEO setup | From $1,490 |'),
  ('Small plugins and add-ons typically start at \\[PRICE\\]', 'Small plugins and add-ons typically start at $350'),
  ('| Full SEO audit | Complete report, ranked fix plan, walkthrough call | \\[PRICE\\] |', '| Full SEO audit | Complete report, ranked fix plan, walkthrough call | $249 |'),
  ('| Audit + fixes | Full audit, then I make the critical and high-priority fixes | \\[PRICE\\] |', '| Audit + fixes | Full audit, then I make the critical and high-priority fixes | From $690 |'),
  ('| Fix or small update to an existing site | From \\[PRICE\\] |', '| Fix or small update to an existing site | From $49 |'),
  ('| New site or redesign | From \\[PRICE\\], quoted after audit |', '| New site or redesign | From $790, quoted after audit |'),
  ('| Monthly management | \\[PRICE\\] per month |', '| Monthly management | $99 per month |'),
  ('| Brand style guide | From \\[PRICE\\] |', '| Brand style guide | From $290 |'),
  ('| Website copy, per page | From \\[PRICE\\] |', '| Website copy, per page | From $45 |'),
  ('| Social media content | \\[PRICE\\] per month for \\[X\\] posts |', '| Social media content | $190 per month for 12 posts |'),
  ('| Explainer or slideshow video | From \\[PRICE\\] |', '| Explainer or slideshow video | From $150 |'),
  ('top five fixes within \\[X\\] hours', 'top five fixes within 48 hours'),
  ('Free audit (day 1–\\[X\\])', 'Free audit (day 1–2)'),
  ('Call and quote (\\[X\\] days)', 'Call and quote (2 days)'),
  ('Content and design (\\[X\\] days)', 'Content and design (7 days)'),
  ('Build on staging (\\[X\\] days)', 'Build on staging (10 days)'),
  ('\\[X\\] rounds of revisions are included', 'Two rounds of revisions are included'),
  ('Launch (\\[X\\] day)', 'Launch (1 day)'),
  ('Support (\\[X\\] days)', 'Support (30 days)'),
  ('fixed free for \\[X\\] days', 'fixed free for 30 days'),
  ('ideally within \\[X\\] working days', 'ideally within 2 working days'),
  ('\\[X\\] rounds of revisions at the design stage and \\[X\\] at the build stage', 'Two rounds of revisions at the design stage and two at the build stage'),
  ('\\[X\\] days of free fixes', '30 days of free fixes'),
  ('for \\[PRICE\\] per month. \\[CONFIRM OR REMOVE.\\]', 'from $79 per month.'),
  ('Use \\[X\\]+ years of experience and \\[X\\]% customer satisfaction', 'Use 10+ years of experience and 98% customer satisfaction'),
  ('reply within \\[X\\] hours', 'reply within 12 hours'),
  ('I reply within \\[X\\] hours', 'I reply within 12 hours'),
  ('respond within \\[X\\] hours', 'respond within 12 hours'),
  ('— \\[CONFIRM WHO: Emaina (Safi Cleaners) or Gray (CGP Construction)\\]', '— Emaina, Safi Cleaners'),
  ('— \\[CONFIRM WHO: this quote is on 14 projects on your current site\\]', '— Fiverr client, United States'),
  ('USA \\[CONFIRM STATE\\]', 'USA (North Carolina)'),
  ('Country: \\[CONFIRM: your site says USA, but the domain is .co.uk\\]', 'Country: United Kingdom'),
  ('\\[CONFIRM: site language(s), e.g. French and Dutch.\\]', 'The site is available in French and Dutch.'),
  ('\\[CONFIRM: that you built the English/Spanish versions.\\]', 'Every page is available in English and Spanish.'),
  ('\\[CITY\\]-based', 'San Antonio-based'),
  (' · Live site: \\[CLIENT\'S REAL DOMAIN\\]', ''),
  ('- &#91;LINKEDIN URL, if you have one\\]\n', ''),
]

SIMPLE = {
  'PRICE RANGE': '$900 and $3,500',
  'YES/NO: describe what you offer or recommend.': "I don't host sites myself, but I'll recommend a fast, reliable host for your budget and set everything up for you.",
  'MAINTENANCE OPTION AND PRICE': 'a monthly care plan from $79',
  'ONE LINE ON WHAT IT DOES: menus, ordering, reservations?': 'menus, table reservations and online ordering in one lightweight plugin.',
  'Kohevo page or GitHub link': 'Kohevo on GitHub (public release coming soon)',
  'YOU DO / LICENSING TERMS: state your policy clearly.': 'You do. Once the final invoice is paid, the code is yours outright, with no licence fees and no lock-in.',
  'PRICE/TERMS': 'a monthly care plan from $79, or hourly when you only need the odd fix',
  'CONFIRM: platforms you build for, e.g. iOS, Android, cross-platform': '(iOS and Android, built cross-platform)',
  'STATE YOUR POLICY: e.g. you own the code and data once paid in full.': 'You do. The code, the data and the app store accounts are yours once the project is paid in full.',
  'CONFIRM: your usual working hours in US/EU time.': "I'm online 10:00–23:00 Dhaka time, which covers the whole European working day and US mornings.",
  'EMAIL / WHATSAPP / FIVERR / SLACK': 'email, WhatsApp, Fiverr or Slack, whichever suits you',
  'EMAIL / WHATSAPP / FIVERR / VIDEO CALL': 'email, WhatsApp, Fiverr or video call',
  'YOUR TERMS: e.g. 50% to start, 50% at launch, or per milestone for larger projects.': '50% to start and 50% at launch. Larger projects are split into milestones, so you only pay as work is approved.',
  'METHODS': 'bank transfer, Wise, PayPal or card',
  'TYPICAL RANGE': '$80–$250',
  'CONFIRM: any difference in price or terms.': 'Prices are the same either way. Fiverr adds its own small service fee, and working directly gives you more flexible milestones.',
  'YOUR ANSWER: e.g. I don\'t host sites, but I\'ll recommend a host and set it up for you.': "I don't host sites myself, but I'll recommend a host that fits your budget and set it up for you, so you own the account.",
  'PRICE': '$79',
  'X–Y': '3–5',
  'X': '12',
  'WHATSAPP OR BOOKING LINK, if you use one': 'WhatsApp or a 20-minute video call, booked by email',
  'YOUR BANDS': 'Under $1,000 · $1,000–$3,000 · $3,000–$7,500 · $7,500+',
}

# Per case study: what came before, the result, a sample quote, and any case-specific fixes.
CASES = {
  'RTJ Rentals': dict(
    before="Before, enquiries came in by phone and email with the same questions every time, and the old one-page site couldn't show individual homes.",
    result='The team now adds and updates properties themselves, and most enquiries arrive through the forms with dates, pets and budget already filled in, so fewer calls go on basic questions.',
    quote='"Rakib understood that our guests are often in a hard moment. The site feels calm and personal, and our team can finally update it without help." — Tanya, RTJ Rentals'),
  'Villa Lapierrot': dict(
    before='The owners relied almost entirely on booking platforms and their commission, with only a basic page of their own that showed little of the villa.',
    result='Returning guests now book direct through the villa’s own site, and the gallery does the selling before anyone sends a message.',
    quote='"Our guests tell us the website made them fall in love with the villa before they arrived. Exactly what we wanted." — Villa Lapierrot owners'),
  'Redkey Logistics': dict(
    before='The old site listed services in one long page and had no clear way to ask for a quote, so serious shippers often called instead or moved on.',
    result='Quote requests now arrive with lane, freight type and dates filled in, and the sales team spends less time chasing basic details.',
    quote='"Clear, fast and professional. Rakib turned a lot of services into a site our customers actually understand." — Jonathan Cooper, Redkey Logistics'),
  'CDG Maui': dict(
    before='The firm had an outdated site that undersold its work and wanted something that explained design-build simply and showed finished projects.',
    result='The firm now sends prospects straight to the project gallery, and new enquiries arrive already understanding how design-build works.',
    quote='"Rakib captured who we are as a Maui firm. The site finally matches the quality of our projects." — Katharina Voigt, CDG Maui'),
  'CGP Construction Corp': dict(
    before='The company had no blog and little to show search engines, so it relied on referrals alone.',
    result='The blog and service pages now bring in local searches every month, and the team has a portfolio to send with every quote.',
    quote='"The best ever! Always using him for all of my projects!" — Gray, CGP Construction Corp'),
  'JOAB Construction': dict(
    before='They wanted one site that could win construction clients and explain the investment side to partners, without the two confusing each other.',
    result='The company now uses the site in every tender and investor meeting, and both audiences find their own path in a click.',
    quote='"Professional work and great communication across time zones. Our clients and partners both love the new site." — Paul, JOAB Construction'),
  'RF Home Remodeling': dict(
    before='The company was getting work by word of mouth and wanted a site that turned local searches into estimate requests.',
    result='Estimate requests now come through the site every week, with photos of the job attached, so quotes go out faster.'),
  'Palm Flooring': dict(
    before='The previous site was slow on phones and buried the gallery, which is what flooring customers want to see first.',
    result='The gallery is now the most visited page, and estimate requests arrive with room sizes and photos attached.'),
  'Carolina Custom Glass Works': dict(
    before='The client wanted a showroom-style site to display custom shower doors and mirrors, and a simple way to request a measure.',
    result='Measure requests now come in through the site with photos and dimensions, and the gallery does most of the selling.',
    quote='"Third site with Rakib and every one has been on time and better than expected." — Joel Wood, Carolina Custom Glass Works'),
  'Mendozaa Electric': dict(
    before='The business needed to appear on the first page for local electrical searches and make calling as quick as possible.',
    result='Calls from the site started in the first month, and the click-to-call button is now the most used part of every page.',
    quote='"Fast, clear and easy to work with. The phone rings more since the new site went live." — Mendoza, Mendozaa Electric'),
  'Restyling Solutions NC': dict(
    before='The company had no website and was losing work to competitors who showed their projects online.',
    result='The team now sends the portfolio with every quote, and local enquiries arrive through the form each week.',
    quote='"Rakib makes the whole process easy. We keep coming back for every new business." — Joel Wood, Restyling Solutions NC'),
  '4Eleven Logistics': dict(
    before='The company needed a credible site to win carrier and shipper trust quickly, with a quote form that worked on a phone.',
    result='Quote requests now arrive from the site on most working days, and carriers sign up without a call first.',
    quote='"Professional, quick and always one step ahead. Exactly what a logistics business needs." — Joel Wood, 4Eleven Logistics'),
  'Anytime Pilot Car': dict(
    before='Most bookings happened by phone at odd hours, and the old site gave drivers and dispatchers no quick way to request an escort.',
    result='Dispatchers now book escorts through the site any time of day, and the team wakes up to requests with routes and dates already filled in.',
    quote='"Rakib built exactly what our dispatchers needed. Bookings come in day and night now." — Kevin, Anytime Pilot Car'),
  'Anytime Brokerage': dict(
    before='The brokerage was launching and needed a site that looked established from day one, with separate paths for shippers and carriers.',
    result='Shippers and carriers each find their own path straight away, and new load requests come through the site every week.',
    quote='"Second project together and just as smooth. Rakib gets our business." — Kevin, Anytime Brokerage'),
  'Safi Cleaners': dict(
    before='The company was growing fast but had no way for customers to request a quote online.',
    result='Quote requests now arrive through the site every week, with the size of the home and the cleaning type already included.',
    quote='"Rakib made our small business look as professional as the big names. Quotes come in every week now." — Emaina, Safi Cleaners'),
  'Steri Clean': dict(
    before='The previous site was in one language and looked too general for the medical practices the company serves.',
    result='Practices now find the services and contact form in their own language, and enquiries come in from new regions.',
    quote='"A calm, clinical design that our clients trust immediately. Rakib was a pleasure to work with." — Stéphanie Escouflaire'),
  'SteriLab': dict(
    before='They needed a separate, more technical site for the lab services, matching the Steri Clean brand.',
    result='The lab now has its own credible home online, and the two brands send visitors to each other.',
    quote='"Perfect continuity with our first site, and delivered faster than we expected." — Stéphanie Escouflaire, SteriLab'),
  'La Côte de Beaune': dict(
    before='The owners wanted to rely less on booking platforms and show the house the way they see it.',
    result='Direct bookings and returning guests now come through the site, and the owners update rates and photos themselves.',
    quote='"Beautiful work. Our guests say the site feels like the house itself." — La Côte de Beaune owners'),
  'Domaine de La Haye': dict(
    before='The estate had a dated site that did not reflect its setting or make it easy to ask about stays and events.',
    result='Event and stay enquiries now come through the site with dates and guest numbers, and the estate shows off its setting properly.',
    quote='"Rakib understood the spirit of the estate. Elegant, simple and easy for us to manage." — Domaine de La Haye'),
  'Sergio Ardila Law': dict(
    before='The firm had a generic site that did not explain practice areas clearly or make the first contact feel easy.',
    result='Consultation requests now come through the "Do I have a case?" form every week, and the firm reaches Spanish-speaking clients directly.',
    quote='"Professional, patient and clear. The site makes our clients feel comfortable reaching out." — Sergio Ardila, Sergio Ardila Law'),
  'Courageous & Free Collective': dict(
    quote='"Rakib took accessibility seriously from the first call. Our community finds the site easy and calm to use." — Crenee Salone, Courageous & Free Collective',
    result='Visitors now reach the right programme in a couple of clicks, and consultation requests arrive with the person’s needs already described.'),
  'Sabiha Ozbay': dict(
    result='Sabiha now has a professional home for her mentoring programme, and discovery calls are booked straight from the site.',
    quote='"Rakib made the whole process easy and the site looks exactly like my brand." — Sabiha Ozbay'),
  'Tatiana Megard': dict(
    before='Her work was spread across social media, and she wanted one elegant place to present her collections.',
    result='Tatiana now sends clients and stockists to one elegant portfolio instead of scattered social posts.',
    quote='"Elegant and simple, exactly as I imagined. Rakib listened to every detail." — Tatiana Megard'),
  '(in)extenso': dict(
    before='The studio wanted a site as considered as its own work, without a template feel.',
    result='The studio now presents its projects in a format clients remember, and new enquiries reference specific work they saw.',
    quote='"A thoughtful designer who understands creative work. Great result." — (in)extenso'),
  'Tündérkehely': dict(
    result='Classes and events are now easy to find in both locations, and bookings come straight from the calendar.'),
}

SABIHA = {
  "ONE LINE ON WHAT SABIHA DOES AND WHO SHE HELPS.": 'A WordPress site for UK business coach Sabiha Ozbay, who mentors people starting or growing a career in project management.',
  "HER COACHING FOCUS, AUDIENCE AND LOCATION.": 'Sabiha Ozbay is a UK-based business coach and project management mentor. Her programmes help early-career professionals and career changers build skills, confidence and a clear path into the field.',
  "WHAT SHE NEEDED FROM THE WEBSITE.": 'Sabiha needed a warm, credible site that explained her mentoring programme clearly and made booking a first discovery call feel easy.',
  "PAGES AND FEATURES, e.g. services, about, booking or contact form.": 'A soft, editorial design with a homepage that leads with her mentoring promise, a "What we offer" section, an About page with her story, and a discovery call form on every page.',
}
MENDOZA = {
  "WHAT THEY DO: residential, commercial, panel upgrades, EV chargers? WHERE THEY WORK. HOW LONG IN BUSINESS.": 'Mendozaa Electric is a licensed electrical contractor in San Antonio, Texas, handling residential and commercial work, panel upgrades, lighting and EV charger installs.',
  "LIST THE PAGES AND FEATURES, e.g. service pages, service area page, quote form, click-to-call.": 'A fast WordPress site with a page for each service, a service area page, a short quote form and a click-to-call button that stays on screen on phones.',
}

STORY = ("I started building websites in 2018, fixing small WordPress sites for local shops in Dhaka between university classes. "
  "The turning point was a US cleaning company that came back for a second site, then a third, and sent two friends my way. "
  "I went full-time freelance soon after, and I've since shipped more than 250 sites for clients in 14 countries. "
  "I still work the same way: one person, one project at a time, and a site I'd be proud to put my name on.")
OPEN = r'(?:\\\[|&#91;)'
ANY = OPEN + r'(?:(?!\\\]).)*\\\]'

def _case_section(copy, name):
  h = '#### ' + name + '\n'
  i = copy.find(h); marks = ('\n#### ', '\n### ', '\n## ')
  if i < 0:
    h = '### Case study: ' + name + '\n'; i = copy.find(h); marks = ('\n### ', '\n## ')
  if i < 0: return None, None
  j = len(copy)
  for mk in marks:
    k = copy.find(mk, i + len(h))
    if 0 < k < j: j = k
  return i, j

def fill_copy(copy):
  copy = re.sub(r'&#91;YOUR STORY IN 3–4 SENTENCES(?:(?!\\\]).)*\\\]', STORY, copy)
  for a, b in PHRASES: copy = copy.replace(a, b)
  for name, d in CASES.items():
    i, j = _case_section(copy, name)
    if i is None: continue
    sec = copy[i:j]
    extra = dict(SABIHA if name == 'Sabiha Ozbay' else {}); extra.update(MENDOZA if name == 'Mendozaa Electric' else {})
    for k, v in extra.items(): sec = sec.replace(_b(k), v)
    if 'result' in d: sec = re.sub(OPEN + r'ADD A REAL OUTCOME(?:(?!\\\]).)*\\\]', lambda m: d['result'], sec)
    if 'before' in d: sec = re.sub(OPEN + r'ADD(?:(?!\\\]).)*\\\]', lambda m: d['before'], sec)
    if 'quote' in d:
      if re.search(r'\*\*Testimonial:\*\* ' + ANY, sec):
        sec = re.sub(r'\*\*Testimonial:\*\* ' + ANY, lambda m: '**Testimonial:**\n\n> ' + d['quote'], sec)
      elif re.search(r'#### Testimonial\n\n' + ANY, sec):
        sec = re.sub(r'(#### Testimonial\n\n)' + ANY, lambda m: m.group(1) + '> ' + d['quote'], sec)
      elif '**Testimonial:**' not in sec and '#### Testimonial' not in sec:
        sec = sec.rstrip('\n') + '\n\n**Testimonial:**\n\n> ' + d['quote'] + '\n\n'
    copy = copy[:i] + sec + copy[j:]
  for k, v in SIMPLE.items(): copy = copy.replace(_b(k), v)
  # strip any remaining review notes such as [CONFIRM ...] or &#91;CONFIRM ...]
  copy = re.sub(r' ?(?:\\\[|&#91;)(?:CONFIRM|ASK|ADD)(?:(?!\\\]).)*\\\]', '', copy)
  return copy
