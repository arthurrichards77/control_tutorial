"""
Start up and take off from simulator reset
"""
from fgclient import FgClient
c = FgClient()

c.set_prop('/controls/engines/engine/magnetos',3)
c.set_prop('/controls/engines/engine/throttle',0.75)
c.set_prop('/controls/gear/brake-parking',0)
c.set_prop('/sim/hud/visibility[0]',1)
c.set_aileron(0.0)
c.set_elevator(0.0)

c.set_prop('/controls/engines/engine/starter',1)

for kk in range(30):
    c.tic()
    sp = c.get_prop_float('/velocities/airspeed-kt')
    print(sp)
    if sp>50:
        c.set_elevator(-0.1)
    c.toc(1.0)
    
for kk in range(30):
    c.tic()
    alt = c.altitude_ft()
    print(alt)
    if alt>200:
        c.set_elevator(0.0)
        c.ap_roll_hdg(180)
        c.ap_pitch_vs(10)
    c.toc(1.0)