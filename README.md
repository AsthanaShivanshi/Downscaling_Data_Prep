Data processing scripts and outputs for AsthanaShivanshi/Downscaling repository.

######Repository under construction ################

workflow documentation : 

conservative regridder : conservatively regridding the 1km files to 12 km files. As 1 km files have no edge information (lat_bounds and lon_bounds) T. The edges are created by taking the average of the four surrounding cell centers. and then edge information is stored in source grid file. Then remapcon is performed. 

ßß