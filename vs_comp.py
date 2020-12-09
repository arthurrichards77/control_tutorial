"""
Execute step in vertical speed using (optional) state
space compensator in the control loop
"""
from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()

# compensator definition
comp_a = 0.9950124791926824
comp_b = 0.4987520807317687
comp_c = 0.09000000000000001
comp_d = 1.0
x_comp = 0.0 # initial internal state

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
    err = vs_des - vs
    # update compensator
    y_comp = comp_c*x_comp + comp_d*err
    x_comp = comp_a*x_comp + comp_b*err
    # apply feedback
    c.set_elevator(-0.005*y_comp) # with compensator
    #c.set_elevator(-0.005*err) # without compensator
    print(vs)
    c.toc(dt)
