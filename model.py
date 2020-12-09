"""
Fit linear system model to step response data
then design simple lag compensator
"""
from fgplot import import_log, last_log_filename
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import scipy.signal
from math import log, sqrt, pi

# import last log data
file_name = last_log_filename()
# file_name = 'logs/fglog201209163356.csv'
step_data = import_log(file_name)

# plot the step response
plt.figure()
ax = plt.subplot(2, 1, 1)
(tv, v) = step_data['/velocities/vertical-speed-fps']
plt.plot(tv, v)
plt.subplot(2, 1, 2, sharex=ax)
(te, e) = step_data['/controls/flight/elevator']
plt.plot(te, e)
plt.show()

# extract peak information
y_max = max(v) # first peak in output
k_ymax = np.argmax(v) # and its index in the data
y_tr1 = min(v[k_ymax:-1]) # first trough after max
k_ytr1 = k_ymax+np.argmin(v[k_ymax:-1]) # and its index in the data
y_pk2 = max(v[k_ytr1:-1]) # second peak
k_ypk2 = k_ytr1+np.argmax(v[k_ytr1:-1]) # and its index in the data

# extract steady state values
u_ss = min(e) # the size of the input step
y_ss = sum(v[-21:-1])/20

# another step plot, this time with the extracted
# values added for sanity checking
plt.figure()
ax = plt.subplot(2, 1, 1)
plt.plot(tv, v)
plt.plot(tv[k_ymax], y_max, 'rs')
plt.plot(tv[k_ytr1], y_tr1, 'bs')
plt.plot(tv[k_ypk2], y_pk2, 'rs')
plt.plot([tv[0], tv[-1]], [y_ss, y_ss], 'k:')
plt.subplot(2, 1, 2, sharex=ax)
plt.plot(te, e)
plt.plot([te[0], te[-1]], [u_ss, u_ss], 'k:')
plt.show()

# %% now use the log decrement method to find the system model
# https://en.wikipedia.org/wiki/Logarithmic_decrement
logdec = log((y_max-y_ss)/(y_pk2-y_ss)) # log ratio of peak heights
zeta = 1/sqrt(1+(2*pi/logdec)**2) # gives us damping ratio
wd = 2*pi/(tv[k_ypk2] - tv[k_ymax]) # time between peaks gives damped natural freq
wn = wd/sqrt(1-zeta**2) # undamped natural freq
k_ss = y_ss/u_ss # scalar gain

A = np.array([[0, 1], [-wn*wn, -2*zeta*wn]])
B = np.array([[0.0], [wn*wn]])*k_ss
C = np.array([[1.0, 0]])
D = np.array([0.0])

# make data set comparable - remove offset and time before step
t_data = [t - tv[0] - 5.0 for t in tv if t >= tv[0]+5]
y_data = np.array([v[k] for k in range(len(v)) if tv[k] >= tv[0]+5])

(t_mdl, y_mdl) = scipy.signal.step((A, B, C, D),
                                  T=t_data)
plt.figure()
plt.plot(t_mdl, u_ss*y_mdl, 'k')
plt.plot(t_data, y_data) # compare with real data
plt.show()

# %% use more formal approach - optimize the fit
# first define mismatch cost
def sys_id_cost(p_in):
    A2 = A + np.array([[0,0], [p_in[0], p_in[1]]])
    B2 = B + np.array([[p_in[2]], [p_in[3]]])
    (_, y_eval) = scipy.signal.step((A2, B2, C, D),
                                    T=t_data)
    errors = u_ss*y_eval - y_data
    #print(errors)
    return sum(errors*errors)

# test it with initial guess
p0 = [0.0, 0.0, 0.0, 0.0]
print('Initial error cost:',
      sys_id_cost(p0),
      'Starting optimizer.')

# now minimize this cost
res = scipy.optimize.minimize(sys_id_cost,
                              p0,
                              method='BFGS')
print(res)

# let's see what it gave us
p = res.x
A3 = A + np.array([[0, 0], [p[0], p[1]]])
B3 = B + np.array([[p[2]], [p[3]]])
C = np.array([[1.0, 0]])
D = np.array([0.0])
(t_mdl, y_mdl) = scipy.signal.step((A3, B3, C, D),
                                   T=t_data)
plt.figure()
plt.plot(t_mdl,u_ss*y_mdl,'k')
plt.plot(t_data,y_data) # compare with real data
plt.show()

# %% draw the Bode diagram
w, mag, phase = scipy.signal.bode((A3,-B3,C,D))
plt.figure()
plt.subplot(2,1,1)
plt.grid()
plt.semilogx(w, mag)    # Bode magnitude plot
plt.subplot(2,1,2)
plt.grid()
plt.semilogx(w, phase)  # Bode phase plot
plt.show()

# %% add a scalar gain of x0.005
w, mag, phase = scipy.signal.bode((A3,-0.005*B3,C,D))
kk_cross = max([kk for (kk,wk) in enumerate(w) if mag[kk]>0])

plt.figure()
plt.subplot(2,1,1)
plt.grid()
plt.semilogx(w, mag)    # Bode magnitude plot
plt.semilogx(w[kk_cross+1], mag[kk_cross+1], 'rs')
plt.subplot(2,1,2)
plt.grid()
plt.semilogx(w, phase)  # Bode phase plot
plt.semilogx(w[kk_cross+1], phase[kk_cross+1], 'rs')
plt.show()

print('Phase margin',180+phase[kk_cross+1])

# %% now add lag compensator - boost gain at low frequencies
lag_comp = scipy.signal.TransferFunction([1,0.1],[1,0.01])
openloop_sys = lag_comp.to_ss()*scipy.signal.StateSpace(A3,-0.005*B3,C,D)
w, mag, phase = scipy.signal.bode(openloop_sys)
plt.figure()
plt.subplot(2,1,1)
plt.grid()
plt.semilogx(w, mag)    # Bode magnitude plot
plt.subplot(2,1,2)
plt.grid()
plt.semilogx(w, phase)  # Bode phase plot
plt.show()

# %% get discrete form of compensator
lag_comp_ss = lag_comp.to_ss()
lag_comp_disc = lag_comp_ss.to_discrete(dt=0.5)
print('comp_a =',lag_comp_disc.A[0,0])
print('comp_b =',lag_comp_disc.B[0,0])
print('comp_c =',lag_comp_disc.C[0,0])
print('comp_d =',lag_comp_disc.D[0,0])