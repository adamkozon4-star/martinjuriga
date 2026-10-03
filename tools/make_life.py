"""Vygeneruje 3D ostrovčeky pre sekciu „V akej životnej etape ste?“ (tools/partials/life-*.html).

Každý ostrovček je naklonená doska so sklenenými objektmi, pod ním odkazy na podstránky služieb.
Spúšťa sa z koreňa repozitára:  python3 tools/make_life.py && python3 tools/build_pages.py
"""
import os

GLASS_DIR = os.path.join(os.path.dirname(__file__), 'glass')

# (partial, farba, [(objekt, x %, y %, veľkosť)], [(odkaz, text)])
SCENES = [
    ('life-start', 'blue', [('chart', 50, 46, 'lg'), ('coins', 22, 64, 'sm'), ('shield', 79, 66, 'sm')],
     [('/investovanie/', 'Investovanie'), ('/zivotne-poistenie/', 'Poistenie príjmu'), ('/financny-plan/', 'Finančný plán')]),
    ('life-home', 'mint', [('house', 50, 44, 'lg'), ('arrows', 21, 66, 'sm'), ('umbrella', 80, 64, 'sm')],
     [('/hypoteky-a-uvery/', 'Hypotéka'), ('/refinancovanie/', 'Refinancovanie'), ('/majetkove-poistenie/', 'Poistenie domu')]),
    ('life-family', 'peach', [('heart', 50, 46, 'lg'), ('sprout', 21, 64, 'sm'), ('shield', 80, 66, 'sm')],
     [('/zivotne-poistenie/', 'Životné poistenie'), ('/sporenie-pre-deti/', 'Sporenie pre deti'), ('/financny-plan/', 'Revízia zmlúv')]),
    ('life-retire', 'lilac', [('hourglass', 50, 44, 'lg'), ('coins', 21, 66, 'sm'), ('chart', 80, 64, 'sm')],
     [('/dochodok/', 'II. a III. pilier'), ('/investovanie/', 'Dlhodobé investovanie'), ('/financny-plan/', 'Finančný plán')]),
]


def glass(name):
    s = open(os.path.join(GLASS_DIR, name + '.svg')).read()
    return s.replace('class="glass svc-stage__pct"', 'class="glass"')


os.makedirs('tools/partials', exist_ok=True)
for name, tone, objs, links in SCENES:
    items = '\n'.join(
        f'                <span class="isle__obj isle__obj--{size}" style="left:{x}%;top:{y}%"><span class="isle__obj-in">{glass(g)}</span></span>'
        for g, x, y, size in objs)
    chips = ''.join(f'<a href="{href}">{text} <span aria-hidden="true">→</span></a>' for href, text in links)
    html = f'''            <div class="life__visual" data-tone="{tone}">
              <div class="isle" aria-hidden="true"><div class="isle__plane">
{items}
              </div></div>
              <div class="life__chips">{chips}</div>
            </div>
'''
    open(f'tools/partials/{name}.html', 'w').write(html)
    print(name)
