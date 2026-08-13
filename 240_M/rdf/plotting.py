import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

ccom_data = np.loadtxt(f'ccom.txt', delimiter=',')
ccom_bins = ccom_data[0, :]
ccom_rdf = ccom_data[1, :]

hcom_data = np.loadtxt(f'hcom.txt', delimiter=',')
hcom_bins = hcom_data[0, :]
hcom_rdf = hcom_data[1, :]

ocom_data = np.loadtxt(f'ocom.txt', delimiter=',')
ocom_bins = ocom_data[0, :]
ocom_rdf = ocom_data[1, :]

fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'sans-serif'
fig.set_size_inches(5.5,5)


ocom_offset = 0.8
hcom_offset = 1.6
ccom_offset = 0.0

offsets = [ocom_offset, hcom_offset, ccom_offset]
rdfs = [ocom_rdf, hcom_rdf, ccom_rdf]
bins = [ocom_bins, hcom_bins, ccom_bins]
colors = ["tab:orange", "tab:blue", "tab:green"]
labels = ['O-(H) CoM RDF', 'H-(O) CoM RDF', 'C-(O) CoM RDF']

for i in range(3):
    ax.plot(bins[i], rdfs[i] + offsets[i], label=labels[i], color=colors[i])
    peaks, properties = find_peaks(rdfs[i], height=0.1, distance=10)

    #ax.axvline(bins[i][peaks[0]], color=colors[i], ls='--', lw=1, alpha=0.6)
    #ax.text(bins[i][peaks[0]], offsets[i], f'{bins[i][peaks[0]]:.2f} Å', color=colors[i],
            #   ha='center', fontsize=10, fontweight='bold')

ax.set_xlabel('r / Å')
ax.set_ylabel ('g(r) CoM - MeOH')
ax.legend()
plt.savefig(f'rdf.pdf', bbox_inches='tight')