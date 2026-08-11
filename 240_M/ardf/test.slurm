#!/bin/bash

#SBATCH --job-name=md
#SBATCH --time=1-00:00:00
#Sbatch --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=144
#SBATCH --cpus-per-task=1
#SBATCH --exclusive



cd $SLURM_SUBMIT_DIR
source ~/miniforge3/bin/activate ""
conda activate md

echo "Running script: ardf_test.py"
/home/b35bh/joe3010.b35bh/miniforge3/envs/md/bin/python ardf_test.py 
