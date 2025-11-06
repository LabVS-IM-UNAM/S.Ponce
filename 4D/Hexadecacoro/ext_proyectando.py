from sage.all import *
import numpy as np
import json

#4D Figura
P = polytopes.cross_polytope(4)

#Invoca los vértices desde SageMath
sage_vertices = list(P.vertices())
#Extrar vertices en forma matricial
vertices_4d = np.array([list(v) for v in sage_vertices], dtype=np.float32)

# === Proyección 4D → 3D ===

# Proyección en perspectiva: (x, y, z, w) → (x+(w/2)), y+(w/2), z+(w/2))
P_matrix = np.array([
    [1, 0, 0, 0.5],
    [0, 1, 0, 0.5],
    [0, 0, 1, 0.5]
], dtype=np.float32)

vertices_3d = vertices_4d @ P_matrix.T  # shape (8, 3)

#Indexar vértices (funcion)
vertex_to_index = {v: i for i, v in enumerate(sage_vertices)}   

#Gráfica plana de la figura (vértices y aristas) [1-skeleton graph]
G = P.graph()

# Lista de aristas (parejas de  vértices conectadas)
edges = [(vertex_to_index[u], vertex_to_index[v]) for u, v, _ in G.edges()]

# Convertir arrays de NumPy a listas de Python para serializar en JSON
vertices_3d_list = vertices_3d.tolist()
edges_list = edges  # ya es una lista de tuplas de enteros

# Crear estructura de datos para el JSON
data = {
    "vertices_4d": vertices_4d.tolist(), # opcional: para debugging
    "vertices_3d": vertices_3d.tolist(),
    "edges": edges
}

# Guardar en archivo JSONx
with open('hexadecacoro_4d.json', 'w') as f:
    json.dump(data, f, indent=2)

#Prueba de resultados
print("Number of vertices 4D:", len(vertices_4d))
print(vertices_4d)
print("Número de vértices únicos en 3D:", len(np.unique(np.round(vertices_3d, decimals=5), axis=0)))
print(vertices_3d)
print("Number of edges:", len(edges))
print(edges)


#CAMBIO DE MOTOR DE VISUALIZACIÓN (VisPy en lugar de PyVista)
#VisPy opera con OpenGL (ESTO SERVIRA PARA MANEJAR MEJOR LAS IMÁGENES CON MAYOR DETALLE Y EFICIENCIA)
#Otro proyecto del servicio cuenta con la recomendación de utulizar la herramienta de OpenGL
#La recomendación de OpenGL para el otro proyecto NO es adecuada
#El otro proyecto requiere de el uso de OpenCV
#De igual manera la mejor opción para mostrar los gráficos esperados es OpenGL