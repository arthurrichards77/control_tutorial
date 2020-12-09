from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()

initial_altitide = c.altitude_ft()
integral_error = 0.0
kk = 0
dt = 0.5
while True:
    kk += 1
    c.tic()
    if kk > 10:
        alt_des = initial_altitide + 100
    else:
        alt_des = initial_altitide
    alt = c.altitude_ft()
    vs_des = 0.03*(alt_des - alt)
    vs = c.vertical_speed_fps()
    integral_error = integral_error + dt*(vs_des - vs)
    c.set_elevator(-0.014*((vs_des - vs) + 0.4*integral_error))
    print(alt_des,alt,vs_des,vs)
    c.toc(dt)
