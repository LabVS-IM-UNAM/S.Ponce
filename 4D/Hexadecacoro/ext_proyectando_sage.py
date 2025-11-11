from sage.all import *
import numpy as np
import json

#4D Figure
P = polytopes.cross_polytope(4)

# --- 4D vertices as tuples (immutable)
sage_vertices_4d = [tuple(v) for v in P.vertices()]
vertex_to_index = {v: i for i, v in enumerate(sage_vertices_4d)}
vertices_4d = np.array(sage_vertices_4d, dtype=np.float64)

# --- Manual Schlegel projection from 4D -> 3D ---
    #A Schlegel diagram is a projection of a d-dimensional polytope into (d−1)-dimensional space, done via perspective projection from a point just outside one of its facets (faces of dimension d−1).
# Choose a facet: one with max x4 = 1 (you can pick any)
facet = P.facets()[0]
    #Choose the first of the 3D facets
ineq = facet.ambient_Hrepresentation()[0]
    #Take that first inequality, the one that defines the hyperplane corresponding to the facet face
    #A⋅x <= b
        #A:=normal vector of that face (perpendicular to the face)
        #b:=distance from origin
normal_4d = np.array(ineq.A(), dtype=float).flatten()
offset = float(ineq.b())
    #define for further use into formulas

# --- Choose a projection point just outside that facet [normalizing the normal vector that defines the facet]
    #Scaling it to position the view, 10% beyond the polytope surface along that normal direction.
    #This is our "CAMERA" or "projection eye point"
projection_point = 1.5 * normal_4d / np.linalg.norm(normal_4d)

# --- Project each vertex from 4D → 3D ---
vertices_3d = []
for v in vertices_4d:
    direction = v - projection_point
    #4D direction vector along which we’ll trace the line from the projection point toward the vertex.

    denom = np.dot(normal_4d, direction)
    #dot product to find the scalar projection (length of a vector's shadow on another)

    if abs(denom) < 1e-11: #one trillionth of one
        # vertex lies in or parallel to the facet plane; skip or copy directly (projects into itself or really close to it)
        x_proj = v
    else:
        #Take the line form "v" to the point where it crosses the facet by:
            #Defining the line under the PARAMETRIC DEFINITION of "l={P + tD | t  in R(#)} with P the projection point which it passes by and D direction vector"
            #Substitute inside "A ⋅ x = b" to obtain "t"
        t = (offset - np.dot(normal_4d, projection_point)) / denom
        x_proj = projection_point + t * direction
    vertices_3d.append(x_proj[:-1])  # drop 4th coordinate → 3D

vertices_3d = np.array(vertices_3d, dtype=np.float64)

# --- Center 3D figure at origin ---
#center = vertices_3d.mean(axis=0)
#vertices_3d -= center

#scaled to unit radius
#vertices_3d /= np.linalg.norm(vertices_3d, axis=1).max()

#Gráfica plana de la figura (vértices y aristas) [1-skeleton graph]
G = P.graph()

# Lista de aristas (parejas de  vértices conectadas)
edges = [
    (vertex_to_index[tuple(u)], vertex_to_index[tuple(v)])
    for u, v, _ in G.edges()
]



# Crear estructura de datos para el JSON
data = {
    "vertices_4d": vertices_4d.tolist(), # opcional: para debugging
    "vertices_3d": vertices_3d.tolist(),
    "edges": edges
}

# Guardar en archivo JSONx
with open('hexadecacoro_4d_sage_extract_15.json', 'w') as f:
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