import numpy as np  
from MDAnalysis.lib.distances import capped_distance

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

def angular_dis_func ( benzene, max, trajectory, dist_shown):
    all_angles = []
    all_dists = []

    for ts in trajectory:
        vector1 = calc_ccom_vectors(benzene)
        vector2 = calc_ccom_vectors(benzene)

        
        benzene_com = np.array([res.atoms.center_of_mass() for res in benzene.residues])

        pairs, dists = capped_distance(benzene_com, benzene_com, max_cutoff=max, return_distances=True)
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

    expected_counts = (n_frames * benzene_number_density
                    * shell_volumes[:, np.newaxis]
                    * solid_angle_frac[np.newaxis, :])

    g_r_theta = np.divide(counts, expected_counts,
                       out=np.zeros_like(counts, dtype=float),
                       where=expected_counts != 0)

     

    return dist_edges, angle_edges, g_r_theta.T


