"""
Initial skeleton example: run a proportional controller
on the vertical speed, and look at a step response
"""
from fgclient import FgClient
c = FgClient()

# check zero elevator
el = c.get_elevator()
if el != 0.0:
    raise ValueError('Elevator not central: ', el)

c.ap_pitch_off()

kk = 0
dt = 0.5
while True:
    kk += 1
    c.tic()
    if kk > 10:
        vs_des = 5.0
    else:
        vs_des = 0.0
    vs = c.vertical_speed_fps()
    c.set_elevator(-0.01*(vs_des - vs))
    print(vs)
    c.toc(dt)
