import attractors
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.video.VideoClip import DataVideoClip
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Lake parameters
b = 0.65
q = 4

# One step dynamic (P increment rate)
# arguments are current state x and lake parameters b,q and input l
def Dynamics(x, b, q, l):
    dp = (x ** q) / (1 + x ** q) - b * x + l
    return dp

# Time parameters
dt = 0.01 # time step
T = 40 # final horizon
nt = int(T/dt+1E-6) # number of time steps

# Initial phosphorus levels
pmin = 0
pmed = 1
pmax = 2.5

# Inputs levels
l = np.arange(0.001,0.401,0.005)

# Store trajectories
low_p = np.zeros([len(l),nt+1]) # Correspond to pmin
med_p = np.zeros([len(l),nt+1]) # Correspond to pmed
high_p = np.zeros([len(l),nt+1]) # Correspond to pmax

# Equilibria of the lake problem
eqList = attractors.lakeAttractors(b,q,l[-1])
# PLot them!
def lakeAttBase(eqList,dl,alpha):
    l1 = np.arange(eqList.first[0], eqList.first[0] + len(eqList.Oligo) * dl, dl)
    l2 = np.arange(eqList.first[1], eqList.first[1] + len(eqList.Unst) * dl - 1E-10, dl)
    l3 = np.arange(eqList.first[2], eqList.first[2] + len(eqList.Eutro) * dl - 1E-10, dl)
    plt.plot(l1, eqList.Oligo, color='k', alpha=alpha)
    plt.plot(l2, eqList.Unst, linestyle='--', color='k', alpha=alpha)
    plt.plot(l3, eqList.Eutro, color='k', alpha=alpha)
    return None
unstable = mlines.Line2D([], [], color='k', linestyle='--', label = 'Unstable equilibria')
stable = mlines.Line2D([], [], color='k', label='Stable equilibria')

# Generating the data: trajectories
def trajectory(b,q,p0,l,dt,T):
    # Declare outputs
    time = np.arange(0,T+dt,dt)
    traj = np.zeros(len(time))
    # Initialize traj
    traj[0] = p0
    # Fill traj with values
    for i in range(1,len(traj)):
        traj[i] = traj[i-1] + dt * Dynamics(traj[i-1],b,q,l)
    return traj
# Get them!
for i in range(len(l)):
    low_p[i,:] = trajectory(b,q,pmin,l[i],dt,T)
    med_p[i, :] = trajectory(b, q, pmed, l[i], dt, T)
    high_p[i,:] = trajectory(b,q,pmax,l[i],dt,T)

# Draw animated figure
fig, ax = plt.subplots(1)
ax.set_xlabel('Phosphorus inputs L')
ax.set_ylabel('Phosphorus concentration P')
ax.set_xlim(0,l[-1])
ax.set_ylim(0,pmax)
line_low, = ax.plot(l,low_p[:,0],'.', label='State, P(0)=0')
line_med, = ax.plot(l,med_p[:,0],'.', label='State, P(0)=1')
line_high, = ax.plot(l,high_p[:, 0], '.', label='State, P(0)=2.5')

# Parameters of the animation
initial_delay = 0.5 # in seconds, delay where image is fixed before the animation
final_delay = 0.5 # in seconds, time interval where image is fixed at end of animation
time_interval = 0.25 # interval of time between two snapshots in the dynamics (time unit or non-dimensional)
fps = 20 # number of frames per second on the GIF
# Translation in the data structure
data_interval = int(time_interval/dt) # interval between two snapshots in the data structure
t_initial = -initial_delay*fps*data_interval
t_final = final_delay*fps*data_interval
time = np.arange(t_initial,low_p.shape[1]+t_final,data_interval) # time in the data structure

# Making frames
def make_frame(t):
    t = int(t)
    if t<0:
        return make_frame(0)
    elif t>nt:
        return make_frame(nt)
    else:
        line_low.set_ydata(low_p[:,t])
        line_med.set_ydata(med_p[:,t])
        line_high.set_ydata(high_p[:, t])
        ax.set_title(' Lake attractors, and dynamics at t=' + str(int(t*dt)), loc='left', x=0.2)
        if t > 0.25*nt:
            alpha = (t-0.25*nt) / (1.5*nt)
            lakeAttBase(eqList, 0.001, alpha=alpha)
            plt.legend(handles=[stable, unstable], loc=2)
        return mplfig_to_npimage(fig)

# Animating
animation = DataVideoClip(time,make_frame,fps=fps)
animation.write_gif("lake_attractors.gif",fps=fps)