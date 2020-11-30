from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()
from math import sin

kk = 0
while True:
    kk += 1
    c.tic()
    vs = c.vertical_speed_fps()
    print(vs)
    c.set_elevator(0.75*sin(0.5*kk))
    c.toc(0.5)
