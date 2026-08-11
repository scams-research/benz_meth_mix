import MDAnalysis as mda

def call_traj(DATA,ATOM,DT):
    '''
    DATA is the topology file
    ATOM is the trajectory file
    '''

    u = mda.Universe(DATA, ATOM, format="LAMMPSDUMP", topology_format="DATA", dt=DT)

    benzenes = u.select_atoms("type 1 2 3 4 5 6  7 8 9 10 11 12 ") # select benzene molecules
    methanols = u.select_atoms("type 13 14 15 16 17 18 ") # select methanol molecules

    return u, benzenes, methanols