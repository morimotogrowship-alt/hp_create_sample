import numpy as np, math
from PIL import Image
from local import *
from geo import px

def grid(res, pad=0):
    xs = np.arange(XMIN-pad, XMAX+pad+1e-6, res); zs = np.arange(ZMIN-pad, ZMAX+pad+1e-6, res)
    return xs, zs

def merc_coords(xs, zs, z):
    X, Z = np.meshgrid(xs, zs)
    lon = LON0 + X/MLON; lat = LAT0 - Z/MLAT
    n = 2**z
    gx = (lon+180)/360*n*256
    gy = (1-np.arcsinh(np.tan(np.radians(lat)))/math.pi)/2*n*256
    return gx, gy

def bilinear(img, fx, fy):
    h, w = img.shape[:2]
    fx = np.clip(fx, 0, w-1.001); fy = np.clip(fy, 0, h-1.001)
    x0 = np.floor(fx).astype(int); y0 = np.floor(fy).astype(int)
    tx = fx-x0; ty = fy-y0
    if img.ndim == 3: tx = tx[..., None]; ty = ty[..., None]
    a = img[y0, x0]; b = img[y0, x0+1]; c = img[y0+1, x0]; d = img[y0+1, x0+1]
    return (a*(1-tx)+b*tx)*(1-ty) + (c*(1-tx)+d*tx)*ty

if __name__ == '__main__':
    im = np.asarray(Image.open('near18.jpg')).astype(np.float32)
    ox, oy = 59016892.545524195, 26552376.85159966
    for res, name in [(0.5, 'aer05.png'), (1.0, 'aer1.jpg')]:
        xs, zs = grid(res)
        gx, gy = merc_coords(xs, zs, 18)
        out = bilinear(im, gx-ox, gy-oy)
        Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(name)
        print(name, out.shape)
