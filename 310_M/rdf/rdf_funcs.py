import numpy as np
from MDAnalysis.analysis import rdf

# ----- RDFs ------
class BeadGroup(object):
    def __init__(self, groups):
        self._groups = groups

    def __len__(self):
        return len(self._groups)

    @property
    def positions(self):
        return np.array([g.center_of_mass(unwrap = True) for g in self._groups], dtype=np.float32)

    @property
    def universe(self):
        return self._groups[0].universe

def COM_RDF(u):
    com_groups = u.fragments  # if you have bond information
    c = BeadGroup(com_groups) 
    irdf_res = rdf.InterRDF(c,c,range =(0,10), exclusion_block=(1,1), verbose = True)
    irdf_res.run()
    return irdf_res