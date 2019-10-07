from carsim import CarSim
import numpy as np
import matplotlib.pyplot as plt

num_steps=1000

ts = np.zeros(num_steps)
vs = np.zeros(num_steps)
us = np.zeros(num_steps)
rs = np.zeros(num_steps)

c = CarSim()

cmd_spd = 0.0
p_gain = 20.0
spd_ip = 0.0

for t in range(num_steps):
  c.step()
  cur_spd = c.get_speed()
  if t>=200:
    cmd_spd = 1.0
    spd_ip=p_gain*(cmd_spd-cur_spd)
    c.speed(spd_ip)
  us[t]=spd_ip
  ts[t]=c.time
  vs[t]=cur_spd
  rs[t]=cmd_spd

c.quit()

plt.plot(ts,vs,ts,rs,ts,us)
plt.show()
