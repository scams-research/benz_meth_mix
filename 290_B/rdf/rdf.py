from utility import call_traj
import rdf_funcs as rd
import MDAnalysis as mda
from MDAnalysis.analysis import rdf
import numpy as np 
import os


u, benzenes, methanols = call_traj(f'../prod_traj/prod.data', f'../prod_traj/production_6000frames_50fsframe.atom', 50)

com_groups = benzenes.fragments  # if you have bond information
c = rd.BeadGroup(com_groups)

com_com = rdf.InterRDF(c, c, range=(0,10)) 
com_com.run(verbose=False)
X = com_com.results.bins, com_com.results.rdf
outpath = f"com_com.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')



