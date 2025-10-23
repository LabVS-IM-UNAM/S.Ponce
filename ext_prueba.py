from sage.all import *
import numpy as np

#4D Cubo
P = polytopes.hypercube(4)

#Invoca los vértices desde SageMath
sage_vertices = list(P.vertices())
#Extrar vertices en forma matricial
vertices_4d = np.array([list(v) for v in sage_vertices])
#Proyección ortogonal de vértices (4D ---> 3D)
vertices_3d = vertices_4d[:, :3]

#Indexar vértices (funcion)
vertex_to_index = {v: i for i, v in enumerate(sage_vertices)}   

#Gráfica plana de la figura (vértices y aristas) [1-skeleton graph]
G = P.graph()

# Lista de aristas (parejas de  vértices conectadas)
edges = [(vertex_to_index[u], vertex_to_index[v]) for u, v, _ in G.edges()]

#Prueba de resultados
print("Number of vertices:", len(vertices_4d))
print(vertices_4d)
print("Number of edges:", len(edges))
print(edges)


#CAMBIO DE MOTOR DE VISUALIZACIÓN (VisPy en lugar de PyVista)
#VisPy opera con OpenGL (ESTO SERVIRA PARA MANEJAR MEJOR LAS IMÁGENES CON MAYOR DETALLE Y EFICIENCIA)
#Otro proyecto del servicio cuenta con la recomendación de utulizar la herramienta de OpenGl