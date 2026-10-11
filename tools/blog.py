"""Blog: zoznam článkov a šablóna článku. Text článku je v tools/blog/<slug>.html.
Generuje ho tools/build_pages.py (blog/index.html aj blog/<slug>/index.html)."""
import os, re, html

BLOG_DIR = os.path.join(os.path.dirname(__file__), 'blog')
SITE = 'https://martinjuriga.sk'
MONTHS = ['januára', 'februára', 'marca', 'apríla', 'mája', 'júna', 'júla', 'augusta', 'septembra', 'októbra', 'novembra', 'decembra']

ARTICLES = [  # najnovší hore
    dict(slug='koniec-fixacie-hypoteky',
         title='Koniec fixácie hypotéky: čo robiť krok za krokom | Martin Juriga',
         h1='Končí vám fixácia hypotéky? Čo robiť krok za krokom',
         card='Kedy začať, čo ponúkne vaša banka, ako porovnať ponuky a kedy sa oplatí refinancovanie alebo mimoriadna splátka.',
         desc='Končí vám fixácia hypotéky? Kedy to začať riešiť, aké máte možnosti, ako porovnať ponuky bánk, akú fixáciu zvoliť a kedy splatiť časť úveru bez poplatku.',
         tag='Hypotéky', tema='Hypotéka', date='2026-10-11', minutes=7,
         lead='Fixácia je obdobie, počas ktorého sa úrok na vašej hypotéke nemení. Keď skončí, banka vám pošle novú sadzbu a väčšina ľudí ju jednoducho nechá tak. Pritom je to najvýhodnejší moment, kedy sa dá s hypotékou niečo urobiť, a to bez sankcií.',
         summary=['Riešte to 2 až 3 mesiace pred koncom fixácie, nie až po liste z banky.',
                  'Máte 4 možnosti: prijať ponuku, vyjednať lepšiu, refinancovať alebo úver skrátiť.',
                  'Ku koncu fixácie môžete splatiť časť úveru bez poplatku za predčasné splatenie.'],
         visual=('hourglass', 'coins', 'Koniec fixácie', ('3 % → 4 %', '+54 € mesačne pri 100 000 €')),
         related=[('/refinancovanie/', 'Refinancovanie hypotéky'), ('/skratenie-uveru/', 'Skrátenie úveru'), ('/hypoteky-a-uvery/', 'Hypotéky a úvery')]),
]

def nice_date(d):
    y, m, dd = d.split('-')
    return f'{int(dd)}. {MONTHS[int(m) - 1]} {y}'

def crumbs(items):
    lis = ''.join(f'<li><a href="{u}">{n}</a></li>' if u else f'<li aria-current="page">{n}</li>' for n, u in items)
    return f'<ol class="crumbs reveal">{lis}</ol>'

def faq_of(body):
    items = re.findall(r'<summary>(.*?)<span class="faq__icon"></span></summary>\s*<p>(.*?)</p>', body, re.S)
    return [(html.unescape(q), html.unescape(re.sub('<[^>]+>', '', a))) for q, a in items]

def glass(name, cls):
    g = open(os.path.join(os.path.dirname(__file__), 'glass', name + '.svg')).read()
    g = g.replace('class="glass svc-stage__pct"', 'class="glass"')
    return g.replace('<svg class="glass"', f'<svg class="glass {cls}"', 1)

def article_body(a):
    text = open(os.path.join(BLOG_DIR, a['slug'] + '.html')).read()
    toc = ''.join(f'<li><a href="#{i}">{html.unescape(re.sub("<[^>]+>", "", t))}</a></li>' for i, t in re.findall(r'<h2 id="([\w-]+)">(.*?)</h2>', text))
    summ = ''.join(f'<li>{x}</li>' for x in a['summary'])
    rel = ''.join(f'<li><a href="{u}">{n} <span aria-hidden="true">→</span></a></li>' for u, n in a['related'])
    big, small, label, (stat, stat_s) = a['visual']
    defs = open(os.path.join(os.path.dirname(__file__), 'partials', 'glass-defs.html')).read()
    return f'''    <!-- ============ ČLÁNOK ============ -->
    <article class="post">
{defs}
      <header class="post-hero">
        <div class="hero__bg" aria-hidden="true"></div>
        <div class="container post-hero__grid">
          <div class="post-hero__copy">
            {crumbs([('Domov', '/'), ('Články', '/blog/'), (a['tag'], None)])}
            <h1 class="reveal"><span class="pill h1-kicker"><span class="pill__dot"></span>{a['tag']} · Orava a Žilina</span> {a['h1']}</h1>
            <p class="post__lead reveal">{a['lead']}</p>
            <div class="post__meta reveal">
              <img src="/img/martin-tvar.webp" width="400" height="400" alt="Martin Juriga" />
              <span><strong>Martin Juriga</strong><small>Aktualizované <time datetime="{a['date']}">{nice_date(a['date'])}</time> · {a['minutes']} min čítania</small></span>
            </div>
          </div>
          <div class="post-visual reveal" aria-hidden="true">
            <div class="post-visual__glow"></div>
            {glass(big, 'post-visual__big')}
            {glass(small, 'post-visual__small')}
            <div class="post-visual__stat"><strong>{stat}</strong><span>{stat_s}</span></div>
            <span class="post-visual__label">{label}</span>
          </div>
        </div>
      </header>

      <div class="container post-layout">
        <aside class="post-side">
          <nav class="post-toc" aria-label="Obsah článku">
            <p>Obsah článku</p>
            <ol>{toc}</ol>
          </nav>
          <div class="post-help">
            <p class="post-help__h">Končí vám fixácia?</p>
            <p>Pošlite mi list od banky, porovnám ho s ponukami ďalších bánk.</p>
            <a href="tel:+421915448705" class="post-help__tel">+421 915 448 705</a>
            <a href="#kontakt" class="btn btn--primary btn--sm">Napísať správu <span aria-hidden="true">→</span></a>
          </div>
        </aside>

        <div class="post__body">
          <div class="post__summary">
            <p>V skratke</p>
            <ul>{summ}</ul>
          </div>
{text}
          <aside class="post__author">
            <img src="/img/martin-tvar.webp" width="400" height="400" loading="lazy" alt="Martin Juriga" />
            <div>
              <p class="post__author-h">Martin Juriga</p>
              <p>Podriadený finančný agent v spolupráci s MeruCompany, s.r.o., registrovaný v NBS pod č. 277707. Pomáham ľuďom z Oravy, Žiliny a celého Slovenska s hypotékami, poistením a investovaním.</p>
            </div>
          </aside>
          <nav class="post__related" aria-label="Súvisiace služby">
            <p>Súvisiace služby</p>
            <ul>{rel}</ul>
          </nav>
          <p class="post__note">Článok má informatívny charakter a nie je ponukou ani odporúčaním. Konkrétne podmienky úveru určuje banka po posúdení vašej žiadosti.</p>
        </div>
      </div>
    </article>
'''

def article_ld(a, body):
    url = f'{SITE}/blog/{a["slug"]}/'
    return [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a['h1'], "description": a['desc'],
         "url": url, "mainEntityOfPage": url, "datePublished": a['date'], "dateModified": a['date'], "inLanguage": "sk",
         "image": [f"{SITE}/img/og.jpg", f"{SITE}/img/martin-juriga.jpg"],
         "author": {"@type": "Person", "name": "Martin Juriga", "url": f"{SITE}/", "jobTitle": "Podriadený finančný agent"},
         "publisher": {"@type": "Organization", "name": "Martin Juriga – finančné plánovanie", "logo": {"@type": "ImageObject", "url": f"{SITE}/img/favicon-192.png"}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Domov", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Články", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": a['h1'], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in faq_of(body)]},
    ]

def index_body():
    cards = ''.join(f'''
          <a class="post-card reveal" href="/blog/{a['slug']}/">
            <span class="post-card__visual" aria-hidden="true">{glass(a['visual'][0], 'post-card__ic')}<span>{a['visual'][2]}</span></span>
            <span class="post-card__tag">{a['tag']}</span>
            <h2>{a['h1']}</h2>
            <p>{a['card']}</p>
            <span class="post-card__meta"><time datetime="{a['date']}">{nice_date(a['date'])}</time> · {a['minutes']} min čítania</span>
            <span class="post-card__more">Čítať článok <span aria-hidden="true">→</span></span>
          </a>''' for a in ARTICLES)
    defs = open(os.path.join(os.path.dirname(__file__), 'partials', 'glass-defs.html')).read()
    return f'''    <!-- ============ ČLÁNKY ============ -->
{defs}
    <section class="post-hero post-hero--index">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="container">
        {crumbs([('Domov', '/'), ('Články', None)])}
        <h1 class="reveal"><span class="pill h1-kicker"><span class="pill__dot"></span>Články o financiách · Orava a Žilina</span> Financie po ľudsky.</h1>
        <p class="post__lead reveal">Praktické rady k hypotékam, poisteniu, investovaniu a dôchodku. Píšem ich pre ľudí z Oravy, Žiliny a celého Slovenska, ktorí chcú svojim financiám rozumieť.</p>
      </div>
    </section>
    <section class="section section--tight">
      <div class="container">
        <div class="post-grid">{cards}
        </div>
      </div>
    </section>
'''

def index_ld():
    return [
        {"@context": "https://schema.org", "@type": "Blog", "name": "Články o financiách – Martin Juriga", "url": f"{SITE}/blog/", "inLanguage": "sk",
         "blogPost": [{"@type": "BlogPosting", "headline": a['h1'], "url": f"{SITE}/blog/{a['slug']}/", "datePublished": a['date']} for a in ARTICLES]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Domov", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Články", "item": f"{SITE}/blog/"}]},
    ]
