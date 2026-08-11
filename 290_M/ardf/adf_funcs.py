import numpy as np  
from MDAnalysis.lib.distances import capped_distance
from multiprocessing import Pool
from utility import call_traj

# defining vectors for angulare distribution function (ADF) calculation
def calc_OH_vectors(methanols):
    o = methanols.select_atoms("type 14").positions  # select oxygen atoms of methanol molecules
    h = methanols.select_atoms("type 18").positions  # select hydrogen atom of the OH bond of methanol molecules
    # Calculate the vector from oxygen to hydrogen for each methanol molecule
    oh_vectors = h - o
    return oh_vectors

def calc_ccom_vectors(benzene):
    ccom_vectors = []
    benzene.unwrap()
    for res in benzene.residues:
        com = res.atoms.center_of_mass()
        c = res.atoms.select_atoms("type 1 ").positions[0]
        com_vector = c - com
        ccom_vectors.append(com_vector)
    # normalize the vector
    ccom_vector = np.array(ccom_vectors)
    return ccom_vector

def calc_angles(vectors1, vectors2):
    # Normalize the vectors
    norm_vectors1 = vectors1 / np.linalg.norm(vectors1, axis=1)[:, np.newaxis]
    norm_vectors2 = vectors2 / np.linalg.norm(vectors2, axis=1)[:, np.newaxis]

    # Calculate the dot product and then the angle

    dot_product = np.clip(np.einsum('ij,ij->i', norm_vectors1, norm_vectors2), -1, 1)
    angles = np.arccos(dot_product)  # in radians

    return np.degrees(angles)  # convert to degrees

def angular_dis_func ( benzene, methanol, max, trajectory, dist_shown):
    all_angles = []
    all_dists = []

    for ts in trajectory:
        vector1 = calc_OH_vectors(methanol)
        vector2 = calc_ccom_vectors(benzene)

        o_positions = methanol.select_atoms("type 14").positions
        benzene.unwrap()
        benzene_com = np.array([res.atoms.center_of_mass() for res in benzene.residues])

        pairs, dists = capped_distance(o_positions, benzene_com, max_cutoff=max, box=ts.dimensions, return_distances=True)
        # pairs: (n_pairs, 2) array of [methanol_idx, benzene_idx]

        v1 = vector1[pairs[:, 0]]
        v2 = vector2[pairs[:, 1]]

        angles = calc_angles(v1, v2)
        all_angles.append(angles)
        all_dists.append(dists)

    all_angles = np.concatenate(all_angles)
    all_dists = np.concatenate(all_dists)

    box_volume = trajectory[0].dimensions[:3].prod() 
    n_frames = len(trajectory)
    n_methanol = len(methanol.residues)
    n_benzene = len(benzene.residues)
    benzene_number_density = n_benzene / box_volume   # molecules per Å³

    dist_bins = np.linspace(0, dist_shown, 50)
    angle_bins = np.linspace(0, 180, 50)

    counts, dist_edges, angle_edges = np.histogram2d(all_dists, all_angles, bins=[dist_bins, angle_bins])

    r1 = dist_edges[:-1]
    r2 = dist_edges[1:]
    shell_volumes = (4/3) * np.pi * (r2**3 - r1**3)  

    theta1 = np.radians(angle_edges[:-1])
    theta2 = np.radians(angle_edges[1:])
    solid_angle_frac = (np.cos(theta1) - np.cos(theta2)) / 2   

    expected_counts = (n_frames * n_methanol * benzene_number_density
                    * shell_volumes[:, np.newaxis]
                    * solid_angle_frac[np.newaxis, :])

    g_r_theta = np.divide(counts, expected_counts,
                       out=np.zeros_like(counts, dtype=float),
                       where=expected_counts != 0)

    return dist_edges, angle_edges, g_r_theta.T

### parrelel procesing implementtaion 

def _workers(args) :

    topo_path, traj_path, start, stop, dist_shown, dt, cutoff = args

    u, benzenes, methanols = call_traj(topo_path, traj_path, dt)
    
    dist_bins = np.linspace(0, dist_shown, 50)
    angle_bins = np.linspace(0, 180, 50)

    all_angles = []
    all_dists = []

    for ts in u.trajectory[start:stop]:
        vector1 = calc_OH_vectors(methanols)
        vector2 = calc_ccom_vectors(benzenes)

        o_positions = methanols.select_atoms("type 14").positions
        benzenes.unwrap()
        benzene_com = np.array([res.atoms.center_of_mass() for res in benzenes.residues])

        pairs, dists = capped_distance(o_positions, benzene_com, max_cutoff=cutoff, box=ts.dimensions, return_distances=True)
        # pairs: (n_pairs, 2) array of [methanol_idx, benzene_idx]

        v1 = vector1[pairs[:, 0]]
        v2 = vector2[pairs[:, 1]]

        angles = calc_angles(v1, v2)
        all_angles.append(angles)
        all_dists.append(dists)

    all_angles = np.concatenate(all_angles)
    all_dists = np.concatenate(all_dists)

    counts, dist_edges, angle_edges = np.histogram2d(all_dists, all_angles, bins=[dist_bins, angle_bins])

    n_frames_chunk = stop - start

    return n_frames_chunk, counts, dist_edges, angle_edges

def multiproccesing_angular_radidal_func(topo_path, traj_path, dist_shown, dt, cutoff, n_workers=None, n_frames=None):

    u, benzenes, methanols = call_traj(topo_path, traj_path, dt)

    box_volume = u.trajectory[0].dimensions[:3].prod() 
    total_frames = len(u.trajectory)
    n_methanol = len(methanols.residues)
    n_benzene = len(benzenes.residues)
    benzene_number_density = n_benzene / box_volume   # molecules per Å³

    if n_workers == None :
        n_workers = min(Pool()._processes, total_frames)
    bounds = np.linspace(0,total_frames, n_workers + 1, dtype=int)
    
    chunks = []
    for i in range(n_workers):
        chunks.append((bounds[i], bounds[i+1]))

    tasks = [(topo_path, traj_path, start, stop, dist_shown, dt, cutoff) for start, stop in chunks]

    with Pool(processes=n_workers) as pool:
        results = pool.map(_workers, tasks)

    total_counts = np.sum([r[1] for r in results], axis=0)
    total_frames = sum(r[0] for r in results)

    dist_edges, angle_edges = results[0][2], results[0][3]

    r1 = dist_edges[:-1]
    r2 = dist_edges[1:]
    shell_volumes = (4/3) * np.pi * (r2**3 - r1**3)  

    theta1 = np.radians(angle_edges[:-1])
    theta2 = np.radians(angle_edges[1:])
    solid_angle_frac = (np.cos(theta1) - np.cos(theta2)) / 2   

    expected_counts = (total_frames * n_methanol * benzene_number_density
                    * shell_volumes[:, np.newaxis]
                    * solid_angle_frac[np.newaxis, :])

    g_r_theta = np.divide(total_counts, expected_counts,
                       out=np.zeros_like(total_counts, dtype=float),
                       where=expected_counts != 0)

    return dist_edges, angle_edges, g_r_theta.T



    