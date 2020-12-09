"""
Fit linear system model to step response data
"""
from fgplot import import_log, last_log_filename
import matplotlib.pyplot as plt
from numpy import argmax, argmin, array, dot, real, imag, linspace
from numpy.linalg import eig
from math import log, sqrt, pi

# import last log data
file_name = last_log_filename()
step_data = import_log(file_name)

# plot the step response
plt.figure()
ax=plt.subplot(2,1,1)
(tv,v)=step_data['/velocities/vertical-speed-fps']
plt.plot(tv,v)
plt.subplot(2,1,2,sharex=ax)
(te,e)=step_data['/controls/flight/elevator']
plt.plot(te,e)
plt.show()

# extract peak information
y_max = max(v) # first peak in output
k_ymax = argmax(v) # and its index in the data
y_tr1 = min(v[k_ymax:-1]) # first trough after max
k_ytr1 = k_ymax+argmin(v[k_ymax:-1]) # and its index in the data
y_pk2 = max(v[k_ytr1:-1]) # second peak
k_ypk2 = k_ytr1+argmax(v[k_ytr1:-1]) # and its index in the data

# extract steady state values
u_ss = min(e) # the size of the input step
y_ss = sum(v[-21:-1])/20

# another step plot, this time with the extracted 
# values added for sanity checking
plt.figure()
ax=plt.subplot(2,1,1)
plt.plot(tv,v)
plt.plot(tv[k_ymax],y_max,'rs')
plt.plot(tv[k_ytr1],y_tr1,'bs')
plt.plot(tv[k_ypk2],y_pk2,'rs')
plt.plot([tv[0],tv[-1]],[y_ss,y_ss],'k:')
plt.subplot(2,1,2,sharex=ax)
plt.plot(te,e)
plt.plot([te[0],te[-1]],[u_ss,u_ss],'k:')
plt.show()

# now use the log decrement method to find the system model
# https://en.wikipedia.org/wiki/Logarithmic_decrement
logdec = log((y_max-y_ss)/(y_pk2-y_ss)) # log ratio of peak heights
zeta = 1/sqrt(1+(2*pi/logdec)**2) # gives us damping ratio
wd = 2*pi/(tv[k_ypk2] - tv[k_ymax]) # time between peaks gives damped natural freq
wn = wd/sqrt(1-zeta**2) # undamped natural freq
k_ss = y_ss/u_ss # scalar gain

A = array([[0,1],[-wn*wn,-2*zeta*wn]])
B = array([[0.0],[wn*wn]])*k_ss 
C = array([[1.0,0]]) 
D = array([0.0])

# make data set comparable - remove offset and time before step
t_data = [t - tv[0] - 5.0 for t in tv if t > tv[0]+5]
y_data = array([v[k] for k in range(len(v)) if tv[k] > tv[0]+5])

import scipy.signal
(t_mdl,y_mdl) = scipy.signal.step((A,B,C,D),T=t_data)
plt.figure()
plt.plot(t_mdl,u_ss*y_mdl,'k')
plt.plot(t_data,y_data) # compare with real data
plt.show()

# use more formal approach - optimize the fit
# first define mismatch cost
def sys_id_cost(p):
    A2 = A + array([[0,0],[p[0],p[1]]])
    B2 = B + array([[0.0],[p[2]]])
    (t_mdl,y_mdl) = scipy.signal.step((A2,B2,C,D),T=t_data)
    errors = u_ss*y_mdl - y_data
    #print(errors)
    return sum(errors*errors)

# test it with initial guess
p0 = [0.0, 0.0, 0.0]
print('Initial error cost:',
      sys_id_cost(p0),
      'Starting optimizer.')

# now minimize this cost
import scipy.optimize
res = scipy.optimize.minimize(sys_id_cost,p0)
print(res)

# let's see what it gave us
p = res.x
A = A + array([[0,0],[p[0],p[1]]])
B = B + array([0.0,[p[2]]])
C = array([[1.0,0]])
D = array([0.0])
(t_mdl,y_mdl) = scipy.signal.step((A,B,C,D),T=t_data)
plt.figure()
plt.plot(t_mdl,u_ss*y_mdl,'k')
plt.plot(t_data,y_data) # compare with real data
plt.show()

# plot the root locus
plt.figure()
for kp in linspace(0,0.05):
    Acl = A+kp*dot(B,C)
    w,v = eig(Acl)
    plt.plot(real(w),imag(w),'x')
plt.show()

# try to place both poles together on the real axis
# do this with a bisection search
k_ub = 0.05
k_lb = 0.001
for kk in range(20):
    kp = 0.5*(k_ub+k_lb)
    Acl = A+kp*dot(B,C)
    w,v = eig(Acl)
    #print(k_lb,k_ub,w)
    if any(imag(w)):
        k_lb = kp
    else:
        k_ub = kp
print(kp,w)

# finally have a look at how this should respond to a 5FPS step
Bcl = -5*kp*B
(t_pred,y_pred) = scipy.signal.step((Acl,Bcl,C,D))
plt.figure()
plt.plot(t_pred,y_pred) # compare with real data
plt.show()