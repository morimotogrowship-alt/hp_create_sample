import numpy as np
from PIL import Image
from scipy import ndimage as ndi

im = np.asarray(Image.open('aer05.png')).astype(np.float32)/255
R, G, B = im[..., 0], im[..., 1], im[..., 2]
V = im.max(-1); mn = im.min(-1); S = (V-mn)/(V+1e-6)
L = (R+G+B)/3
# local texture
Lb = ndi.uniform_filter(L, 5); tex = np.sqrt(np.maximum(ndi.uniform_filter(L*L, 5)-Lb*Lb, 0))
exg = 2*G-R-B          # excess green
np.savez_compressed('feat.npz', L=L, S=S, tex=tex, exg=exg, R=R, G=G, B=B)

def show(pt):
    x, z = pt; i, j = int((z+350)*2), int((x+420)*2)
    return dict(RGB=(im[i-2:i+3, j-2:j+3].reshape(-1, 3).mean(0)*255).round(), tex=round(float(tex[i, j]), 3), exg=round(float(exg[i, j]), 3))
# sample points in local coords (x east, z south), from 1m image px (px-420, py-350)
pts = {'fairway': (450-420, 305-350), 'rough': (480-420, 270-350), 'bunker': (423-420, 318-350), 'water': (490-420, 470-350),
       'forest': (700-420, 100-350), 'path': (455-420, 360-350), 'green': (612-420, 452-350), 'forest_shadow': (650-420, 330-350),
       'autumn': (275-420, 305-350), 'shadow_on_rough': (330-420, 300-350)}
for k, p in pts.items(): print(k, show(p))
