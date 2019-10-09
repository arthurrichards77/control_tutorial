from fgclient import FgClient
c = FgClient()

hdg_des = c.heading_deg()+15
if hdg_des<0:
  hdg_des+=360
if hdg_des>360:
  hdg_des-=360

c.ap_pitch_vs()
c.ap_roll_off()

last_hdg = None
kk = 0
while True:
  kk+=1
  c.tic()
  hdg = c.heading_deg()
  ail = 0.005*(hdg_des - hdg)
  if last_hdg:
    ail += -0.05*(hdg - last_hdg)/0.5
  last_hdg = hdg
  c.set_aileron(ail)
  print(hdg_des,hdg,ail)
  c.toc(0.5)
