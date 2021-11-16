import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import dijkstra_path 

class path__ (object):
	def __init__(self,path,costo):
		self.path = path
		self.costo = costo


def error (a,b):
	error = (abs (a-b) / a )*100
	return error


def costo (ni,nf,attr):
	funcosto_arco = attr["fcosto"]
	flujo_arco = attr["flujo"]
	return funcosto_arco(flujo_arco) 

G = nx.DiGraph ()

f1 = lambda f: 10. + f/120.
f2 = lambda f: 14. + (3*f)/240.
f3 = lambda f: 10. + f/240.
#matriz origen-destino

OD = {
	("A", "C") : 1100.,
	("A", "D") : 1110.,
	("A", "E") : 1020.,
	("B", "C") : 1140.,
	("B", "D") : 1160.,
	("C", "E") : 1170.,
	("C", "G") : 1180.,
	("D", "C") : 350.,
	("D", "E") : 1190.,
	("D", "G") : 1200.



}


OD_target = OD.copy()

G.add_node("A", pos = (0,0))
G.add_node("B", pos = (0,-1))
G.add_node("C", pos = (1,-1))
G.add_node("D", pos = (1,-2))
G.add_node("E", pos = (2,0))
G.add_node("G", pos = (2,-1))

G.add_edge("A","B", fcosto=f1, flujo = 0., costo=0., rec="10 + f/120") #r
G.add_edge("A","C", fcosto=f2, flujo = 0., costo=0., rec="14 + 3f/240") #s

G.add_edge("B","C", fcosto=f3, flujo = 0., costo=0., rec="10 + f/240") #t
G.add_edge("B","D", fcosto=f2, flujo = 0., costo=0., rec="14 + 3f/240") #u


G.add_edge("C","E", fcosto=f2, flujo = 0., costo=0., rec="14 + 3f/240") #w
G.add_edge("C","G", fcosto=f3, flujo = 0., costo=0., rec="10 + f/240") #x

G.add_edge("D","C", fcosto=f1, flujo = 0., costo=0., rec="10 + f/120") #v
G.add_edge("D","G", fcosto=f2, flujo = 0., costo=0., rec="14 + 3f/240") #y

G.add_edge("G","E", fcosto=f1, flujo = 0., costo=0., rec="10 + f/120") #z



	


vector_precision = [0.01]*90 + [0.01]*9 + [0.001]*9 + [0.0001]*10 # 90% + 9% + 0.9% + 0.1%
indice_precision= 0


while 1:
	
	se_asigno_demanda= False
	for key in OD:
		
		origen = key[0]
		destino = key[1]
		demanda_actual = OD[key]
		demanda_target = OD_target[key]

		if demanda_actual>0:

			#ruta minima
			path = dijkstra_path(G, origen,destino,weight=costo)


			#incrementar flujo en ruta minima
			Nparadas= len(path)
			for i_parada in range(Nparadas-1):
				o = path[i_parada]
				d = path[i_parada+1]
				G.edges[o,d]["flujo"] += vector_precision[indice_precision]*demanda_target
			OD[key]-= vector_precision[indice_precision]*demanda_target
			OD[key] = round(OD[key],5)
			
			
			se_asigno_demanda=True
	
	if not se_asigno_demanda:
		break
	indice_precision+=1

for ni, nf in G.edges:
	arco = G.edges[ni, nf]
	funcosto_arco=arco["fcosto"]
	flujo_arco=arco["flujo"]
	arco["costo"] = funcosto_arco(flujo_arco)


for i in G.edges():
    G.edges[i]["flujo"] = round(G.edges[i]["flujo"],4)
    G.edges[i]["costo"] = round(G.edges[i]["costo"],2)


for key in OD:
	inicio = key[0]; final = key[1];
	paths = list(nx.all_simple_paths(G, source=inicio, target=final))
	caminos=[]
	for c in paths:
		i=0
		costo_actual=0
		while i < len(c)-1:
			ni = c[i]
			nf = c[i+1]
			costo_actual+= G.edges[ni,nf]["costo"]
			i+=1
		caminos.append(path__(c,costo_actual))


	target = min(caminos,key = lambda x: x.costo).costo

	tolerancia = 1
	resultado_caminos_final = caminos.copy()
	for i in caminos:
		
		if error(target,i.costo) > tolerancia:
			resultado_caminos_final.remove (i)
		else:
			pass
			
	print(f"Par Origen-Destino {inicio}-{final}")
	for i,j in enumerate(resultado_caminos_final):
		
		print(f"Camino N{i} aceptado con tolerancia del {tolerancia}%: ")
		print(f"Costo = {j.costo:.2f}")
		print(F"Recorrido = {j.path}")
	print("--------------")




plt.figure(1)
ax1 = plt.subplot(111)
pos = nx.get_node_attributes (G,'pos')
nx.draw(G,pos,with_labels=True,font_weight="bold")
labels= nx.get_edge_attributes (G,'flujo')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.title ("flujo")

plt.figure(2)
ax1 = plt.subplot(111)
pos = nx.get_node_attributes (G,'pos')
nx.draw(G,pos,with_labels=True,font_weight="bold")
labels= nx.get_edge_attributes (G,'costo')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.title ("costo")

plt.figure(3)
ax1 = plt.subplot(111)
pos = nx.get_node_attributes (G,'pos')
nx.draw(G,pos,with_labels=True,font_weight="bold")
labels= nx.get_edge_attributes (G,'rec')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.title ("funciones_costos")




plt.show()