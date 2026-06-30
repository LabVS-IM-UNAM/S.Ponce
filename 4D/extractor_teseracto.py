# extractor_teseracto.py
from sage.all import *
import json

# 1. Crear el teseracto (hipercubo 4D)
P = polytopes.hypercube(4)

# 2. Obtener vértices en 4D
vertices_4d = P.vertices()

# 3. Proyectar a 3D: simplemente tomamos las primeras 3 coordenadas
#    (esto es una proyección ortogonal válida)
vertices_3d = []
for v in vertices_4d:
    coords = v.vector()  # vector en QQ^4
    # Convertir a float y tomar x, y, z
    x, y, z = float(coords[0]), float(coords[1]), float(coords[2])
    vertices_3d.append([x, y, z])

# 4. Obtener aristas: pares de vértices conectados
edges = []
verts_list = list(vertices_4d)
for i, v1 in enumerate(verts_list):
    for j, v2 in enumerate(verts_list):
        if j > i and P.vertex_adjacent(v1, v2):
            edges.append([i, j])

# Guardar
data = {
    "vertices": vertices_3d,
    "edges": edges
}

with open("tesseract_data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Teseracto guardado: {len(vertices_3d)} vértices, {len(edges)} aristas.")
