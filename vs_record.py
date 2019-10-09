from fgclient import FgClient
c = FgClient()
c.ap_pitch_off()

while True:
  c.tic()
  vs = c.vertical_speed_fps()
  e = c.get_elevator()
  print(e,vs)
  c.toc(0.5)
