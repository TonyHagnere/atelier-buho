#!/usr/bin/env python3
"""Dessine le plan du quartier de l'atelier à partir des données OpenStreetMap (rues réelles).

usage : python3 plan.py trait     (version claire, celle de v4/index.html)
        python3 plan.py sombre    (version sur fond sauge)
Écrit plan-STYLE.svg à côté de ce script : un fragment SVG à coller dans la page,
entre les repères <!-- CARTE --> et <!-- /CARTE -->, à la place du <svg> existant.

osm.json contient les rues, parcs et stations du quartier, téléchargés depuis
l'API Overpass d'OpenStreetMap le 15 novembre 2026. Licence ODbL : le crédit
« OpenStreetMap » est obligatoire. Il figure dans le pied de page de l'accueil."""
import json, math, os, sys
D = os.path.dirname(os.path.abspath(__file__)) + '/'
style = sys.argv[1] if len(sys.argv) > 1 else 'trait'
W, E, S, N = 2.3682, 2.3882, 48.8482, 48.8582
ATELIER = (48.8531990, 2.3794453)        # 58 rue Trousseau, géocodé (Nominatim)
VW = 1000.0
VH = VW * (N - S) / ((E - W) * math.cos(math.radians((N + S) / 2)))
def xy(lat, lon): return ((lon - W) / (E - W) * VW, (N - lat) / (N - S) * VH)

P = {
 'trait':  dict(ground='#ded8c6', road='#ece6d4', casing='#333322', casing_op=0.42, park='#85918a', park_op=0.30, water='#85918a', water_op=0.42,
                label='#4a4f44', own='#bcb794', ink='#333322', box='#ece6d4', box_stroke='#333322', dot='#333322', ring='#ece6d4', metro_fill='#ece6d4'),
 'sombre': dict(ground='#4a4f44', road='#ded8c6', casing=None, casing_op=0, park='#5f6559', park_op=1, water='#3b4037', water_op=1,
                label='#ded8c6', own='#b58f60', ink='#ece6d4', box='#ece6d4', box_stroke='none', dot='#b58f60', ring='#ece6d4', metro_fill='#4a4f44'),
}[style]

els = json.load(open(D + 'osm.json'))['elements']
WIDTH = {'primary': 16, 'primary_link': 12, 'secondary': 13, 'secondary_link': 10, 'tertiary': 10, 'tertiary_link': 8,
         'unclassified': 7, 'residential': 6.5, 'living_street': 5, 'pedestrian': 5}
ORDER = ['pedestrian', 'living_street', 'residential', 'unclassified', 'tertiary_link', 'tertiary', 'secondary_link', 'secondary', 'primary_link', 'primary']

def pts(e): return [xy(g['lat'], g['lon']) for g in e['geometry']]
def d_of(p, close=False):
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in p) + ('Z' if close else '')
def visible(p, m=60): return any(-m <= x <= VW + m and -m <= y <= VH + m for x, y in p)

roads = {k: [] for k in ORDER}; named = {}; parks = []; waters = []; areas = []; stations = {}
for e in els:
    t = e.get('tags', {})
    if e['type'] == 'node':
        stations[t.get('name', '')] = xy(e['lat'], e['lon']); continue
    if e['type'] != 'way' or 'geometry' not in e: continue
    p = pts(e)
    if not visible(p): continue
    if 'highway' in t:
        hw = t['highway']
        if hw == 'pedestrian' and t.get('area') == 'yes': areas.append(p); continue
        if hw in roads:
            roads[hw].append(p)
            if t.get('name'): named.setdefault(t['name'], []).append(p)
    elif 'leisure' in t and p[0] == p[-1]: parks.append(p)
    elif t.get('natural') == 'water': waters.append(p)

o = []
o.append(f'<svg viewBox="0 0 {VW:.0f} {VH:.0f}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" aria-hidden="true">')
o.append(f'<rect width="{VW:.0f}" height="{VH:.0f}" fill="{P["ground"]}"/>')
if parks:  o.append(f'<path d="{" ".join(d_of(p, True) for p in parks)}" fill="{P["park"]}" fill-opacity="{P["park_op"]}"/>')
if waters: o.append(f'<path d="{" ".join(d_of(p, True) for p in waters)}" fill="{P["water"]}" fill-opacity="{P["water_op"]}"/>')
o.append('<defs>')
for k in ORDER:
    if roads[k]: o.append(f'<path id="r-{k}" d="{" ".join(d_of(p) for p in roads[k])}"/>')
o.append('</defs>')
o.append('<g fill="none" stroke-linecap="round" stroke-linejoin="round">')
if P['casing']:
    for k in ORDER:
        if roads[k]: o.append(f'<use href="#r-{k}" stroke="{P["casing"]}" stroke-opacity="{P["casing_op"]}" stroke-width="{WIDTH[k] + 2.2:.1f}"/>')
if areas: o.append(f'<path d="{" ".join(d_of(p, True) for p in areas)}" fill="{P["road"]}" stroke="none"/>')
for k in ORDER:
    if roads[k]: o.append(f'<use href="#r-{k}" stroke="{P["road"]}" stroke-width="{WIDTH[k]:.1f}"/>')
# la rue de l'atelier, légèrement soulignée
if 'Rue Trousseau' in named:
    o.append(f'<path d="{" ".join(d_of(p) for p in named["Rue Trousseau"])}" stroke="{P["own"]}" stroke-width="6.5"/>')
o.append('</g>')

# --- Noms de rues, posés le long du tracé
def chain(ways):
    ways = [list(w) for w in ways]
    ways.sort(key=lambda w: -sum(math.dist(a, b) for a, b in zip(w, w[1:])))
    c = ways.pop(0)
    changed = True
    while changed and ways:
        changed = False
        for w in list(ways):
            for cand in (w, w[::-1]):
                if math.dist(c[-1], cand[0]) < 3: c = c + cand[1:]; ways.remove(w); changed = True; break
                if math.dist(c[0], cand[-1]) < 3: c = cand[:-1] + c; ways.remove(w); changed = True; break
            if changed: break
    return c
def inside(c, m=25):
    keep = [p for p in c if m <= p[0] <= VW - m and m <= p[1] <= VH - m]
    return keep
LABELS = [('Rue du Faubourg Saint-Antoine', 'Rue du Faubourg St-Antoine', (625, 590), 13), ('Avenue Ledru-Rollin', 'Avenue Ledru-Rollin', (545, 215), 13),
          ('Rue de Charonne', 'Rue de Charonne', (735, 330), 10), ('Rue de la Roquette', 'Rue de la Roquette', (330, 215), 10), ('Boulevard Voltaire', 'Boulevard Voltaire', (745, 160), 13)]
o.append(f'<g font-family="Manrope, sans-serif" font-weight="500" font-size="13.5" letter-spacing="2.4" fill="{P["label"]}" stroke="{P["ground"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke" style="text-transform:uppercase">')
for i, (name, text, pos, w) in enumerate(LABELS):
    if name not in named: continue
    c = inside(chain(named[name]))
    if len(c) < 2: continue
    dx, dy = c[-1][0] - c[0][0], c[-1][1] - c[0][1]
    if (abs(dx) >= abs(dy) and dx < 0) or (abs(dx) < abs(dy) and dy > 0): c = c[::-1]
    length = sum(math.dist(a, b) for a, b in zip(c, c[1:]))
    need = len(text) * 13.5 * 0.92
    if length < need * 1.05: continue
    o.append(f'<path id="n-{i}" d="{d_of(c)}" fill="none" stroke="none"/>')
    acc, best, off = 0.0, 1e9, 0.0
    for a, b in zip(c, c[1:]):
        seg = math.dist(a, b)
        for k in range(11):
            q = (a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10)
            dd = math.dist(q, pos)
            if dd < best: best, off = dd, acc + seg * k / 10
        acc += seg
    cls = ' class="d-only"' if name == 'Rue de la Roquette' else ''
    o.append(f'<text{cls} dy="-{w / 2 + 6:.0f}"><textPath href="#n-{i}" startOffset="{off:.0f}" text-anchor="middle">{text}</textPath></text>')
o.append('</g>')

# --- Stations de métro
o.append(f'<g font-family="Manrope, sans-serif" font-size="17" fill="{P["ink"]}" stroke="{P["ground"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke">')
for name, label, side in [('Ledru-Rollin', 'Ledru-Rollin', 'bl'), ('Faidherbe — Chaligny', 'Faidherbe-Chaligny', 'bl'), ('Bastille', 'Bastille', 'r'), ('Charonne', 'Charonne', 'r')]:
    if name not in stations: continue
    x, y = stations[name]
    o.append('<g class="d-only">' if name in ('Charonne', 'Bastille') else '<g>')
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11.5" fill="{P["metro_fill"]}" stroke="{P["ink"]}" stroke-width="1.5" paint-order="normal"/>')
    o.append(f'<text x="{x:.1f}" y="{y + 5.2:.1f}" text-anchor="middle" font-weight="600" font-size="13.5" stroke="none">M</text>')
    if side == 'r': o.append(f'<text x="{x + 19:.1f}" y="{y + 6.5:.1f}">{label}</text>')
    elif side == 'l': o.append(f'<text x="{x - 19:.1f}" y="{y + 6.5:.1f}" text-anchor="end">{label}</text>')
    else: o.append(f'<text x="{x + 12:.1f}" y="{y + 34:.1f}" text-anchor="end">{label}</text>')
    o.append('</g>')
o.append('</g>')

# --- L'atelier
ax, ay = xy(*ATELIER)
bx, by, bw, bh = ax + 30, ay + 26, 276, 78
o.append(f'<path d="M{ax:.1f} {ay:.1f}L{bx:.1f} {by:.1f}" stroke="{P["dot"]}" stroke-width="1.4" fill="none"/>')
o.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw}" height="{bh}" fill="{P["box"]}" stroke="{P["box_stroke"]}" stroke-width="1.1"/>')
o.append(f'<text x="{bx + 18:.1f}" y="{by + 36:.1f}" font-family="Fraunces, Georgia, serif" font-weight="500" font-size="28" fill="#333322">Atelier BUHO</text>')
o.append(f'<text x="{bx + 18:.1f}" y="{by + 61:.1f}" font-family="Manrope, sans-serif" font-size="16" fill="#4a4f44">58 rue Trousseau, Paris 11e</text>')
o.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="10.5" fill="{P["dot"]}" stroke="{P["ring"]}" stroke-width="3"/>')

# --- Échelle (200 m)
m200 = 200 / (((E - W) * math.cos(math.radians((N + S) / 2)) * 111320) / VW)
sx, sy = 34, VH - 34
o.append('<g class="d-only">')
o.append(f'<path d="M{sx} {sy - 6}V{sy}H{sx + m200:.1f}V{sy - 6}" fill="none" stroke="{P["ink"]}" stroke-width="1.4"/>')
o.append(f'<text x="{sx + m200 + 10:.1f}" y="{sy + 1}" font-family="Manrope, sans-serif" font-size="15.5" fill="{P["ink"]}" stroke="{P["ground"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke">200 m</text>')
o.append('</g>')
o.append('</svg>')
svg = '\n'.join(o)
open(D + f'plan-{style}.svg', 'w', encoding='utf-8').write(svg)
print(style, f'{len(svg) / 1024:.0f} Ko', f'viewBox {VW:.0f}x{VH:.0f}', 'atelier', f'{ax:.0f},{ay:.0f}', 'rues nommées dessinées:', sum(1 for l in LABELS if l[0] in named))
