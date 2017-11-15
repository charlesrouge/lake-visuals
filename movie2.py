import attractors
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.video.VideoClip import DataVideoClip
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Lake parameters
b = 0.65
q = 4

# Time parameters
dt = 0.01 # time step
T = 40 # final horizon
nt = int(T/dt+1E-6) # number of time steps

# Parameters of animation
l0 = [0.35, 0.375, 0.4] # initial inputs
p0 = [0] # initial phosphorus levels
# Policy parameters
dldt=1E-2 # rate of input decrease
lmin = 0.08 # minimal input levels
# Maximal phosphorus input considered in this code
lmax = 0.4

# One step dynamic (P increment rate)
# arguments are current state x and lake parameters b,q and input l
def Dynamics(x, b, q, l):
    dp = (x ** q) / (1 + x ** q) - b * x + l
    return dp

# Equilibria of the lake problem
eqList = attractors.lakeAttractors(b,q,lmax)
# PLot them!
def lakeAttBase(eqList,dl):
    l1 = np.arange(eqList.first[0], eqList.first[0] + len(eqList.Oligo) * dl, dl)
    l2 = np.arange(eqList.first[1], eqList.first[1] + len(eqList.Unst) * dl - 1E-10, dl)
    l3 = np.arange(eqList.first[2], eqList.first[2] + len(eqList.Eutro) * dl - 1E-10, dl)
    plt.plot(l1, eqList.Oligo, color='k')
    plt.plot(l2, eqList.Unst, linestyle='--', color='k')
    plt.plot(l3, eqList.Eutro, color='k')
    return None
unstable = mlines.Line2D([], [], color='k', linestyle='--', label = 'Unstable')
stable = mlines.Line2D([], [], color='k', label='Stable')

# Generating the data: trajectories
def trajectory(b,q,p0,l0,dldt,dt,T):
    # Declare outputs
    time = np.arange(0,T+dt,dt)
    traj = np.zeros([len(time),2])
    # Initialize traj
    traj[0,:] = [l0,p0]
    # Fill traj with values
    for i in range(1,len(traj)):
        traj[i,0] = max(lmin, traj[i-1,0] - dldt*dt)
        traj[i,1] = traj[i-1,1] + dt * Dynamics(traj[i-1,1],b,q,traj[i-1,0])
    return traj
# Get them!
trajectories = []
for i in range(len(l0)):
    for j in range(len(p0)):
        traj = trajectory(b,q,p0[j],l0[i],dldt,dt,T)
        trajectories.append(traj)

# Draw animated figure
fig, ax = plt.subplots(1)
ax.set_xlabel('Phosphorus inputs L')
ax.set_ylabel('Phosphorus concentration P')
ax.set_xlim(0,0.4)
ax.set_ylim(0,2.5)
lakeAttBase(eqList, 0.001)
lines=[]
current_states = []
for i in range(len(trajectories)):
    traj = trajectories[i]
    line, = ax.plot(traj[0,0],traj[0,1], color='b', label='Trajectory')
    point, = ax.plot(traj[0,0],traj[0,1],'.', color='r', label='Current state')
    lines.append(line)
    current_states.append(point)
plt.legend(handles=[line,point],loc = 2)

# Parameters of the animation
initial_delay = 0 # in seconds, delay where image is fixed before the animation
final_delay = 1 # in seconds, time interval where image is fixed at end of animation
time_interval = 0.25 # interval of time between two snapshots in the dynamics (time unit or non-dimensional)
fps = 20 # number of frames per second on the GIF
# Translation in the data structure
data_interval = int(time_interval/dt) # interval between two snapshots in the data structure
t_initial = -initial_delay*fps*data_interval
t_final = final_delay*fps*data_interval

def make_frame(t):
    t = int(t)
    if t<0:
        return make_frame(0)
    elif t>nt:
        return make_frame(nt)
    else:
        for i in range(len(trajectories)):
            traj = trajectories[i]
            lines[i].set_xdata(traj[0:t,0])
            lines[i].set_ydata(traj[0:t,1])
            current_states[i].set_xdata(traj[t,0])
            current_states[i].set_ydata(traj[t,1])
            ax.set_title(' Lake attractors, and dynamics at t=' + str(int(t * dt)), loc='left', x=0.2)
    return mplfig_to_npimage(fig)

# Animating
time = np.arange(t_initial,traj.shape[0]+t_final,data_interval) # time in the data structure
animation = DataVideoClip(time,make_frame,fps=fps)
animation.write_gif("lake_trajectories.gif",fps=fps)
