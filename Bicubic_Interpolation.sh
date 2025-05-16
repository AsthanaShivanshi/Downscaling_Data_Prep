#!/bin/bash
#SBATCH --job-name=bicubic
#SBATCH --output=coarsen_%j.out
#SBATCH --error=coarsen_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=3-00:00:00

cd /work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep
module load cdo

# Extract grid definitions to temporary files
cdo griddes wet_days_filtered_files/Targets/RhiresD_wet_1971_2023.nc > grid_rhiresd.txt
cdo griddes wet_days_filtered_files/Targets/TabsD_wet_1971_2023.nc   > grid_tabsd.txt
cdo griddes wet_days_filtered_files/Targets/TmaxD_wet_1971_2023.nc   > grid_tmaxd.txt
cdo griddes wet_days_filtered_files/Targets/TminD_wet_1971_2023.nc   > grid_tmind.txt

# Perform bicubic interpolation using the saved grid files
cdo remapbic,grid_rhiresd.txt wet_days_filtered_files/Features/rhiresd_wet_coarsened.nc Bicubic_Baselines/bicubic_rhiresd.nc
cdo remapbic,grid_tabsd.txt   wet_days_filtered_files/Features/tabsd_wet_coarsened.nc   Bicubic_Baselines/bicubic_tabsd.nc
cdo remapbic,grid_tmaxd.txt   wet_days_filtered_files/Features/tmaxd_wet_coarsened.nc   Bicubic_Baselines/bicubic_tmax.nc
cdo remapbic,grid_tmind.txt   wet_days_filtered_files/Features/tmind_wet_coarsened.nc   Bicubic_Baselines/bicubic_tmind.nc

# Optional: Clean up temporary grid files
rm grid_*.txt
