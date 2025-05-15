import xarray as xr
import numpy as np

def coarsen_file_conservatively(
    infile,
    varname,
    block_size,
    outfile=None,
    latname='lat',
    lonname='lon'
):
    """
    Coarsens a 2D or 3D variable in a NetCDF file using area-weighted averaging.

    Parameters:
        infile: str
            Path to the input NetCDF file
        varname: str
            Name of the variable to coarsen
        block_size: int
            Coarsening factor (N x N block size)
        outfile: str (optional)
            If provided, output file to write coarsened data
        latname: str
            Name of latitude variable (default 'lat')
        lonname: str
            Name of longitude variable (default 'lon')

    Returns:
        xr.DataArray of coarsened variable
    """

    # Load dataset
    ds = xr.open_dataset(infile)
    var = ds[varname]
    lat = ds[latname].values
    lon = ds[lonname].values

    if lat.shape != var.shape[-2:] or lon.shape != var.shape[-2:]:
        raise ValueError("lat/lon shape must match variable spatial shape")

    # Trim to make divisible
    ny, nx = lat.shape
    nlat_block, nlon_block = block_size, block_size
    ny_trim = (ny // nlat_block) * nlat_block
    nx_trim = (nx // nlon_block) * nlon_block

    var = var[..., :ny_trim, :nx_trim]
    lat = lat[:ny_trim, :nx_trim]
    lon = lon[:ny_trim, :nx_trim]

    R = 6371000
    dlat = np.deg2rad(np.diff(lat[:, 0]).mean())
    dlon = np.deg2rad(np.diff(lon[0, :]).mean())
    area = (R ** 2) * dlat * dlon * np.cos(np.deg2rad(lat))

    # Add time dim if needed
    has_time = 'time' in var.dims
    if not has_time:
        var = var.expand_dims('time')

    data = var.values
    area_blocks = area.reshape(ny_trim // nlat_block, nlat_block,
                               nx_trim // nlon_block, nlon_block)

    # Reshape to blocks
    var_blocks = data.reshape(data.shape[0],
                              ny_trim // nlat_block, nlat_block,
                              nx_trim // nlon_block, nlon_block)

    # Weighted sum
    weighted = (var_blocks * area_blocks).sum(axis=(2, 4))
    total_area = area_blocks.sum(axis=(1, 3))
    coarsened_data = weighted / total_area

    # Coarsen coordinates
    lat_coarse = lat.reshape(ny_trim // nlat_block, nlat_block,
                             nx_trim // nlon_block, nlon_block).mean(axis=(1, 3))
    lon_coarse = lon.reshape(ny_trim // nlat_block, nlat_block,
                             nx_trim // nlon_block, nlon_block).mean(axis=(1, 3))

    coords = {
        'lat': (['y', 'x'], lat_coarse),
        'lon': (['y', 'x'], lon_coarse)
    }

    if has_time:
        coords['time'] = var['time']
        dims = ('time', 'y', 'x')
    else:
        coarsened_data = coarsened_data.squeeze()
        dims = ('y', 'x')

    da_out = xr.DataArray(coarsened_data, coords=coords, dims=dims, name=varname)

    # Optional save to NetCDF
    if outfile:
        da_out.to_netcdf(outfile)

    return da_out
