from fgclient import FgClient
c = FgClient()
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
