import glob
import netCDF4
import xarray 
import numpy as np
import datetime as dt
import pandas as pd
from pandas import DataFrame
from math import *

import os
import csv
import numpy as np                  # For doing math
import matplotlib.pyplot as plt     # For plotting
import matplotlib.dates as mdates   # For formatting dates when plotting
import matplotlib.colors as colors  # For truncating colorbars
import matplotlib.style as style
import xarray as xr  
import matplotlib.path as mpath  # For dealing with netCDF data
import pandas as pd                 # A quick way to deal with time stamps
import cartopy.crs as ccrs

def circular_polar_plot(data, lat_min, colors, title_, no_col_bar=False, 
                        cbar_label=False, levels_=False, cbar_levels_=False, 
                        extend_kw=False, horizontal=False, add_text=False,
                        text_lat=-152, text_lon=57, text_string = 'K', text_size=24):
    
    '''
    This function requires an input of an xarray dataarray with lat/lon and a third varaible
    '''
    
    #define the overall figure charachteristics
    fig = plt.figure(figsize=[8,8]) #set the size of the figure
    ax = fig.add_subplot(projection = ccrs.NorthPolarStereo(central_longitude=0)) #define the axes in terms of the polar projection
    ax.set_extent((-180,180,int(lat_min),90), ccrs.PlateCarree()) #only include data above the minimum latitude
    if(add_text):
        ax.text(text_lat, text_lon, text_string, fontsize=text_size, transform=ccrs.PlateCarree() ) 
    
    #make the plot circular using matplotlib.path
    theta = np.linspace(0, 2*np.pi, 100) 
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T #matrix transpose
    circle = mpath.Path(verts * radius + center) #this is now a circle boundary defined in matplotlib
    ax.set_boundary(circle, transform=ax.transAxes) #cut the plot at the circle boundary
    
    
    if no_col_bar: #we don't include a colorbar if this argument is True
        data.plot(ax=ax,cmap=str(colors), add_colorbar=False, add_labels=False, transform=ccrs.PlateCarree())
    else:
        fig.subplots_adjust(right=0.87) #make space at the right side of the plot for the colorbar
        plotting = data.plot(ax=ax, cmap=str(colors), add_colorbar=False, transform=ccrs.PlateCarree(), levels=levels_, add_labels=False)
#         plt.annotate('k',(.29,.87),xycoords='axes fraction')



        ####################################### define the colorbar ############################################
        if horizontal: #=True means we want the colobar horizontal
            orient = 'horizontal'
            cbar_ax = fig.add_axes([0.1, 0.05, 0.8, 0.04]) #this is x,y position of the colorbar and length and height
        else:
            orient = 'vertical'
            cbar_ax = fig.add_axes([0.9, 0.15, 0.05, 0.7])
        
        #define whether the colorbar should be capped, default if no 'extend_kw' keyword is for both caps to be there so 'extend=both'
        if extend_kw:
             cb = fig.colorbar(plotting, cax=cbar_ax, ticks=cbar_levels_, spacing='uniform', extend=extend_kw, orientation=orient)
        else:
             cb = fig.colorbar(plotting, cax=cbar_ax, ticks=cbar_levels_, spacing='uniform', extend='both', orientation=orient)
        
        #set the label and label size of the colorbar
        if horizontal:
            cb.ax.set_xlabel(str(cbar_label), fontsize=20)
        else:
            cb.ax.set_ylabel(str(cbar_label), fontsize=20)
    
        cb.ax.tick_params(labelsize=20) #set the tick size on the colobar
        #####################################################################################################
    
    #add details to the figure after the data is plotted
    ax.coastlines() #add coastlines
    ax.gridlines() #add gridlines
    ax.set_title(str(title_), fontsize=20) #set the title and fontzise
    ax.set_facecolor('0.5') #make the background (usually land) gray

    
def circular_polar_wind_plot(U_data, V_data, lat_min, title_, plot_type='stream', s_density=1, b_linewidth=0.95, q_scale=100):
    
    '''
    This function requires an input of two xarray dataarrays with lat/lon and a third wind varaible
    '''
    xx, yy = np.meshgrid(U_data.lon, U_data.lat)
    
    #define the overall figure charachteristics
    fig = plt.figure(figsize=[8,8]) #set the size of the figure
    ax = fig.add_subplot(projection = ccrs.NorthPolarStereo(central_longitude=0)) #define the axes in terms of the polar projection
    ax.set_extent((-180,180,int(lat_min),90), ccrs.PlateCarree()) #only include data above the minimum latitude
    
    #make the plot circular using matplotlib.path
    theta = np.linspace(0, 2*np.pi, 100) 
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T #matrix transpose
    circle = mpath.Path(verts * radius + center) #this is now a circle boundary defined in matplotlib
    ax.set_boundary(circle, transform=ax.transAxes) #cut the plot at the circle boundary
    
    if(plot_type.lower()=='stream'):
        ax.streamplot(xx,yy,U_data.data,V_data.data, density=s_density, transform=ccrs.PlateCarree())
    elif(plot_type.lower() == 'barb'):
        ax.barbs(xx,yy,U_data.data,V_data.data, length=6,sizes=dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=b_linewidth, transform=ccrs.PlateCarree())
    elif(plot_type.lower()== 'quiver'):
        ax.quiver(xx,yy,U_data.data,V_data.data, scale=q_scale, transform=ccrs.PlateCarree())
    
    #add details to the figure after the data is plotted
    ax.coastlines() #add coastlines
    ax.gridlines() #add gridlines
    ax.set_title(str(title_), fontsize=20) #set the title and fontzise