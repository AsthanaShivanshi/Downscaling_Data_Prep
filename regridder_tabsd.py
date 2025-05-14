#!/usr/bin/env python

import xarray as xr
import numpy as np
import subprocess
import netCDF4
import os

def cell_corners_computation(lat, lon):
    ny, nx = lat.shape
    lat_bounds = np.zeros((ny + 1, nx + 1))
    lon_bounds = np.zeros((ny + 1, nx + 1))

    lat_bounds[1:-1, 1:-1] = 0.25 * (
        lat[0:-1, 0:-1] + lat[0:-1, 1:] +
        lat[1:, 0:-1] + lat[1:, 1:]
    )
    lon_bounds[1:-1, 1:-1] = 0.25 * (
        lon[0:-1, 0:-1] + lon[0:-1, 1:] +
        lon[1:, 0:-1] + lon[1:, 1:]
    )

    lat_bounds[0, :] = lat_bounds[1, :]
    lat_bounds[-1, :] = lat_bounds[-2, :]
    lat_bounds[:, 0] = lat_bounds[:, 1]
    lat_bounds[:, -1] = lat_bounds[:, -2]

    lon_bounds[0, :] = lon_bounds[1, :]
    lon_bounds[-1, :] = lon_bounds[-2, :]
    lon_bounds[:, 0] = lon_bounds[:, 1]
    lon_bounds[:, -1] = lon_bounds[:, -2]

    return lat_bounds, lon_bounds

def main():
    print("Loading dataset")
    ds = xr.open_dataset("TabsD_1971_2022.nc", chunks={"time": 100})
    lat = ds["lat"].values
    lon = ds["lon"].values

    print("Computing corners")
    lat_b, lon_b = cell_corners_computation(lat, lon)

    print("Creating grid dataset in memory")
    grid_ds = xr.Dataset({
        "lat": (["y", "x"], lat),
        "lon": (["y", "x"], lon),
        "lat_b": (["y_b", "x_b"], lat_b),
        "lon_b": (["y_b", "x_b"], lon_b),
    })

    print("Preparing TabsD dataset")
    ds_new = xr.Dataset(
        {"tabsd": ds["TabsD"].transpose("N", "E", "time")},
        coords={
            "lat": ds["lat"],
            "lon": ds["lon"],
            "time": ds["time"]
        }
    ).chunk({"time": 100})

    # Save temporary files needed by CDO
    print("Writing temporary input files for CDO...")
    grid_path = "tmp_grid_tabsd_01.nc"
    input_path = "tmp_tabsd_01.nc"
    tmp_output = "tmp_tabsd_01.nc"

    grid_ds.to_netcdf(grid_path)
    ds_new.to_netcdf(input_path)

    print("Running CDO setgrid...")
    subprocess.run(["cdo", f"setgrid,{grid_path}", input_path, tmp_output], check=True)

    print("Running CDO remapcon...")
    target_grid = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/cordex_grid_CH.txt"
    final_output = "/work/FAC/FGSE/IDYST/tbeucler/downscaling/sasthana/Downscaling/Downscaling_Data_Prep/tabsd_conservatively_regridded_12km_versionbash.nc"

    subprocess.run(["cdo", f"remapcon,{target_grid}", tmp_output, final_output], check=True)

    print("Cleaning up temporary files...")
    os.remove(grid_path)
    os.remove(input_path)
    os.remove(tmp_output)

    print("File saved to:", final_output)

if __name__ == "__main__":
    main()
