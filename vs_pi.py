from fgclient import FgClient
c = FgClient()

int_err = 0.0
kk = 0
while True:
  kk+=1
  c.tic()
  if kk>10:
    vs_des = 5.0
  else:
    vs_des = 0.0
  vs = c.vertical_speed_fps()
  err = (vs_des - vs)
  int_err += 0.5*err
  c.set_elevator(-0.04*err - 0.02*int_err)
  print(vs)
  c.toc(0.5)
