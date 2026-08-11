#!/bin/bash

#SBATCH --job-name=md
#SBATCH --time=1-00:00:00
#SBATCH --cpus-per-task=1

cd $SLURM_SUBMIT_DIR
source ~/miniforge3/bin/activate ""
conda activate md

echo "Running script: racf.py"
/home/b35bh/joe3010.b35bh/miniforge3/envs/md/bin/python racf.py 
