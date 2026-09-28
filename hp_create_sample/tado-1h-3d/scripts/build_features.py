import numpy as np, json
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from local import *

NX, NZ = 841, 701                        # 1 m grid, px (i=x+420, j=z+350)
def L(p): return (p[0]-420.0, p[1]-350.0)   # 1m image px -> local x,z

def poly(pts, width=None):
    img = Image.new('L', (NX, NZ), 0); d = ImageDraw.Draw(img)
    if width: d.line(pts, fill=255, width=width, joint='curve')
    else: d.polygon(pts, fill=255)
    return np.asarray(img) > 127

def down(m05):  # 0.5 m bool -> 1 m bool
    a = ndi.uniform_filter(m05.astype(float), 3)[::2, ::2]; return a > 0.5

def smooth(m, s=1.0): return ndi.gaussian_filter(m.astype(float), s) > 0.5

h1 = np.load('/tmp/h1masks.npz')
auto05 = np.load('/tmp/auto_cls.npy')
auto = np.zeros((NZ, NX), np.uint8)
for k in [1, 2, 5, 3]:
    auto[down(auto05 == k)] = k
gap = np.load('/tmp/near_gap.npy')
near = np.load('/tmp/near_h.npy')

# ---------- water: DEM5A gaps (= water bodies), cleaned ----------
lab, n = ndi.label(ndi.binary_opening(gap, iterations=1))
water = np.zeros_like(gap); ponds = []
for k in range(1, n+1):
    m = lab == k
    if m.sum() < 40: continue
    ring = ndi.binary_dilation(m, iterations=3) & ~ndi.binary_dilation(m, iterations=1)
    lvl = float(np.percentile(near[ring], 10)) - 0.35
    water |= m
    jj, ii = np.nonzero(m)
    ponds.append(dict(level=round(lvl, 2), cx=float(ii.mean()-420), cz=float(jj.mean()-350), area=int(m.sum())))
f05 = np.load('/tmp/feat.npz'); tex1 = ndi.uniform_filter(f05['tex'], 3)[::2, ::2]; L1 = ndi.uniform_filter(f05['L'], 3)[::2, ::2]
tex1 = ndi.gaussian_filter(tex1, 1.0)
cand = ndi.binary_dilation(water, iterations=4) & (tex1 < 0.022) & (L1 < 0.62) & (auto != 3)
w0 = cand | ndi.binary_erosion(water, iterations=2)
hl, hn = ndi.label(ndi.binary_fill_holes(w0) & ~w0)
hs = ndi.sum(np.ones_like(hl), hl, range(1, hn+1))
water = w0 | np.isin(hl, [i+1 for i, v in enumerate(hs) if v < 30])
water = ndi.binary_opening(water, iterations=2)
water = smooth(water, 1.6)
pond_id = ndi.label(water)[0]

# ---------- hole 1 ----------
corr = poly([(290, 250), (330, 245), (400, 250), (470, 270), (530, 300), (575, 340), (620, 390), (645, 440), (640, 480),
             (600, 485), (560, 450), (500, 400), (450, 360), (380, 318), (320, 300), (290, 285)])
fw1 = smooth(down(h1['fw']) & corr, 2.0)
green1 = poly([(603, 445), (615, 442), (627, 446), (633, 455), (631, 466), (622, 473), (609, 474), (600, 467), (598, 456)])
green1 = smooth(green1, 1.0)
tee_pads = {
    'FULL': [(210, 228), (228, 225), (231, 233), (229, 241), (212, 242), (209, 235)],
    'BACK': [(237, 229), (255, 228), (258, 236), (256, 245), (240, 245), (236, 237)],
    'REG': [(262, 244), (277, 242), (280, 250), (278, 259), (265, 260), (261, 252)],
    'FRONT': [(300, 259), (318, 259), (320, 265), (318, 271), (301, 271), (299, 265)],
    'LADIES': [(330, 265), (345, 265), (347, 271), (345, 277), (331, 277), (329, 271)],
}
tees = np.zeros((NZ, NX), bool)
for k, p in tee_pads.items(): tees |= poly(p)
bunk1 = np.zeros((NZ, NX), bool)
for b in h1['bk']: bunk1 |= down(b)
bunk1 = smooth(ndi.binary_dilation(bunk1, iterations=1), 1.0)

# ---------- generic layers ----------
bld = poly([(172, 98), (228, 98), (228, 192), (172, 192)])             # hotel block (excluded from sand/paved)
sand = (smooth(auto == 3, 0.8) & ~bld & ~water) | bunk1
turf = smooth(auto == 2, 1.5) & ~water & ~sand
fair = (turf | fw1) & ~green1 & ~tees & ~sand
_R = ndi.uniform_filter(f05['R'], 3)[::2, ::2]; _G = ndi.uniform_filter(f05['G'], 3)[::2, ::2]; _B = ndi.uniform_filter(f05['B'], 3)[::2, ::2]
_R, _G, _B = [ndi.gaussian_filter(c, 1.2) for c in (_R, _G, _B)]
dark = (_B > _G + 0.025) & (_B > _R + 0.02)          # bluish = in shade (cast shadow on grass OR shaded canopy)
dl, dn = ndi.label(ndi.binary_opening(dark, iterations=1)); dsz = ndi.sum(np.ones_like(dl), dl, range(1, dn+1))
shadow = dark & ~np.isin(dl, [i+1 for i, v in enumerate(dsz) if v >= 900])   # small shaded patches = cast shadows; large = shaded forest
forest = smooth((auto == 1) & ~shadow, 1.5) & ~water & ~fair & ~green1 & ~tees & ~sand

paths = {
    'h1_right': [(300, 262), (307, 282), (318, 292), (360, 317), (380, 329), (415, 342), (440, 350), (455, 360),
                 (475, 373), (487, 392), (497, 405), (505, 417), (520, 424), (535, 438), (552, 447), (570, 452),
                 (585, 480), (610, 488), (640, 482), (662, 462), (680, 447)],
    'h1_left': [(297, 252), (320, 258), (340, 256), (360, 250), (380, 238), (400, 230), (420, 229), (440, 232)],
    'pond_n': [(430, 405), (450, 420), (480, 424), (505, 422)],
}
path = np.zeros((NZ, NX), bool)
for k, p in paths.items(): path |= poly(p, width=3)
pv = smooth(auto == 5, 0.8) & ~bld
pl, pn = ndi.label(pv); psz = ndi.sum(np.ones_like(pl), pl, range(1, pn+1))
pv = np.isin(pl, [i+1 for i, v in enumerate(psz) if v >= 300])   # keep roads / parking, drop shadow speckles
path = (path | pv) & ~water & ~green1 & ~tees
path |= bld  # hotel footprint rendered as paved base
sand &= ~path
fair &= ~path
forest &= ~path
green_all = green1
collar = ndi.binary_dilation(green1, iterations=2) & ~green1 & ~sand & ~water
fair &= ~collar
cut1 = ndi.binary_dilation(fair, iterations=3) & ~fair & ~green1 & ~collar & ~tees & ~sand & ~water & ~path & ~forest

# ---------- centre line / yardage ----------
cl_px = [(220, 234), (300, 262), (370, 275), (430, 292), (480, 330), (520, 370), (560, 410), (600, 445), (615, 458)]
cl = [L(p) for p in cl_px]
def along(pts):
    d = [0.0]
    for a, b in zip(pts, pts[1:]): d.append(d[-1]+float(np.hypot(b[0]-a[0], b[1]-a[1])))
    return d
dl = along(cl)
tee_ll = {}
tee_xy = {k: L(tuple(np.mean(p, 0))) for k, p in tee_pads.items()}
for k, (x, z) in tee_xy.items():
    lon, lat = to_ll(x, z); tee_ll[k] = (round(lat, 6), round(lon, 6))
pin = L((616, 457))
lon, lat = to_ll(*pin)
feat = dict(
    tees={k: dict(x=v[0], z=v[1], lat=tee_ll[k][0], lon=tee_ll[k][1]) for k, v in tee_xy.items()},
    pin=dict(x=pin[0], z=pin[1], lat=round(lat, 6), lon=round(lon, 6)),
    centerline=cl, centerline_len_m=dl[-1], ponds=ponds,
    ob=[L(p) for p in [(360, 236), (400, 226), (440, 238), (480, 250), (515, 270), (545, 300), (572, 335), (598, 372), (625, 405), (650, 432), (668, 455)]],
    hotel=dict(poly=[L(p) for p in [(172, 98), (228, 98), (228, 192), (172, 192)]], h=22),
    paths={k: [L(p) for p in v] for k, v in paths.items()},
)
json.dump(feat, open('/tmp/features.json', 'w'), indent=1)
print('centerline length m', round(dl[-1], 1), 'yd', round(dl[-1]/0.9144, 1))
for k, (x, z) in tee_xy.items():
    print(k, tee_ll[k], 'straight to pin', round(np.hypot(pin[0]-x, pin[1]-z)/0.9144, 1), 'yd')
print('ponds', ponds)

np.savez_compressed('/tmp/layers.npz', water=water, fair=fair, green=green_all, collar=collar, tees=tees, sand=sand,
                    forest=forest, path=path, cut1=cut1, pond_id=pond_id, bunk1=bunk1)
# preview
pal = dict(forest=(34, 70, 34), cut1=(120, 160, 70), fair=(110, 190, 80), collar=(90, 200, 90), green=(60, 220, 110),
           tees=(40, 150, 200), sand=(245, 235, 200), path=(90, 90, 90), water=(40, 90, 170))
img = np.zeros((NZ, NX, 3), np.uint8); img[:] = (160, 150, 90)
lay = dict(forest=forest, cut1=cut1, fair=fair, collar=collar, green=green_all, tees=tees, sand=sand, path=path, water=water)
for k, c in pal.items(): img[lay[k]] = c
Image.fromarray(img).save('/tmp/layers.png')
