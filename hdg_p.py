from fgclient import FgClient
c = FgClient()
c.ap_roll_off()

kk = 0
dt = 0.5
initial_hdg = c.heading_deg()
while True:
    kk += 1
    c.tic()
    if kk > 10:
        hdg_des = initial_hdg+15
    else:
        hdg_des = initial_hdg
    hdg = c.heading_deg()
    c.set_aileron(0.01*(hdg_des - hdg))
    print(hdg_des,hdg)
    c.toc(dt)
