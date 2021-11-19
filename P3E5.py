import networkx as nx 
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gps
from networkx.algorithms import astar_path, all_simple_paths, all_shortest_paths, dijkstra_path
import numpy as np
import csv
from shapely.geometry import Point, LineString

def zonas_selected (zonas_gdf,archivo_csv):


    
    id_zonas_a_graficar = [] #680,676,672,667,668,669,671,670,679
    with open(f'{archivo_csv}.csv', 'r') as inp:
        
        for row in csv.reader(inp):
            zona_origen = int(row[0])
            zona_destino = int(row[1])
            if zona_origen not in id_zonas_a_graficar:
                id_zonas_a_graficar.append(int(zona_origen))
            if zona_destino not in id_zonas_a_graficar:
                id_zonas_a_graficar.append(int(zona_destino))


    

    id_zonas_a_graficar.sort()
    return id_zonas_a_graficar

def calcular_distancia(l1,l2):
    R = 6373
    lat1 = np.radians(l1[1])
    lon1 = np.radians(l1[0])
    lat2 = np.radians(l2[1])
    lon2 = np.radians(l2[0])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = np.sin(dlat/2)**2 + np.cos(lat2)*np.sin(dlon/2)**2
    c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))

    dis = R*c
    return dis


zonas_gdf = gps.read_file ('eod.json')


ox.config (use_cache=True, log_console=False)

G=nx.read_gpickle("stgo_grueso.gpickle")

gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

plt.figure ()

ax = plt.subplot (111)
zonas_gdf = gps.read_file("eod.json") 

id_zonas_a_graficar=zonas_selected(zonas_gdf,"mod_edit")
id_zonas_a_graficar= [str(x) for x in id_zonas_a_graficar]
zonas_seleccionadas = zonas_gdf[zonas_gdf["id"].isin(id_zonas_a_graficar)]

zonas_totales = zonas_gdf[zonas_gdf["id"].isin(id_zonas_a_graficar)]
gdf_edges = gps.clip(gdf_edges,zonas_totales)

zonas_seleccionadas.plot(ax=ax, color="#CDCDCD") 
# gdf_nodes.plot(ax=ax,legend=True)
gdf_edges[gdf_edges.highway=="motorway"].plot(ax=ax,color='orange')
gdf_edges[gdf_edges.highway=="primary"].plot(ax=ax,color='yellow')
gdf_edges[gdf_edges.highway=="secondary"].plot(ax=ax,color='green')
gdf_edges[gdf_edges.highway=="tertiary"].plot(ax=ax,color='blue')
gdf_edges[gdf_edges.name=="Autopista Vespucio Oriente"].plot(ax=ax,color='red',linewidth=3)
# gdf_edges[gdf_edges.osmid=="AVO"].plot(ax=ax,color='red',linewidth=3)

plt.show()




