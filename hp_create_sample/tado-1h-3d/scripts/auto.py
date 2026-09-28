import numpy as np
from PIL import Image
from scipy import ndimage as ndi
f = np.load('/tmp/feat.npz'); L, S, tex, exg, R, G, B = [f[k] for k in 'L S tex exg R G B'.split()]
Ls = ndi.gaussian_filter(L, 1.5); texs = ndi.gaussian_filter(tex, 3)
Rs, Gs, Bs = [ndi.gaussian_filter(c, 1.5) for c in (R, G, B)]
exs = 2*Gs-Rs-Bs
# classes: 0 rough/grass, 1 forest, 2 mowed turf, 3 sand, 4 water, 5 paved
cls = np.zeros(L.shape, np.uint8)
forest = (texs > 0.045) | (Ls < 0.30)
turf = (exs > 0.035) & (texs < 0.03) & (Ls > 0.42)
sand = (Ls > 0.78) & (np.abs(Rs-Bs) < 0.08) & (texs < 0.04)
paved = (np.abs(Rs-Gs) < 0.03) & (np.abs(Gs-Bs) < 0.04) & (Ls > 0.30) & (Ls < 0.62) & (texs < 0.035) & ~turf
cls[forest] = 1
cls[turf & ~forest] = 2
cls[paved & ~forest] = 5
cls[sand] = 3
# cleanup: majority-ish smoothing
def clean(m, o=2, c=2): return ndi.binary_closing(ndi.binary_opening(m, iterations=o), iterations=c)
out = np.zeros_like(cls)
for k in [1, 2, 5, 3]:
    m = clean(cls == k, 1 if k in (3, 5) else 3, 2)
    out[m] = k
np.save('/tmp/auto_cls.npy', out)
pal = np.array([[196, 170, 120], [30, 70, 30], [110, 190, 90], [250, 240, 210], [40, 90, 160], [90, 90, 90]], np.uint8)
Image.fromarray(pal[out]).resize((L.shape[1]//2, L.shape[0]//2)).save('/tmp/auto_cls.png')
