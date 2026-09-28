import numpy as np, json, base64, io, math, sys
from PIL import Image
from scipy import ndimage as ndi
from local import *
from resample import bilinear

VERSION = sys.argv[1] if len(sys.argv) > 1 else '軽量版 v1（地形＋コース形状）'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/tmp/out.html'

def b64(a): return base64.b64encode(a.tobytes()).decode()
def png_uri(arr, fmt='PNG', q=85):
    buf = io.BytesIO(); Image.fromarray(arr).save(buf, fmt, **({'quality': q} if fmt == 'JPEG' else {'optimize': True}))
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(buf.getvalue()).decode()

# heights
h = np.load('/tmp/near_final.npy').astype(np.float64)
base = math.floor(h.min()) - 1
hu = np.round((h-base)*100).astype('<u2')
near = dict(nx=h.shape[1], nz=h.shape[0], x0=XMIN, z0=ZMIN, res=1, base=base, h=b64(hu))
mid = np.load('/tmp/mid_h.npy'); far = np.load('/tmp/far_h.npy')
midd = dict(n=mid.shape[0], ext=6000, res=30, h=b64(np.round(mid*10).astype('<i2')))
fard = dict(n=far.shape[0], ext=36000, res=200, h=b64(np.round(far*10).astype('<i2')))

# masks
L = np.load('/tmp/layers.npz')
def ch(m, s=0.7): return (np.clip(ndi.gaussian_filter(m.astype(float), s), 0, 1)*255).astype(np.uint8)
m1 = np.dstack([ch(L['fair']), ch(L['green']), ch(L['sand'])])
m2 = np.dstack([ch(L['water']), ch(L['tees']), ch(L['forest'], 1.0)])
m3 = np.dstack([ch(L['path'], 0.6), ch(L['cut1']), ch(L['collar'])])
aer = np.asarray(Image.open('/tmp/aer1.jpg'))

# mid / far aerial drapes resampled onto the local grid
def drape(fname, ox, oy, z, ext, npx):
    im = np.asarray(Image.open(fname)).astype(np.float32)
    xs = np.linspace(-ext, ext, npx)
    X, Z = np.meshgrid(xs, xs)
    lon = LON0 + X/MLON; lat = LAT0 - Z/MLAT; n = 2**z
    gx = (lon+180)/360*n*256 - ox; gy = (1-np.arcsinh(np.tan(np.radians(lat)))/math.pi)/2*n*256 - oy
    out = bilinear(im, gx, gy)
    return np.clip(out, 0, 255).astype(np.uint8)
import re
_o = open('/tmp/mid14_origin.txt').read().split()
midimg = drape('/tmp/mid14.jpg', float(_o[0]), float(_o[1]), 14, 6000, 1536)
farimg = drape('/tmp/far10.jpg', 230242.58240068035, 103425.57787622715, 10, 36000, 512)

def grade(img):
    import colorsys
    a = img.astype(np.float32)/255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); sat = (mx-mn)/(mx+1e-6)
    tan = np.clip((r-b)*4, 0, 1)*np.clip((r-g+0.08)*6, 0, 1)*np.clip(1-np.abs(mx-0.55)*2, 0, 1)
    tan = ndi.gaussian_filter(tan, 1.0)[..., None]
    lum = (0.3*r+0.59*g+0.11*b)[..., None]
    green = np.dstack([0.55*lum[..., 0]+0.02, 0.85*lum[..., 0]+0.06, 0.40*lum[..., 0]])
    out = a*(1-tan*0.85) + green*tan*0.85
    out = out*0.92
    # remove large-scale tone differences between photo acquisitions (local mean normalisation)
    mean = np.dstack([ndi.gaussian_filter(out[..., c], out.shape[0]/40) for c in range(3)])
    target = np.array([0.24, 0.29, 0.20])
    out = out/np.maximum(mean, 1e-3)*target
    return (np.clip(out, 0, 1)*255).astype(np.uint8)
midimg = grade(midimg); farimg = grade(farimg)
feat = json.load(open('/tmp/features.json'))
feat['ponds'] = json.load(open('/tmp/final_log.json'))['ponds']
info = dict(
    par=5, hdcp='未確認（公式ページに記載なし）',
    yards=dict(FULL=540, BACK=512, REG=482, FRONT=454, LADIES=411),
    mapMarks=[245, 445],
    teeColors=dict(FULL=dict(name='FULL', hex='#1b1b1b', fg='#fff'), BACK=dict(name='BACK', hex='#1f5fd1', fg='#fff'),
                   REG=dict(name='REG', hex='#f2f2f2', fg='#111'), FRONT=dict(name='FRONT', hex='#f0c419', fg='#111'),
                   LADIES=dict(name='LADIES', hex='#d8262f', fg='#fff')),
    desc='スターティングホールにふさわしい、圧迫感のないロングホールです。フェアウェイ右のバンカーは意外と近くに見えますが、実際には250ヤードオーバーのロングドライブがないと越えません。（公式サイトより）',
    date='2026-05-20', lat0=LAT0, lon0=LON0,
)
D = dict(near=near, mid=midd, far=fard, feat=feat, info=info,
         tex=dict(m1=png_uri(m1), m2=png_uri(m2), m3=png_uri(m3), aer=png_uri(aer, 'JPEG', 80),
                  mid=png_uri(midimg, 'JPEG', 78), far=png_uri(farimg, 'JPEG', 78)))
credit = ('出典：国土地理院　基盤地図情報 数値標高モデル（5mメッシュ DEM5A／10mメッシュ DEM10B）〔地理院タイル 標高タイル dem5a_png・dem_png〕、'
          '地理院タイル 全国最新写真（シームレス）〔seamlessphoto〕を加工して作成／コース情報：東建多度カントリークラブ・名古屋 公式サイト　｜　'
          '3D表現は推定・簡略化を含みます')
html = open('/tmp/template.html', encoding='utf-8').read()
html = html.replace('__VERSION__', VERSION).replace('__DATE__', '2026年5月20日').replace('__CREDIT__', credit)
html = html.replace('__DATA__', json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
open(OUT, 'w', encoding='utf-8').write(html)
print(OUT, round(len(html.encode())/1e6, 2), 'MB')
