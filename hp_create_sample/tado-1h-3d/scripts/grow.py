import numpy as np
from PIL import Image
from scipy import ndimage as ndi

im = np.asarray(Image.open('/tmp/aer05.png')).astype(np.float32)/255
sm = ndi.gaussian_filter(im, (1.2, 1.2, 0))
H, W = im.shape[:2]

def P(p):  # 1m-image px (x,y) -> 0.5m array index (i,j)
    return int(p[1]*2), int(p[0]*2)

def grow(seeds, tol=0.06, close=3, maxr=None, within=None, iters=3, fill=True):
    """seeds: list of 1m px points. Returns bool mask at 0.5m."""
    ij = [P(s) for s in seeds]
    ref = np.mean([sm[i-2:i+3, j-2:j+3].reshape(-1, 3).mean(0) for i, j in ij], 0)
    for _ in range(iters):
        d = np.sqrt(((sm-ref)**2).sum(-1))
        m = d < tol
        if within is not None: m &= within
        lab, n = ndi.label(m)
        ids = {lab[i, j] for i, j in ij} - {0}
        reg = np.isin(lab, list(ids))
        if reg.sum() == 0: break
        ref = sm[reg].mean(0)
    if close: reg = ndi.binary_closing(reg, iterations=close)
    if fill: reg = ndi.binary_fill_holes(reg)
    reg = ndi.binary_opening(reg, iterations=1)
    return reg

def poly_mask(pts):
    from PIL import ImageDraw
    img = Image.new('L', (W, H), 0)
    ImageDraw.Draw(img).polygon([(x*2, y*2) for x, y in pts], fill=1)
    return np.asarray(img).astype(bool)

def overlay(masks, name, crop=None, scale=1):
    base = (im*255).astype(np.uint8).copy()
    cols = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 0, 255), (255, 128, 0), (0, 255, 0), (255, 255, 255)]
    out = base.astype(np.float32)
    for k, m in enumerate(masks):
        edge = m & ~ndi.binary_erosion(m, iterations=1)
        c = np.array(cols[k % len(cols)], np.float32)
        out[m] = out[m]*0.75 + c*0.25
        out[edge] = c
    img = Image.fromarray(out.astype(np.uint8))
    if crop: img = img.crop(tuple(v*2 for v in crop))
    if scale != 1: img = img.resize((int(img.size[0]*scale), int(img.size[1]*scale)))
    img.save(name)
