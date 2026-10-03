"""Vygeneruje img/vzor.svg: art-deco vzor z prezentácie MeruCompany (kosoštvorce s pruhmi).

Vektor, takže je ostrý v akomkoľvek rozlíšení. Spúšťa sa z koreňa repozitára:
    python3 tools/make_pattern.py
"""
T = 300           # veľkosť dlaždice v px
H = T // 2
GAP = 28          # rozostup pruhov
COLOR = '#141414'
W = 3

def diamond(cx, cy, k):
    """Jeden kosoštvorec: horná polovica zvislé pruhy, dolné štvrtiny šikmé pruhy rovnobežné s dolnými hranami."""
    pts = f'{cx},{cy-H} {cx+H},{cy} {cx},{cy+H} {cx-H},{cy}'
    v = ''.join(f'M{x} {cy-H}V{cy}' for x in range(cx - H + GAP, cx + H, GAP))
    dl = ''.join(f'M{cx-H+d} {cy}l{H} {H}' for d in range(GAP // 2, H, GAP))
    dr = ''.join(f'M{cx+H-d} {cy}l{-H} {H}' for d in range(GAP // 2, H, GAP))
    clip_t = f'{cx-H},{cy} {cx},{cy-H} {cx+H},{cy}'
    clip_l = f'{cx-H},{cy} {cx},{cy} {cx},{cy+H}'
    clip_r = f'{cx},{cy} {cx+H},{cy} {cx},{cy+H}'
    return (f'<clipPath id="t{k}"><polygon points="{clip_t}"/></clipPath><clipPath id="l{k}"><polygon points="{clip_l}"/></clipPath><clipPath id="r{k}"><polygon points="{clip_r}"/></clipPath>',
            f'<path clip-path="url(#t{k})" d="{v}"/><path clip-path="url(#l{k})" d="{dl}"/><path clip-path="url(#r{k})" d="{dr}"/>'
            f'<polygon points="{pts}"/><path d="M{cx} {cy}V{cy+H}"/>')

defs, body = [], []
for k, (cx, cy) in enumerate([(0, 0), (T, 0), (0, T), (T, T), (H, H)]):
    d, b = diamond(cx, cy, k)
    defs.append(d); body.append(b)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}">'
       f'<defs>{"".join(defs)}</defs>'
       f'<g fill="none" stroke="{COLOR}" stroke-width="{W}" stroke-linecap="square">{"".join(body)}</g></svg>')
open('img/vzor.svg', 'w').write(svg)
print('img/vzor.svg', len(svg) // 1024, 'kB')
