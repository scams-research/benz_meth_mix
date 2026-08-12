# Molecular dynamic simulations and analysis of a benzene and methanol mixture 

This project allows the running and anaylysis of lammps simulations. The lammps files that run the simmulations are split into two parts the equiliberation and then the production, they are intened to be run in this order. The files together produce a porduction topography and trajectory that is then able to be proccesed using python code to analysis the structure and dynamics of the benzene and methanol mixture. The python code produces angular-radial distribution functions (ARDFs), radial distribution functions (RDFs), translational diffusion coeffecients and rotational autocorrelation functions (RACFs).

## Requirments 
- python 3.11.15
- Packages can be found in requirments.txt
- lammps exacutable configured for use on HPC

## Installation 

First install the repository form git hub using commands below.

```bash
git clone git@github.com:scams-research/benz_meth_mix.git
cd benz_meth_mix
pip install -r requirments.txt
```

Install lammps exacutable. For help installing a lammps exacutable see [lammps docs](https://docs.lammps.org/Manual.html).

Then insert the lammps exacutable into every prod.slurm and equil.slurm where it says lmp=<path/to/exacutable>. See below lines 17-18 in prod.slurm.

```bash
LMP=<path/to/lammps/exacutable>
srun "$LMP" -in prod.lammps -log ${SLURM_JOB_ID}.log
```

## Usage

### Running the equiliberation simulations

To submit equiliberation simulations in every temperture directory a bash command such as this can be used.

```bash
for temp in 190_M 240_M 290_B 290_M 310_M; do 
    ( cd "$temp" || exit
      sbatch equil.slurm
    )
done
```
To submit a single equiliberation simply navigate to the directory contating the lammps file u wish to submit using `cd`. the us the sbatch command followed by slurm file whcih calls the mamps file of intrest. See the example below.

```bash
cd 190_M
sbatch equil.slurm
```

### Running the box_sizer.py

To run the production simulations the `box_sizer.py` needs to be run and the out put needs to be pasted into the production lammps so it nows which frame to read the box size from in the equilberation trajectory (file usually found in lines 13-14). The lines below show where to input the frame number.

```lammps
read_data equil_traj/density.data
read_dump equil_traj/density.atom <output of box sizer> x y z box yes
```
The box_sizer can be run for each equiliberation trajectory across all directories using this command.

```bash
for loc in 190_M 240_M 290_B 310_M; do 
 (
 cd "$loc" || exit
 pyhton3 box_sizer.py ../equil_traj/density.data ../equil_traj/density.atom
 )
 done
```

To run for any single trajectory there must be an in put of a topography file (i.e the .data file in equil_traj folder) and a trajetory (the .atom folder in the same folder). See example below.

```bash
cd 190_M # navigate to directory as before
python3 box_sizer.py ../equil_traj/density.data ../equil_traj/density.atom 
```

### Running the production simulation 

The process to submit the production simulations is the same as when submitting the equiliberation simulatations but remeber to paste the output from the box_sizer.py for the simulations corrasponding equiliberation trajectory. 

This command can be used to submit all the production simulations.

```bash
for temp in 190_M 240_M 290_B 290_M 310_M; do 
    ( cd "$temp" || exit
      sbatch prod.slurm
    )
done
```

### Running the read_frames.py

Runnig `read_frames.py` saves the first n from a trajectory file (`.atom` files) and to a new trajectory file. This is done as the trajectory files produced by the production simulations are very long this step can be skipped if the simulation dumps are shortend. But is is useful to have a long simulatin that can be sampled form as if the analysis is optimiesed to be faster more of the simulation can be sampled with out re sumbmitting and waiting in the queue. This function could also be edited to sample not just from the start of the sim but within the simulation so the start of the frame isnt just resampled.

To run read_frames.py it requires and input .atom file path and an file path to output to and then the number of frames you wish to sample.

This command can runs  read_frames across all the current directories.

```bash
for loc in 190_M 240_M 290_B 310_M; do 
 (
 cd "$loc" || exit
 pyhton3 read_frames.py ../prod_traj/production_1ns.atom ../prod_traj/production_6000frames_50fsframe.atom 6000
 )
 done
```

### Running python analysis

The python anaalysis constist of calculating ARDFs, RDFs, RACFs and translational diffusion ceffecients. To run all of this analysis across all the temperature directories the command below can be used.

```bash
for temp in 190_M 240_M 290_B 290_M 310_M; do 
    for analysis in ardf diffusion racf rdf; do
        ( cd "$temp/$analysis" || exit
          sbatch analysis.slurm
        )
    done
done
```

To run a single analysis first navigated to the to a tempertaure directory (`190_M, 240_M, 290_B, 290_M, 310_M,`) then in to an analysis directory (`ardf, rdf, diffusion, racf`) then submit it analysis.slurm using the sbatch command. See an example below.

```bash
cd 190_M/ardf
sbatch anaysis.slurm
```

### Running all the plotting for the analysis

Once the analysis has finished running plotting can be run to get some visualisations of the data that has been calculated.

Plotting can be run for all analysis in all temperature directorys using this command.

```bash
for temp in 190_M 240_M 290_B 290_M 310_M; do 
    for analysis in ardf diffusion racf rdf; do
        ( cd "$temp/$analysis" || exit
          python plotting.slurm
        )
    done
done
```

To run for a single type of analysis navigate to analysis folder and run `plotting.py`. See example below.

```bash
cd 190_M/ardf
python3 plotting.py
```

## Project structure
```
.
├── 190_M
│   ├── ardf
│   │   ├── adf_funcs.py
│   │   ├── adf.py
│   │   ├── analysis.slurm
│   │   ├── ardf_test.py
│   │   ├── plotting.py
│   │   ├── test.slurm
│   │   └── utility.py
│   ├── diffusion
│   │   ├── analysis.slurm
│   │   ├── diffusion_funcs.py
│   │   ├── diffusion.py
│   │   ├── plotting.py
│   │   └── utility.py
│   ├── equil.lammps
│   ├── equil.slurm
│   ├── mol_files
│   │   ├── benzene.mol
│   │   └── methanol.mol
│   ├── prod.lammps
│   ├── prod.slurm
│   ├── racf
│   │   ├── analysis.slurm
│   │   ├── nest_sampling_funcs.py
│   │   ├── plotting.py
│   │   ├── racf_funcs.py
│   │   ├── racf_models_ns.py
│   │   ├── racf.py
│   │   └── utility.py
│   ├── rdf
│   │   ├── analysis.slurm
│   │   ├── plottin.py
│   │   ├── rdf_funcs.py
│   │   ├── rdf.py
│   │   └── utility.py
│   └── utility
│       ├── box_sizer.py
│       └── read_frames.py
├── 240_M
│   ├── ardf
│   │   ├── adf_funcs.py
│   │   ├── adf.py
│   │   ├── analysis.slurm
│   │   ├── ardf_test.py
│   │   ├── plotting.py
│   │   ├── test.slurm
│   │   └── utility.py
│   ├── diffusion
│   │   ├── analysis.slurm
│   │   ├── diffusion_funcs.py
│   │   ├── diffusion.py
│   │   ├── plotting.py
│   │   └── utility.py
│   ├── equil.lammps
│   ├── equil.slurm
│   ├── mol_files
│   │   ├── benzene.mol
│   │   └── methanol.mol
│   ├── prod.lammps
│   ├── prod.slurm
│   ├── racf
│   │   ├── analysis.slurm
│   │   ├── nest_sampling_funcs.py
│   │   ├── plotting.py
│   │   ├── racf_funcs.py
│   │   ├── racf_models_ns.py
│   │   ├── racf.py
│   │   └── utility.py
│   ├── rdf
│   │   ├── analysis.slurm
│   │   ├── plottin.py
│   │   ├── rdf_funcs.py
│   │   ├── rdf.py
│   │   └── utility.py
│   └── utility
│       ├── box_sizer.py
│       └── read_frames.py
├── 290_B
│   ├── ardf
│   │   ├── adf_funcs.py
│   │   ├── adf.py
│   │   ├── analysis.slurm
│   │   └── utility.py
│   ├── diffusion
│   │   ├── analysis.slurm
│   │   ├── diffusion_funcs.py
│   │   ├── diffusion.py
│   │   ├── plotting.py
│   │   └── utility.py
│   ├── equil.lammps
│   ├── equil.slurm
│   ├── mol_files
│   │   ├── benzene.mol
│   │   └── methanol.mol
│   ├── prod.lammps
│   ├── prod.slurm
│   ├── racf
│   │   ├── analysis.slurm
│   │   ├── nest_sampling_funcs.py
│   │   ├── plotting.py
│   │   ├── racf_funcs.py
│   │   ├── racf_models_ns.py
│   │   ├── racf.py
│   │   └── utility.py
│   ├── rdf
│   │   ├── analysis.slurm
│   │   ├── rdf_funcs.py
│   │   ├── rdf.py
│   │   └── utility.py
│   └── utility
│       ├── box_sizer.py
│       └── read_frames.py
├── 290_M
│   ├── ardf
│   │   ├── adf_funcs.py
│   │   ├── adf.py
│   │   ├── analysis.slurm
│   │   ├── ardf_test.py
│   │   ├── plotting.py
│   │   ├── test.slurm
│   │   └── utility.py
│   ├── diffusion
│   │   ├── analysis.slurm
│   │   ├── diffusion_funcs.py
│   │   ├── diffusion.py
│   │   ├── plotting.py
│   │   └── utility.py
│   ├── equil.lammps
│   ├── equil.slurm
│   ├── mol_files
│   │   ├── benzene.mol
│   │   └── methanol.mol
│   ├── prod.lammps
│   ├── prod.slurm
│   ├── racf
│   │   ├── analysis.slurm
│   │   ├── nest_sampling_funcs.py
│   │   ├── plotting.py
│   │   ├── racf_funcs.py
│   │   ├── racf_models_ns.py
│   │   ├── racf.py
│   │   └── utility.py
│   ├── rdf
│   │   ├── analysis.slurm
│   │   ├── plottin.py
│   │   ├── rdf_funcs.py
│   │   ├── rdf.py
│   │   └── utility.py
│   └── utility
│       ├── box_sizer.py
│       └── read_frames.py
├── 310_M
│   ├── ardf
│   │   ├── adf_funcs.py
│   │   ├── adf.py
│   │   ├── analysis.slurm
│   │   ├── ardf_test.py
│   │   ├── plotting.py
│   │   ├── test.slurm
│   │   └── utility.py
│   ├── diffusion
│   │   ├── analysis.slurm
│   │   ├── diffusion_funcs.py
│   │   ├── diffusion.py
│   │   ├── plotting.py
│   │   └── utility.py
│   ├── equilibrate_310_M.slurm
│   ├── equil.lammps
│   ├── mol_files
│   │   ├── benzene.mol
│   │   └── methanol.mol
│   ├── prod.lammps
│   ├── prod.slurm
│   ├── racf
│   │   ├── analysis.slurm
│   │   ├── nest_sampling_funcs.py
│   │   ├── plotting.py
│   │   ├── racf_funcs.py
│   │   ├── racf_models_ns.py
│   │   ├── racf.py
│   │   └── utility.py
│   ├── rdf
│   │   ├── analysis.slurm
│   │   ├── plottin.py
│   │   ├── rdf_funcs.py
│   │   ├── rdf.py
│   │   └── utility.py
│   └── utility
│       ├── box_sizer.py
│       └── read_frames.py
└── analysis
    ├── diffusion.ipynb
    ├── rdf.ipynb
    └── test_analysis
        ├── arrhenius_testing.ipynb
        └── rotational-auto_corr.ipynb
```
For `190_M, 240_M, 290_B, 290_M and 310_M` the number and represents the temperature of the molecular dynsmaics simulation is held at. The letter M stands for the mixture of benzene and methanol the letter B stands for a pure Benzene simulation. The Directories are all structured in the same way apart from analysis which is for analysis that compares simulation or trends in various simulations. The analysis of the M directories are all the same B varies as RDFs, ARDFs and diffussion use methanol in there calculations and therefoe cannot be used in the B directories. Moving fowards if the number of B and M directories increase they could be seperatied into two directories.

The directories ardf, diffusion, racf and rdf contain python scripts for the analysis and plotting. Each of the directories has an `analysis.slurm` file which can be used to submit the python scripts to run on a HPC.

The directories equuil_traj and prod_traj are where their respective lammps files output their trajectories and topography files to. The lammps files equil.lammps and prod.lammps are the instruction that the lammps exacutable lmp reads and exacutes.The slurm files submit there repective lammps file to the hpcs aswell as tell it to use where the lmp exacutable is. The utility directory holds the read_frames.py and the box_sizer.py files. The mol_files directory contain .mol files which used by lammps to build the benzene and methanol molecules.

## Reporducing results

To reproduce results run following comands in order. Only run the next command until all jobs are finished.

```bash
for temp in 190_M 240_M 290_B 290_M 310_M; do 
    ( cd "$temp" || exit
      sbatch equil.slurm
    )
done

for loc in 190_M 240_M 290_B 310_M; do 
 (
 cd "$loc" || exit
 pyhton3 box_sizer.py ../equil_traj/density.data ../equil_traj/density.atom
 )
 done

for temp in 190_M 240_M 290_B 290_M 310_M; do 
    ( cd "$temp" || exit
      sbatch prod.slurm
    )
done

for loc in 190_M 240_M 290_B 310_M; do 
 (
 cd "$loc" || exit
 pyhton3 read_frames.py ../prod_traj/production_1ns.atom ../prod_traj/production_6000frames_50fsframe.atom 6000
 )
 done

for temp in 190_M 240_M 290_B 290_M 310_M; do 
    for analysis in ardf diffusion racf rdf; do
        ( cd "$temp/$analysis" || exit
          sbatch analysis.slurm
        )
    done
done

for temp in 190_M 240_M 290_B 290_M 310_M; do 
    for analysis in ardf diffusion racf rdf; do
        ( cd "$temp/$analysis" || exit
          sbatch plotting.slurm
        )
    done
done
```

## Contributing 

Currently only the ARDFs are parallelised so RDFs, RACFs and the calculation of diffusion coeffeceints would benifit from being confguired to use muti core proccessing. I recommend using multiproccessing module as it currently in use in the ARDF code.

Add additional pure bezene simulations at different temperature if the temperature range is expanded consider splitting the bezene and and mix simulations into seperate directories.

## Future work

A good extension of this work would be to begin to look at the meachansim of reorintaion with in the metahnol and benzene mixture as the data suggest benzene spins and tumbles faster within methanol than in pure benzene. Probing the collective reorintation could give insight into why we see an increase in rate or spinning when methanol is added to benzene. A paper on [The collective burst mechanism of angular jumps in liquid water](https://doi.org/10.1038/s41467-023-37069-9) maybe of use for this future work.