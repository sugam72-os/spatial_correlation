import netCDF4
import numpy as np
import pandas as pd
from scipy.stats import linregress
def spatial_correlation(netCDF_file, chron, month_range=[3,5],variable='pr'):
    crn=chron
    if variable=='pr':
        crn2=crn.iloc[np.where((crn.iloc[:,0]>1979) & (crn.iloc[:,0]<2019))]
    else:
        crn2=crn.iloc[np.where((crn.iloc[:,0]>1979) & (crn.iloc[:,0]<2020))]
    nc=netCDF4.Dataset(netCDF_file)
    lat=nc.variables['lat'][:]
    lon=nc.variables['lon'][:]
    var=nc.variables[variable][:]
    corr_value=np.ndarray(shape=(var.shape[1],var.shape[2]))
    p_value=np.ndarray(shape=(var.shape[1],var.shape[2]))
    for i in range(495):
        for j in range(978):
            clim=var[:,i,j].reshape(40,12)
            if len(clim)!=len(crn2):
                break
            if variable=='pr':
                clim_range=np.sum(clim[:,month_range[0]-1:month_range[1]], axis=1)
            else:
                clim_range=np.mean(clim[:,month_range[0]-1:month_range[1]], axis=1)
            #########
            corr_=linregress(clim_range,crn2.iloc[:,1])
            corr_value[i,j]=corr_[2]
            p_value[i,j]=corr_[3]
            #######################
            
    output=netCDF4.Dataset('./corr_'+variable+'_'+str(month_range[0])+'-'+str(month_range[1])+'.nc', 'w')
    #creating dimensions
    lat_dim = output.createDimension('lat', len(lat))     # latitude axis
    lon_dim = output.createDimension('lon', len(lon))    # longitude axis
    #time_dim = output.createDimension('time', None) # unlimited axis (can be appended to).
    output.title='Correlation with CHELSA '+variable+'_'+str(month_range[0])+'-'+str(month_range[1])
    #output.subtitle='1980 to 2018 after converting to mm per month'
    #creating variables
    latitude=output.createVariable('lat', np.float32, ('lat',))
    longitude=output.createVariable('lon', np.float32, ('lon',))
    #time=output.createVariable('time', np.float32, ('time',))
    #time.units='YYYY.MM format'
    var=output.createVariable('corr_value', np.float64, ('lat','lon'))
    var2=output.createVariable('p_value', np.float64, ('lat','lon'))
    #var.units='mm per month'
    var.standard_name="Pearson's correlation value"
    var2.standard_name="Significance of Pearson's correlation value"
    #writing data to the variables
    #time[:]=t
    latitude[:]=lat
    longitude[:]=lon
    var[:,:]=corr_value
    var2[:,:]=p_value
    output.close()
