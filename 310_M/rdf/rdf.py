from utility import call_traj
import rdf_funcs as rd
import MDAnalysis as mda
from MDAnalysis.analysis import rdf
import numpy as np 
import os


u, benzenes, methanols = call_traj(f'../prod_traj/prod.data', f'../prod_traj/production_6000frames_50fsframe.atom', 50)

current_dir = os.getcwd()

com_groups = benzenes.fragments  # if you have bond information
c = rd.BeadGroup(com_groups)

O = u.select_atoms('type 14')
ocom = rdf.InterRDF(O, c, range=(0,10)) 
ocom.run(verbose=False)
X = ocom.results.bins, ocom.results.rdf
outpath = f"{current_dir}/ocom.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')


H = u.select_atoms('type 18')
hcom = rdf.InterRDF(H, c, range=(0,10)) 
hcom.run(verbose=False)
X = hcom.results.bins, hcom.results.rdf
outpath = f"{current_dir}/hcom.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')

C = u.select_atoms('type 13')
ccom = rdf.InterRDF(C, c, range=(0,10)) 
ccom.run(verbose=False)
X = ccom.results.bins, ccom.results.rdf
outpath = f"{current_dir}/ccom.txt"
os.makedirs(os.path.dirname(outpath), exist_ok=True)
np.savetxt(outpath, X, delimiter=',')


