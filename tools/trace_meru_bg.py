"""Pozadie 1:1 podľa prezentácie MeruCompany: art-deco vzor + kresba hôr v jednom vektore (img/hory.svg).

Postup: vzor sa opakuje vodorovne každých 254 px, takže z celého obrázka sa poskladá jeden
čistý pás 254 × 890 (bez hôr), obkreslí sa do vektora a zopakuje cez celú šírku.
Vnútri hôr sa vzor skryje rovnako ako v predlohe. Hory sa obkreslia zvlášť.
Spúšťa sa z koreňa repozitára:  python3 tools/trace_meru_bg.py <obrázok z prezentácie>
Potrebuje:  pip install potracer numpy pillow scipy
"""
import sys
import numpy as np
import potrace
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = sys.argv[1]             # obrázok z prezentácie (vzor)
P = 254                       # vodorovná perióda vzoru
img = Image.open(SRC).convert('L')
W, H = img.size
g = np.array(img).astype(float)
# hory bez loga (img/hory.webp) určujú, kde vzor nie je
bright = np.array(Image.open('img/hory.webp').convert('L')).astype(float) > 40
bright_all = g > 40           # aj logo, aby sa nedostalo do vzoru
# obrys hôr: svetlé čiary zlepiť do plochy a vyplniť
sil = ndimage.binary_closing(bright, structure=np.ones((3, 3)), iterations=14)
sil = ndimage.binary_fill_holes(sil)
sil = ndimage.binary_opening(sil, iterations=3)
near = ndimage.binary_dilation(bright_all, iterations=6)

# 1) pás vzoru 254 × H: medián cez všetky opakovania mimo hôr
blur = np.array(Image.fromarray(g.astype('uint8')).filter(ImageFilter.GaussianBlur(1.0))).astype(float)
valid = ~(near | sil)
strip = np.full((H, P), np.nan)
cols = [[] for _ in range(P)]
for x0 in range(0, W, P):
    seg = blur[:, x0:x0 + P]
    v = valid[:, x0:x0 + P]
    s = np.where(v, seg, np.nan)
    cols.append(s)
stack = np.stack([np.pad(c, ((0, 0), (0, P - c.shape[1])), constant_values=np.nan) for c in cols[P:]])
strip = np.nanmedian(stack, axis=0)
# kde nie je žiadna vzorka, doplň z rovnakého miesta o periódu vyššie/nižšie (zriedkavé)
strip = np.where(np.isnan(strip), np.nanmedian(strip), strip)
lines = strip < 28.6

SCALE = 3
def trace(mask, scale=SCALE, turd=8):
    big = Image.fromarray((mask * 255).astype('uint8')).resize((mask.shape[1] * scale, mask.shape[0] * scale), Image.LANCZOS)
    m = np.array(big.filter(ImageFilter.GaussianBlur(1.2))) > 127
    plist = potrace.Bitmap(~m).trace(turdsize=turd, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=0.9, opticurve=True, opttolerance=0.3)
    f = lambda p: f'{p.x / scale:.1f} {p.y / scale:.1f}'
    out = []
    for c in plist:
        d = [f'M{f(c.start_point)}']
        for s in c.segments:
            d.append(f'L{f(s.c)}L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}')
        out.append(''.join(d) + 'Z')
    return ''.join(out)

pat = trace(lines)
import re
mountain = re.search(r' d="([^"]+)"', open('tools/hory-mountains.svg').read().split('<path',1)[1] if '<path' in open('tools/hory-mountains.svg').read() else '').group(1)
silpath = trace(sil, scale=1, turd=50)

uses = ''.join(f'<use href="#p" x="{x}"/>' for x in range(0, W + P, P))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
       f'<defs><path id="p" d="{pat}"/>'
       f'<mask id="m"><rect width="{W}" height="{H}" fill="#fff"/><path d="{silpath}" fill="#000"/></mask></defs>'
       f'<g fill="#191919" mask="url(#m)">{uses}</g>'
       f'<path fill="#333333" fill-rule="evenodd" d="{mountain}"/></svg>')
open('img/hory.svg', 'w').write(svg)
print('img/hory.svg', len(svg) // 1024, 'kB')
