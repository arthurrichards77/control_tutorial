"""
Implement PID control on the heading of FlightGear simulated aircraft
"""
from fgclient import FgClient
c = FgClient()
c.ap_roll_off()

kk = 0
dt = 0.5
integral_error = 0.0
initial_hdg = c.heading_deg()
last_hdg = initial_hdg
while True:
    kk += 1
    c.tic()
    if kk > 10:
        hdg_des = initial_hdg+15
    else:
        hdg_des = initial_hdg
    hdg = c.heading_deg()
    # differentiate
    hdg_deriv = (hdg - last_hdg)/dt
    last_hdg = hdg
    # integrate
    integral_error += dt*(hdg_des - hdg)
    c.set_aileron(0.01*((hdg_des - hdg) - 4*hdg_deriv + 0.03*integral_error))
    print(hdg_des, hdg)
    c.toc(dt)
