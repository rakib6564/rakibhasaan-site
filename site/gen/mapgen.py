# Builds a dot-matrix world map (equirectangular) from world-atlas topojson -> geo/mapdata.json
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
t = json.load(open(os.path.join(HERE, '..', 'geo', 'countries.json')))
sx, sy = t['transform']['scale']; tx, ty = t['transform']['translate']
arcs = []
for a in t['arcs']:
  x = y = 0; pts = []
  for dx, dy in a:
    x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
  arcs.append(pts)
def ring(idx):
  out = []
  for i in idx:
    p = arcs[i] if i >= 0 else arcs[~i][::-1]
    out.extend(p if not out else p[1:])
  return out
CLIENT = {'United States of America': 'US', 'Belgium': 'BE', 'United Kingdom': 'GB', 'Canada': 'CA', 'Germany': 'DE', 'Hungary': 'HU',
  'Slovakia': 'SK', 'Denmark': 'DK', 'Latvia': 'LV', 'Azerbaijan': 'AZ', 'Nigeria': 'NG', 'Uganda': 'UG', 'Vietnam': 'VN', 'New Zealand': 'NZ', 'Bangladesh': 'BD'}
shapes = []
for g in t['objects']['countries']['geometries']:
  polys = [g['arcs']] if g['type'] == 'Polygon' else g.get('arcs', [])
  for poly in polys:
    rings = [ring(r) for r in poly]
    xs = [p[0] for p in rings[0]]; ys = [p[1] for p in rings[0]]
    shapes.append((g['properties']['name'], (min(xs), min(ys), max(xs), max(ys)), rings))
def inside(lon, lat, r):
  c = False; n = len(r); j = n - 1
  for i in range(n):
    xi, yi = r[i]; xj, yj = r[j]
    if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi: c = not c
    j = i
  return c
W, STEP, LAT0, LAT1 = 1000, 5.0, 83.0, -56.0
H = round((LAT0 - LAT1) / 360 * W)
base, client, home = [], {}, []
row = 0; y = STEP / 2
while y < H:
  off = STEP / 2 if row % 2 else 0
  x = STEP / 4 + off
  while x < W:
    lon = x / W * 360 - 180; lat = LAT0 - y / W * 360
    for name, (a, b, c2, d), rings in shapes:
      if a <= lon <= c2 and b <= lat <= d and inside(lon, lat, rings[0]) and not any(inside(lon, lat, h) for h in rings[1:]):
        pt = 'M%g %gh0' % (round(x, 2), round(y, 2))
        code = CLIENT.get(name)
        if code == 'BD': home.append(pt)
        elif code: client.setdefault(code, []).append(pt)
        else: base.append(pt)
        break
    x += STEP
  y += STEP; row += 1
json.dump({'w': W, 'h': H, 'lat0': LAT0, 'base': ''.join(base), 'client': {k: ''.join(v) for k, v in client.items()}, 'home': ''.join(home)},
  open(os.path.join(HERE, '..', 'geo', 'mapdata.json'), 'w'))
print('H', H, 'base', len(base), {k: len(v) for k, v in client.items()}, 'home', len(home))
