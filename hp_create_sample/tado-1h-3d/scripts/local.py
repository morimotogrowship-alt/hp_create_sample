import math
LAT0, LON0 = 35.1254, 136.5960
a = 6378137.0; e2 = 0.00669437999014
_s = math.sin(math.radians(LAT0))
MLAT = math.radians(1) * a*(1-e2)/(1-e2*_s*_s)**1.5   # m per deg lat
MLON = math.radians(1) * a/math.sqrt(1-e2*_s*_s)*math.cos(math.radians(LAT0))
XMIN, XMAX, ZMIN, ZMAX = -420.0, 420.0, -350.0, 350.0   # x east, z south
def to_local(lon, lat): return (lon-LON0)*MLON, -(lat-LAT0)*MLAT
def to_ll(x, z): return LON0 + x/MLON, LAT0 - z/MLAT
def bbox(pad=0):
    W, N = to_ll(XMIN-pad, ZMIN-pad); E, S = to_ll(XMAX+pad, ZMAX+pad)
    return W, S, E, N
