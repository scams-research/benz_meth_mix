import os
from utility import call_traj
import racf_funcs as rf
import numpy as np 
import dynesty
from racf_models_ns import *
import pickle
from nest_sampling_funcs import *



u, benzenes, methanols = call_traj('../prod_traj/prod.data', '../prod_traj/production_6000frames_50fsframe.atom', 50)

window_size = 150

mean_tumble, std_tumble, t_ps_tumble = rf.NOW_compute_acf(benzenes, rf.perp_to_ring_vector, window_size=window_size, u=u)
mean_tns, std_tns, t_ps_tns = rf.NOW_compute_acf(benzenes, rf.ccom_vector, window_size=window_size, u=u)

sterr_tns = std_tns/(6000/150) + 1E-10
sterr_tumble = std_tumble/(6000/150) + 1E-10

current_dir = os.getcwd()

X = mean_tns, std_tns, sterr_tns, t_ps_tns
outpath = f"{current_dir}/tns.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')

X = mean_tumble, std_tumble, sterr_tumble, t_ps_tumble
outpath = f"{current_dir}tumble.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')

y = np.array([mean_tns,mean_tumble])
err = np.array([sterr_tns,sterr_tumble])
t = t_ps_tns

perpendicular_results = {}
for name, bounds, model in zip(names, bounds_list, perpendicular_models):
    sampler = dynesty.DynamicNestedSampler(log_likelihood, prior_transform, len(bounds), logl_args=(t, y, model, err), ptform_args=(bounds,), sample='rslice')
    sampler.run_nested(print_progress=True, nlive_init=1000, nlive_batch=500)
    ns_res =sampler.results

    outpath = f"{current_dir}/{name}.pkl"
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    with open(f'{name}.pkl', 'wb') as f:
        pickle.dump(ns_res.asdict(), f)
    perpendicular_results[name] = ns_res
