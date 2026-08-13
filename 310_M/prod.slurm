#!/usr/bin/env bash
#SBATCH --job-name=meth_lammps
#SBATCH --time=01-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=144
#SBATCH --cpus-per-task=1
#SBATCH --exclusive



export OMP_NUM_THREADS=1
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

module load PrgEnv-cray

LMP= <insert/path/to/lammps/exactuable>
srun "$LMP" -in prod.lammps -log ${SLURM_JOB_ID}.log