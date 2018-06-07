from pylab import *
cmap = cm.get_cmap('Dark2',8);
for i in range(cmap.N):
    rgb = cmap(i)[:3]
    r,g,b = rgb
    rgb = (int(256*r),int(256*g),int(256*b))
    print(rgb)

