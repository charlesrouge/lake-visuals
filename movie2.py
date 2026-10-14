import attractors
import numpy as np
from moviepy.video.VideoClip import DataVideoClip
import matplotlib.pyplot as plt
from matplotlib import lines

# 2026 update unfinished

# Lake parameters
b = 0.42  # 0.65 in blog post
q = 2  # 4 in blog post

# Time parameters
dt = 0.01  # time step
T = 40  # final horizon
nt = int(T/dt+1E-6)  # number of time steps

# Parameters of animation
l0 = [0.35, 0.375, 0.4]  # initial inputs
p0 = [0]  # initial phosphorus levels
# Policy parameters
dl_over_dt = 1E-2  # rate of input decrease
l_min = 0.08  # minimal input levels
# Maximal phosphorus input considered in this code
l_max = 0.4
# Maximal phosphorus concentration in animation
p_max = 2.5

# Equilibria of the lake problem
equilibrium_list = attractors.lake_attractors(b, q, l_max)
"""
# PLot them!
def lakeAttBase(equilibrium_list,dl):
    l1 = np.arange(equilibrium_list.first[0], equilibrium_list.first[0] + len(equilibrium_list.oligotrophic) * dl, dl)
    l2 = np.arange(equilibrium_list.first[1], equilibrium_list.first[1] + len(equilibrium_list.Unst) * dl - 1E-10, dl)
    l3 = np.arange(equilibrium_list.first[2], equilibrium_list.first[2] + len(equilibrium_list.eutrophic) * dl - 1E-10, dl)
    plt.plot(l1, equilibrium_list.oligotrophic, color='k')
    plt.plot(l2, equilibrium_list.Unst, linestyle='--', color='k')
    plt.plot(l3, equilibrium_list.eutrophic, color='k')
    return None
unstable = lines.Line2D([], [], color='k', linestyle='--', label = 'Unstable')
stable = lines.Line2D([], [], color='k', label='Stable')


# Generating the data: trajectories
def trajectory(b,q,p0,l0,dldt,dt,T):
    # Declare outputs
    time = np.arange(0,T+dt,dt)
    traj = np.zeros([len(time),2])
    # Initialize traj
    traj[0,:] = [l0,p0]
    # Fill traj with values
    for i in range(1,len(traj)):
        traj[i,0] = max(l_min, traj[i - 1,0] - dldt * dt)
        traj[i, 1] = traj[i-1, 1] + dt * attractors.lake_dynamics(traj[i-1, 1], b, q, traj[i-1, 0])
    return traj
"""

# Get them!
trajectories = []
for i in range(len(l0)):
    for j in range(len(p0)):
        traj = attractors.trajectory(b, q, p0[j], l0[i], dt, T)  # dl_over_dt, dt, T)
        trajectories.append(traj)

# Draw animated figure
fig, ax = plt.subplots(1)
ax.set_xlabel('Phosphorus inputs L')
ax.set_ylabel('Phosphorus concentration P')
ax.set_xlim(0, l_max)
ax.set_ylim(0, p_max)
attractors.lake_att_base(equilibrium_list, 0.001)
lines = []
current_states = []
for i in range(len(trajectories)):
    traj = trajectories[i]
    line, = ax.plot(traj[0, 0], traj[0, 1], color='b', label='Trajectory')
    point, = ax.plot(traj[0, 0], traj[0, 1], '.', color='r', label='Current state')
    lines.append(line)
    current_states.append(point)
plt.legend(handles=[line, point], loc=2)
# Save initial figure if you want
# fig.savefig('canvas_2.png')

# Parameters of the animation
initial_delay = 0  # in seconds, delay where image is fixed before the animation
final_delay = 1  # in seconds, time interval where image is fixed at end of animation
time_interval = 0.25  # interval of time between two snapshots in the dynamics (time unit or non-dimensional)
fps = 20  # number of frames per second on the GIF
# Translation in the data structure
data_interval = int(time_interval/dt)  # interval between two snapshots in the data structure
t_initial = -initial_delay*fps*data_interval
t_final = final_delay*fps*data_interval


# Making frames
def make_frame(t):
    t = int(t)
    if t < 0:
        return make_frame(0)
    elif t > nt:
        return make_frame(nt)
    else:
        for tra in range(len(trajectories)):
            this_tra = trajectories[tra]
            lines[tra].set_xdata(this_tra[0:t, 0])
            lines[tra].set_ydata(this_tra[0:t, 1])
            current_states[tra].set_xdata(this_tra[t, 0])
            current_states[tra].set_ydata(this_tra[t, 1])
        ax.set_title(' Lake attractors, and dynamics at t=' + str(int(t * dt)), loc='left', x=0.2)
        fig.canvas.draw()
    return np.asarray(fig.canvas.buffer_rgba())[:, :, :3]


# Animating
time = np.arange(t_initial, traj.shape[0]+t_final, data_interval)  # time in the data structure
animation = DataVideoClip(time, make_frame, fps=fps)
animation.write_gif("lake_trajectories.gif", fps=fps)
