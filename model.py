from math import log,sqrt,pi
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

p1 = 13.4
p2 = 7.6
y0 = 1.2
yss = 5.5
uss = -0.1
T = 93-72

logdec = log((p1-yss)/(p2-yss))
print('logdec=',logdec)
zeta = 1/sqrt(1+(2*pi/logdec)**2)
print('zeta=',zeta)
wd = 2*pi/T
print('wd=',wd)
wn = wd/sqrt(1-zeta**2)
print('wn=',wn)

k = (yss-y0)/uss
print('k=',k)

A = np.array([[0,1],[-wn*wn,-2*zeta*wn]])
B = np.array([[0],[1]])
C = np.array([-k*wn*wn,0])
D = np.array([0])

(t,y) = scipy.signal.step((A,B,C,D))
plt.plot(t,y*-uss)
plt.show()

