###############################################################################
# The data. This could be loaded from a file, or scraped from a website
#LINHAS COMENTADAS 97,98
#Alerta 1117
#23 - estimativa para raio da terra

import numpy as np
import os

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime
from netCDF4 import Dataset # https://unidata.github.io/netcdf4-python/netCDF4/index.html#netCDF4.Dataset
import xarray as xr
import csv


def carrega_dados(nc_file):
    fh = Dataset(nc_file, mode='r')
    #print (fh)
    ds = xr.open_dataset(xr.backends.NetCDF4DataStore(fh))
    print('1#########################################')
    print(ds)
    #df = ds.to_dataframe() #converteu para o formato panda dataframe
    #print(df)
    print('longitude#########################################')
    lista_longitude = ds.coords['longitude'].values
    print(lista_longitude)
    print('latitude#########################################')
    lista_latitude = ds.coords['latitude'].values
    print(lista_latitude)
    print('level#########################################')
    lista_level = ds.coords['level'].values
    print(lista_level)
    print('time#########################################')
    lista_time = ds.coords['time'].values
    print(lista_time)
    return ds, lista_longitude, lista_latitude, lista_level, lista_time




def listagem_de_tudo(ds, lista_longitude, lista_latitude, lista_level, lista_time):
    print('pv########## listagem de tudo ###############################')
    
    for long in lista_longitude:
        for lat in lista_latitude:
            for lev in lista_level:
                for tim in lista_time:
                    t= ds.t.sel(time=tim,level=lev,latitude=lat,longitude=long).values
                    #print("t=%s lev=%d lat=%f long=%f temp=%f"%(tim,lev,lat,long,t))
                   
                    
       

    
###############################################################################
# Load the data, and put it in data structures we can use
##routes_table = [i for i in csv.reader(routes_data.split('\n')[1:-1])]
# Build a dictionnary returning GPS coordinates for each city
#cities_coord = dict()
def cria_dic_locais(lista_longitude, lista_latitude, lista_level):
    #Criação de um dicionario !
    cidades = {} # isto é o mesmo que fazer cidades=dict() e cria um dicionário vazio
    num_cidade=1 #variavel para me ir contando as cidades
    for long in lista_longitude:
        for lat in lista_latitude:
            for lev in lista_level: #com estes 3 fors consigo ir buscar todos os conjuntos de long,lat,lev
                nome_cidade = "cidade_%d"%(num_cidade) #tambem poderia ter colocado "cidade_" + num_cidade mas como fiz é mais elegante 
                cidades[nome_cidade] = (long, lat, lev)
                num_cidade+=1
    print(len(cidades))
    return cidades
    
def cria_lista_coords(cidades):
    coords = []
    for coordenadas in cidades.values():
        coords.append(coordenadas)   
    return coords
    

###############################################################################
def display_mapa2(ds, lista_longitude, lista_latitude, lista_level, lista_time):
    from mayavi import mlab
    mlab.figure(1, bgcolor=(0.48, 0.48, 0.48), fgcolor=(0, 0, 0), size=(400, 400))
    mlab.clf()
    # Display points at city positions
    #coords = np.array(coords)
    
    print('pv########## listagem de tudo ###############################')
    Rt=6400
    conta_tempos=0
    for tim in lista_time:
        conta_tempos+=1
        for long in lista_longitude:
            lat_t=np.array([long * np.pi / 180])
            for lat in lista_latitude:
                long_t=np.array([lat * np.pi / 180])
                for lev in lista_level: 
                    
                    lev_t = np.array([lev]) #* np.pi / 180
                    #lat, long, lev = coords.T * np.pi / 180
                    #lev_t = lev_t*180/np.pi
                    #print("t=%s lev=%d lat=%f long=%f"%(tim,lev,lat,long)) 
                    x = (1+lev_t/Rt)*np.cos(long_t) * np.cos(lat_t)
                    y = (1+lev_t/Rt)*np.cos(long_t) * np.sin(lat_t)
                    z = (1+lev_t/Rt)*np.sin(long_t)      
                    t = ds.t.sel(time=tim,level=lev,latitude=lat,longitude=long).values
                    #print("t=%s lev=%d lat=%f long=%f temp=%f"%(tim,lev,lat,long,t)) 
                    #print(x[0],y[0],z[0])
                    
                    
                    
                    # branco ->até 4º, azul -> 4---24, verde -> 24 ---40, laranja -> 40+).
                    t = t-273.15
                    
                    if t<-47:
                        cor = (0, 0, 1)     #blue
                    elif t<-30:
                        cor = (0.2, 0.2, 1)
                    elif t<-1:
                        cor = (0.5, 0.5, 1)
                    elif t<-0.5:
                        cor = (0.4, 0.4, 1)
                    elif t<0:
                        cor = (0.5, 0.5, 1)
                    elif t<0.5:
                        cor = (0.6, 0.6, 1)
                    elif t<1:
                        cor = (0.7, 0.7, 1)
                    elif t<1.5:
                        cor = (0.5, 0.5, 1)  
                    elif t<2:
                        cor = (0.5, 0.5, 1)
                    elif t<2.5:
                        cor = (0.5, 0.5, 1)
                    elif t<3:
                        cor = (0.5, 0.5, 1)
                    elif t<3.5:
                        cor = (0.6, 0.6, 1)
                    elif t<4:
                        cor = (0.6, 0.6, 1)
                    elif t<4.5:
                        cor = (0.7, 0.7, 1)
                    elif t<5:
                        cor = (0.7, 0.7, 1)
                    elif t<5.5:
                        cor = (0.8, 0.8, 1)
                    elif t<6:
                        cor = (0.8, 0.8, 1)
                    else: 
                        cor = (1, 1, 1)     #white

                        
                    
                    points = mlab.points3d(x, y, z, scale_mode='none', scale_factor=0.003, color= cor)  
                    
                
                    
                    
                    
                    
                    
                    
        if conta_tempos == 1:
            break;
    # Display continents outline, using the VTK Builtin surface 'Earth'
    from mayavi.sources.builtin_surface import BuiltinSurface
    continents_src = BuiltinSurface(source='earth', name='Continents')
    # The on_ratio of the Earth source controls the level of detail of the continents outline.
    continents_src.data_source.on_ratio = 2
    continents = mlab.pipeline.surface(continents_src, color=(0, 0, 0))
    # Display a semi-transparent sphere, for the surface of the Earth
    # We use a sphere Glyph, throught the points3d mlab function, rather than
    # building the mesh ourselves, because it gives a better transparent rendering.
    sphere = mlab.points3d(0, 0, 0, scale_mode='none', scale_factor=2, color=(0.67, 0.77, 0.93), resolution=50, opacity=0.7, name='Earth')
    # These parameters, as well as the color, where tweaked through the GUI,
    # with the record mode to produce lines of code usable in a script.
    sphere.actor.property.specular = 0.45
    sphere.actor.property.specular_power = 5
    # Backface culling is necessary for more a beautiful transparent rendering.
    sphere.actor.property.backface_culling = True
    # Plot the equator and the tropiques
    theta = np.linspace(0, 2 * np.pi, 100)
    for angle in (- np.pi / 6, 0, np.pi / 6):
        x = np.cos(theta) * np.cos(angle)
        y = np.sin(theta) * np.cos(angle)
        z = np.ones_like(theta) * np.sin(angle)
    mlab.plot3d(x, y, z, color=(1, 1, 1), opacity=0.2, tube_radius=None)
    mlab.view(63.4, 73.8, 4, [-0.05, 0, 0])
    mlab.show()




def display_mapa(coords):
    from mayavi import mlab
    mlab.figure(1, bgcolor=(0.48, 0.48, 0.48), fgcolor=(0, 0, 0), size=(400, 400))
    mlab.clf()
    # Display points at city positions
    coords = np.array(coords)
    # First we have to convert latitude/longitude information to 3D positioning.
    Rt=6400
    lat, long, lev = coords.T * np.pi / 180
    
    lev = lev*180/np.pi
    print(lat[0],long[0],lev[0])
    x = (1+lev/Rt)*np.cos(long) * np.cos(lat)
    y = (1+lev/Rt)*np.cos(long) * np.sin(lat)
    z = (1+lev/Rt)*np.sin(long) 
    
    ##np.sin(long)
    ##print(z)
    #print(coords.T)
    #print(x)
    #print(y)
    #print(z)
    ##cor e formato dos obj
    print(x[0],y[0],z[0])
    points = mlab.points3d(x, y, z, scale_mode='none', scale_factor=0.003, color= (1, 0, 0))
    # Display city names
    #long_ant=0
    #lat_ant=0
    #for city, index in cities.items():
    #    if (x[index]== long_ant)and (y[index]== lat_ant):
    #        pass
    #    else:
    #        label = mlab.text(x[index], y[index], city, z=z[index],
    #                      width=0.016 * len(city), name=city)
    #        label.property.shadow = True
    #    long_ant= x[index]
    #    lat_ant=y[index]

    # Display continents outline, using the VTK Builtin surface 'Earth'
    from mayavi.sources.builtin_surface import BuiltinSurface
    continents_src = BuiltinSurface(source='earth', name='Continents')
    # The on_ratio of the Earth source controls the level of detail of the continents outline.
    continents_src.data_source.on_ratio = 2
    continents = mlab.pipeline.surface(continents_src, color=(0, 0, 0))
    # Display a semi-transparent sphere, for the surface of the Earth
    # We use a sphere Glyph, throught the points3d mlab function, rather than
    # building the mesh ourselves, because it gives a better transparent rendering.
    sphere = mlab.points3d(0, 0, 0, scale_mode='none', scale_factor=2, color=(0.67, 0.77, 0.93), resolution=50, opacity=0.7, name='Earth')
    # These parameters, as well as the color, where tweaked through the GUI,
    # with the record mode to produce lines of code usable in a script.
    sphere.actor.property.specular = 0.45
    sphere.actor.property.specular_power = 5
    # Backface culling is necessary for more a beautiful transparent rendering.
    sphere.actor.property.backface_culling = True
    # Plot the equator and the tropiques
    theta = np.linspace(0, 2 * np.pi, 100)
    for angle in (- np.pi / 6, 0, np.pi / 6):
        x = np.cos(theta) * np.cos(angle)
        y = np.sin(theta) * np.cos(angle)
        z = np.ones_like(theta) * np.sin(angle)
    mlab.plot3d(x, y, z, color=(1, 1, 1), opacity=0.2, tube_radius=None)
    mlab.view(63.4, 73.8, 4, [-0.05, 0, 0])
    mlab.show()



if __name__ == '__main__':
    #my_example_nc_file = "C:\\Users\\Pedro Alves\\Desktop\\Project beta\\potvort_2013119.nc"
    #my_example_nc_file = "C:\\Users\\Pedro Alves\\Desktop\\Project beta\\temperaturee836cf5d-7a5e-4fe7-8292-1453c211e31e.nc"
    my_example_nc_file = "temperaturee836cf5d-7a5e-4fe7-8292-1453c211e31e.nc"
    ds, lista_longitude, lista_latitude, lista_level, lista_time = carrega_dados(my_example_nc_file)
    listagem_de_tudo(ds, lista_longitude, lista_latitude, lista_level, lista_time)
    display_mapa2(ds, lista_longitude, lista_latitude, lista_level, lista_time)
    
    #cidades = cria_dic_locais(lista_longitude, lista_latitude, lista_level)
    #coord_cidades = cria_lista_coords(cidades)
    #display_mapa(coord_cidades)
