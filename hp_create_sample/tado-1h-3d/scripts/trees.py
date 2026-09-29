import numpy as np, json
from scipy import ndimage as ndi
rng = np.random.default_rng(7)
L = np.load('/tmp/layers.npz')
forest = L['forest']
block = L['fair'] | L['green'] | L['sand'] | L['water'] | L['path'] | L['tees'] | L['collar']
free = forest & ~ndi.binary_dilation(block, iterations=4)
# manual corrections (user-confirmed ground truth): no trees in these zones (1 m image px coords)
from PIL import Image, ImageDraw
NO_TREE = [
    # tee complex between REG and FRONT: stone path, cart path and lawn (the dark area is a cast shadow)
    [(262, 240), (282, 234), (300, 238), (318, 250), (338, 258), (345, 268), (335, 276), (310, 274), (290, 272), (272, 266), (262, 256)],
]
_img = Image.new('L', (841, 701), 0); _d = ImageDraw.Draw(_img)
for p in NO_TREE: _d.polygon(p, fill=1)
free &= ~(np.asarray(_img) > 0)
lab, n = ndi.label(free)
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n+1))
trees = []
# isolated trees (small blobs in the rough) -> one tree each
for k, s in enumerate(sizes, 1):
    if 12 <= s < 160:
        jj, ii = np.nonzero(lab == k)
        trees.append((ii.mean()-420, jj.mean()-350, min(20, 7+np.sqrt(s)*0.9), 'iso'))
# forest stands: jittered grid ~5.5 m
big = np.isin(lab, [k for k, s in enumerate(sizes, 1) if s >= 160])
sp = 5.5
for z in np.arange(-350, 350, sp):
    for x in np.arange(-420, 420, sp):
        px, pz = x + rng.uniform(-2, 2), z + rng.uniform(-2, 2)
        i, j = int(px+420), int(pz+350)
        if 0 <= i < 841 and 0 <= j < 701 and big[j, i]:
            trees.append((px, pz, rng.uniform(10, 19), 'forest'))
out = []
for x, z, h, kind in trees:
    r = rng.random()
    # species mix (broadleaf 0 = konara/sakura type, 1 = hinoki/sugi cone, 2 = akamatsu)
    sp_ = 0 if r < 0.55 else (1 if r < 0.85 else 2)
    out.append([round(float(x), 1), round(float(z), 1), sp_, round(float(h), 1), round(float(rng.uniform(0, 6.283)), 2)])
json.dump(out, open('/tmp/trees.json', 'w'))
print('trees', len(out), 'iso', sum(1 for t in trees if t[3] == 'iso'))

# ---------------------------------------------------------------------------
# Manual edits matched to the official drone video (2026-09-29)
# species: 0 broadleaf, 1 hinoki/sugi, 2 akamatsu, 3 low shrub / hedge, 4 metasequoia
# ---------------------------------------------------------------------------
def poly_mask(p):
    im = Image.new('L', (841, 701), 0); ImageDraw.Draw(im).polygon(p, fill=1); return np.asarray(im) > 0
def inside(m, x, z):
    i, j = int(round(x+420)), int(round(z+350)); return 0 <= i < 841 and 0 <= j < 701 and m[j, i]

# right (south-west) side of the hole 1 fairway: a single row of tall trees along the cart path
FW_RIGHT = [(268, 276), (300, 284), (360, 304), (420, 328), (470, 350), (520, 373), (562, 398), (602, 424),
            (596, 442), (556, 422), (506, 397), (460, 380), (410, 360), (350, 337), (300, 320), (262, 302)]
# left of the tee complex: gazebo, low hedges and garden shrubs (no tall trees in the video)
TEE_LEFT = [(200, 214), (240, 211), (276, 221), (300, 231), (332, 244), (332, 256), (300, 251), (262, 241), (230, 245), (204, 245)]
# rock garden with flowers on the slope right of the forward tees
ROCKERY = [(298, 272), (318, 270), (334, 280), (330, 292), (306, 292), (296, 284)]
mFW, mTL, mRK = poly_mask(FW_RIGHT), poly_mask(TEE_LEFT), poly_mask(ROCKERY)
out = [t for t in out if not (inside(mFW, t[0], t[1]) or inside(mTL, t[0], t[1]) or inside(mRK, t[0], t[1]))]

def peaks(canopy, min_sp):
    dt = ndi.distance_transform_edt(canopy)
    cand = np.argwhere((dt == ndi.maximum_filter(dt, size=5)) & (dt >= 1.2))
    cand = sorted(cand, key=lambda p: -dt[p[0], p[1]])
    pts = []
    for j, i in cand:
        if all((i-a)**2 + (j-b)**2 >= min_sp**2 for a, b, _ in pts): pts.append((i, j, dt[j, i]))
    return pts

canopy = forest & ~ndi.binary_dilation(block, iterations=1)
n_fw = 0
mNear = np.zeros_like(mFW); mNear[:, :360] = True     # metasequoia only near the tees (video t=0-6s); round broadleaf trees further on (t=12-22s)
fw_pts = [(i, j, r, 4) for i, j, r in peaks(canopy & mFW & mNear, 8.0)] + [(i, j, r, 0) for i, j, r in peaks(canopy & mFW & ~mNear, 13.0)]
for i, j, r, sp_ in fw_pts:
    x, z = i-420.0, j-350.0
    h = float(np.clip(13 + r*1.8, 12, 24)) if sp_ == 4 else float(np.clip(9 + r*1.3, 8, 16))
    out.append([round(x, 1), round(z, 1), sp_, round(h, 1), round(float(rng.uniform(0, 6.283)), 2)]); n_fw += 1
n_sh = 0
for i, j, r in peaks((canopy | forest) & mTL, 3.5):
    out.append([round(i-420.0, 1), round(j-350.0, 1), 3, round(float(rng.uniform(1.4, 2.6)), 1), round(float(rng.uniform(0, 6.283)), 2)]); n_sh += 1
for k in range(14):
    x, z = rng.uniform(298, 332), rng.uniform(272, 291)
    if inside(mRK, x, z):
        out.append([round(x-420, 1), round(z-350, 1), 3, round(float(rng.uniform(0.7, 1.4)), 1), round(float(rng.uniform(0, 6.283)), 2)]); n_sh += 1
json.dump(out, open('/tmp/trees.json', 'w'))
print('after manual edits:', len(out), 'fw-right row', n_fw, 'shrubs', n_sh)
