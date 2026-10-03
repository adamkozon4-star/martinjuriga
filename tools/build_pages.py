"""Generátor podstránok služieb.

Spúšťa sa z koreňa repozitára:  python3 tools/build_pages.py
Obsah každej podstránky je v tools/pages/<slug>.html (iba <main> bez kontaktu),
title a popis sú v slovníku PAGES nižšie. Hlavička, kontakt a pätička sa berú z index.html,
takže po ich zmene na úvodnej stránke stačí skript spustiť znova.
"""
import re, sys, json, html, os
sys.path.insert(0, os.path.dirname(__file__))
from services import nav, footer_services, SERVICES, has_page, PAGES_DIR

PAGES = {
  'hypoteky-a-uvery': dict(
    title='Hypotéka Orava – Dolný Kubín, Námestovo, Tvrdošín, Žilina | Martin Juriga',
    desc='Hypotéky a úvery na Orave a v Žiline. Porovnám ponuky viacerých bánk, pomôžem s dokladmi a prevediem vás procesom až po podpis. Prvé stretnutie zdarma.',
    tema='Hypotéka'),
  'refinancovanie': dict(
    title='Refinancovanie hypotéky Orava – Dolný Kubín, Námestovo, Žilina | Martin Juriga',
    desc='Končí vám fixácia? Porovnám ponuky viacerých bánk a ak sa prechod oplatí, vybavím refinancovanie hypotéky či úveru za vás. Orava, Žilina aj online.',
    tema='Hypotéka'),
  'investovanie': dict(
    title='Investovanie Orava – Dolný Kubín, Námestovo, Tvrdošín, Žilina | Martin Juriga',
    desc='Pravidelné aj jednorazové investovanie nastavené podľa vašich cieľov. Vysvetlím, ako investovanie funguje, porovnáme možnosti a nastavíme plán. Orava, Žilina aj online.',
    tema='Investície'),
}

idx = open('index.html').read()

def cut(start, end):
    i = idx.index(start); j = idx.index(end, i) + len(end); return idx[i:j]

def to_sub(fragment):
    f = fragment.replace('src="img/', 'src="/img/').replace('href="ochrana-osobnych-udajov.html"', 'href="/ochrana-osobnych-udajov.html"')
    # kotvy na úvodnú stránku, okrem tých, ktoré sú aj na podstránke
    return re.sub(r'href="#(?!kontakt"|top")([\w-]+)"', r'href="/#\1"', f)

def page(slug, title, desc, h_name, body, tema, faq, og_image):
    url = f'https://martinjuriga.sk/{slug}/'
    header = cut('  <!-- ============ HEADER', '</header>')
    header = re.sub(r'      <nav class="nav".*?</nav>', lambda m: nav(False, slug), header, flags=re.S)
    header = header.replace('<a href="#top" class="logo"', '<a href="/" class="logo"')
    header = to_sub(header)
    contact = to_sub(cut('    <!-- ============ KONTAKT', '</section>'))
    contact = contact.replace('value="Finančný plán" checked', 'value="Finančný plán"').replace(f'value="{tema}" />', f'value="{tema}" checked />')
    foot = cut('  <!-- ============ FOOTER', '</html>')
    foot = re.sub(r'(<h4>Služby</h4>\n).*?(\s*</nav>)', lambda m: m.group(1)+footer_services(False)+m.group(2), foot, count=1, flags=re.S)
    foot = to_sub(foot).replace('<a href="#top" class="logo">', '<a href="/" class="logo">').replace('src="main.js"', 'src="/main.js"')
    ld = [
      {"@context": "https://schema.org", "@type": "Service", "name": h_name, "serviceType": h_name, "url": url,
       "description": desc,
       "provider": {"@type": "FinancialService", "name": "Martin Juriga – finančné plánovanie", "url": "https://martinjuriga.sk/", "telephone": "+421915448705",
                    "address": {"@type": "PostalAddress", "streetAddress": "Medzibrodie nad Oravou 136", "postalCode": "026 01", "addressLocality": "Dolný Kubín", "addressCountry": "SK"}},
       "areaServed": ["Dolný Kubín", "Námestovo", "Tvrdošín", "Trstená", "Žilina", "Slovensko"]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Domov", "item": "https://martinjuriga.sk/"},
        {"@type": "ListItem", "position": 2, "name": h_name, "item": url}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    ld_html = '\n'.join(f'  <script type="application/ld+json">\n  {json.dumps(x, ensure_ascii=False)}\n  </script>' for x in ld)
    return f'''<!doctype html>
<html lang="sk">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#f3f6fd" />
  <link rel="icon" href="/img/favicon.png" type="image/png" />
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="https://martinjuriga.sk/img/{og_image}" />
  <meta property="og:locale" content="sk_SK" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lexend:wght@500;600&family=Caveat:wght@500;600&family=Mrs+Saint+Delafield&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/style.css" />

{ld_html}
</head>
<body id="top">

{header}

  <main>
{body}
{contact}
  </main>

{foot}
'''

def faq_from(body):
    items = re.findall(r'<summary>(.*?)<span class="faq__icon"></span></summary>\s*<p>(.*?)</p>', body, re.S)
    return [(html.unescape(q), html.unescape(re.sub('<[^>]+>', '', a))) for q, a in items]

def partial(name):
    return open(os.path.join(PAGES_DIR, '..', 'partials', name + '.html')).read()

def update_index():
    global idx
    s = re.sub(r'      <nav class="nav" aria-label="Hlavná navigácia">.*?</nav>', lambda m: nav(True), idx, count=1, flags=re.S)
    s = re.sub(r'(<nav class="footer__col" aria-label="Služby">\s*<h4>Služby</h4>\n).*?(\s*</nav>)', lambda m: m.group(1)+footer_services(True)+m.group(2), s, count=1, flags=re.S)
    # bloky <!-- @partial:x --> … <!-- /@partial:x --> na úvodnej stránke
    s = re.sub(r'<!-- @partial:([\w-]+) -->\n.*?<!-- /@partial:\1 -->\n',
               lambda m: f'<!-- @partial:{m.group(1)} -->\n' + partial(m.group(1)) + f'<!-- /@partial:{m.group(1)} -->\n', s, flags=re.S)
    open('index.html', 'w').write(s)
    idx = s

def update_sitemap(slugs):
    urls = ['  <url><loc>https://martinjuriga.sk/</loc><priority>1.0</priority></url>']
    urls += [f'  <url><loc>https://martinjuriga.sk/{s}/</loc><priority>0.8</priority></url>' for s in slugs]
    urls += ['  <url><loc>https://martinjuriga.sk/ochrana-osobnych-udajov.html</loc><priority>0.2</priority></url>']
    open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')

if __name__ == '__main__':
    update_index()
    names = {s: n for s, n, _, _ in SERVICES}
    built = []
    for slug, _, _, _ in SERVICES:
        if not has_page(slug):
            continue
        meta = PAGES[slug]
        body = open(os.path.join(PAGES_DIR, slug + '.html')).read()
        body = re.sub(r'<!-- @partial:([\w-]+) -->\n', lambda m: partial(m.group(1)), body)
        out = page(slug, meta['title'], meta['desc'], names[slug], body, meta['tema'], faq_from(body), meta.get('og', 'og.jpg'))
        os.makedirs(slug, exist_ok=True)
        open(os.path.join(slug, 'index.html'), 'w').write(out)
        built.append(slug)
    update_sitemap(built)
    print('postavené:', ', '.join(built))
