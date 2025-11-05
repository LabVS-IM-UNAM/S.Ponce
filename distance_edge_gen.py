import numpy as np
from scipy.spatial.distance import pdist, squareform

# VERTICES
phi = (1 + np.sqrt(5)) / 2       # número áureo
s = phi / 2                      # factor de escala para arista = 1

vertices = np.array([
    [0,  s,  s*phi],
    [0, -s,  s*phi],
    [0,  s, -s*phi],
    [0, -s, -s*phi],
    [ s,  s*phi, 0],
    [-s,  s*phi, 0],
    [ s, -s*phi, 0],
    [-s, -s*phi, 0],
    [ s*phi, 0,  s],
    [-s*phi, 0,  s],
    [ s*phi, 0, -s],
    [-s*phi, 0, -s]
], dtype=np.float64)

# Calcular distancias
dist_matrix = squareform(pdist(vertices))

# Ignore zero distances (distance to self)
nonzero_distances = dist_matrix[dist_matrix > 1e-6]

# Minimum distance corresponds to edges
min_dist = np.min(nonzero_distances)
tolerance = 1e-3  # still reasonable

edges = [(i, j) for i in range(len(vertices)) 
                for j in range(i + 1, len(vertices))
                if abs(dist_matrix[i, j] - min_dist) < tolerance]

print(f"Número de aristas: {len(edges)}")
print(f"Lista de aristas: {edges}")
