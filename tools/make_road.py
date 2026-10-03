"""Vygeneruje tools/partials/cesta.html: 3D cestu so štyrmi krokmi nad zoznamom .steps.

Cesta sa pri scrollovaní vyfarbuje (premenná --p z main.js) a dlaždice sa postupne nadvihnú.
Spúšťa sa z koreňa repozitára:  python3 tools/make_road.py
"""
W, H = 1000, 360
STOPS = [(125, 210), (375, 140), (625, 220), (875, 140)]
ROAD = 'M-20 250C40 240 70 214 125 210S300 140 375 140 540 222 625 220 800 140 875 140 1000 110 1030 100'


def tube(d, w=12):
    return (f'<path d="{d}" class="g-tube-edge" stroke-width="{w}"/><path d="{d}" class="g-tube" stroke-width="{w - 4}"/>'
            f'<path d="{d}" class="g-core" stroke-width="2.5"/>')


SPRITES = [
    # rozhovor
    '<path d="M18 30a14 14 0 0 1 14-14h46a14 14 0 0 1 14 14v24a14 14 0 0 1-14 14H48L30 82V68a14 14 0 0 1-12-14z" class="g-body"/>'
    '<circle cx="40" cy="42" r="5" class="g-core-fill"/><circle cx="55" cy="42" r="5" class="g-core-fill"/><circle cx="70" cy="42" r="5" class="g-core-fill"/>'
    '<path d="M28 26v22" class="g-shine"/>',
    # analýza: stĺpce a lupa
    '<rect x="16" y="58" width="18" height="40" rx="5" class="g-body"/><rect x="40" y="40" width="18" height="58" rx="5" class="g-body"/>'
    '<rect x="64" y="26" width="18" height="72" rx="5" class="g-core-fill"/>' + tube('M76 44a18 18 0 1 0 36 0a18 18 0 1 0-36 0', 12)
    + tube('M106 58l12 14', 12),
    # plán: dokument
    '<path d="M24 12h48l20 20v66H24z" class="g-body"/><path d="M72 12v20h20" class="g-inner"/>'
    '<path d="M36 46h40M36 60h40M36 74h24" class="g-core" stroke-width="5"/><circle cx="86" cy="88" r="16" class="g-core-fill"/>'
    '<path d="M79 88l5 5 9-10" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M32 20v70" class="g-shine"/>',
    # podpis: kľúč
    tube('M20 44a20 20 0 1 0 40 0a20 20 0 1 0-40 0', 16) + tube('M60 44h46M92 44v16M104 44v12', 14),
]


def pct(x, y):
    return f'left:{x / W * 100:.2f}%;top:{y / H * 100:.2f}%'


tiles = []
for i, ((x, y), sprite) in enumerate(zip(STOPS, SPRITES)):
    tiles.append(
        f'<div class="road__tile" style="{pct(x, y)}"><span class="road__obj"><span class="road__obj-in">'
        f'<b>0{i + 1}</b><svg class="glass" viewBox="0 0 120 110" aria-hidden="true">{sprite}</svg></span></span></div>')

html = f'''        <!-- 3D cesta krokov (generuje tools/make_road.py) -->
        <div class="road" aria-hidden="true">
          <div class="road__scene">
            <div class="road__plane">
              <svg class="road__ground" viewBox="0 0 {W} {H}" preserveAspectRatio="none">
                <defs><pattern id="roadGrid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#efe9e4" stroke-width="1"/></pattern></defs>
                <rect width="{W}" height="{H}" rx="40" fill="#fefdfc"/>
                <rect width="{W}" height="{H}" rx="40" fill="url(#roadGrid)" opacity=".8"/>
                <path d="M40 286c50-16 120-4 128 22s-40 40-90 36-64-44-38-58z" fill="#e5f3e8"/>
                <path d="M760 250c50-12 130 6 134 40s-60 50-110 44-70-70-24-84z" fill="#e5f3e8"/>
                <path d="M440 40c50-12 120 0 124 24s-60 34-100 30-60-42-24-54z" fill="#e5f3e8"/>
                <path d="{ROAD}" fill="none" stroke="#ffffff" stroke-width="46" stroke-linecap="round"/>
                <path d="{ROAD}" fill="none" stroke="#f1ece7" stroke-width="34" stroke-linecap="round"/>
                <path d="{ROAD}" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="14 14" stroke-linecap="round"/>
                <path d="{ROAD}" class="road__progress" pathLength="1" fill="none" stroke-width="34" stroke-linecap="round"/>
              </svg>
              {chr(10).join("              " + t for t in tiles).lstrip()}
            </div>
          </div>
        </div>
'''
open('tools/partials/cesta.html', 'w').write(html)
print('cesta.html', len(html))
