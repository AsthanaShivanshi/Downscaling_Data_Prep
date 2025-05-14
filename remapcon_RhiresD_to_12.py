import subprocess

input= "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/RhiresD_with_polygon_bounds.nc"
output = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/RhiresD_12_km_regridded.nc"
grid = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/cordex_grid_CH.txt"


command = [
    "cdo",
    f"remapcon,{grid}",
    input,
    output
]

try:
    subprocess.run(command, check=True)
    print(f"Regridding completed successfully: {output}")
except subprocess.CalledProcessError as e:
    print(f"Error during CDO execution: {e}")
