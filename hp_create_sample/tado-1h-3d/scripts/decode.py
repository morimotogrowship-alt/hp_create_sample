import numpy as np
from PIL import Image
def dem(f):
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.int64)
    x = a[..., 0]*65536 + a[..., 1]*256 + a[..., 2]
    h = np.where(x < 2**23, x*0.01, (x-2**24)*0.01).astype(np.float64)
    h[x == 2**23] = np.nan
    return h
