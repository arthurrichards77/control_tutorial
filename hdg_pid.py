from fgclient import FgClient
c = FgClient()
c.ap_roll_off()

hdg_des = c.heading_deg()+15
if hdg_des<0:
  hdg_des+=360
if hdg_des>360:
  hdg_des-=360

c.ap_pitch_vs()
c.ap_roll_off()

last_hdg = None
int_err = 0.0
kk = 0
while True:
  kk+=1
  c.tic()
  hdg = c.heading_deg()
  # P
  err = hdg_des - hdg
  ail = 0.005*err
  # D
  if last_hdg:
    ail += -0.03*(hdg - last_hdg)/0.5
  last_hdg = hdg
  # I
  int_err += 0.5*err
  ail += 0.001*int_err
  # out
  c.set_aileron(ail)
  print(hdg_des,hdg,ail)
  c.toc(0.5)
