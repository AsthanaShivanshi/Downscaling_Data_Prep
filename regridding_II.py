import xarray as xr
import numpy as np

def conservative_coarsening(
    infile,
    varname,
    block_size, #For NxN downsampling 
    outfile=None,
    latname='lat',
    lonname='lon'):
    """
    Coarsens a 2D or 3D variable using grid-aware logic.

    - For projected grids (dimensions E/N), uses arithmetic mean (equal area).
    - For geographic grids (lat/lon), uses area-weighted averaging (cos(lat)).

    Parameters:
        infile: str
            Path to the NetCDF input file.
        varname: str
            Name of variable to coarsen.
        block_size: int
            Coarsening factor (NxN).
        outfile: str (optional)
            Output NetCDF file.
        latname, lonname: str
            Names of latitude and longitude variables.

    Returns:
        Coarsened xarray.DataArray.
    """

    ds = xr.open_dataset(infile)
    da = ds[varname]

    dims = da.dims
    has_time = 'time' in dims #Covering bases in case it has time., Our case, for each case, has time

    # E/N grid
    if 'E' in dims and 'N' in dims:
        print("projected grid (E/N) ,, using simple arithmetic mean over every NxN block")
        da_coarse = da.coarsen(N=block_size, E=block_size, boundary='pad').mean() #Alternatives : pad, trim or exact. 

        #.coarsen() from xarray used to downsample by grouping it into coarser blocks and applying an aggr function


    # curvilinear grid
    elif latname in ds and lonname in ds:
        print("Detected curvilinear,, using area-weighted averging")
        lat = ds[latname].values
        lon = ds[lonname].values
        var = da

        if lat.shape != var.shape[-2:] or lon.shape != var.shape[-2:]:
            raise ValueError("lat/lon shape must match last 2 dims")

        ny, nx = lat.shape
        ny_trim = (ny // block_size) * block_size
        nx_trim = (nx // block_size) * block_size

        var = var[..., :ny_trim, :nx_trim]
        lat = lat[:ny_trim, :nx_trim]
        lon = lon[:ny_trim, :nx_trim]

        # Area weights via cos(lat)
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

    if outfile:
        da_coarse.to_netcdf(outfile)

    return da_coarse
