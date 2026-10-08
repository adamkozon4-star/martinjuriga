"""Obsah podstránok služieb v jednotnej šablóne (3D úvod, sklenené karty, cesta, zásady, mapa, otázky).

Vygeneruje tools/pages/<slug>.html pre stránky v CONTENT. Potom treba spustiť build:
    python3 tools/service_pages.py && python3 tools/build_pages.py
Hypotéky a investovanie sú písané ručne priamo v tools/pages/.
"""
import os

GLASS_DIR = os.path.join(os.path.dirname(__file__), 'glass')
CHECK = '<li><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
SCRIBBLE = ('<svg class="scribble__line" viewBox="0 0 300 24" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="M4 17C58 7 132 5 196 11c38 4 70 7 100-3"/><path d="M40 21c60-6 130-8 210-4"/></svg>')
TOWNS = 'Pre klientov z Dolného Kubína, Námestova, Tvrdošína, Trstenej, Žiliny, Bratislavy a osobne aj online z celého Slovenska.'


def glass(name, cls=None):
    s = open(os.path.join(GLASS_DIR, name + '.svg')).read()
    s = s.replace('class="glass svc-stage__pct"', 'class="glass"')
    return s.replace('<svg class="glass"', f'<svg class="glass {cls}"', 1) if cls else s


def h1(text):
    # slovo v [hranatých zátvorkách] dostane ručne kreslené podčiarknutie
    a, rest = text.split('[', 1)
    word, b = rest.split(']', 1)
    return f'{a}<span class="scribble">{word}{SCRIBBLE}</span>{b}'


def lis(items, indent=14):
    pad = ' ' * indent
    return '\n'.join(f'{pad}<li>{i}</li>' for i in items)


def render(c):
    cards = ''.join(f'''          <article class="svc-card reveal">
            <div class="svc-card__media">{glass(ic)}</div>
            <h3>{h}</h3>
            <p>{p}</p>{f'{chr(10)}            <a href="{link[0]}" class="svc-card__link">{link[1]} <span aria-hidden="true">→</span></a>' if link else ''}
          </article>
''' for ic, h, p, *rest in c['cards'] for link in [rest[0] if rest else None])
    cta_h, cta_p, cta_btn, cta_href = c.get('cta', ('Neviete, kde začať?', 'Na prvom stretnutí prejdeme vašu situáciu a poviem vám, aké máte možnosti. Zadarmo a bez záväzkov.', 'Dohodnúť stretnutie', '#kontakt'))
    steps = ''.join(f'''          <li class="step reveal">
            <span class="step__num">0{i + 1}</span>
            <h3>{h}</h3>
            <p>{p}</p>
          </li>
''' for i, (h, p) in enumerate(c['steps']))
    faq = ''.join(f'''          <details class="faq__item reveal"{" open" if i == 0 else ""}>
            <summary>{q}<span class="faq__icon"></span></summary>
            <p>{a}</p>
          </details>
''' for i, (q, a) in enumerate(c['faq']))
    d = c['docs']
    w = c['why']
    badge_ic, badge_strong, badge_small = c['badge']
    return f'''    <!-- ============ ÚVOD ============ -->
    <section class="svc-hero svc-hero--stage">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="container svc-hero__inner">
        <div class="svc-hero__copy">
          <ol class="crumbs reveal">
            <li><a href="/">Domov</a></li>
            <li><a href="/#sluzby">Služby</a></li>
            <li aria-current="page">{c['name']}</li>
          </ol>
          <span class="pill reveal"><span class="pill__dot"></span>{c['name']} · Orava a Žilina</span>
          <h1 class="reveal">{h1(c['h1'])}</h1>
          <p class="svc-hero__lead reveal">{c['lead']} {TOWNS}</p>
          <div class="hero__actions reveal">
            <a href="#kontakt" class="btn btn--primary">Nezáväzná konzultácia <span aria-hidden="true">→</span></a>
            <a href="tel:+421915448705" class="btn btn--outline">+421 915 448 705</a>
          </div>
          <ul class="hero__trust reveal">
            {CHECK}Prvé stretnutie zdarma</li>
            {CHECK}Osobne aj online</li>
            {CHECK}Registrovaný v NBS</li>
          </ul>
        </div>

        <div class="svc-stage reveal">
          <div class="svc-stage__glow" aria-hidden="true"></div>
          {glass(c['big'], 'svc-stage__house svc-stage__house--icon')}
          <img class="svc-stage__person" src="/img/martin-sluzby-1000.webp" srcset="/img/martin-sluzby-640.webp 640w, /img/martin-sluzby-1000.webp 1000w" sizes="(max-width: 900px) 80vw, 460px" width="1000" height="1195" alt="Martin Juriga, {c['name'].lower()}" fetchpriority="high" />
          {glass(c['small'], 'svc-stage__pct')}
          <div class="h-card h-card--free"><span class="pill__dot"></span>{c.get('free', 'Služba je pre vás bezplatná')}</div>
          <div class="h-card h-card--badge">
            <span class="h-card__medal"><svg viewBox="0 0 24 24">{badge_ic}</svg></span>
            <span><strong>{badge_strong}</strong><small>{badge_small}</small></span>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ S ČÍM POMÔŽEM ============ -->
    <section class="section" id="pomoc">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{c.get('cards_eyebrow', 'S čím pomôžem')}</span>
          <h2>{c['cards_h2']}</h2>
        </div>
<!-- @partial:glass-defs -->
        <div class="svc-grid">
{cards}          <article class="svc-card svc-card--cta reveal">
            <div>
              <h3>{cta_h}</h3>
              <p>{cta_p}</p>
            </div>
            <a href="{cta_href}" class="btn btn--primary btn--block">{cta_btn} <span aria-hidden="true">→</span></a>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ PREČO CEZ MŇA ============ -->
    <section class="section section--soft section--panel svc-why">
      <div class="container">
        <div class="about">
          <div class="about__media reveal">
            <div class="about__block" aria-hidden="true"></div>
            {w['img']}
            <div class="about__stat">
              <strong>{w['stat'][0]}</strong>
              <span>{w['stat'][1]}</span>
            </div>
          </div>

          <div class="about__copy">
            <span class="eyebrow reveal">Prečo cez mňa</span>
            <h2 class="reveal">{w['h2']}<br /><span class="text-muted">{w['muted']}</span></h2>
            <p class="reveal">{w['p']}</p>
            <ul class="checks reveal">
              <li>Banky, poisťovne aj investičné spoločnosti pod jednou strechou</li>
{lis(w['checks'])}
            </ul>
            <a href="#kontakt" class="btn btn--dark reveal">{w['btn']} <span aria-hidden="true">→</span></a>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ POSTUP ============ -->
    <section class="section" id="postup">
      <div class="container">
        <div class="section-head section-head--center reveal">
          <span class="eyebrow">Ako to prebieha</span>
          <h2>{c['steps_h2']}</h2>
          <span class="script-accent">krok za krokom</span>
        </div>
<!-- @partial:cesta -->
        <ol class="steps">
{steps}        </ol>
        <p class="svc-note reveal">{c['steps_note']}</p>
      </div>
    </section>

    <!-- ============ {d['eyebrow'].upper()} ============ -->
    <section class="section section--soft section--panel">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">{d['eyebrow']}</span>
          <h2>{d['h2']}</h2>
          <p class="text-muted">{d['p']}</p>
        </div>

        <div class="docs">
          <div class="docs__col reveal">
            <h3>{d['col1'][0]}</h3>
            <ul class="checks">
{lis(d['col1'][1])}
            </ul>
          </div>
          <div class="docs__col reveal">
            <h3>{d['col2'][0]}</h3>
            <ul class="checks">
{lis(d['col2'][1])}
            </ul>
          </div>
        </div>
        <p class="svc-note reveal">{d['note']}</p>
      </div>
    </section>

<!-- @partial:mapa -->
    <!-- ============ FAQ ============ -->
    <section class="section" id="faq">
      <div class="container faq">
        <div class="section-head reveal">
          <span class="eyebrow">Časté otázky</span>
          <h2>{c['faq_h2']}</h2>
          <span class="script-accent">rád odpoviem</span>
          <p class="text-muted">Nenašli ste odpoveď? <a href="#kontakt" class="link">Napíšte mi.</a></p>
        </div>

        <div class="faq__list">
{faq}        </div>
      </div>
    </section>
'''


def office(name):
    w, h = OFFICE[name]
    return (f'<img src="/img/kancelaria-{name}-1600.webp" srcset="/img/kancelaria-{name}-800.webp 800w, /img/kancelaria-{name}-1600.webp 1600w" '
            f'sizes="(max-width: 900px) 90vw, 560px" width="{w}" height="{h}" loading="lazy" alt="Kancelária, kde sa stretávame s klientmi" />')


OFFICE = {'pracovisko-okna': (1600, 1200), 'priestor': (1200, 1600), 'chodba': (1070, 1436), 'vstup': (1200, 1600), 'recepcia2': (1200, 1600), 'stol': (1600, 1200), 'stol2': (1600, 1200), 'pracovisko': (1600, 1200)}

IMG = {
    'portrait': '<img src="/img/martin-portrait.webp" width="800" height="978" loading="lazy" alt="Martin Juriga, finančný sprostredkovateľ z Oravy" />',
    'povysenie': '<img src="/img/martin-portrait.webp" width="800" height="978" loading="lazy" alt="Martin Juriga, finančný sprostredkovateľ z Oravy" />',
    'studio': '<img src="/img/martin-1200.webp" width="1200" height="1200" loading="lazy" alt="Martin Juriga, finančný sprostredkovateľ z Oravy" />',
}
IC_HOUSE = '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'
IC_TREND = '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>'
IC_SHIELD = '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>'
IC_CLOCK = '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'
IC_DOC = '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>'
IC_REFI = '<path d="M4 12a8 8 0 0 1 14-5.3L20 9M20 12a8 8 0 0 1-14 5.3L4 15M20 4v5h-5M4 20v-5h5"/>'
IC_SPROUT = '<path d="M12 21v-9M12 12C12 8 9 5 4 5c0 4 3 7 8 7zM12 10c0-3 2-6 7-6 0 4-3 6-7 6z"/>'

INVEST_NOTE = 'Hodnota investície môže stúpať aj klesať. Výnosy z minulosti nie sú zárukou budúcich výnosov.'
FEES_FAQ = ('Koľko zaplatím za vaše služby?', 'Prvé stretnutie je zadarmo a za moju prácu mi neplatíte. Samotné produkty však môžu mať poplatky, napríklad vstupný alebo správcovský. Vždy vám ich ukážem vopred.')
INS_FAQ = ('Koľko zaplatím za vaše služby?', 'Za moju prácu mi neplatíte, odmenu mi vypláca poisťovňa. Platíte len poistné, ktoré poznáte vopred a ktoré spolu nastavíme tak, aby sedelo k vášmu rozpočtu.')

CONTENT = {
  'refinancovanie': dict(
    name='Refinancovanie',
    h1='Končí vám fixácia? [Porovnajme] to.',
    lead='Refinancovanie hypotéky aj iných úverov. Porovnám ponuky viacerých bánk, prepočítam, či sa prechod naozaj oplatí, a ak áno, vybavím ho za vás.',
    big='arrows', small='coins',
    badge=(IC_REFI, 'Porovnanie viacerých bánk', 'na jednom stretnutí'),
    cards_eyebrow='Kedy to riešiť',
    cards_h2='Kedy sa oplatí<br />refinancovanie zvážiť.',
    cards=[
      ('hourglass', 'Blíži sa koniec fixácie', 'Banka vám pošle novú sadzbu, no nemusí byť jedinou možnosťou. Pred koncom fixácie je dobrý čas porovnať ponuky.'),
      ('coins', 'Chcete nižšiu splátku', 'Pozrieme sa, či iná banka ponúka lepšie podmienky, alebo či pomôže úprava doby splácania.'),
      ('plan', 'Máte viac úverov naraz', 'Spotrebné úvery, kreditnú kartu či kontokorent môžeme spojiť do jedného úveru s jednou prehľadnou splátkou.'),
      ('roller', 'Potrebujete peniaze navyše', 'Pri refinancovaní sa dá v niektorých prípadoch úver aj navýšiť, napríklad na rekonštrukciu alebo zariadenie bývania.'),
      ('heart', 'Zmenila sa vaša situácia', 'Nový príjem, rodina alebo zmena spoludlžníka. Úver upravíme tak, aby sedel k tomu, ako žijete dnes.'),
    ],
    cta=('Ešte len kupujete bývanie?', 'Pozrite si, ako vám pomôžem s novou hypotékou na kúpu, výstavbu alebo rekonštrukciu.', 'Hypotéky a úvery', '/hypoteky-a-uvery/'),
    why=dict(img=office('pracovisko-okna'), stat=('0 €', 'platíte za moje služby'),
      h2='Vaša banka ukáže svoju ponuku.', muted='Ja vám ukážem aj ostatné.',
      p='Pri konci fixácie väčšina ľudí podpíše to, čo im pošle vlastná banka. Niekedy je to dobrá voľba, inokedy nie. Spolu to porovnáme a rozhodnete sa podľa čísel, nie podľa pohodlia.',
      checks=['Porovnanie ponúk viacerých bánk na jednom mieste', 'Prepočet, či sa prechod oplatí aj po započítaní nákladov', 'Komunikáciu s novou aj pôvodnou bankou vybavím za vás', 'Ak sa prechod neoplatí, férovo vám to poviem'],
      btn='Chcem porovnať ponuky'),
    steps_h2='Do novej banky<br />bez starostí.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Porovnanie a prepočet', 'Porovnáme splátku aj celkové náklady vrátane poplatkov spojených s prechodom.'),
           ('Žiadosť v novej banke', 'Pomôžem s dokladmi a počas schvaľovania komunikujem s bankou.'),
           ('Splatenie starého úveru', 'Nová banka splatí pôvodný úver a vy už platíte len jednu splátku v novej banke.')],
    steps_note='Konečné podmienky úveru určuje banka po posúdení vašej žiadosti.',
    docs=dict(eyebrow='Čo si pripraviť', h2='Doklady k refinancovaniu.',
      p='Na prvé stretnutie stačí úverová zmluva a posledný výpis. Ostatné doplníme postupne.',
      col1=('K súčasnému úveru', ['Úverová zmluva a jej dodatky', 'Posledný výpis z úverového účtu alebo potvrdenie o zostatku', 'Informácia o konci fixácie, ak ju banka už poslala', 'List vlastníctva a znalecký posudok, ak ide o hypotéku']),
      col2=('O vás', ['Občiansky preukaz', 'Potvrdenie o príjme od zamestnávateľa, pri podnikaní daňové priznanie', 'Výpisy z bankového účtu za posledné mesiace', 'Prehľad ostatných úverov a kreditných kariet']),
      note='Presný zoznam závisí od banky a od vašej situácie. Na stretnutí vám poviem, čo presne treba.'),
    faq_h2='Otázky o refinancovaní',
    faq=[('Koľko zaplatím za vaše služby?', 'Nič. Prvé stretnutie aj vybavenie refinancovania sú pre vás bezplatné. Odmenu mi vypláca finančná inštitúcia, s ktorou úver uzatvoríte.'),
         ('Kedy mám začať riešiť koniec fixácie?', 'Ideálne aspoň dva až tri mesiace vopred. Je tak dosť času na porovnanie ponúk, prípadný nový znalecký posudok aj schválenie v novej banke.'),
         ('Zaplatím poplatok za predčasné splatenie?', 'Pri hypotéke ku koncu fixácie zvyčajne nie, vtedy ju môžete splatiť alebo refinancovať bez poplatku. Mimo tohto termínu môže banka poplatok účtovať, zákon ho však obmedzuje. Konkrétne podmienky si overíme vo vašej zmluve.'),
         ('Oplatí sa mi refinancovanie?', 'Nie vždy. Rozhoduje rozdiel v podmienkach, zostatok úveru, zostávajúca doba splácania aj náklady spojené s prechodom, napríklad znalecký posudok či poplatok za vklad do katastra. Spolu to prepočítame a ak sa to neoplatí, poviem vám to.'),
         ('Môžem pri refinancovaní úver navýšiť?', 'Často áno, ak to dovolí hodnota nehnuteľnosti a váš príjem. Navýšené peniaze môžete použiť napríklad na rekonštrukciu alebo na splatenie iných úverov.'),
         ('Dá sa refinancovať aj spotrebný úver?', 'Áno. Spotrebné úvery, kreditné karty či kontokorent sa dajú spojiť do jedného úveru. Niekedy je výhodnejšie zahrnúť ich do hypotéky, inokedy nie. Prejdeme to spolu.')],
  ),

  'skratenie-uveru': dict(
    name='Skrátenie úveru',
    h1='Splaťte hypotéku [skôr], nie za 30 rokov.',
    lead='Pomôžem vám zistiť, o koľko rokov sa dá vaša hypotéka alebo úver skrátiť a koľko tým ušetríte na úrokoch. Prepočítame viac ciest a vyberiete si tú, ktorá sedí k vášmu rozpočtu.',
    big='hourglass', small='coins',
    badge=(IC_CLOCK, 'Kratšie splácanie', 'menej zaplatených úrokov'),
    cards_eyebrow='Ako na to',
    cards_h2='Cesty, ako úver<br />splatiť skôr.',
    cards=[
      ('coins', 'Mimoriadne splátky', 'Občas vložíte do úveru peniaze navyše, napríklad z odmeny alebo úspor. Pozrieme sa, kedy to vaša zmluva dovoľuje bez poplatku.'),
      ('hourglass', 'Kratšia doba splácania', 'Pri konci fixácie alebo pri refinancovaní sa dá nastaviť kratšia doba splácania s o niečo vyššou splátkou.'),
      ('arrows', 'Nižší úrok, rovnaká splátka', 'Ak po refinancovaní dostanete nižší úrok a ponecháte si pôvodnú splátku, väčšia časť ide na istinu a úver skončí skôr.', ('/refinancovanie/', 'Viac o refinancovaní')),
      ('plan', 'Spojenie viacerých úverov', 'Drahé spotrebné úvery či kreditnú kartu môžeme splatiť ako prvé, aby ste neplatili vysoké úroky zbytočne dlho.'),
      ('target', 'Plán podľa vašich cieľov', 'Chcete mať bývanie splatené do dôchodku alebo skôr, ako deti pôjdu na vysokú? Nastavíme plán k tomuto cieľu.'),
    ],
    cta=('Potrebujete novú hypotéku?', 'Pozrite si, ako vám pomôžem s hypotékou na kúpu, výstavbu alebo rekonštrukciu.', 'Hypotéky a úvery', '/hypoteky-a-uvery/'),
    why=dict(img=office('stol2'), stat=('0 €', 'platíte za moje služby'),
      h2='Každý rok splácania navyše', muted='stojí peniaze na úrokoch.',
      p='Pri dlhej hypotéke zaplatíte na úrokoch často veľkú časť z požičanej sumy. Spolu prepočítame, koľko by ste ušetrili pri kratšom splácaní, a nastavíme splátku tak, aby vám v rozpočte ostala aj rezerva.',
      checks=['Prepočet viacerých možností skrátenia vedľa seba', 'Kontrola podmienok mimoriadnych splátok vo vašej zmluve', 'Splátka, pri ktorej vám ostane rezerva na nečakané výdavky', 'Ak sa skracovanie práve neoplatí, férovo vám to poviem'],
      btn='Chcem prepočítať skrátenie'),
    steps_h2='Od prepočtu<br />po kratšie splácanie.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Prepočet možností', 'Pozrieme sa na zostatok, úrok a fixáciu a prepočítame, o koľko rokov sa dá úver skrátiť.'),
           ('Výber cesty', 'Mimoriadne splátky, kratšia doba pri fixácii alebo refinancovanie. Rozhodnete sa podľa čísel.'),
           ('Vybavenie v banke', 'Pomôžem s dokladmi a komunikáciou s bankou, kým nie je zmena hotová.')],
    steps_note='Konečné podmienky úveru určuje banka po posúdení vašej žiadosti.',
    docs=dict(eyebrow='Čo si pripraviť', h2='Doklady k prepočtu.',
      p='Na prvé stretnutie stačí úverová zmluva a posledný výpis. Ostatné doplníme podľa toho, akú cestu si vyberiete.',
      col1=('K súčasnému úveru', ['Úverová zmluva a jej dodatky', 'Posledný výpis z úverového účtu alebo potvrdenie o zostatku', 'Informácia o konci fixácie', 'Podmienky mimoriadnych splátok, ak ich máte']),
      col2=('O vás', ['Občiansky preukaz', 'Prehľad príjmov a pravidelných výdavkov', 'Prehľad ostatných úverov a kreditných kariet', 'Informácia o úsporách, ktoré by ste chceli použiť']),
      note='Presný zoznam závisí od banky a od vašej situácie. Na stretnutí vám poviem, čo presne treba.'),
    faq_h2='Otázky o skrátení úveru',
    faq=[('Koľko zaplatím za vaše služby?', 'Nič. Prvé stretnutie aj prepočet sú pre vás bezplatné. Ak úver refinancujete, odmenu mi vypláca finančná inštitúcia, s ktorou ho uzatvoríte.'),
         ('Oplatí sa skrátiť úver, alebo radšej investovať?', 'Závisí to od úroku, vašej rezervy a cieľov. Niekedy dáva zmysel kombinácia oboch. Na stretnutí to prepočítame pre vašu situáciu.'),
         ('Zaplatím poplatok za mimoriadnu splátku?', 'Pri konci fixácie zvyčajne nie. Mimo nej môže banka poplatok účtovať a niektoré banky dovoľujú časť úveru splatiť bezplatne každý rok. Overíme to vo vašej zmluve.'),
         ('Zvýši sa mi splátka?', 'Pri kratšej dobe splácania áno, pri mimoriadnych splátkach či nižšom úroku nie nutne. Vždy nastavíme splátku tak, aby vám ostala rezerva.'),
         ('Kedy je najlepší čas úver skrátiť?', 'Najviac možností máte ku koncu fixácie. Vtedy sa dajú meniť podmienky aj vložiť väčšia suma bez poplatku. Ideálne začnite riešiť dva až tri mesiace vopred.'),
         ('Dá sa skrátiť aj spotrebný úver?', 'Áno. Spotrebný úver sa dá často splatiť skôr alebo spojiť s inými úvermi. Prejdeme spolu, čo je pre vás výhodnejšie.')],
  ),

  'sporenie-pre-deti': dict(
    name='Sporenie pre deti',
    h1='Peniaze pre deti na [štart] do života.',
    lead='Pomôžem vám nastaviť pravidelné sporenie alebo investovanie pre deti, aby mali peniaze na štúdium, prvé bývanie či vodičák. Pre rodičov aj starých rodičov.',
    big='sprout', small='coins', free='Prvé stretnutie zdarma',
    badge=(IC_SPROUT, 'Od narodenia', 'až po štart do života'),
    cards_h2='Sporenie pre deti<br />na to, čo ich čaká.',
    cards=[
      ('coins', 'Pravidelné sporenie od narodenia', 'Aj menšia mesačná suma môže za roky narásť, lebo pri deťoch pracuje pre vás čas.'),
      ('cap', 'Peniaze na štúdium', 'Vysoká škola, jazykový kurz či internát. Pripravíme peniaze na chvíľu, keď ich budú potrebovať.'),
      ('house', 'Na prvé bývanie', 'Vlastné peniaze na prvý nájom alebo vlastný zdroj k hypotéke, keď budú stáť na vlastných nohách.', ('/hypoteky-a-uvery/', 'Viac o hypotékach')),
      ('gift', 'Príspevok od starých rodičov', 'Pravidelný darček od starých či krstných rodičov, ktorý má väčší zmysel ako ďalšia hračka.'),
      ('shield', 'Úrazové poistenie detí', 'Pre aktívne deti, aby vás nezaskočili výdavky po úraze pri športe či v škole.'),
    ],
    why=dict(img=office('priestor'), stat=('0 €', 'platíte za moje služby'),
      h2='Pri deťoch je čas', muted='najväčšia výhoda.',
      p='Kto začne skôr, môže sporiť menšiu mesačnú sumu. Pomôžem vám vybrať riešenie, ktoré sedí k tomu, na čo a na ako dlho chcete pre dieťa odkladať.',
      checks=['Vysvetlím rozdiel medzi sporením a investovaním', 'Suma, ktorá vám nebude chýbať v rozpočte', 'Dohodneme, kedy a ako dieťa peniaze dostane', 'Pravidelne spolu skontrolujeme, ako sa plánu darí'],
      btn='Chcem sporiť pre dieťa'),
    steps_h2='Od prvej otázky<br />po sporenie pre dieťa.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Cieľ a suma', 'Zistíme, koľko, na ako dlho a aké riziko vám je príjemné.'),
           ('Výber riešenia', 'Porovnáme sporenie a investovanie a vysvetlím rozdiely. Rozhodnutie je na vás.'),
           ('Podpis a pravidelný servis', 'Podpis zmlúv a minimálne raz za rok servisné stretnutie.')],
    steps_note=INVEST_NOTE,
    docs=dict(eyebrow='Na čo myslieť', h2='Ako na sporenie pre deti.',
      p='Z týchto zásad vychádzam, keď s rodičmi nastavujeme sporenie pre deti.',
      col1=('Pri nastavovaní', ['Začať čo najskôr, ideálne od narodenia', 'Suma, ktorá vám nechýba v rozpočte', 'Jasný cieľ a približný termín', 'Dohoda, kto bude s peniazmi narábať']),
      col2=('Počas sporenia', ['Pravidelnosť namiesto jednorazových vkladov', 'Pri dlhom horizonte môže dávať zmysel investovanie', 'Znižovať riziko, keď sa blíži cieľ', 'Pravidelná kontrola, či plán stále sedí']),
      note='Informácie na tejto stránke majú informatívny charakter a nie sú investičným odporúčaním.'),
    faq_h2='Otázky o sporení pre deti',
    faq=[FEES_FAQ,
         ('Kedy je najlepšie začať?', 'Čím skôr, tým lepšie, ideálne hneď po narodení. Začať sa však dá kedykoľvek a aj pár rokov sporenia urobí rozdiel.'),
         ('Sporenie alebo investovanie?', 'Pri krátkom horizonte do pár rokov býva vhodnejšie sporenie. Pri dlhšom horizonte môže investovanie priniesť vyšší výnos, no jeho hodnota kolíše. Rozdiel vám vysvetlím a rozhodnete sa sami.'),
         ('Môžu prispievať aj starí rodičia?', 'Áno. Prispievať môže ktokoľvek z rodiny, pravidelne aj jednorazovo, napríklad k narodeninám či Vianociam.'),
         ('Čo ak budeme peniaze potrebovať skôr?', 'Pri väčšine riešení sa k peniazom dostanete, no pri investíciách môže byť ich hodnota v danom momente nižšia. Podmienky výberu prejdeme vopred.'),
         ('Kedy dostane peniaze dieťa?', 'To si dohodneme pri nastavení. O tom, kedy a na čo sa peniaze použijú, rozhodujete vy ako rodičia.')],
  ),

  'dochodok': dict(
    name='Dôchodok',
    h1='Dôchodok, na ktorý sa [tešíte].',
    lead='Pomôžem vám skontrolovať II. pilier, nastaviť III. pilier a dlhodobé investovanie, aby ste sa na dôchodku nespoliehali len na štát.',
    big='hourglass', small='coins',
    badge=(IC_CLOCK, 'II. a III. pilier', 'aj investovanie navyše'),
    cards_h2='Dôchodok, ktorý<br />nenecháte na náhodu.',
    cards=[
      ('chart', 'II. pilier', 'Skontrolujeme, či máte v II. pilieri stratégiu a fondy, ktoré sedia k vášmu veku a cieľom.'),
      ('coins', 'III. pilier', 'Doplnkové dôchodkové sporenie, ku ktorému môže prispievať aj zamestnávateľ a ktoré prináša daňovú výhodu.'),
      ('target', 'Investovanie na dôchodok', 'Pravidelné investovanie navyše pre tých, ktorí chcú na dôchodku viac ako minimum.', ('/investovanie/', 'Viac o investovaní')),
      ('hourglass', 'Odhad budúceho dôchodku', 'Približne spočítame, s akým dôchodkom môžete rátať a koľko vám bude chýbať do životnej úrovne, ktorú chcete.'),
      ('magnifier', 'Kontrola súčasných zmlúv', 'Pozrieme sa na zmluvy, ktoré už máte: poplatky, fondy a to, či ešte sedia k vašej situácii.'),
    ],
    why=dict(img=office('chodba'), stat=('0 €', 'platíte za moje služby'),
      h2='Na štát sa spoliehať nedá.', muted='Na plán áno.',
      p='Dôchodok sa nedá vyriešiť rok pred ním. Čím skôr začnete, tým menšia mesačná suma stačí. Pozrieme sa na to, čo už máte, a doplníme, čo chýba.',
      checks=['Kontrola II. piliera a výber stratégie', 'III. pilier s príspevkom zamestnávateľa, ak ho máte', 'Investovanie navyše podľa vašich možností', 'Pravidelné prehodnotenie, ako sa blíži dôchodok'],
      btn='Chcem riešiť dôchodok'),
    steps_h2='Od prvého stretnutia<br />po dôchodkový plán.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Kontrola súčasného stavu', 'Pozrieme sa na II. a III. pilier aj ďalšie sporenia a investície.'),
           ('Dôchodkový plán', 'Pripravím návrh, koľko a kam odkladať. Rozhodnutie je na vás.'),
           ('Podpis a pravidelný servis', 'Podpis zmlúv a minimálne raz za rok servisné stretnutie.')],
    steps_note=INVEST_NOTE,
    docs=dict(eyebrow='Na čo myslieť', h2='Zásady pri dôchodku.',
      p='Na tieto veci sa s klientmi pri dôchodku pozeráme najčastejšie.',
      col1=('Čo vám pomôže', ['Začať čo najskôr', 'Využiť príspevok zamestnávateľa v III. pilieri', 'Stratégiu, ktorá zodpovedá vášmu veku', 'Pravidelne kontrolovať, ako sa sporeniu darí']),
      col2=('Na čo si dať pozor', ['Fondy, ktoré nesedia k vášmu veku a cieľom', 'Vysoké poplatky, o ktorých neviete', 'Zabudnuté zmluvy, ktoré nikto nekontroluje', 'Predčasné vyberanie peňazí bez dôvodu']),
      note='Informácie na tejto stránke majú informatívny charakter a nie sú investičným odporúčaním.'),
    faq_h2='Otázky o dôchodku',
    faq=[FEES_FAQ,
         ('Mám zostať v II. pilieri?', 'Závisí to od veku, príjmu a ďalších okolností. Pozrieme sa na vašu situáciu a vysvetlím vám, čo jednotlivé možnosti znamenajú.'),
         ('Oplatí sa III. pilier?', 'Často áno, najmä ak vám zamestnávateľ prispieva. Príspevky si navyše môžete v zákonom stanovenej výške odpočítať zo základu dane.'),
         ('Môžem zmeniť fond alebo spoločnosť v II. pilieri?', 'Áno, stratégiu aj dôchodkovú správcovskú spoločnosť sa dá zmeniť. Pomôžem vám zistiť, či to má vo vašom prípade zmysel, a vybaviť to.'),
         ('Koľko budem mať na dôchodku?', 'Presne to nevie nikto, ale dá sa to približne odhadnúť. Spolu spočítame, s čím môžete rátať a koľko odkladať, aby vám nič nechýbalo.'),
         ('Kedy je najlepšie začať?', 'Čím skôr, tým lepšie. Ale aj desať rokov pred dôchodkom sa dá ešte veľa urobiť.')],
  ),

  'zivotne-poistenie': dict(
    name='Životné poistenie',
    h1='Životné poistenie, ktoré [naozaj] chráni.',
    lead='Nastavím poistenie na skutočné riziká: vážnu chorobu, úraz, invaliditu či zabezpečenie rodiny. Bez zbytočných pripoistení, len to, čo dáva zmysel.',
    big='shield', small='heart',
    badge=(IC_SHIELD, '22 životných poistení', 'nastavených s klientmi'),
    cards_h2='Poistenie na to,<br />čo by vás naozaj zaskočilo.',
    cards=[
      ('heart', 'Zabezpečenie rodiny', 'Aby vaši blízki zvládli splátky aj bežný život, keby sa vám niečo stalo.'),
      ('shield', 'Vážne choroby a invalidita', 'Peniaze v čase, keď nemôžete pracovať a potrebujete sa sústrediť na liečbu.'),
      ('plus', 'Úraz a práceneschopnosť', 'Kompenzácia výpadku príjmu pri dlhšej práceneschopnosti alebo po úraze.'),
      ('house', 'Poistenie k hypotéke', 'Aby úver nebol pre rodinu záťažou, ak by ste ho nemohli splácať.', ('/hypoteky-a-uvery/', 'Viac o hypotékach')),
      ('magnifier', 'Kontrola súčasnej zmluvy', 'Pozrieme sa na vaše poistenie: poistné sumy, výluky a to, či ešte sedí k vášmu životu.'),
    ],
    why=dict(img=office('vstup'), stat=('22', 'životných poistení s klientmi'),
      h2='Poistenie nie je o tom, koľko platíte.', muted='Je o tom, čo vám vyplatí.',
      p='Veľa ľudí má poistenie, ktoré v ťažkej chvíli nepomôže, lebo poistné sumy sú nízke alebo kryje nesprávne riziká. Nastavíme ho podľa vášho príjmu, rodiny a záväzkov.',
      checks=['Poistné sumy podľa príjmu a záväzkov', 'Bez zbytočných pripoistení', 'Porovnanie viacerých poisťovní', 'Pomoc pri nahlásení poistnej udalosti'],
      btn='Chcem skontrolovať poistenie'),
    steps_h2='Od rozhovoru<br />po poistenie, ktoré sedí.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Analýza rizík', 'Zistíme, ktoré situácie by vás finančne najviac zasiahli.'),
           ('Návrh a porovnanie', 'Porovnám ponuky viacerých poisťovní a vysvetlím rozdiely. Rozhodnutie je na vás.'),
           ('Podpis a pravidelný servis', 'Podpis zmlúv, minimálne raz za rok servis a pomoc aj pri poistnej udalosti.')],
    steps_note='Rozsah krytia a výluky určujú poistné podmienky konkrétnej poisťovne.',
    docs=dict(eyebrow='Na čo myslieť', h2='Na čo myslieť pri životnom poistení.',
      p='Na tieto veci sa pri nastavovaní a kontrole životného poistenia pozeráme najčastejšie.',
      col1=('Čo má zmysel poistiť', ['Smrť, ak máte rodinu alebo úver', 'Invaliditu, ktorá vás pripraví o príjem', 'Vážne choroby', 'Dlhodobú práceneschopnosť']),
      col2=('Na čo si dať pozor', ['Nízke poistné sumy, ktoré v ťažkej chvíli nepomôžu', 'Pripoistenia, ktoré nepotrebujete', 'Zmluvy, ktoré už nesedia k vášmu životu', 'Výluky v poistných podmienkach']),
      note='Konkrétne podmienky krytia vždy prejdeme spolu podľa poistných podmienok vybranej poisťovne.'),
    faq_h2='Otázky o životnom poistení',
    faq=[INS_FAQ,
         ('Koľko stojí životné poistenie?', 'Závisí od veku, zdravia, povolania a výšky poistných súm. Nastavíme ho tak, aby chránilo to podstatné a zároveň sedelo k vášmu rozpočtu.'),
         ('Mám poistenie k úveru z banky. Stačí to?', 'Poistenie k úveru zvyčajne kryje hlavne splácanie úveru. Pozrieme sa, či vás a vašu rodinu chráni aj v ďalších situáciách.'),
         ('Aký je rozdiel medzi rizikovým a investičným životným poistením?', 'Rizikové poistenie chráni pred následkami choroby, úrazu či smrti. Investičné k tomu pridáva aj investovanie. Vysvetlím vám rozdiel, aby ste vedeli, za čo platíte.'),
         ('Môžem upraviť zmluvu, ktorú už mám?', 'Často áno. Pozrieme sa na ňu a zistíme, či ju stačí upraviť, alebo má zmysel uvažovať o inom riešení.'),
         ('Čo robiť pri poistnej udalosti?', 'Ozvite sa mi. Pomôžem vám s nahlásením, dokladmi a komunikáciou s poisťovňou.')],
  ),

  'majetkove-poistenie': dict(
    name='Majetkové poistenie',
    h1='Poistenie domova [bez prekvapení].',
    lead='Poistenie nehnuteľnosti, domácnosti aj zodpovednosti nastavené tak, aby poistná suma zodpovedala skutočnej hodnote vášho majetku.',
    big='house', small='umbrella',
    badge=(IC_HOUSE, 'Byt, dom a domácnosť', 'aj zodpovednosť'),
    cards_h2='Poistenie toho,<br />na čom vám záleží.',
    cards=[
      ('house', 'Poistenie nehnuteľnosti', 'Dom, byt, garáž či chata. Poistenie stavby pre prípad požiaru, vody, víchrice a ďalších rizík.'),
      ('sofa', 'Poistenie domácnosti', 'Nábytok, elektronika, oblečenie a všetko, čo by vypadlo, keby ste dom otočili hore nohami.'),
      ('shield', 'Zodpovednosť v bežnom živote', 'Ak omylom spôsobíte škodu niekomu inému, napríklad vytopíte suseda.'),
      ('umbrella', 'Živelné riziká', 'Povodeň, záplava, krupobitie či zosuv pôdy. Pozrieme sa, ktoré riziká má zmysel kryť práve vo vašej lokalite.'),
      ('magnifier', 'Kontrola súčasnej zmluvy', 'Pozrieme sa, či poistná suma ešte zodpovedá hodnote majetku a či zmluva kryje to, čo potrebujete.'),
    ],
    why=dict(img=office('recepcia2'), stat=('0 €', 'platíte za moje služby'),
      h2='Podpoistený majetok', muted='je najdrahšia chyba.',
      p='Ak je poistná suma nižšia ako skutočná hodnota majetku, poisťovňa môže plnenie pomerne znížiť. Preto začíname tým, aby bol majetok ocenený správne.',
      checks=['Poistná suma podľa skutočnej hodnoty majetku', 'Porovnanie viacerých poisťovní', 'Pozor na výluky a spoluúčasť', 'Pomoc pri nahlásení škody'],
      btn='Chcem skontrolovať poistenie'),
    steps_h2='Od ocenenia<br />po poistený domov.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Ocenenie majetku', 'Spolu určíme, akú hodnotu má nehnuteľnosť a domácnosť.'),
           ('Porovnanie ponúk', 'Porovnám ponuky viacerých poisťovní a vysvetlím rozdiely. Rozhodnutie je na vás.'),
           ('Podpis a pravidelný servis', 'Podpis zmlúv, minimálne raz za rok servis a pomoc aj pri škode.')],
    steps_note='Rozsah krytia a výluky určujú poistné podmienky konkrétnej poisťovne.',
    docs=dict(eyebrow='Čo si pripraviť', h2='Čo budeme potrebovať.',
      p='Na prvé stretnutie stačí pár základných údajov. Ostatné doplníme spolu.',
      col1=('K nehnuteľnosti', ['Adresa a rok výstavby', 'Podlahová plocha a typ stavby', 'Vedľajšie stavby, napríklad garáž či plot', 'Súčasná poistná zmluva, ak ju máte']),
      col2=('K domácnosti', ['Približná hodnota vybavenia', 'Cennosti, elektronika a drahšie veci', 'Bicykle, náradie a vybavenie mimo bytu', 'Informácia, či nehnuteľnosť zabezpečuje úver']),
      note='Ak je nehnuteľnosť zabezpečením hypotéky, banka zvyčajne vyžaduje jej poistenie a vinkuláciu plnenia v jej prospech.'),
    faq_h2='Otázky o majetkovom poistení',
    faq=[INS_FAQ,
         ('Aký je rozdiel medzi poistením nehnuteľnosti a domácnosti?', 'Poistenie nehnuteľnosti kryje samotnú stavbu. Poistenie domácnosti kryje veci vo vnútri, teda všetko, čo by vypadlo, keby ste dom otočili hore nohami.'),
         ('Čo je podpoistenie?', 'Ak je poistná suma nižšia ako skutočná hodnota majetku, poisťovňa môže plnenie pomerne znížiť. Preto je dôležité majetok oceniť správne a poistnú sumu občas aktualizovať.'),
         ('Potrebujem poistenie zodpovednosti?', 'Odporúča sa takmer každému. Kryje škody, ktoré omylom spôsobíte iným, napríklad keď vytopíte suseda alebo dieťa niečo poškodí.'),
         ('Banka chce poistenie k hypotéke. Môžem si vybrať poisťovňu?', 'Zvyčajne áno. Banka vyžaduje poistenie nehnuteľnosti a vinkuláciu v jej prospech, poisťovňu si však často môžete vybrať sami. Pomôžem vám s porovnaním.'),
         ('Čo robiť pri škode?', 'Zdokumentujte škodu fotkami a ozvite sa mi. Pomôžem vám s nahlásením a komunikáciou s poisťovňou.')],
  ),

  'financny-plan': dict(
    name='Finančný plán',
    h1='Všetky financie v [jednom] pláne.',
    lead='Prejdeme vaše príjmy, výdavky, zmluvy a ciele. Dostanete prehľadný plán, čo robiť s peniazmi dnes aj o 20 rokov.',
    big='plan', small='target',
    badge=(IC_DOC, '50 finančných plánov', 'pripravených s klientmi'),
    cards_eyebrow='Čo plán obsahuje',
    cards_h2='Jeden plán.<br />Všetky oblasti financií.',
    cards=[
      ('magnifier', 'Analýza zmlúv', 'Pozrieme sa na všetky vaše zmluvy: poistenia, úvery aj sporenia. Čo sedí, čo je zbytočné a čo chýba.'),
      ('coins', 'Rezerva a rozpočet', 'Koľko odkladať, koľko mať bokom na nečakané výdavky a kde vám peniaze zbytočne unikajú.'),
      ('target', 'Vaše ciele', 'Bývanie, deti, auto či dôchodok. Ku každému cieľu suma, termín a cesta, ako sa k nemu dostať.'),
      ('shield', 'Ochrana príjmu a rodiny', 'Poistenie nastavené na riziká, ktoré by vás finančne najviac zasiahli.', ('/zivotne-poistenie/', 'Viac o životnom poistení')),
      ('hourglass', 'Dôchodok a dlhodobé investovanie', 'Aby ste mali na dôchodku viac ako minimum od štátu.', ('/dochodok/', 'Viac o dôchodku')),
    ],
    why=dict(img=office('stol'), stat=('60', 'analýz cieľov a potrieb'),
      h2='Plán namiesto', muted='náhodných zmlúv.',
      p='Veľa ľudí má zmluvy, ktoré im niekto kedysi ponúkol, a nevie, či do seba zapadajú. Finančný plán ich dá dokopy a ukáže, čo má zmysel ponechať, upraviť alebo doplniť.',
      checks=['Prehľad všetkých financií na jednom mieste', 'Konkrétne kroky, nie všeobecné rady', 'Rozhodnutie je vždy na vás', 'Pravidelná aktualizácia, keď sa vám zmení život'],
      btn='Chcem finančný plán'),
    steps_h2='Štyri kroky<br />k jasnému plánu.',
    steps=[('Stretnutie', 'Zadarmo, do hodiny. Spoznáme sa a zistíme, či chcete spolupracovať vy so mnou a ja s vami.'),
           ('Analýza cieľov a potrieb', 'Prejdeme príjmy, výdavky, zmluvy a ciele. Zmapujeme, kde ste dnes.'),
           ('Plán na mieru', 'Predstavím vám plán šitý na vás a vysvetlím každý krok. Rozhodnutie je na vás.'),
           ('Podpis a pravidelný servis', 'Podpis zmlúv a minimálne raz za rok servisné stretnutie.')],
    steps_note='Finančný plán je pre vás bezplatný a nezaväzuje vás k podpisu žiadnej zmluvy.',
    docs=dict(eyebrow='Čo si pripraviť', h2='Čo prineste na stretnutie.',
      p='Nemusíte mať všetko. Čím viac však budeme vedieť, tým presnejší bude plán.',
      col1=('Zmluvy, ktoré máte', ['Životné a majetkové poistenie', 'Úvery, hypotéky a kreditné karty', 'Sporenia, investície, II. a III. pilier', 'Stavebné sporenie a iné produkty']),
      col2=('O vás', ['Približné mesačné príjmy a výdavky', 'Úspory a rezerva, ktorú máte', 'Vaše ciele na najbližšie roky', 'Plány, ktoré by mohli zmeniť financie, napríklad dieťa či bývanie']),
      note='Všetky informácie, ktoré mi poskytnete, sú dôverné a slúžia len na prípravu vášho plánu.'),
    faq_h2='Otázky o finančnom pláne',
    faq=[('Koľko stojí finančný plán?', 'Pre vás nič. Prvé stretnutie, analýza aj finančný plán sú bezplatné. Odmenu mi vyplácajú finančné inštitúcie, ak sa rozhodnete niektorú zmluvu uzatvoriť.'),
         ('Musím potom niečo podpísať?', 'Nie. Dostanete plán a rozhodnete sa sami, či a ktoré kroky chcete urobiť.'),
         ('Čo všetko plán obsahuje?', 'Prehľad vašich financií, rezervu, ciele s konkrétnymi sumami a termínmi, ochranu príjmu a rodiny, dôchodok a dlhodobé investovanie.'),
         ('Je finančný plán len pre ľudí s vysokým príjmom?', 'Vôbec nie. Najväčší zmysel má práve vtedy, keď chcete z bežného príjmu dostať čo najviac a vyhnúť sa zbytočným zmluvám.'),
         ('Ako často treba plán aktualizovať?', 'Vždy, keď sa vám výrazne zmení život, napríklad pri novej práci, dieťati či kúpe bývania. Inak ho stačí raz za čas spolu skontrolovať.'),
         ('Ako dlho trvá príprava plánu?', 'Závisí od toho, koľko zmlúv a cieľov máte. Zvyčajne stačia dve až tri stretnutia.')],
  ),
}

if __name__ == '__main__':
    for slug, c in CONTENT.items():
        open(os.path.join(os.path.dirname(__file__), 'pages', slug + '.html'), 'w').write(render(c))
        print('stránka', slug)
