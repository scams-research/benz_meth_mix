from utility import call_traj
import adf_funcs as af
import numpy as np 
import os
from multiprocessing import Pool

if __name__ =="__main__":
    cutoff = 30
    dist_shown = 12
    topo_path = '../prod_traj/prod.data'
    traj_path = '../prod_traj/production_6000frames_50fsframe.atom'
    dt = 50
    dist_shown = 12
    n_workers = 144
    dist_edges, angle_edges, g_r_theta = af.multiproccesing_angular_radidal_func(topo_path, traj_path, dist_shown, dt, cutoff, n_workers)


    current_dir = os.getcwd()
    
    X = g_r_theta
    outpath = f"{current_dir}/g_r_theta.txt"
    np.savetxt(outpath, X, delimiter=',')

    X = dist_edges, angle_edges
    outpath = f"{current_dir}/edges.txt"
    np.savetxt(outpath, X, delimiter=',')