import numpy as np

### defing vectors to be used in the autocorrelation function for benzene molecules

# defing vectors for spinning motion for benzene molecules
def ccom_vector(benzene):
    ccom_vectors = []
    benzene.unwrap()
    for res in benzene.residues:
        com = res.atoms.center_of_mass()
        c = res.atoms.select_atoms("type 1 ").positions[0]
        com_vector = c - com
        ccom_vectors.append(com_vector)
    # normalize the vector
    ccom_vector = np.array(ccom_vectors)
    ccom_vector /= np.linalg.norm(ccom_vector, axis=1, keepdims=True)
    return ccom_vector

# defing vectors for tumbling motion for benzene molecules
def perp_to_ring_vector(benzene):
    benzene.unwrap()
    coms = np.array([res.atoms.center_of_mass() for res in benzene.residues])
    c1 = benzene.select_atoms("type 1 ").positions
    c2 = benzene.select_atoms("type 2 ").positions
    c1com_vector = c1 - coms
    c2com_vector = c2 - coms
    c1com_x_c2com = np.cross(c1com_vector, c2com_vector)
    # normalize the vector
    c1com_x_c2com /= np.linalg.norm(c1com_x_c2com, axis=1, keepdims=True)
    return c1com_x_c2com

### rotational autocorrelation functions ###


def compute_acf(benzene, vector_function, u):
    '''
    Computes rotational auto correlation function form a single reference point at frame 0.
    It uses the second order legrendre polynomial.
    '''
    acf = np.zeros(len(u.trajectory)) # initialize the autocorrelation function array
    ts = u.trajectory[0]
    vectors_0 = vector_function(benzene)

    # compute the autocorrelation function for each frame in the trajectory
    for ts in u.trajectory:
        vectors = vector_function(benzene)
        cos_theta = np.sum(vectors * vectors_0, axis=1)
        acf[ts.frame] = np.mean(0.5*(3*cos_theta**2- 1))
    return acf

def NOW_compute_acf(benzene, vector_function, window_size, u): # non-overlapping window (NOW) autocorrelation function
    '''
    Computes a non-overlapping sliding rotational autocorelation function of a given window size 
    '''
    benzene.unwrap() # unwrap the benzene molecules to avoid periodic boundary condition
    length = len(u.trajectory)
    number_of_windows = length // window_size
    acf = np.zeros((window_size,number_of_windows)) # initialize the autocorrelation function array
    t_ps = np.arange(window_size) * u.trajectory.dt * 1e-3 # time in ps

    for start in range(0, number_of_windows, 1):
        start_of_window = start * window_size
        end_of_window = start_of_window + window_size

        u.trajectory[start_of_window]
        vectors_reference = vector_function(benzene)
        
        window = u.trajectory[start_of_window:end_of_window] 
        for ts in window:
            benzene.unwrap()
            vectors = vector_function(benzene)
            cos_theta = np.sum(vectors * vectors_reference, axis=1)
            window_index = ts.frame - start_of_window
            acf[window_index,start] = np.mean(0.5*(3*cos_theta**2- 1), axis=0) # compute the autocorrelation function using the second Legendre polynomial 
    
    mean_acf = np.mean(acf, axis=1) # compute the mean autocorrelation function over all windows
    std_acf = np.std(acf, axis=1)   
    
    return mean_acf, std_acf, t_ps