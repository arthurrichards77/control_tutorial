from fgclient import FgClient

c = FgClient(savelog=False)
# centre controls
c.set_elevator(0.0)
c.set_aileron(0.0)
# AP on level and south
c.ap_pitch_vs()
c.ap_roll_hdg(180.0)
