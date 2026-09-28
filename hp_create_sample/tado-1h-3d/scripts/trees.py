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
