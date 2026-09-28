import os, subprocess, numpy as np
from PIL import Image
from decode import dem
from geo import px

def fetch(layer, z, x, y):
    f = f'/tmp/dem/{layer}_{z}_{x}_{y}.png'
    if not os.path.exists(f) or os.path.getsize(f) < 100:
        code = '000'
        for i in range(4):
            r = subprocess.run(['curl', '-sS', '--max-time', '30', '-o', f, '-w', '%{http_code}',
                                f'https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.png'], capture_output=True, text=True)
            code = r.stdout
            if code in ('200', '404'): break
        if code != '200':
            if os.path.exists(f): os.remove(f)
            return None
    try: return dem(f)
    except Exception: return None

def mosaic(layer, z, W, S, E, N):
    x0, y0 = px(W, N, z); x1, y1 = px(E, S, z)
    tx0, ty0, tx1, ty1 = int(x0//256), int(y0//256), int(x1//256), int(y1//256)
    A = np.full(((ty1-ty0+1)*256, (tx1-tx0+1)*256), np.nan)
    got, miss = 0, 0
    for x in range(tx0, tx1+1):
        for y in range(ty0, ty1+1):
            t = fetch(layer, z, x, y)
            if t is None: miss += 1; continue
            got += 1
            A[(y-ty0)*256:(y-ty0+1)*256, (x-tx0)*256:(x-tx0+1)*256] = t
    info = dict(layer=layer, z=z, tiles_x=(tx0, tx1), tiles_y=(ty0, ty1), got=got, missing=miss)
    return A, tx0*256, ty0*256, info
