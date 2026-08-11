import scipp as sc
from kinisi.analyze import DiffusionAnalyzer
import numpy as np

def com_diffusion(residues, u):
    p_params = {
        'specie_indices': sc.array(dims=['particle', 'atoms in particle'],
                      values=np.array([r.atoms.indices for r in residues])),
        'time_step': 1 * sc.Unit('fs'),
        'step_skip': 500 * sc.Unit('dimensionless'),
        'masses': sc.array(dims=['atoms in particle'], values=residues[0].atoms.masses)
    }

    return DiffusionAnalyzer.from_universe(u, **p_params)