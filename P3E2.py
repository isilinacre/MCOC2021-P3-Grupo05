import networkx as nx
import matplotlib.pyplot as plt

def calcular_tiempo(l1,l2,vel):
    dis = (((l2[0]-l1[0])**2) +  ((l2[1]-l1[1])**2))**0.5
    t = round(dis/vel,4)
    return t

def funcion_costo(ni, nf, atributos_arco):
	return atributos_arco["weight"]

class red (object):
    def __init__(self):
        self.G = nx.Graph()
    
    def mostrar_red(self, colores, nombre_archivo, titulo=False, size = 2):
        plt.figure()
        if titulo != False:
            plt.suptitle(titulo)
            
        plt.ylabel("Y (km)")
        plt.xlabel("X (km)")
        y1_vals = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0] 
        y1_txt = ["0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"] 
        plt.yticks(y1_vals,y1_txt) 
        x1_vals = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0] 
        x1_txt = ["0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"]
        plt.xticks(x1_vals,x1_txt) 
        
        ax = plt.gca() 
        
        nx.draw_networkx_nodes(self.G, pos=pos, ax=ax)
        nx.draw_networkx_labels(self.G, pos=pos, ax=ax)
        
        nx.draw_networkx_edges(self.G, pos, ax=ax, width=size, edge_color=colores)
        #nx.draw_networkx_edge_labels(red_entrega_1.G, pos, edge_labels=labels, ax=ax)
        
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        ax.set_axisbelow(True)
        plt.grid('on') 
        plt.tight_layout()
        plt.savefig(nombre_archivo)
        
        
            
        plt.show()
    
    
    def camino_mas_corto (self, ni, nf, nombre_archivo):
        ruta = nx.dijkstra_path(self.G, source=ni, target=nf, weight=funcion_costo)
        costo_ruta = 0.
        Nparadas = len(ruta)
        
        for i in range(Nparadas-1):
        	parada_i = ruta[i]
        	parada_f = ruta[i+1]
        	costo_tramo_i = self.G.edges[parada_i, parada_f]["weight"]
        	
        	costo_ruta += costo_tramo_i
        colores = []
        edgelist = []
        edge_size = []
        for ni, nf in self.G.edges:
        	if ni in ruta and nf in ruta:
        		colores.append("r"); edge_size.append(6);
                
        	else:
        		colores.append("#808080"); edge_size.append(2);
        
        	edgelist.append((ni,nf))
        	
        costo_ruta = round(costo_ruta,4)




        self.mostrar_red(colores, nombre_archivo,f"Ruta minima: {ruta} tiempo_de_viaje={costo_ruta}",edge_size)

        return





if __name__ == "__main__":
    


    red_entrega_1 = red()
    
    nodos = [
        (0,{"pos": [1,2]}),
        (1,{"pos": [4,3]}),
        (2,{"pos": [1,6]}),
        (3,{"pos": [7,3]}),
        (4,{"pos": [10,1]}),
        (5,{"pos": [0,10]}),
        (6,{"pos": [4,0]}),
        (7,{"pos": [5,8]}),
        (8,{"pos": [9,7]}),
        (9,{"pos": [8,10]}),
        ]
    
    #Colores arcos
    cafe, verde, gris = '#6C4E09', '#00701A', '#7C7C7C'
    
    edges = [
        (0,2,{"velocidad": 120,'weight': calcular_tiempo(nodos[0][1]["pos"],nodos[2][1]["pos"],120), "color": gris}),
        (0,6,{"velocidad": 120,'weight': calcular_tiempo(nodos[0][1]["pos"],nodos[6][1]["pos"],120), "color": gris}),
        (6,4,{"velocidad": 120,'weight': calcular_tiempo(nodos[6][1]["pos"],nodos[4][1]["pos"],120), "color": gris}),
        (4,8,{"velocidad": 120,'weight': calcular_tiempo(nodos[4][1]["pos"],nodos[8][1]["pos"],120), "color": gris}),
        (5,7,{"velocidad": 120,'weight': calcular_tiempo(nodos[5][1]["pos"],nodos[7][1]["pos"],120), "color": gris}),
        (3,4,{"velocidad": 60,'weight': calcular_tiempo(nodos[3][1]["pos"],nodos[4][1]["pos"],60), "color": verde}),
        (1,3,{"velocidad": 60,'weight': calcular_tiempo(nodos[1][1]["pos"],nodos[3][1]["pos"],60), "color": verde}),
        (3,7,{"velocidad": 60,'weight': calcular_tiempo(nodos[3][1]["pos"],nodos[7][1]["pos"],60), "color": verde}),
        (7,9,{"velocidad": 60,'weight': calcular_tiempo(nodos[7][1]["pos"],nodos[9][1]["pos"],60), "color": verde}),
        (9,8,{"velocidad": 60,'weight': calcular_tiempo(nodos[9][1]["pos"],nodos[8][1]["pos"],60), "color": verde}),
        (6,3,{"velocidad": 40,'weight': calcular_tiempo(nodos[6][1]["pos"],nodos[3][1]["pos"],40), "color": cafe}),
        (8,3,{"velocidad": 40,'weight': calcular_tiempo(nodos[8][1]["pos"],nodos[3][1]["pos"],40), "color": cafe}),
        (0,1,{"velocidad": 40,'weight': calcular_tiempo(nodos[0][1]["pos"],nodos[1][1]["pos"],40), "color": cafe}),
        (7,1,{"velocidad": 40,'weight': calcular_tiempo(nodos[7][1]["pos"],nodos[1][1]["pos"],40), "color": cafe}),
        (2,1,{"velocidad": 40,'weight': calcular_tiempo(nodos[2][1]["pos"],nodos[1][1]["pos"],40), "color": cafe}),
        (2,5,{"velocidad": 40,'weight': calcular_tiempo(nodos[2][1]["pos"],nodos[5][1]["pos"],40), "color": cafe})
        ]
    
    red_entrega_1.G.add_nodes_from(nodos)
    red_entrega_1.G.add_edges_from(edges)
    pos=nx.get_node_attributes(red_entrega_1.G,'pos')
    labels = nx.get_edge_attributes(red_entrega_1.G,"weight")
    coloresEdges = nx.get_edge_attributes(red_entrega_1.G, 'color')
    
    #Para graficar el color de cada arco  
    colores = []
    for dato in coloresEdges:
        colores.append(coloresEdges[dato])
    
    red_entrega_1.mostrar_red(colores, "fig1.png")
    red_entrega_1.camino_mas_corto(0, 9, "fig2.png")
    red_entrega_1.camino_mas_corto(4, 5, "fig3.png")
    red_entrega_1.camino_mas_corto(0, 4, "fig4.png")
        
