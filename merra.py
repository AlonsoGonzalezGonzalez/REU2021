from netCDF4 import Dataset as nc
import matplotlib.pyplot as plt
import numpy as np

"""
Data from 2009/01/09
downloaded from https://goldsmr5.gesdisc.eosdis.nasa.gov/data/MERRA2/M2I3NPASM.5.12.4/2009/01/
"""

file   = '/Users/schmidt/service/grad-students/reu21/alonso/MERRA2_300.inst3_3d_asm_Np.20090119.nc4'
handle = nc(file)
level  = handle.variables['lev'][:]  # This is the pressure level
height = -np.log(level*0.001)*8.       # Just approximate: The height in km
time   = handle.variables['time'][...] # Time in minutes since midnight
U      = handle.variables['U'][...]    # U wind (zonal: eastward)
V      = handle.variables['V'][...]    # V wind (meridional: northward)
lon    = handle.variables['lon'][...]  # longitude
lat    = handle.variables['lat'][...]  # latitude
ps     = handle.variables['PS'][...]   # surface pressure
handle.close()

time   = time/60. # convert time into hours

# first figure: wind speed profile in Boulder at UTC=18 (11am local)
# ...and at north pole
plt.figure(0)
time_0   = 18
lon_0    = -105.7
lat_0    = +40
time_ind = np.argmin(np.abs(time-time_0))
lon_ind  = np.argmin(np.abs(lon-lon_0))
lat_ind  = np.argmin(np.abs(lat-lat_0)) 
plt.plot(height,np.sqrt(np.power(U[time_ind,:,lat_ind,lon_ind],2)+np.power(V[time_ind,:,lat_ind,lon_ind],2)),'go-',label='speed Boulder')
plt.plot(height,U[time_ind,:,lat_ind,lon_ind],'b:',label='U')
plt.plot(height,V[time_ind,:,lat_ind,lon_ind],'r:',label='V')
lat_0    = +90
time_ind = np.argmin(np.abs(time-time_0))
lon_ind  = np.argmin(np.abs(lon-lon_0))
lat_ind  = np.argmin(np.abs(lat-lat_0)) 
plt.plot(height,np.sqrt(np.power(U[time_ind,:,lat_ind,lon_ind],2)+np.power(V[time_ind,:,lat_ind,lon_ind],2)),'ko-',label='speed NP')
plt.legend()
plt.xlabel('Approximate altitude [km]')
plt.ylabel('Wind Speed [m/s]')

# second figure map of surface pressure (you can also make maps of sub-regions, e.g., in the Arctic)
plt.figure(1)
plt.contourf(ps[0,:,:],30,cmap='jet')
plt.xlabel('LONGITUDE INDEX')
plt.ylabel('LATITUDE INDEX')
plt.title('surface pressure')

# third figure: wind speeds from south pole to north pole along 0 deg longitude
plt.figure(2)
#lon_0 = 0
#lon_ind  = np.argmin(np.abs(lon-lon_0))
plt.contourf(U[time_ind,:,:,lon_ind],cmap='jet')
plt.xlabel('LATITUDE INDEX')
plt.ylabel('ALTITUDE INDEX')


