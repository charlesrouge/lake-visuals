import attractors
import numpy as np
from moviepy.video.VideoClip import DataVideoClip
import matplotlib.pyplot as plt
from matplotlib import lines

# Lake parameters
b = 0.42  # 0.65 in blog post
q = 2  # 4 in blog post

# Time parameters
dt = 0.01  # time step
T = 30  # final horizon
nt = int(T/dt+1E-6)  # number of time steps

# Initial phosphorus levels
p_min = 0
pmed = 1
p_max = 2.5

# Inputs levels
p_inputs = np.arange(0.001, 0.201, 0.005)

# Store trajectories
low_p = np.zeros([len(p_inputs), nt + 1])  # Correspond to p_min
med_p = np.zeros([len(p_inputs), nt + 1])  # Correspond to pmed
high_p = np.zeros([len(p_inputs), nt + 1])  # Correspond to p_max

# Equilibria of the lake problem
equilibrium_list = attractors.lake_attractors(b, q, p_inputs[-1])

# Get them!
for i in range(len(p_inputs)):
    low_p[i, :] = attractors.trajectory(b, q, p_min, p_inputs[i], dt, T)
    med_p[i, :] = attractors.trajectory(b, q, pmed, p_inputs[i], dt, T)
    high_p[i, :] = attractors.trajectory(b, q, p_max, p_inputs[i], dt, T)

# Draw animated figure
fig, ax = plt.subplots(1)
ax.set_xlabel('Phosphorus inputs L')
ax.set_ylabel('Phosphorus concentration P')
ax.set_xlim(0, p_inputs[-1])
ax.set_ylim(0, p_max)
ax.plot(p_inputs, low_p[:, 0], '.', label='State, P(0)=0', alpha=0.3, color='b')
ax.plot(p_inputs, med_p[:, 0], '.', label='State, P(0)=1', alpha=0.3, color='orange')
ax.plot(p_inputs, high_p[:, 0], '.', label='State, P(0)=2.5', alpha=0.3, color='r')
line_low, = ax.plot(p_inputs, low_p[:, 0], '.', label='State, P(0)=0', color='b')
line_med, = ax.plot(p_inputs, med_p[:, 0], '.', label='State, P(0)=1', color='orange')
line_high, = ax.plot(p_inputs, high_p[:, 0], '.', label='State, P(0)=2.5', color='r')
attractors.lake_att_base(equilibrium_list, 0.001)
# Save initial figure if you want
# fig.savefig('canvas_1.png')

# Parameters of the animation
initial_delay = 0.5  # in seconds, delay where image is fixed before the animation
final_delay = 0.5  # in seconds, time interval where image is fixed at end of animation
time_interval = 0.25  # interval of time between two snapshots in the dynamics (time unit or non-dimensional)
fps = 20  # number of frames per second on the GIF
# Translation in the data structure
data_interval = int(time_interval/dt)  # interval between two snapshots in the data structure
t_initial = -initial_delay*fps*data_interval
t_final = final_delay*fps*data_interval
time = np.arange(t_initial, low_p.shape[1]+t_final, data_interval)  # time in the data structure


# Making frames
def make_frame(t):
    t = int(t)
    if t < 0:
        return make_frame(0)
    elif t > nt:
        return make_frame(nt)
    else:
        line_low.set_ydata(low_p[:, t])
        line_med.set_ydata(med_p[:, t])
        line_high.set_ydata(high_p[:, t])
        ax.set_title(' Lake attractors, and dynamics at t=' + str(int(t*dt)), loc='left', x=0.2)
        fig.canvas.draw()
        return np.asarray(fig.canvas.buffer_rgba())[:, :, :3]


# Animating
animation = DataVideoClip(time, make_frame, fps=fps)
animation.write_gif("lake_attractors.gif", fps=fps)
