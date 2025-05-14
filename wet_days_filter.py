import xarray as xr
import numpy as np
import netCDF4

def filter_wet_days(file1, file2, output_path,var_1, var_2, threshold=0.1):
    """
    Filters var2 time series based on where var1 exceeds or equals the threshold.
    
    Args:
        file1: Path to the input file with var1.
        file2: Path to the input file with var2.
        output_path: Path to save the output filtered var2, only time series for each pixel when correspinding var1 threshold is reached or exceeded.
        threshold : Threshold to filter var1 .
    """
    var1 = xr.open_dataset(file1)[var_1]
    var2 = xr.open_dataset(file2)[var_2]

    if var1.shape != var2.shape:
        raise ValueError("var1 and var2 must have the same shape")

    # Masking based on threshold
    mask = var1 >= threshold 

    filtered_var2 = np.where(mask, var2, np.nan) #Else set to NaN

    filtered_var2.to_netcdf(output_path, filtered_var2)