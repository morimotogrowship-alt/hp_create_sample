import math,sys,os,subprocess,io
from PIL import Image
def xy(lon,lat,z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n; return x,y
def get(layer,z,x,y,ext):
    f=f"tiles/{layer}_{z}_{x}_{y}.{ext}"
    if not os.path.exists(f):
        for i in range(4):
            r=subprocess.run(["curl","-sS","-f","--max-time","30","-o",f,f"https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.{ext}"])
            if r.returncode==0: break
        else: return None
    return f
lon,lat,z,r,layer,ext,out=float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5],sys.argv[6],sys.argv[7]
cx,cy=xy(lon,lat,z); cx,cy=int(cx),int(cy)
im=Image.new("RGB",(256*(2*r+1),256*(2*r+1)))
for dx in range(-r,r+1):
  for dy in range(-r,r+1):
    f=get(layer,z,cx+dx,cy+dy,ext)
    if f: im.paste(Image.open(f).convert("RGB"),((dx+r)*256,(dy+r)*256))
im.save(out); print(cx-r,cy-r,z)
