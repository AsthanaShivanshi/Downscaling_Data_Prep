#!/bin/bash
#SBATCH --job-name=coarsening
#SBATCH --output=coarsen_%j.out
#SBATCH --error=coarsen_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=3-00:00:00

# Load micromamba module from your HPC
module load micromamba

# Initialize the micromamba shell hook
eval "$(micromamba shell hook --shell=bash)"

# Activate your env by full path
micromamba activate /work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/MyPythonEnvNew

# Run your script
python /work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/regridding_II.py

