import numpy as np, json, math
from scipy import ndimage as ndi
from local import *
from demmosaic import mosaic
from resample import bilinear

def sample(A, ox, oy, z, xs, zs):
    X, Z = np.meshgrid(xs, zs)
    lon = LON0 + X/MLON; lat = LAT0 - Z/MLAT
    n = 2**z
    gx = (lon+180)/360*n*256 - ox - 0.5
    gy = (1-np.arcsinh(np.tan(np.radians(lat)))/math.pi)/2*n*256 - oy - 0.5
    return bilinear(A, gx, gy)

def llbox(xmin, xmax, zmin, zmax):
    W, N = to_ll(xmin, zmin); E, S = to_ll(xmax, zmax); return W, S, E, N

report = {}
# ---- near 1 m grid ----
xs = np.arange(XMIN, XMAX+0.5, 1.0); zs = np.arange(ZMIN, ZMAX+0.5, 1.0)
A5, ox5, oy5, i5 = mosaic('dem5a_png', 15, *llbox(XMIN-50, XMAX+50, ZMIN-50, ZMAX+50))
A10, ox10, oy10, i10 = mosaic('dem_png', 14, *llbox(XMIN-100, XMAX+100, ZMIN-100, ZMAX+100))
h5 = sample(A5, ox5, oy5, 15, xs, zs)
h10 = sample(A10, ox10, oy10, 14, xs, zs)
nanfrac = float(np.isnan(h5).mean())
valid = ~np.isnan(h5)
w = ndi.gaussian_filter(valid.astype(float), 3)  # soft blend at gap edges
w = np.where(valid, w, 0)
near = np.where(valid, h5, 0)*w + h10*(1-w)
near = ndi.gaussian_filter(near, 1.2)
report['near'] = dict(dem5a=i5, dem10=i10, grid_m=1.0, nx=len(xs), nz=len(zs), dem5a_gap_fraction=round(nanfrac, 4),
                      hmin=float(near.min()), hmax=float(near.max()))
np.save('/tmp/near_h.npy', near.astype(np.float32))
np.save('/tmp/near_gap.npy', ~valid)

# ---- mid: +-6 km, 30 m ----
R = 6000; res = 30
xm = np.arange(-R, R+1, res); zm = np.arange(-R, R+1, res)
Am, oxm, oym, im_ = mosaic('dem_png', 14, *llbox(-R-300, R+300, -R-300, R+300))
Am = np.where(np.isnan(Am), 0, Am)
mid = sample(Am, oxm, oym, 14, xm, zm)
report['mid'] = dict(dem=im_, grid_m=res, extent_m=R, n=len(xm))
np.save('/tmp/mid_h.npy', mid.astype(np.float32))

# ---- far: +-36 km, 200 m ----
R = 36000; res = 200
xf = np.arange(-R, R+1, res)
Af, oxf, oyf, if_ = mosaic('dem_png', 11, *llbox(-R-2000, R+2000, -R-2000, R+2000))
seaf = np.isnan(Af)
Af = np.where(seaf, -1, Af)
far = sample(Af, oxf, oyf, 11, xf, xf)
report['far'] = dict(dem=if_, grid_m=res, extent_m=R, n=len(xf))
np.save('/tmp/far_h.npy', far.astype(np.float32))
json.dump(report, open('/tmp/terrain_report.json', 'w'), indent=1, default=str)
print(json.dumps(report, indent=1, default=str))
