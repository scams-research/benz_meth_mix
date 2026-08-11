import os
from diffusion_funcs import com_diffusion
from utility import call_traj
import numpy as np
import scipp as sc



u, benzenes, methanols = call_traj('../prod_traj/prod.data', '../prod_traj/production_6000frames_50fsframe.atom', 50)

methanol_diffusion = com_diffusion(methanols.residues, u)
benzene_diffusion = com_diffusion(benzenes.residues, u)

fickian_start = 100.0  

for d in (methanol_diffusion, benzene_diffusion):
    d.diffusion(start_dt=sc.scalar(fickian_start, unit='ps'))

methanol_diffusion.to_hdf5('methanol_diffusion.h5')
benzene_diffusion.to_hdf5('benzene_diffusion.h5')
    