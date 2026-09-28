import math
def ll(px,py,x0,y0,z):
  n=2**z; x=x0+px/256; y=y0+py/256
  return x/n*360-180, math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n))))
def px(lon,lat,z):
  n=2**z; return (lon+180)/360*n*256, (1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n*256
