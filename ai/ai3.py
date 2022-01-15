import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

fig = plt.figure(figsize = (3, 3))

plt.plot([0, 3], [3, 3], color = 'k')
plt.plot([0, 3], [0, 0], color = 'k')
plt.plot([0, 0], [0, 2], color = 'k')
plt.plot([3, 3], [1, 3], color = 'k')
plt.plot([1, 1], [1, 2], color = 'k')
plt.plot([2, 3], [2, 2], color = 'k')
plt.plot([2, 1], [1, 1], color = 'k')
plt.plot([2, 2], [0, 1], color = 'k')

for i in range(3):
    for j in range(3):
        plt.text(0.5 + i, 2.5 - j, str(i + j*3), size =20, ha='center', va = 'center')

circle, = plt.plot([0.5], [2.5], marker='o', color = '#d3d3d3', markersize = 40)

plt.tick_params(axis='both', which ='both', bottom = False, top = False, labelbottom = False, right = False, left = False, labelleft = False)
plt.box(False)

theta_0 = np.array([[np.nan, 1, 1, np.nan], [np.nan, 1, 1, 1], [np.nan, np.nan, np.nan, 1],[1,np.nan, 1, np.nan], [1, 1, np.nan, np.nan], [np.nan, np.nan, 1, 1], [1, 1, np.nan, np.nan], [np.nan, np.nan, np.nan, 1]])

def get_pi(theta):
    [m,n] = theta.shape
    pi = np.zeros((m,n))
    exp_theta = np.exp(theta)

    for i in range(0, m):
        pi[i, :] = exp_theta[i, :] / np.nansum(exp_theta[i, :])

    pi = np.nan_to_num(pi)
    return pi

def get_s_next(s, a):
    if  a == 0:
        return s-3
    elif a == 1:
        return s+1
    elif a == 2:
        return s+3
    elif a == 3:
        return s-1

def get_a(s, Q, epsilon, pi_0):
    if np.random.rand() < epsilon:
        return np.random.choice([0,1 , 2, 3], p = pi_0[s])
    else:
        return np.nanargmax(Q[s])

def sarsa(s, a, r, s_next, a_next, Q):
    eta = 0.1
    gamma = 0.9

    if s_next == 8:
        Q[s, a] = Q[s, a] + eta * (r-Q[s,a])
    else:
        Q[s, a] = Q[s, a] + eta * (r + gamma * Q[s_next, a_next] - Q[s, a])
    
    return Q


def q_learning(s, a, r, s_next, a_next, Q):
    eta = 0.1

    gamma = 0.9

    if s_next == 8:
        Q[s, a] = Q[s, a] + eta * (r-Q[s,a])
    else:
        Q[s, a] = Q[s, a] + eta * (r + gamma * np.nanmax(Q[s_next, :]) - Q[s, a])
    
    return Q

def play(Q, epsilon, pi):
    s = 0
    a = a_next = get_a(s, Q, epsilon, pi)
    s_a_history = [[0, np.nan]]

    while True:
        a=a_next
        s_next = get_s_next(s,a)

        s_a_history[-1][1] = a
        s_a_history.append([s_next, np.nan])

        if s_next == 8:
            r = 1
            a_next = np.nan
        else:
            r = 0
            a_next = get_a(s_next, Q, epsilon, pi)

        Q = sarsa(s, a, r, s_next, a_next, Q)

        if s_next == 8:
            break
        else:
            s = s_next

    return [s_a_history, Q]

pi_0 = get_pi(theta_0)
[a, b] = theta_0.shape
Q = np.random.rand(a, b) * theta_0

epsilon = 0.5

for episode in range(10):
    epsilon = epsilon / 2
    [s_a_history, Q] = play(Q, epsilon, pi_0)

    print('에피소드: {}, 스텝: {}'.format(episode, len(s_a_history)-1))