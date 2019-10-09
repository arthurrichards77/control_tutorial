from fgclient import FgClient
c = FgClient()

a_des = c.altitude_ft()+100.0

int_err = 0.0
kk = 0
while True:
  kk+=1
  c.tic()
  a = c.altitude_ft()
  vs_des = 0.05*(a_des - a)
  vs = c.vertical_speed_fps()
  err = (vs_des - vs)
  int_err += 0.5*err
  c.set_elevator(-0.04*err - 0.02*int_err)
  print(a_des,a,vs_des,vs)
  c.toc(0.5)
