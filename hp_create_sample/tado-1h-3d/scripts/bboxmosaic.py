import sys, os, subprocess, math
from PIL import Image
from geo import px
# usage: layer ext z W S E N out
layer, ext, z = sys.argv[1], sys.argv[2], int(sys.argv[3])
W, S, E, N = map(float, sys.argv[4:8]); out = sys.argv[8]
x0, y0 = px(W, N, z); x1, y1 = px(E, S, z)
tx0, ty0, tx1, ty1 = int(x0//256), int(y0//256), int(x1//256), int(y1//256)
im = Image.new('RGB', ((tx1-tx0+1)*256, (ty1-ty0+1)*256))
os.makedirs('tiles', exist_ok=True)
miss = 0
for x in range(tx0, tx1+1):
    for y in range(ty0, ty1+1):
        f = f'tiles/{layer}_{z}_{x}_{y}.{ext}'
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            for i in range(4):
                r = subprocess.run(['curl', '-sS', '-f', '--max-time', '30', '-o', f,
                                    f'https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.{ext}'])
                if r.returncode == 0: break
        try:
            im.paste(Image.open(f).convert('RGB'), ((x-tx0)*256, (y-ty0)*256))
        except Exception:
            miss += 1
# crop to exact bbox
im = im.crop((int(x0-tx0*256), int(y0-ty0*256), int(x1-tx0*256), int(y1-ty0*256)))
im.save(out, quality=92)
print(out, im.size, 'missing', miss, 'global px origin', x0, y0)
