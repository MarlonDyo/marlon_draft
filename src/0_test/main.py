import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
import math

k = 4.6033

x0 = np.zeros(2)
x0[0] = 0
x0[1] = math.pi
def get_theta(r):
    if r < 1/k:
        theta = math.asin(r * k)
    else:
        theta = math.asin(1/(r * k))
    return theta
def first_derivative(x, t0, k):
    theta = get_theta(x[0])
    if x[0] < 0.0001:
        xdot = np.array([
            1,
            -k 
        ])
    else:
        xdot = np.array([
            math.cos(theta),
            -k + math.sin(theta) / x[0]
        ])
    return xdot



t = np.linspace(0., 2., 3000)
x = spi.odeint(first_derivative, x0, t, args=(k,))
theta = np.array([get_theta(x) for x in x[:,0]])

flag = any((x[:,1] < 0) & (x[:,0] < 1))
if flag == 1:
    print("Failed")
else:
    print("Success")
theta[x[:,1] < 0] = np.nan
theta[x[:,0] > 1.01] = np.nan
x[x[:,1] < 0, :] = np.nan
x[x[:,0] > 1.01, :] = np.nan

_, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)
ax1.plot(
    t,
    x[:, 0],
    '-', 
)
ax1.set_ylabel('r')
ax1.grid()
ax2.plot(
    t, 
    x[:, 1] / math.pi * 180, 
    '-', 
)
ax2.grid()
ax2.set_ylabel('alpha (graus)')
ax3.plot(
    t,
    theta / math.pi * 180,
    '-',
)
ax3.set_ylabel('theta (graus)')
ax3.grid()
plt.show()