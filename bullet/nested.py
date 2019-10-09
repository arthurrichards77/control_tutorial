from carsim import CarSim
import matplotlib.pyplot as plt

ts = []
ys = []
us = []
rs = []
ps = []

c = CarSim()
c.speed(10.0)

p_gain = 40
i_gain = 20
last_time = 0.0
int_err = 0.0
str_ip = 0.0

t=0
while c.time<30:
  t += 1
  c.step()
  cur_pos = c.position[1]
  des_hdg = 1.0*(1.0-cur_pos)
  cur_hdg = c.heading()
  str_ip = p_gain*(des_hdg-cur_hdg)
  int_err += (c.time-last_time)*(des_hdg-cur_hdg)
  last_time = c.time
  str_ip += i_gain*int_err
  c.steer(str_ip)
  ts.append(c.time)
  us.append(str_ip)
  ys.append(cur_hdg)
  rs.append(des_hdg)
  ps.append(cur_pos)

c.quit()

plt.plot(ts,ys,ts,rs,ts,us,ts,ps)
plt.show()
