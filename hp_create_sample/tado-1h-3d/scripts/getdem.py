from geo import *
import subprocess, math, sys
lat0 = 35.1254
mlat = 111000; mlon = 111000 * math.cos(math.radians(lat0))
S, N = 35.12444 - 200/mlat - 0.0005, 35.12637 + 200/mlat + 0.0005
W, E = 136.59397 - 200/mlon - 0.0005, 136.59813 + 200/mlon + 0.0005
print('bbox', S, N, W, E)
for layer, z in [('dem5a_png', 15), ('dem5b_png', 15), ('dem5c_png', 15), ('dem_png', 14)]:
    x0, y0 = px(W, N, z); x1, y1 = px(E, S, z)
    res = []
    for x in range(int(x0//256), int(x1//256)+1):
        for y in range(int(y0//256), int(y1//256)+1):
            f = f'dem/{layer}_{z}_{x}_{y}.png'
            r = subprocess.run(['curl', '-sS', '--max-time', '30', '-o', f, '-w', '%{http_code}',
                                f'https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.png'],
                               capture_output=True, text=True)
            res.append((x, y, r.stdout))
    print(layer, z, res)
