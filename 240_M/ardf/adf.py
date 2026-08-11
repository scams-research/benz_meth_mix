from utility import call_traj
import adf_funcs as af
import numpy as np 
import os
from multiprocessing import Pool

u, benzenes, methanols = call_traj('../prod_traj/prod.data', '../prod_traj/production_6000frames_50fsframe.atom', 50)

current_dir = os.getcwd()

cutoff = 30
dist_shown = 12
dist_edges, angle_edges, g_r_theta = af.angular_dis_func(benzenes, methanols, cutoff, u.trajectory, dist_shown)

X = g_r_theta
outpath = f"{current_dir}/g_r_theta.txt"
np.savetxt(outpath, X, delimiter=',')

X = dist_edges, angle_edges
outpath = f"{current_dir}/edges.txt"
np.savetxt(outpath, X, delimiter=',')