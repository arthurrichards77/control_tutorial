from carsim import CarSim
import matplotlib.pyplot as plt

ts = []
ys = []
us = []
rs = []

c = CarSim()
c.speed(10.0)

des_hdg = 0.0
p_gain = 40
i_gain = 20
last_time = 0.0
int_err = 0.0
str_ip = 0.0

t=0
while c.time<10:
  t += 1
  c.step()
  if c.time>3.0:
    des_hdg = -0.4
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

c.quit()

plt.plot(ts,ys,ts,rs,ts,us)
plt.show()
