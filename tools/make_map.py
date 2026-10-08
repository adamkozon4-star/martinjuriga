"""Vygeneruje tools/partials/mapa.html: 3D mapu Oravy a Žiliny so špendlíkmi.

Súradnice sú približné (x = východ, y = juh) na ploche 600 × 420.
Spúšťa sa z koreňa repozitára:  python3 tools/make_map.py
"""
import os

W, H = 600, 420
TOWNS = [  # (názov, x, y, hlavné mesto?)
    ('Trstená', 452, 62, False),
    ('Námestovo', 236, 104, False),
    ('Tvrdošín', 404, 150, False),
    ('Dolný Kubín', 300, 262, True),
    ('Žilina', 92, 352, False),
]
# stromy a domy stoja na mape, natočené ku kamere
TREES = [(150, 70), (176, 52), (120, 120), (520, 120), (548, 160), (500, 220), (470, 300), (520, 330), (200, 200),
         (180, 236), (380, 330), (410, 372), (60, 250), (40, 290), (150, 300), (560, 260), (330, 60), (360, 40), (250, 330)]
HOUSES = [(486, 70), (472, 50), (268, 92), (210, 86), (430, 128), (338, 272), (270, 252), (330, 240), (126, 362), (62, 340), (122, 338)]

def pct(x, y):
    return f'left:{x / W * 100:.2f}%;top:{y / H * 100:.2f}%'

ground = f'''<svg class="geo__ground" viewBox="0 0 {W} {H}" aria-hidden="true">
              <defs>
                <linearGradient id="geoLand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#faf5f1"/></linearGradient>
                <pattern id="geoGrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#efe9e4" stroke-width="1"/></pattern>
              </defs>
              <rect width="{W}" height="{H}" rx="34" fill="url(#geoLand)"/>
              <rect width="{W}" height="{H}" rx="34" fill="url(#geoGrid)" opacity=".7"/>
              <!-- lesy a kopce -->
              <path d="M110 30c40-18 90-6 110 22s-10 60-60 62-90-20-90-46 10-28 40-38z" fill="#dcefe1"/>
              <path d="M480 100c40-10 90 20 96 60s-20 90-70 96-70-40-66-80 10-68 40-76z" fill="#dcefe1"/>
              <path d="M150 190c30-12 70 6 76 34s-24 46-56 44-50-20-48-44 10-28 28-34z" fill="#e5f3e8"/>
              <path d="M20 240c26-14 70-6 80 22s-16 50-46 50-48-14-50-38 0-26 16-34z" fill="#e5f3e8"/>
              <path d="M360 300c36-14 92 2 100 36s-30 62-70 60-60-24-60-50 12-38 30-46z" fill="#e5f3e8"/>
              <!-- Oravská priehrada -->
              <path d="M262 120c18-20 60-24 92-14s36 30 18 42-56 10-80 6-46-14-30-34z" fill="#f5e8dd" stroke="#f3d2b5" stroke-width="2"/>
              <!-- Orava a Váh -->
              <path d="M362 146c18 8 32 6 42 4M404 150c-10 34-40 50-66 70s-38 34-38 42c0 30-30 50-60 72s-50 26-62 26" fill="none" stroke="#f3d2b5" stroke-width="7" stroke-linecap="round"/>
              <path d="M10 380c40-14 70-24 100-28s70-6 108-10 70-8 100 4" fill="none" stroke="#f3d2b5" stroke-width="8" stroke-linecap="round"/>
              <!-- cesty -->
              <g fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path d="M92 352c50-6 90-10 128-8s60-30 80-82c20-40 60-70 104-112 20-30 36-60 48-88M300 262c-20-60-50-110-64-158M404 150c-50-30-110-36-168-46" stroke="#ffffff" stroke-width="12"/>
                <path d="M92 352c50-6 90-10 128-8s60-30 80-82c20-40 60-70 104-112 20-30 36-60 48-88M300 262c-20-60-50-110-64-158M404 150c-50-30-110-36-168-46" stroke="#e9c77d" stroke-width="5"/>
              </g>
              <text x="470" y="400" class="geo__region">ORAVA · ŽILINA</text>
            </svg>'''

def tree(x, y, i):
    s = 0.8 + (i % 3) * 0.15
    return (f'<span class="geo__obj geo__tree" style="{pct(x, y)};--s:{s:.2f}"><svg viewBox="0 0 24 34" aria-hidden="true">'
            '<path d="M12 1L3 17h5L2 27h20l-6-10h5z" fill="url(#geoTree)"/><rect x="10.5" y="27" width="3" height="6" rx="1" fill="#9a6b45"/></svg></span>')

def house(x, y):
    return (f'<span class="geo__obj geo__house" style="{pct(x, y)}"><svg viewBox="0 0 30 30" aria-hidden="true">'
            '<path d="M15 3L28 9 15 15 2 9z" fill="#ffffff"/><path d="M2 9l13 6v13L2 22z" fill="#f7f4f1"/><path d="M28 9L15 15v13l13-6z" fill="#e2dad3"/>'
            '<path d="M5 14v3M8 15.5v3M18 18v3M22 16v3M25 14.5v3" stroke="#c4b6aa" stroke-width="1.4"/></svg></span>')

def pin(name, x, y, main, i):
    cls = 'geo__pin geo__pin--main' if main else 'geo__pin'
    return (f'<span class="geo__shadow{" geo__shadow--main" if main else ""}" style="{pct(x, y)}"></span>\n'
            f'            <span class="{cls}" style="{pct(x, y)};--d:{i * 140}ms"><span class="geo__pin-in">'
            '<svg viewBox="0 0 40 54" aria-hidden="true"><path d="M20 1C9.5 1 1 9.5 1 20c0 14.5 19 33 19 33s19-18.5 19-33C39 9.5 30.5 1 20 1z" fill="url(#geoPin)"/>'
            '<circle cx="20" cy="19" r="7.5" fill="#fff"/><path d="M11 9c3-3 7-4.5 11-4" stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".6" fill="none"/></svg>'
            f'<b>{name}</b></span></span>')

objs = []
for i, (x, y) in enumerate(TREES):
    objs.append(tree(x, y, i))
for x, y in HOUSES:
    objs.append(house(x, y))
for i, (n, x, y, m) in enumerate(TOWNS):
    objs.append(pin(n, x, y, m, i))

PHOTOS = [  # (súbor, šírka, výška 1600-verzie, popis); prvé SHOWN sú viditeľné náhľady
    ('fasada', 1600, 1200, 'Budova kancelárie MeruCompany zvonku'),
    ('recepcia-pult', 1200, 1600, 'Recepcia s logom MeruCompany'),
    ('zasadacky', 1600, 1200, 'Presklené zasadačky na stretnutia'),
    ('skolenie', 1600, 1200, 'Miestnosť na stretnutia a školenia'),
    ('vchod', 1600, 1200, 'Vchod do kancelárie'),
    ('dvere', 1600, 1200, 'Vstupné dvere s logom MeruCompany'),
    ('recepcia4', 1600, 1200, 'Recepcia kancelárie'),
    ('recepcia-kancelaria', 1600, 1200, 'Recepcia a pracovné miesta'),
    ('kreslo', 1600, 1200, 'Pracovisko v kancelárii'),
    ('recepcia2', 1200, 1600, 'Recepcia kancelárie'),
    ('chodba', 1070, 1436, 'Chodba v kancelárii'),
]
SHOWN = 4
def photo(i, f, w, h, alt):
    more = len(PHOTOS) - SHOWN
    extra = f' data-more="+{more}"' if i == SHOWN - 1 and more > 0 else ''
    hidden = ' hidden' if i >= SHOWN else ''
    return (f'<a href="/img/kancelaria-{f}-1600.webp" class="geo-gallery__item"{extra}{hidden} data-w="{w}" data-h="{h}">'
            f'<img src="/img/kancelaria-{f}-800.webp" width="{w // 2}" height="{h // 2}" loading="lazy" alt="{alt}" /></a>')
gallery = '\n          '.join(photo(i, *p) for i, p in enumerate(PHOTOS))

towns_text = ', '.join(t[0] for t in TOWNS[:-1]) + ' a ' + TOWNS[-1][0]

html = f'''    <!-- ============ KDE POMÁHAM (3D mapa, generuje tools/make_map.py) ============ -->
    <section class="section geo-section" id="kde">
      <div class="container geo-wrap">
        <div class="geo-copy">
          <div class="section-head reveal">
            <span class="eyebrow">Kde pomáham</span>
            <h2>Orava, Žilina<br />aj celé Slovensko.</h2>
            <span class="script-accent">osobne aj online</span>
          </div>
          <p class="reveal">Klientov mám najmä z Dolného Kubína, Námestova, Tvrdošína, Trstenej, Žiliny a Bratislavy. Za klientmi chodím aj osobne, takže pomôžem komukoľvek zo Slovenska, osobne aj online.</p>
          <ul class="geo-towns reveal">
            <li>Dolný Kubín</li><li>Námestovo</li><li>Tvrdošín</li><li>Trstená</li><li>Žilina</li><li>Bratislava</li><li>osobne aj online po celom Slovensku</li>
          </ul>
          <a href="#kontakt" class="btn btn--dark reveal">Dohodnúť stretnutie <span aria-hidden="true">→</span></a>
        </div>

        <div class="geo reveal" role="img" aria-label="Mapa Oravy a Žiliny so zvýraznenými mestami {towns_text}">
          <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
            <defs>
              <radialGradient id="geoPin" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#f5c79b"/><stop offset=".55" stop-color="#e09a5b"/><stop offset="1" stop-color="#b8743a"/></radialGradient>
              <linearGradient id="geoTree" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4fae6a"/><stop offset="1" stop-color="#1f7a43"/></linearGradient>
            </defs>
          </svg>
          <div class="geo__scene">
            <div class="geo__plane">
            {ground}
            {chr(10).join("            " + o for o in objs).lstrip()}
            </div>
          </div>
        </div>
        <div class="geo-office reveal">
          <div>
            <span class="eyebrow">Kancelária</span>
            <h3>Tu sa stretneme</h3>
          </div>
          <p>Na osobné stretnutie vás pozvem do kancelárie MeruCompany. Pokojné prostredie, kde si všetko v kľude prejdeme. Kliknite na fotku a pozrite sa dnu.</p>
        </div>
        <div class="geo-gallery reveal" data-lightbox>
          {gallery}
        </div>
      </div>
    </section>
'''

os.makedirs('tools/partials', exist_ok=True)
open('tools/partials/mapa.html', 'w').write(html)
print('mapa.html', len(html))
