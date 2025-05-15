import xarray as xr
import numpy as np

def conservative_coarsening(
    infile,
    varname,
    block_size,
    outfile=None,
    latname='lat',
    lonname='lon'):
    ds = xr.open_dataset(infile)
    da = ds[varname]

    dims = da.dims
    has_time = 'time' in dims

    if 'E' in dims and 'N' in dims:
        print(f"{varname}: Projected grid (E/N), using arithmetic mean over {block_size}x{block_size} blocks.")
        da_coarse = da.coarsen(N=block_size, E=block_size, boundary='pad').mean()

    elif latname in ds and lonname in ds:
        print(f"{varname}: Curvilinear grid detected, using area-weighted averaging.")
        lat = ds[latname].values
        lon = ds[lonname].values
        var = da

        if lat.shape != var.shape[-2:] or lon.shape != var.shape[-2:]:
            raise ValueError("lat/lon shape must match last two dimensions of variable")

        ny, nx = lat.shape
        ny_trim = (ny // block_size) * block_size
        nx_trim = (nx // block_size) * block_size

        var = var[..., :ny_trim, :nx_trim]
        lat = lat[:ny_trim, :nx_trim]
        lon = lon[:ny_trim, :nx_trim]

        R = 6371000
        dlat = np.deg2rad(np.diff(lat[:, 0]).mean())
        dlon = np.deg2rad(np.diff(lon[0, :]).mean())
        area = (R**2) * dlat * dlon * np.cos(np.deg2rad(lat))

        if not has_time:
            var = var.expand_dims('time')

        data = var.values
        area_blocks = area.reshape(ny_trim // block_size, block_size,
                                   nx_trim // block_size, block_size)
        var_blocks = data.reshape(
            data.shape[0],
            ny_trim // block_size, block_size,
            nx_trim // block_size, block_size
        )

        weighted = (var_blocks * area_blocks).sum(axis=(2, 4))
        total_area = area_blocks.sum(axis=(1, 3))
        data_coarse = weighted / total_area

        lat_coarse = lat.reshape(ny_trim // block_size, block_size,
                                 nx_trim // block_size, block_size).mean(axis=(1, 3))
        lon_coarse = lon.reshape(ny_trim // block_size, block_size,
                                 nx_trim // block_size, block_size).mean(axis=(1, 3))

        coords = {
            'lat': (['y', 'x'], lat_coarse),
            'lon': (['y', 'x'], lon_coarse)
        }
        if has_time:
            coords['time'] = var['time']
            dims = ('time', 'y', 'x')
        else:
            data_coarse = data_coarse.squeeze()
            dims = ('y', 'x')

        da_coarse = xr.DataArray(data_coarse, coords=coords, dims=dims, name=varname)
    else:
        raise ValueError("Could not detect grid type")

    if outfile:
        da_coarse.to_netcdf(outfile)

    return da_coarse

# Perform the coarsening on all four datasets
datasets = [
    ("RhiresD_1971_2023.nc", "RhiresD", "RhiresD_011deg_coarsened.nc"),
    ("TabsD_1971_2023.nc", "TabsD", "TabsD_011deg_coarsened.nc"),
    ("TminD_1971_2023.nc", "TminD", "TminD_011deg_coarsened.nc"),
    ("TmaxD_1971_2023.nc", "TmaxD", "TmaxD_011deg_coarsened.nc")
]

for infile, varname, outfile in datasets:
    conservative_coarsening(infile, varname, block_size=11, outfile=outfile)
