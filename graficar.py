import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import argparse

def grafica(file,varname):

    graf_conf={
        "Tmax":{"label":"Temperatura Máxima (°C)",
                "title":"Temperatura Máxima estaciones PEMBU ", 
                "file_out":"temp_max_"},
        "Pmax":{"label":"Precipitación máxima (mm)",
                "title":"Precipitación estaciones PEMBU ", 
                "file_out":"prec_max_"},        
    }

    df = pd.read_csv(file)
    
    dates=df['Date'].unique()

    for date in dates:        
        #Máximo y mínimo del dominio
        df_filtered = df[df['Date'] == date]
        df_filtered=df_filtered.reset_index(drop=True)
        lonmax = df_filtered.Longitud.max()
        lonmin = df_filtered.Longitud.min()
        latmax = df_filtered.Latitud.max()
        latmin = df_filtered.Latitud.min()


        #Definiendo resolución
        x = np.arange(lonmin,lonmax,0.01)
        y = np.arange(latmin,latmax,0.01)

        #Creando malla
        grid_x, grid_y = np.meshgrid(x,y)

        #Ubicación de los valores
        points = []
        for n in range(len(df_filtered)):
            p = np.array([df_filtered.Longitud[n],df_filtered.Latitud[n]])
            points.append(p)
        points = np.array(points)

        values = df_filtered[varname]

        #Interpolando valores a la nueva malla
        grid_t = griddata(points, values, (grid_x, grid_y), method='linear')
        ruta_shape = 'capas/dest20gw.shp'
        shpmex = gpd.read_file(ruta_shape, rows=slice(24,25))
        cdmx = shpmex.boundary
        #Creando figura
        plt.figure()
        ax = plt.gca()
        #Graficando límites de cdmx
        cdmx.plot(ax=ax)
        #Graficando estaciones
        ss = ax.contourf(grid_x, grid_y, grid_t, cmap='jet', )
        # Agregar la barra de color
        cbar = plt.colorbar(ss, ax=ax)
        cbar.set_label(graf_conf[varname]["label"])  # Etiqueta opcional
        #Graficando malla
        ax.scatter(grid_x, grid_y, s=0.3, c='gray', alpha=0.5)
        ax.set_title(graf_conf[varname]["title"] + date)
        print("Generando ... "+graf_conf[varname]["file_out"]+date+'.png')
        plt.savefig(graf_conf[varname]["file_out"]+date+'.png')
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descripción de tu script")
    parser.add_argument("--file", type=str, default="datos_estaciones.csv", help="Nombre de archivo csv")
    parser.add_argument("--variable", type=str, default="Tmax", help=" posibles valores Tmax ,Pmax")
    args = parser.parse_args()
    grafica(args.file,args.variable)
