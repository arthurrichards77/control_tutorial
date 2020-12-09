from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()

integral_error = 0.0
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
    integral_error = integral_error + dt*(vs_des - vs)
    c.set_elevator(-0.014*((vs_des - vs) + 0.4*integral_error))
    print(vs)
    c.toc(dt)
