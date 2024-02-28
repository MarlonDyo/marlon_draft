import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
import math
import pandas as pd

k = 4.6033*0.99
gamma = 4.4303

def test(zeta = 100, zeta_power = 1.1):
    x0 = np.zeros(2)
    x0[0] = 0.0000001
    x0[1] = math.pi

    def get_theta2(r):
        if r < 1/k:
            theta = math.asin(r * gamma)
        else:
            theta = math.asin(1/(r * k))
        return theta

    def get_theta(r):
        logistic_1 = (1 - (1 / (1+math.exp( -zeta*(r-1/k) )))) ** zeta_power
        logistic_2 = (1 / (1+math.exp( -zeta*(r-1/k) ))) ** zeta_power


        theta = math.asin(
            r*k *logistic_1 + logistic_2 / (r*k)
        )
        return theta

    def first_derivative(x, t0, k):
        theta = get_theta(x[0])
        if x[0] < 0.00001:
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

    t = np.linspace(0., 2., 3000000)
    x = spi.odeint(first_derivative, x0, t, args=(k,))
    theta = np.array([get_theta(x) for x in x[:,0]])
    df = pd.concat(
        [
            pd.Series(t), 
            pd.Series(x[:,0]), 
            pd.Series(x[:,1]), 
            pd.Series(theta)
        ],
        axis=1
    )
    df.columns=['t', 'r', 'alpha', 'theta']
    df = df.set_index('t')
    df = df[df['r']< 1]
    success_flag = df['alpha'].iloc[-1] >= 0
    total_time = df.index[-1]
    return df, success_flag, total_time
result = []

if 0:
    for zeta in np.linspace(40,150,20):
        for zeta_power in np.linspace(1.00, 1.9, 10):
            print([zeta, zeta_power])
            try:
                _, success_flag, total_time = test(zeta=zeta, zeta_power=zeta_power)
            except:
                print('Skipped')
                continue
            if success_flag:
                item = [zeta, zeta_power, total_time]
                print(total_time)
                result.append([zeta, zeta_power, total_time])
            else:
                print("Failed")
    result = pd.DataFrame(result)
    result.to_pickle('result.pkl')
else:
    result = pd.read_pickle('result.pkl')
print(result.sort_values(2))

df, success_flag, total_time = test(zeta=80, zeta_power=1.3)
print('Success' if success_flag else 'Failed')
print(df.index[-1])
_, (ax1, ax2, ax3) = plt.subplots(3,1,sharex=True)
ax1.plot(
    df['r'],
    '-', 
)
ax1.set_ylabel('r')
ax1.grid()
ax2.plot( 
    df['alpha'] / math.pi * 180, 
    '-', 
)
ax2.grid()
ax2.set_ylabel('alpha (graus)')
ax3.plot(
    df['theta'] / math.pi * 180,
    '-',
)
ax3.set_ylabel('theta (graus)')
ax3.grid()
plt.show()