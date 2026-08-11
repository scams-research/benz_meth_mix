import MDAnalysis as mda
import numpy as np
import sys
import matplotlib.pyplot as plt

def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    nearest = array[idx]
    return nearest, idx

def box_sizer(topo,traj):
    '''
    This 100% will not work for triclinic cells
    '''
    # Traj loading
    u  = mda.Universe(topo, format = 'DATA')
    u.load_new(traj, format='LAMMPSDUMP')

    # Extracting box coords
    box_store = np.zeros((len(u.trajectory),6))
    for i,frame in enumerate(u.trajectory):
        box_store[i] = frame.dimensions

    #Analysis
    mean_size = box_store.mean(axis=0)
    med_size = np.median(box_store, axis = 0)
    nearest , index = find_nearest(box_store[:,0], mean_size[0])

    fig, ax = plt.subplots(figsize = (8,4))
    ax.plot(box_store[:,0], label = 'box size')
    ax.axhline(mean_size[0], label = 'Average box size', color = 'tab:red')
    ax.set_ylabel('Box size')
    plt.savefig('sized_box.pdf', bbox_inches = 'tight')

    return int(u.trajectory[index].time)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python box_sizer.py <topo_file> <traj_file>", file=sys.stderr)
        sys.exit(1)
    
    topo_file = sys.argv[1]
    traj_file = sys.argv[2]
    
    result = box_sizer(topo_file, traj_file)
    print(result)  