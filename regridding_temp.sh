#!/bin/bash
#SBATCH --job-name=conservative_regridding_temperature   
#SBATCH --output=job_output-%j.txt 
#SBATCH --error=job_error-%j.txt  
#SBATCH --ntasks=1              
#SBATCH --cpus-per-task=4  
#SBATCH --time=3-00:00:00        
#SBATCH --mem=64G                
#SBATCH --partition=cpu         

module load python
module load cdo

source /work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/MyPythonEnvironment/bin/activate
cd /work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep

python /work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/remapcon_TabsD_to_12.py