from sage.all import *
import numpy as np
import json

#4D Figura
P = polytopes.cross_polytope(4)
sage_vertices_4d = [v.vector() for v in P.vertices()]

# === Proyección 4D → 3D ===
# Get 3D Schlegel projection (affine image in ℝ³)
# This is a 3D polyhedron: use its vertices directly
P3 = P.schlegel_projection()
sage_vertices_3d = [v.vector() for v in P3.vertices()]

vertices_4d = np.array(sage_vertices_4d, dtype=np.float64)
vertices_3d = np.array(sage_vertices_3d, dtype=np.float64)
# Step 4: Center (optional)
#vertices_3d -= vertices_3d.mean(axis=0)

#Indexar vértices (funcion)
vertex_to_index = {v: i for i, v in enumerate(sage_vertices_4d)}   

#Gráfica plana de la figura (vértices y aristas) [1-skeleton graph]
G = P.graph()

# Lista de aristas (parejas de  vértices conectadas)
edges = [(vertex_to_index[u], vertex_to_index[v]) for u, v, _ in G.edges()]



# Crear estructura de datos para el JSON
data = {
    "vertices_4d": vertices_4d.tolist(), # opcional: para debugging
    "vertices_3d": vertices_3d.tolist(),
    "edges": edges
}

# Guardar en archivo JSONx
with open('hexadecacoro_4d_sage_extract.json', 'w') as f:
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