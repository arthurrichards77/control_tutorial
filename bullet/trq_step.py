from carsim import CarSim
import numpy as np
import matplotlib.pyplot as plt

num_steps=1000

ts = np.zeros(num_steps)
vs = np.zeros(num_steps)

c = CarSim()

for t in range(num_steps):
  if t>=500:
    c.torque(30.0)
  c.step()
  ts[t]=c.time
  vs[t]=c.get_speed()

c.quit()

plt.plot(ts,vs)
plt.show()
