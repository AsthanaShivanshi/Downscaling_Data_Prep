import subprocess, os

input  = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/RhiresD_with_polygon_bounds.nc"
output = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/RhiresD_12_km_regridded.nc"
grid   = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/cordex_grid_CH.txt"

#  CDO extrapolates (NN) while it remaps, hence edge cells never come out missing.

env = os.environ.copy()
env["REMAP_EXTRAPOLATE"] = "on"      # <- one-word "on" or "ON"

# Right-to-left:  remap   → fillmiss2   (iterative nearest-valid fill)
command = [
    "cdo",
    "-fillmiss2",                    # patch any NaNs that survive the remap
    f"-remapcon,{grid}",             # 1st-order conservative remap
    input,
    output
]

subprocess.run(command, check=True, env=env)
print(f"Finished: {output}")
