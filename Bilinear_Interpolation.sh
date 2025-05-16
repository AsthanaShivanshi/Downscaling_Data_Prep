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

# Perform bicubic interpolation using the saved grid files
cdo remapbil,wet_days_filtered_files/Targets/RhiresD_wet_1971_2023.nc wet_days_filtered_files/Features/rhiresd_wet_coarsened.nc Bilinear_Baselines/bilinear_rhiresd.nc
cdo remapbil,wet_days_filtered_files/Targets/TabsD_wet_1971_2023.nc  wet_days_filtered_files/Features/tabsd_wet_coarsened.nc   Bilinear_Baselines/bilinear_tabsd.nc
cdo remapbil,wet_days_filtered_files/Targets/TmaxD_wet_1971_2023.nc   wet_days_filtered_files/Features/tmaxd_wet_coarsened.nc   Bilinear_Baselines/bilinear_tmax.nc
cdo remapbil,wet_days_filtered_files/Targets/TminD_wet_1971_2023.nc   wet_days_filtered_files/Features/tmind_wet_coarsened.nc   Bilinear_Baselines/bilinear_tmind.nc


