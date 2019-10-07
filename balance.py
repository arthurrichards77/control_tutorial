from carsim import CarSim
import numpy as np
import matplotlib.pyplot as plt
from math import pi

num_steps=1000

ts = np.zeros(num_steps)
ys = np.zeros(num_steps)
us = np.zeros(num_steps)
rs = np.zeros(num_steps)

c = CarSim()

cmd_ang = pi
p_gain = -10.0
d_gain = 1000.0
spd_ip = 0.0
last_ang = None

for t in range(num_steps):
  c.step()
  cur_ang = c.pitch()
  spd_ip=p_gain*(cmd_ang-cur_ang)
  if last_ang:
    spd_ip += d_gain*(cur_ang-last_ang)  
  c.speed(spd_ip)
  last_ang = cur_ang
  us[t]=spd_ip
  ts[t]=c.time
  ys[t]=cur_ang

c.quit()

plt.plot(ts,ys,ts,us)
plt.show()
