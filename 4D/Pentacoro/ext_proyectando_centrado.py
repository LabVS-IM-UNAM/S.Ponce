from sage.all import *
import numpy as np
import json

#4D Cubo
#P = polytopes.simplex(4)

#Invoca los vértices desde SageMath
#sage_vertices = list(P.vertices())
manual_vertices = [
                (0,0,0,0),
                (1,0,0,0),
                (0,1,0,0),
                (0,0,1,0),
                (0,0,0,1)
                ]
#Extrar vertices en forma matricial
vertices_4d = np.array([list(v) for v in manual_vertices], dtype=np.float32)

#Centrar al origen del espacio (primero tomamos los promedios)
#centroid = np.mean(vertices_4d, axis=0)
#vertices_4d_centered = vertices_4d - centroid

#Escalar para mejorar visibilidad (opcional)
#scale = 1.0
#vertices_4d_centered_scaled = vertices_4d_centered * scale

# === Parámetros de proyección 4D → 3D ===
#d := Punto de vista en la 4ta dimensión (w), distancia desde el origen en w; ajusta para evitar división por cero
# Proyección en perspectiva: (x, y, z, w) → (x*(d/(d - w)), y*(d/(d - w)), z*(d/(d - w)))
def project_4D_to_3D(points, d=3.0):
    projected = []
    for (x, y, z, w) in points:
        factor = d / (d - w)
        projected.append((x * factor, y * factor, z * factor))
    return np.array(projected)

# Apply projection
vertices_4d_centered = vertices_4d - np.mean(vertices_4d, axis=0)
vertices_3d = project_4D_to_3D(vertices_4d_centered, d=3.0)
# Proyección ortogonal: simplemente toma las primeras 3 coordenadas
#vertices_3d = vertices_4d[:, :3].copy()

#CENTRAR FIGURA
#entroid = np.mean(vertices_3d, axis=0)
#vertices_3d_centered = vertices_3d - centroid



#Gráfica plana de la figura (vértices y aristas) [1-skeleton graph]
P = polytopes.simplex(4)
G = P.graph()
sage_vertices = np.array([tuple(v) for v in P.vertices()], dtype=np.float32)

#Indexar vértices (funcion)
#   vertex_to_index = {v: i for i, v in enumerate(sage_vertices)}   

# Lista de aristas (parejas de  vértices conectadas)
#edges = [(vertex_to_index[u], vertex_to_index[v]) for u, v, _ in G.edges()]
edges = [(0,1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

# Convertir arrays de NumPy a listas de Python para serializar en JSON
vertices_3d_list = vertices_3d.tolist()
edges_list = edges  # ya es una lista de tuplas de enteros

# Crear estructura de datos para el JSON
data = {
    "vertices_4d": vertices_4d.tolist(),  # opcional: para debugging
    "vertices_3d": vertices_3d.tolist(),
    "edges": edges
}

# Guardar en archivo JSONx
with open('pentachoron_4d_5.json', 'w') as f:
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