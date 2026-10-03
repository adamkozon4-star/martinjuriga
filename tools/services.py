# Zoznam služieb pre menu a pätičku: (slug, názov, podnadpis, ikona).
# Služba má podstránku, keď existuje tools/pages/<slug>.html, inak odkaz vedie na sekciu Služby.
import os
PAGES_DIR = os.path.join(os.path.dirname(__file__), 'pages')
def has_page(slug):
    return os.path.exists(os.path.join(PAGES_DIR, slug + '.html'))
ICONS = {
 'home': '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 'refi': '<path d="M4 12a8 8 0 0 1 14-5.3L20 9M20 12a8 8 0 0 1-14 5.3L4 15M20 4v5h-5M4 20v-5h5"/>',
 'invest': '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
 'kids': '<path d="M12 21v-9M12 12C12 8 9 5 4 5c0 4 3 7 8 7zM12 10c0-3 2-6 7-6 0 4-3 6-7 6z"/>',
 'pension': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'life': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'property': '<path d="M3 12a9 9 0 0 1 18 0zM12 12v6a2 2 0 0 1-4 0"/>',
 'plan': '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
}
SERVICES = [
 ('hypoteky-a-uvery', 'Hypotéky a úvery', 'Kúpa, výstavba, rekonštrukcia', 'home'),
 ('refinancovanie', 'Refinancovanie', 'Koniec fixácie, nižšia splátka', 'refi'),
 ('investovanie', 'Investovanie', 'Pravidelne aj jednorazovo', 'invest'),
 ('sporenie-pre-deti', 'Sporenie pre deti', 'Štart do samostatného života', 'kids'),
 ('dochodok', 'Dôchodok', 'II. a III. pilier', 'pension'),
 ('zivotne-poistenie', 'Životné poistenie', 'Istota pre vás aj rodinu', 'life'),
 ('majetkove-poistenie', 'Majetkové poistenie', 'Byt, dom a domácnosť', 'property'),
 ('financny-plan', 'Finančný plán', 'Všetky financie v jednom pláne', 'plan'),
]
def href(slug, home):
    return f'/{slug}/' if has_page(slug) else ('#sluzby' if home else '/#sluzby')
def icon(k, cls='nav__ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg>'
def nav(home, current=None):
    pre = '' if home else '/'
    cur = ' aria-current="page"'
    items = '\n'.join(
        f'            <a href="{href(s,home)}" class="nav__item"{cur if s==current else ""}>{icon(i)}<span><strong>{n}</strong><small>{sub}</small></span></a>'
        for s,n,sub,i in SERVICES)
    return f'''      <nav class="nav" aria-label="Hlavná navigácia">
        <div class="nav__drop">
          <button type="button" class="nav__toggle" aria-expanded="false" aria-controls="nav-sluzby">Služby <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
          <div class="nav__menu" id="nav-sluzby">
{items}
            <a href="{pre}#sluzby" class="nav__all">Prehľad všetkých služieb <span aria-hidden="true">→</span></a>
          </div>
        </div>
        <a href="{pre}#o-mne">O mne</a>
        <a href="{pre}#faq">Otázky</a>
      </nav>'''
def footer_services(home):
    return '\n'.join(f'          <a href="{href(s,home)}">{n}</a>' for s,n,_,_ in SERVICES)
