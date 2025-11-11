#¡ESTE ES EL BUENO! Explicación incompleta
from sage.all import *
import numpy as np
import json

#4D Figure
P = polytopes.cross_polytope(4)

# --- 4D vertices
sage_vertices_4d = [tuple(v) for v in P.vertices()]
vertex_to_index = {v: i for i, v in enumerate(sage_vertices_4d)}
vertices_4d = np.array(sage_vertices_4d, dtype=np.float64)


# --- Manual Schlegel projection from 4D -> 3D ---
    #A Schlegel diagram is a projection of a d-dimensional polytope into (d−1)-dimensional space, done via perspective projection from a point just outside one of its facets (faces of dimension d−1).
# Choose a facet
facet = P.facets()[0]
    #Choose the first of the 3D facets
h_eq = facet.ambient_Hrepresentation()[0]
    #Take that first equation, the one that defines the hyperplane where it lands the facet face 
        #(Each facet lies on a hyperplane a₀x₀ + a₁x₁ + a₂x₂ + a₃x₃ = b)
    #A ⋅ x = b
        #A := normal vector of that face (perpendicular to the face)
        #b := distance from origin
normal_4d = np.array(h_eq.A(), dtype=float).flatten()
offset = float(h_eq.b())
    #define for further use into formulas

# Ensure normal points outward (optional but safer)
# Test: pick a vertex NOT in facet
facet_verts = {tuple(v) for v in facet.vertices()}
test_v = next(v for v in sage_vertices_4d if v not in facet_verts)
    #Returns the first vertex in sage_vertices_4d that is not in facet_verts.
if np.dot(normal_4d, test_v) > offset:
    normal_4d = -normal_4d
    offset = -offset
    #ensures that normal_4d points away from the polytope, so projection is well-defined (vectors land inside of view)

# --- Choose a projection point just outside that facet (outside of polytope, along the normal direction)
proj_dist = 1.5  # scale factor > 1
normal_norm = np.linalg.norm(normal_4d)
unit_normal = normal_4d / normal_norm  #normal_4d with length 1
max_proj = max(np.dot(normal_4d, v) for v in vertices_4d) #how far along the normal direction the furthest point lies
p_dist = proj_dist * (max_proj / normal_norm) 
    #maximum distance from the origin to any vertex, measured in relation to the normal_4d length
    #scaled by proj_dist to generate perspective view
projection_point = p_dist * unit_normal
    #define the view point, in direction of the nomal_4d but scaled adequatly to conform to all vertices

# --- Project each vertex onto hyperplane of the chosen facet [normal·x = offset] ---
projected_4d = []  # will store 4D points *on* the hyperplane
for v in vertices_4d:
    direction = v - projection_point
    denom = np.dot(normal_4d, direction)
    if abs(denom) < 1e-11:
        x_proj = v #lies in or parallel to the facet plane, copy directly
    else:
        #Take the line form "v" to the point where it crosses the facet by:
            #Defining the line under the PARAMETRIC DEFINITION of "l={P + tD | t  in R(#)} with P the projection point which it passes by and D direction vector"
            #Substitute inside "A ⋅ x = b" to obtain "t"
        t = (offset - np.dot(normal_4d, projection_point)) / denom
        x_proj = projection_point + t * direction
    projected_4d.append(x_proj)

projected_4d = np.array(np.round(projected_4d,3))

# --- ✅ CRITICAL FIX: Map hyperplane to ℝ³ properly ---
# Pick a reference point on the hyperplane:
x0 = (offset / (normal_4d @ normal_4d)) * normal_4d

# Get orthonormal basis for hyperplane (3 vectors in ℝ⁴)
n = normal_4d / normal_norm
# Use QR decomposition to get orthonormal complement
Q, _ = np.linalg.qr(np.vstack([n, np.eye(4)]).T)  # 4×4 orthogonal matrix
basis_3d = Q[:, 1:]  # last 3 columns: orthonormal basis of hyperplane

# Project each 4D point to 3D coordinates in this basis
vertices_3d = []
for x in projected_4d:
    rel = x - x0  # vector in hyperplane direction
    coords = basis_3d.T @ rel  # 3D coordinates
    vertices_3d.append(coords)

vertices_3d = np.array(np.round(vertices_3d,3), dtype=np.float64)

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
with open('hexadecacoro_4d_sage_extract_sch_7.json', 'w') as f:
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