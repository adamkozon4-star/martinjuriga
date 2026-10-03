"""Jednorazové prefarbenie webu z modrej palety na oranžovú (podľa prezentácie MeruCompany).

Hlavné farby sú zadané presne, ostatné modré a studené sivé tóny sa prepočítajú:
odtieň sa otočí do oranžovej, svetlosť ostane rovnaká.
Spúšťa sa z koreňa repozitára:  python3 tools/recolor.py
"""
import colorsys, glob, re

EXACT = {
    '2f62ff': 'e09a5b',  # hlavná akcentová
    '6b92ff': 'f0b47c',  # svetlejšia akcentová
    '1a3fd6': 'b8743a',  # tmavšia akcentová
    '8fb0ff': 'f5c79b',
    '4d7bff': 'e5a368',
    '0b1020': '1c1c1c',  # text v kartách
    '111830': '262626',
    '030305': '161616',  # pätička
}
EXACT_RGB = {'47, 98, 255': '224, 154, 91', '11, 16, 32': '20, 20, 20', '5, 7, 12': '22, 22, 22', '122, 150, 210': '190, 150, 112'}


def shift(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    deg = h * 360
    if s < 0.04 or not (190 <= deg <= 265):
        return None  # neutrálne alebo nie modré farby nechávame
    if s > 0.6 and 0.3 < l < 0.85:
        s *= 0.72  # sýta modrá -> tlmená oranžová ako v predlohe
    else:
        s *= 0.55  # studené sivé -> teplé sivé
    r2, g2, b2 = colorsys.hls_to_rgb(28 / 360, l, s)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def hex_sub(m):
    raw = m.group(1)
    if len(raw) == 3:
        return m.group(0)
    low = raw.lower()
    if low in EXACT:
        return '#' + EXACT[low]
    out = shift(int(low[0:2], 16), int(low[2:4], 16), int(low[4:6], 16))
    return m.group(0) if out is None else '#%02x%02x%02x' % out


def rgba_sub(m):
    key = f'{m.group(2)}, {m.group(3)}, {m.group(4)}'
    if key in EXACT_RGB:
        return f'{m.group(1)}({EXACT_RGB[key]}{m.group(5)}'
    out = shift(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return m.group(0) if out is None else f'{m.group(1)}({out[0]}, {out[1]}, {out[2]}{m.group(5)}'


def recolor(text):
    text = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', hex_sub, text)
    text = re.sub(r'(rgba?)\((\d+),\s*(\d+),\s*(\d+)(\s*[,)])', rgba_sub, text)
    # farby zakódované v data: URL (napr. vzor v pozadí úvodu)
    return re.sub(r'%23([0-9a-fA-F]{6})', lambda m: hex_sub(re.match(r'#(\w+)', '#' + m.group(1))).replace('#', '%23'), text)


if __name__ == '__main__':
    files = ['style.css', 'index.html', 'ochrana-osobnych-udajov.html', 'main.js', 'api/contact.js'] + \
        glob.glob('tools/*.py') + glob.glob('tools/glass/*.svg') + glob.glob('tools/partials/*.html') + glob.glob('tools/pages/*.html')
    for f in files:
        if f.endswith('recolor.py'):
            continue
        s = open(f).read()
        t = recolor(s)
        if t != s:
            open(f, 'w').write(t)
            print('prefarbené', f)
