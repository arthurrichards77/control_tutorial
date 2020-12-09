"""
Execute step input on elevator and record step response in log
"""
from fgclient import FgClient
c = FgClient()

# require level flight to begin
vs = c.vertical_speed_fps()
if abs(vs) > 0.02:
    raise ValueError('Vertical speed too large: ', vs)

c.ap_pitch_off()

time_step = 0.5
for kk in range(120):
    c.tic()
    vs = c.vertical_speed_fps()
    if kk < 10:
        e = 0.0
    else:
        e = -0.02
    c.set_elevator(e)
    print(kk, e, vs)
    c.toc(0.5)

c.set_elevator(0.0)
c.ap_pitch_vs(0.0)
