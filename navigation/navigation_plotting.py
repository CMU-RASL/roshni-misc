import numpy as np
import matplotlib.pyplot as plt

#Read in txt file
time = []
v_x = []
v_y = []
v_theta_r = []
x = []
y = []
theta_c = []
v_l = []
v_r = []
v_theta_t = []
theta_t = []

with open('test04.txt', 'r') as f:
    counter = 0
    for line in f.readlines():
        l = line.split(' ')
        time.append(float(l[2][:-2]))
        v_x.append(float(l[3][1:-1]))
        v_y.append(float(l[4][:-1]))
        v_theta_r.append(l[5][:-1])
        theta_c.append(float(l[6][:-1]))
        x.append(float(l[7][:-1]))
        y.append(float(l[8][:-1]))
        v_l.append(float(l[9][:-1]))
        v_r.append(float(l[10][:-1]))
        v_theta_t.append(float(l[11][:-1]))
        theta_t.append(float(l[12][:-2]))

        counter += 1

x = np.array(x)
y = np.array(y)
v_l = np.array(v_l)
v_r = np.array(v_r)

print('x', x[0], 'y', y[0], 'th_c',theta_c[0], 'theta_t', theta_t[0], 't', time[0], time[-1], len(time))

dist = 0
for x1, x2, y1, y2 in zip(x[:-1], x[1:], y[:-1], y[1:]):
    dist += np.sqrt((y2-y1)**2 + (x2-x1)**2)

print(dist)
# plt.figure()
# plt.plot(x, y)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.axis([-2, 1.5, -3, 0.5])

# plt.figure()
# plt.plot(time, theta_t)
# plt.plot(time, theta_c)
# plt.plot(time, np.array(theta_t) + np.array(theta_c))
# plt.legend(['th_t', 'th_c', 'th_r'])
# plt.xlabel('Time')
# plt.ylabel('Radians')

plt.figure()
plt.plot(time, x)
plt.plot(time, y)
plt.legend(['x', 'y'])
plt.xlabel('Time')
# plt.ylim([-3, 1.5])
# # plt.ylim([-13, 1])

# plt.figure()
# plt.plot(time, v_l)
# plt.plot(time, v_r)
# plt.legend(['v_l', 'v_r'])
# plt.xlabel('Time')
# plt.ylabel('m/s')
# # plt.ylim([-7, 10])


# plt.figure()
# plt.plot(time, v_theta_t)
# plt.legend(['v_th_t'])
# plt.xlabel('Time')
# plt.ylabel('rad/s')
# plt.ylim([-5, 0.5])

plt.show()


