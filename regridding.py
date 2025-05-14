#!/usr/bin/env python

import xarray as xr
import numpy as np

def cell_corners_computation(lat, lon):
    ny, nx = lat.shape
    lat_bounds = np.zeros((ny + 1, nx + 1))
    lon_bounds = np.zeros((ny + 1, nx + 1))

    # Interior corners
    lat_bounds[1:-1, 1:-1] = 0.25 * (
        lat[0:-1, 0:-1] + lat[0:-1, 1:] +
        lat[1:, 0:-1] + lat[1:, 1:]
    )
    lon_bounds[1:-1, 1:-1] = 0.25 * (
        lon[0:-1, 0:-1] + lon[0:-1, 1:] +
        lon[1:, 0:-1] + lon[1:, 1:]
    )

    # Edge extrapolation
    lat_bounds[0, :] = lat_bounds[1, :]
    lat_bounds[-1, :] = lat_bounds[-2, :]
    lat_bounds[:, 0] = lat_bounds[:, 1]
    lat_bounds[:, -1] = lat_bounds[:, -2]

    lon_bounds[0, :] = lon_bounds[1, :]
    lon_bounds[-1, :] = lon_bounds[-2, :]
    lon_bounds[:, 0] = lon_bounds[:, 1]
    lon_bounds[:, -1] = lon_bounds[:, -2]

    return lat_bounds, lon_bounds

def compute_per_cell_vertices(lat_b, lon_b):
    ny = lat_b.shape[0] - 1
    nx = lat_b.shape[1] - 1
    nv = 4  # number of vertices per cell

    lat_vertices = np.zeros((ny, nx, nv))
    lon_vertices = np.zeros((ny, nx, nv))

    # Assign corners: counter-clockwise (CDO convention)
    lat_vertices[:, :, 0] = lat_b[0:-1, 0:-1]  # top-left
    lat_vertices[:, :, 1] = lat_b[0:-1, 1:  ]  # top-right
    lat_vertices[:, :, 2] = lat_b[1:  , 1:  ]  # bottom-right
    lat_vertices[:, :, 3] = lat_b[1:  , 0:-1]  # bottom-left

    lon_vertices[:, :, 0] = lon_b[0:-1, 0:-1]
    lon_vertices[:, :, 1] = lon_b[0:-1, 1:  ]
    lon_vertices[:, :, 2] = lon_b[1:  , 1:  ]
    lon_vertices[:, :, 3] = lon_b[1:  , 0:-1]

    return lat_vertices, lon_vertices

def main():
    print("Loading RhiresD dataset...")
    ds = xr.open_dataset("RhiresD_1971_2022.nc", chunks={"time": 100})
    lat = ds["lat"].values
    lon = ds["lon"].values

    print("Computing corner bounds...")
    lat_b, lon_b = cell_corners_computation(lat, lon)

    print("Computing per-cell polygon bounds (vertices)...")
    lat_vertices, lon_vertices = compute_per_cell_vertices(lat_b, lon_b)

    print("Embedding polygon bounds into dataset...")
    ds["lat_vertices"] = (["N", "E", "nv"], lat_vertices)
    ds["lon_vertices"] = (["N", "E", "nv"], lon_vertices)

    ds["lat"].attrs["bounds"] = "lat_vertices"
    ds["lon"].attrs["bounds"] = "lon_vertices"
    ds["lat_vertices"].attrs["standard_name"] = "latitude_bounds"
    ds["lon_vertices"].attrs["standard_name"] = "longitude_bounds"

    print("Saving new RhiresD file with polygon bounds...")
    output_path = "RhiresD_with_polygon_bounds.nc"
    ds.to_netcdf(output_path)

    print("Done! Saved to:", output_path)

if __name__ == "__main__":
    main()



    #Regridding later performed 
# cdo remapcon,cordex_grid_CH.txt RhiresD_with_polygon_bounds.nc RhiresD_12_km_regridded.nc
# cdo remapcon,cordex_grid_CH.txt TabsD_with_polygon_bounds.nc TabsD_12_km_regridded.nc
