import numpy as np
import matplotlib.pyplot as plt
from kinisi.analyze import DiffusionAnalyzer


def uncertainty_plotter(kinisi_obnameect, 
                        axis = None,
                        color = '#0173B2'):
    credible_intervals = [[16, 84], [2.5, 97.5], [0.15, 99.85]]
    alpha = [0.6, 0.4, 0.2]

    if axis == None:
        fig, axis = plt.subplots()

    axis.plot(kinisi_obnameect.dt.values, kinisi_obnameect.msd.values, 'k-')
    for i, ci in enumerate(credible_intervals):
        axis.fill_between(kinisi_obnameect.dt.values,
                        *np.percentile(kinisi_obnameect.distributions, ci, axis=1),
                        alpha=alpha[i],
                        color=color,
                        lw=0)
    axis.set_xlabel(f'Time / {kinisi_obnameect.dt.unit}')
    axis.set_ylabel(f'MSD / {kinisi_obnameect.msd.unit}')
    axis.set_xlim(0, None)
    axis.set_ylim(0, None)

methanol_diffusion = DiffusionAnalyzer.from_hdf5('methanol_diffusion.h5')
benzene_diffusion = DiffusionAnalyzer.from_hdf5('benzene_diffusion.h5')

c1 = "#029E73"
c2 = "#CC78BC"
colors = [c1,c2]

fig, ax = plt.subplots(1,2)
fig.set_size_inches(8,3)
fig.subplots_adjust(wspace=0.3)
fig.suptitle('benzene methanol diffusion')



for diff, color, label in zip([methanol_diffusion,benzene_diffusion], colors, ['methanol','benzene']):

    uncertainty_plotter(diff, ax[0], color = color)
    ax[1].hist(diff.D.values, density=True, color = color, label = label, alpha = 0.6)
    ax[1].axvline(diff.D.mean().values, c='k')


ax[1].set_xlabel('$D$/cm$^2$s$^{-1}$')
ax[1].set_ylabel('$p(D$/cm$^2$s$^{-1})$')
ax[1].legend()

fig.savefig('diffusion.pdf', bbox_inches='tight')