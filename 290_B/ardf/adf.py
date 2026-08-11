from utility import call_traj
import adf_funcs as af
import numpy as np 
import os


u, benzenes, methanols = call_traj('../prod_traj/prod.data', f'../prod_traj/production_6000frames_50fsframe.atom', 50)

cutoff = 30
dist_shown = 12
dist_edges, angle_edges, g_r_theta = af.angular_dis_func(benzenes, cutoff, u.trajectory, dist_shown)

X = g_r_theta
outpath = "g_r_theta.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')
X = dist_edges, angle_edges

outpath = "edges.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')