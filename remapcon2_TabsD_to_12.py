import subprocess

input= "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/TabsD_with_polygon_bounds.nc"
output = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/TabsD_12_km_regridded_02.nc"
grid = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/cordex_grid_CH.txt"

# Command for regridding : First order conservative remapping using YAC weights 
command = [
    "cdo",
    f"remapcon2,{grid}",
    input,
    output
]

try:
    subprocess.run(command, check=True)
    print(f"Regridding completed successfully: {output}")
except subprocess.CalledProcessError as e:
    print(f"Error during CDO execution: {e}")
