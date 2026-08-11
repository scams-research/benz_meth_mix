from racf_models_ns import *
import pickle 
from dynesty.utils import Results
import matplotlib.pyplot as plt

max_logz_list = []
for name in names:
    file_name = f'{name}.pkl'
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    res = Results(data)
    max_logz_list.append(res['logz'][-1])
max_arr = np.array(max_logz_list)

max_of_max = max_arr.max()
position_of_max_z = max_logz_list.index(max_of_max)
best_model_name = names[position_of_max_z]
best_model = perpendicular_models[position_of_max_z]
    
file_name = f'{best_model_name}.pkl'
with open(file_name, 'rb') as file:
    data = pickle.load(file)
res = Results(data)
shape = res.samples_equal().shape[1]
rows = int(shape / 2)
fig, axes = plt.subplots(rows, 2, figsize=(14, 4*rows))
fig.set_tight_layout
fig.suptitle(f"parameter distributions for {best_model_name} with Z = {res['logz'][-1]}")
axes = axes.flatten()
for name, k in zip(range(shape), param_names[best_model_name]):
        ax = axes[name]
        ax.hist(res.samples_equal()[:,name], bins=100)
        ax.axvline(res.samples_equal()[:,name].mean(), c='k', label=f'{res.samples_equal()[:,name].mean():.6f}')
        ax.set_xlabel(k)
        ax.tick_params(axis='both', labelsize=8)
        ax.legend()
        fig.savefig(f'ns_params_{best_model_name}.pdf', bbox_inches='tight')

file_name = f'{best_model_name}.pkl'
with open(file_name, 'rb') as file:
    data = pickle.load(file)
res = Results(data)
mean_parms = res.samples_equal().mean(axis=0)

data_tumble = np.loadtxt(f'tumble.txt', delimiter=',')
data_tns = np.loadtxt(f'tns.txt', delimiter=',')

mean_tns = data_tns[0,:]
mean_tumble = data_tumble[0,:]

std_tns = data_tns[1,:]
std_tumble = data_tumble[1,:]

sterr_tns = data_tns[2,:]
sterr_tumble = data_tumble[2,:]

t_tns = data_tns[3,:]
t_tumble = data_tumble[3,:]

y = np.array([mean_tns,mean_tumble])
err = np.array([sterr_tns,sterr_tumble])
t = t_tns

y_fit = best_model(t, *mean_parms)

fig, ax = plt.subplots()

ax.set_title(f'fitted model : {best_model_name}')

ax.plot(t, y_fit[0,:],label='tumbling and spinning', color='orange',alpha=1)
ax.plot(t, y_fit[1,:],label='tumbling and spinning', color='red',alpha=1)

ax.errorbar(t, y[0,:], yerr=sterr_tns*50, ecolor='orange', alpha=0.6, barsabove=True, label='tumbling and spinning ', fmt='None')
ax.errorbar(t, y[1,:], yerr=sterr_tumble*50, ecolor='red', alpha=0.6, barsabove=True, label='tumbling', fmt='None')
ax.set_xlabel('time / ps')
ax.set_ylabel('rotation autocorrelation function')
ax.legend()
fig.savefig(f'fit_{best_model_name}.pdf', bbox_inches='tight')