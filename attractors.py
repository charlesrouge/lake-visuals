import matplotlib.pyplot as plt
from matplotlib import lines
from numpy.polynomial import Polynomial
import numpy as np


# One step dynamic (P increment rate)
# arguments are current state x and lake parameters b,q and input p_inputs
def lake_dynamics(x, b_param, q_param, l_input):
    dp = (x ** q_param) / (1 + x ** q_param) - b_param * x + l_input
    return dp


# Generating the data: trajectories
def trajectory(b_param, q_param, p0, l_input, delta_t, horizon):
    # Declare outputs
    traj = np.zeros(len(np.arange(0, horizon + delta_t, delta_t)))
    # Initialize traj
    traj[0] = p0
    # Fill traj with values
    for i in range(1, len(traj)):
        traj[i] = traj[i-1] + delta_t * lake_dynamics(traj[i - 1], b_param, q_param, l_input)
    return traj



# Define attractors
class LakeAttractorList:
    def __init__(self):
        self.oligotrophic = []  # oligotrophic attractors
        self.unstable = []  # unstable attractors
        self.eutrophic = []  # eutrophic attractors
        self.first = np.zeros(3)  # first input for which attractor type exists


# Polynomial for root search
def lake_poly(b, q, l_in):
    lp = np.zeros(q+2)
    lp[q+1] = -b
    lp[q] = l_in + 1
    lp[1] = lp[1]-b
    lp[0] = l_in
    return lp


# Computing all lake attractors for all values of Ph input p_inputs
def lake_attractors(b, q, lmax):
    eq_list = LakeAttractorList()
    l_in = np.arange(0, lmax, 0.001)
    for i in range(len(l_in)):
        lp = Polynomial(lake_poly(b, q, l_in[i]))
        r = lp.roots()
        rpr = []  # real, positive roots
        for j in range(len(r)):
            if r[j].imag == 0 and r[j].real >= 0:
                rpr.append(r[j].real)  # root is real and positive
        rpr = sorted(rpr)
        if len(eq_list.eutrophic) == 0 and len(rpr) > 1:
            eq_list.first[2] = l_in[i]  # mark first point with eutrophic attractor
        if len(eq_list.unstable) == 0 and len(rpr) == 3:
            eq_list.first[1] = l_in[i]  # mark first point with unstable attractor
        if len(rpr) == 3:
            eq_list.oligotrophic.append(rpr[0])
            eq_list.unstable.append(rpr[1])
            eq_list.eutrophic.append(rpr[2])
        elif len(rpr) == 1:
            if len(eq_list.unstable) == 0:
                eq_list.oligotrophic.append(rpr[0])
            else:
                eq_list.eutrophic.append(rpr[0])
        else:
            eq_list.oligotrophic.append(rpr[0])
            eq_list.eutrophic.append(rpr[1])
    return eq_list


# Plotting attractors for a set of parameters (building block for the 2 routines below)
def lake_att_basic(b, q, lmax, dl, color):
    eq_list = lake_attractors(b, q, lmax)
    fig = lake_att_base(eq_list, dl, color)
    return eq_list, fig


def lake_att_base(eq_list, dl, **kwargs):

    # Optional arguments
    alpha = kwargs.pop("alpha", 1)

    l1 = np.arange(eq_list.first[0], eq_list.first[0] + len(eq_list.oligotrophic) * dl, dl)
    l2 = np.arange(eq_list.first[1], eq_list.first[1] + len(eq_list.unstable) * dl - 1E-10, dl)
    l3 = np.arange(eq_list.first[2], eq_list.first[2] + len(eq_list.eutrophic) * dl - 1E-10, dl)
    stable, = plt.plot(l1, eq_list.oligotrophic, color='k', alpha=alpha, label='Stable equilibria')
    unstable, = plt.plot(l2, eq_list.unstable, linestyle='--',  color='k', alpha=alpha, label='Unstable equilibria')
    plt.plot(l3, eq_list.eutrophic, color='k', alpha=alpha)
    plt.legend(handles=[stable, unstable], loc=4)
    return None


# Plot for attractors with a given set of parameters and input level
def lake_att_plot(b, q, lmax, dl, show):
    plt.figure()
    unstable = lines.Line2D([], [], color='k', linestyle='--', label='Unstable')
    stable = lines.Line2D([], [], color='k', label='Stable')
    eq_list = lake_att_basic(b, q, lmax, dl, 'k')
    l_end = min(lmax, len(eq_list.oligotrophic) * dl + .25)
    plt.xlabel('Total average phosphorus input')
    plt.ylabel('Phosphorus concentration')
    axes = plt.gca()
    axes.set_xlim([0, l_end])
    if len(eq_list.eutrophic) > 0:
        axes.set_ylim([0, np.max(eq_list.eutrophic[1:int(l_end / dl)]) + .1])
    else:
        axes.set_ylim([0, np.max(eq_list.oligotrophic[1:int(l_end / dl)]) + .1])
    plt.title('Attractors for b='+str(b)+', q='+str(q))
    plt.legend(handles=[stable, unstable], loc=4)
    if show == 1:
        plt.show()
    return None


# Plot for attractors in a range. b, q and p_inputs are [min,max] vectors. q INTEGER
def lake_att_range(b, q, l_in, lmax, dl, show):
    plt.figure()
    lake_att_basic(b[0], q[0], lmax, dl, 'c')
    lake_att_basic(b[0], q[1], lmax, dl, 'g')
    lake_att_basic(b[1], q[0], lmax, dl, 'b')
    lake_att_basic(b[1], q[1], lmax, dl, 'y')
    plt.plot(np.ones(11) * l_in[0], np.arange(0, 5.1, .5), ':k')
    plt.plot(np.ones(11) * l_in[1], np.arange(0, 5.1, .5), ':k')
    plt.xlabel('Total average phosphorus input L')
    plt.ylabel('Phosphorus concentration')
    axes = plt.gca()
    axes.set_xlim([0, lmax])
    axes.set_ylim([0, 4])
    plt.title(r'Attractors for b $\in$ [' + str(b[0]) + ', ' + str(b[1]) + '], q $\in$ [' + str(q[0]) + ',' + str(q[1])
              + ']', usetex=True)
    cyan_l = lines.Line2D([], [], color='c', label='b=' + str(b[0]) + ', q=' + str(q[0]))
    green_l = lines.Line2D([], [], color='g', label='b=' + str(b[0]) + ', q=' + str(q[1]))
    blue_l = lines.Line2D([], [], color='b', label='b=' + str(b[1]) + ', q=' + str(q[0]))
    yellow_l = lines.Line2D([], [], color='y', label='b=' + str(b[1]) + ', q=' + str(q[1]))
    unstable = lines.Line2D([], [], color='k', linestyle='--', label='Unstable')
    stable = lines.Line2D([], [], color='k', label='Stable')
    l_range = lines.Line2D([], [], color='r', linestyle=':', label='Range for L')
    plt.legend(handles=[l_range, stable, unstable, cyan_l, green_l, blue_l, yellow_l], loc=4)
    if show == 1:
        plt.show()
    return None
