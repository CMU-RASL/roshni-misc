import numpy as np
import matplotlib.pyplot as plt

# t = np.arange(0, 5, 0.01)
# t = np.linspace(1102.809, 1191.612, 2418)
t = np.linspace(101.101, 180.348, 1732)
dt = t[1]-t[0]
x = np.zeros_like(t)
y = np.zeros_like(t)
th_c = np.zeros_like(t)
th_t = np.zeros_like(t)
v_l = np.zeros_like(t)
v_r = np.zeros_like(t)
v_th_t = np.zeros_like(t)

#Commands
v_x = 0.5
v_y = 0
v_th_r = 0

#Constants
L = 0.246
R = 0.0762
b = 0.123

#Initialize
# x[0] = -0.027758622572896647
# y[0] = -0.0072960808023493934
# th_c[0] = -0.05968577581049065
# th_t[0] = 0.006952255488486436

x[0] = -0.08699943211900385
y[0] = -0.02594564505438163
th_c[0] = -0.2619430600108769
th_t[0] = 0.000801111689093581

wheel_cap = 10
turret_cap = 4

for ii in range(1, t.shape[0]):
    #Calculate velocity commands
    s_c = np.sin(th_c[ii-1])
    c_c = np.cos(th_c[ii-1])
    v_l[ii] = (L/2/R/b*s_c + c_c/R)*v_x + (s_c/R - L/2/R/b*c_c)*v_y
    v_r[ii] = (-L/2/R/b*s_c + c_c/R)*v_x + (s_c/R + L/2/R/b*c_c)*v_y
    v_th_t[ii] = s_c/b*v_x - c_c/b*v_y + v_th_r

    #Cap and scale the velocities
    perc = np.abs(np.array([v_l[ii], v_r[ii], v_th_t[ii]]))/np.array([wheel_cap, wheel_cap, turret_cap])
    lim_ind = np.argmax(perc)
    if np.max(perc) > 1:
        if lim_ind == 0:
            scale = np.abs(wheel_cap/v_l[ii])
            v_l[ii] = np.sign(v_l[ii])*wheel_cap
            v_r[ii] = scale*v_r[ii]
            v_th_t[ii] = scale*v_th_t[ii]
        if lim_ind == 1:
            scale = np.abs(wheel_cap/v_r[ii])
            v_l[ii] = scale*v_l[ii]
            v_r[ii] = np.sign(v_r[ii])*wheel_cap
            v_th_t[ii] = scale*v_th_t[ii]
        if lim_ind == 2:
            scale = np.abs(turret_cap/v_th_t[ii])
            v_l[ii] = scale*v_l[ii]
            v_r[ii] = scale*v_r[ii]
            v_th_t[ii] = np.sign(v_th_t[ii])*turret_cap

    v_l[ii] = 3
    v_r[ii] = 6
    v_th_t[ii] = 0

    #Update position
    v_x_actual = R/2*(v_r[ii] + v_l[ii])*c_c
    v_y_actual = R/2*(v_r[ii] + v_l[ii])*s_c
    x[ii] = x[ii-1] + dt*v_x_actual
    y[ii] = y[ii-1] + dt*v_y_actual
    th_c[ii] = th_c[ii-1] + dt*(- R/L*v_l[ii] + R/L*v_r[ii])
    if th_c[ii] > 3.2:
        th_c[ii] = th_c[ii] - 2*np.pi
    if th_c[ii] < -3.2:
        th_c[ii] = th_c[ii] + 2*np.pi
    th_t[ii] = th_t[ii-1] + dt*v_th_t[ii]


# plt.figure()
# plt.plot(x, y)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.axis([-2, 1.5, -3, 0.5])

# plt.figure()
# plt.plot(t, th_t)
# plt.plot(t, th_c)
# plt.plot(t, th_t + th_c)
# plt.legend(['th_t', 'th_c', 'th_r'])
# plt.xlabel('Time')
# plt.ylabel('Radians')

dist = 0
for x1, x2, y1, y2 in zip(x[:-1], x[1:], y[:-1], y[1:]):
    dist += np.sqrt((y2-y1)**2 + (x2-x1)**2)

print(dist)

plt.figure()
plt.plot(t, x)
plt.plot(t, y)
plt.legend(['x', 'y'])
plt.xlabel('Time')
plt.ylim([-1, 2.5])
# plt.ylim([-13, 1])

# plt.figure()
# plt.plot(t, v_l)
# plt.plot(t, v_r)
# plt.legend(['v_l', 'v_r'])
# plt.xlabel('Time')
# plt.ylabel('m/s')
# plt.ylim([-7, 10])

# plt.figure()
# plt.plot(t, v_th_t)
# plt.legend(['v_th_t'])
# plt.xlabel('Time')
# plt.ylabel('rad/s')
# plt.ylim([-5, 0.5])

plt.show()

