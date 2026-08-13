#!/bin/bash

#SBATCH --job-name=md
#SBATCH --time=1-00:00:00
#SBATCH --cpus-per-task=1

set -euo pipefail  # fail fast on errors, unset vars, pipe failures

cd $SLURM_SUBMIT_DIR
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate md

echo "Running script: racf.py"
python racf.py 
