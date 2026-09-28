import numpy as np, json, base64, io
from PIL import Image
from scipy import ndimage as ndi

h = np.load('/tmp/near_h.npy').astype(np.float64)
Lr = np.load('/tmp/layers.npz')
feat = json.load(open('/tmp/features.json'))
water, green, sand, tees = Lr['water'], Lr['green'], Lr['sand'], Lr['tees']
edt = ndi.distance_transform_edt
log = {}

# greens: DEM only, extra smoothing (no invented undulation)
wg = ndi.gaussian_filter(ndi.binary_dilation(green, iterations=3).astype(float), 2.0)
h = h*(1-wg) + ndi.gaussian_filter(h, 3.0)*wg

# tees: flatten each pad to its median + 0.35 m, 2.5 m ramp
lab, n = ndi.label(tees)
for k in range(1, n+1):
    m = lab == k
    lvl = float(np.median(h[m])) + 0.35
    d = edt(~m)
    w = np.clip(1 - d/2.5, 0, 1); w = w*w*(3-2*w)
    h = h*(1-w) + lvl*w
log['tee_pads'] = int(n)

# bunkers: depressed floor + raised lip (lip taller on the side facing play is not modelled in v1)
din = edt(sand); dout = edt(~sand)
depth = 0.75*np.clip(din/2.5, 0, 1)**0.7
lip = 0.28*np.clip(1 - dout/1.6, 0, 1)*(~sand)
h = h - depth*sand + lip

# ponds: flat surface level per component, bed slopes down from shore
wl, wn = ndi.label(water)
levels = []
for k in range(1, wn+1):
    m = wl == k
    if m.sum() < 30: continue
    ring = ndi.binary_dilation(m, iterations=4) & ~ndi.binary_dilation(m, iterations=1)
    lvl = float(np.percentile(h[ring], 12)) - 0.30
    d = edt(m)
    bed = lvl - 0.25 - np.minimum(d*0.35, 2.5)
    h = np.where(m, np.minimum(h, bed), h)
    # keep banks just above water
    near_ring = ndi.binary_dilation(m, iterations=2) & ~m
    h = np.where(near_ring, np.maximum(h, lvl+0.12), h)
    jj, ii = np.nonzero(m)
    levels.append(dict(id=k, level=round(lvl, 2), x0=int(ii.min())-420-2, x1=int(ii.max())-420+2,
                       z0=int(jj.min())-350-2, z1=int(jj.max())-350+2))
h = ndi.gaussian_filter(h, 0.6)
log['ponds'] = levels
np.save('/tmp/near_final.npy', h.astype(np.float32))
json.dump(log, open('/tmp/final_log.json', 'w'), indent=1)
print('ponds', len(levels), 'h range', h.min(), h.max())
