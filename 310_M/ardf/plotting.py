import numpy as np
import matplotlib.pyplot as plt
import os

ardf_edges = np.loadtxt(f'edges.txt', delimiter=',')
ardf_values = np.loadtxt(f'g_r_theta.txt', delimiter=',')

dist_edges = ardf_edges[0,:]
angle_edges = ardf_edges[1,:]
g_r_theta = ardf_values

plt.figure(figsize=(7, 6))
plt.pcolormesh(dist_edges, angle_edges, g_r_theta, cmap='viridis', vmin=0)
plt.colorbar(label='g(r, θ)')
plt.xlabel('Distance (Å)')
plt.ylabel('Angle (degrees)')
plt.title('Pair Correlation Function g(r, θ)')

current_dir = os.getcwd()

plt.savefig(f'{current_dir}/ardf_colourmap.pdf', bbox_inches='tight')
