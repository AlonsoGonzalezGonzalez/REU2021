#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 16:48:52 2021

@author: schmidt
"""
from netCDF4 import Dataset as nc
import matplotlib.pyplot as plt
import numpy as np


file   = 'WACCMX+DART_UVTGPH_2009011900-2009030523.nc'
handle = nc(file)
#level  = handle.variables['lev'][:]  # This is the pressure level
#height = -np.log(level*0.001)*8.       # Just approximate: The height in km
#time   = handle.variables['time'][...] # Time in minutes since midnight
U      = handle.variables['U'][...]    # U wind (zonal: eastward)
V      = handle.variables['V'][...]    # V wind (meridional: northward)
lon    = handle.variables['LONGITUDE'][...]  # longitude
lat    = handle.variables['LATITUDE'][...]  # latitude
p      = handle.variables['PRESSURE'][...]   # pressure
height = -np.log(p*0.001)*8.35      # Just approximate - ask Lynn about details
gph    = handle.variables['GPH'][...]
time   = handle.variables['YYYYMMDDHH'][...]   # time
handle.close()

# Check correspondence between level number and altitude
if False:
    plt.figure(0)
    plt.plot(gph[0,:,0,0],'ko')
    plt.plot(height*1000.,'go')
    plt.xlabel('Altitude index')
    plt.ylabel('Height [m]')
# ---> Altitude index 34 is approximately 100 km altitude
altitude_index=34
#altitude_index=37 # reproduces the obs winds better

# Get correct time index
# 20090203/20090301: Good/bad correspondence Obs/Model in Kodiak
#time_index=np.argmin(np.abs(2009020300-time))
time_index=np.argmin(np.abs(2009022723-time))

# Get global wind speed field for that time at level 31 (approximately 100 km)
#wind_speed = np.sqrt(np.power(U[time_index,altitude_index,:,:],2)+np.power(V[time_index,altitude_index,:,:],2))
wind_speed = U[time_index,altitude_index,:,:]
# second figure map of wind speed
plt.figure(1)
plt.contourf(wind_speed,30,cmap='jet',vmin=-50,vmax=50)
lon_index=np.argmin(np.abs(152.4-lon)) # Kodiak's lat/lon
lat_index=np.argmin(np.abs(75.79-lat))
plt.scatter(lon_index,lat_index,color='green',label='Kodiak')
plt.xlabel('LONGITUDE INDEX')
plt.ylabel('LATITUDE INDEX')
plt.title('zonal wind speed @ '+str(time[time_index]))
#plt.title('zonal wind speed @ '+str(gph[time_index,altitude_index,lat_index,lon_index])+' km')
plt.legend()
plt.tight_layout()

# Another kind of plot: print altitude/latitude wind field for Kodiak's longitude
lon_index=np.argmin(np.abs(152.4-lon))
lat_index=np.argmin(np.abs(75.79-lat))
#wind_curtain = np.sqrt(np.power(U[time_index,21:75,:,lon_index],2)+np.power(V[time_index,21:75,:,lon_index],2))
wind_curtain = U[time_index,21:75,:,lon_index]
plt.figure(2)
plt.contourf(wind_curtain,30,cmap='jet',vmin=-50,vmax=50)
ws=wind_curtain[altitude_index-21,lat_index]
plt.scatter(lat_index,altitude_index-21,color='green',label='Kodiak @ '+str(height[altitude_index])+' km: '+str(ws)+' m/s')
plt.xticks(ticks=[0,47.5,95],labels=['-90','EQUATOR','+90'])
plt.yticks(ticks=[altitude_index-21,53],labels=[str(height[altitude_index])+' km','20 km'])
plt.xlabel('LATITUDE INDEX')
plt.ylabel('ALTITUDE INDEX')
plt.title('zonal wind speed (U) - eastward')
plt.legend()
plt.tight_layout()

# plt.figure(3)
# Uwind=U[time_index,:,lat_index,lon_index]
# #wind=np.sqrt(np.power(U[time_index,:,lat_index,lon_index],2)+np.power(V[time_index,:,lat_index,lon_index],2))
# #plt.plot(gph[time_index,:,lat_index,lon_index]*0.001,wind)
# plt.plot(gph[time_index,:,lat_index,lon_index]*0.001,Uwind)
# #plt.plot(height,Uwind)

