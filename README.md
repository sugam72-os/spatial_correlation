# spatial_correlation
A function to calculate the spatial correlation of tree-ring width or isotope data with reanalysis of climate data\n
Please install the required modules such as numpy, pandas, scipy, netCDF4
the function chelsa_correlation(defined below) calculates the spatial correlation and automatically saves an output NetCDF file with correlation and their corresponding significance value. The function requires 
netCDF_file = location of the stacked netcdf file including its name, for example, "J:/climate/CHELSA/stacked_tmax_data8.nc"
chron = the chronology file with year in the first column and RWIs in the second column,
month_range = range of the months to define season such that [3,5] represents averaging the temperature from March (3rd month) to May (5th month) or [6,9] representing from June (6th month) to September (9th month)
variable = the standard name of the variable: pr, tasmin and tasmax for precipitation, minimum temperature and maximum temperature, respectively
