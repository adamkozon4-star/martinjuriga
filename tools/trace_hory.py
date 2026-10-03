"""Prekreslí kresbu hôr (img/hory.webp) do vektora img/hory.svg, aby bola ostrá v akomkoľvek rozlíšení.

Spúšťa sa z koreňa repozitára:  python3 tools/trace_hory.py
Potrebuje:  pip install potracer numpy pillow
"""
import numpy as np
import potrace
from PIL import Image, ImageFilter

SRC, OUT = 'img/hory.webp', 'img/hory.svg'
SCALE = 3          # pred obkreslením zväčšiť, aby boli krivky hladké
THRESHOLD = 40     # čiary (#333) sú svetlejšie ako pozadie (#1e1e1e)
COLOR = '#333333'

img = Image.open(SRC).convert('L')
w, h = img.size
big = img.resize((w * SCALE, h * SCALE), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
mask = np.array(big) > THRESHOLD

bmp = potrace.Bitmap(~mask)  # potracer obkresľuje hodnoty False
plist = bmp.trace(turdsize=6, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.3)

f = lambda p: f'{p.x / SCALE:.1f} {p.y / SCALE:.1f}'
parts = []
for curve in plist:
    d = [f'M{f(curve.start_point)}']
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f'L{f(seg.c)}L{f(seg.end_point)}')
        else:
            d.append(f'C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}')
    parts.append(''.join(d) + 'Z')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">'
       f'<path fill="{COLOR}" fill-rule="evenodd" d="{"".join(parts)}"/></svg>')
open(OUT, 'w').write(svg)
print(OUT, len(plist), 'tvarov', len(svg) // 1024, 'kB')
