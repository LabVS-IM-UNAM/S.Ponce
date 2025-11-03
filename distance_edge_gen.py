import numpy as np
from scipy.spatial.distance import pdist, squareform

# VERTICES
phi = 1.618  # Golden ratio
inv_phi = 0.618  # Inverse Golden ratio

vertices = np.array([
    # Even permutations of (0, ±1/φ, ±φ)
    [0, inv_phi, phi], [0, inv_phi, -phi], [0, -inv_phi, phi], [0, -inv_phi, -phi],
    [inv_phi, phi, 0], [-inv_phi, phi, 0], [inv_phi, -phi, 0], [-inv_phi, -phi, 0],
    [phi, 0, inv_phi], [-phi, 0, inv_phi], [phi, 0, -inv_phi], [-phi, 0, -inv_phi],
    # Even permutations of (±1, ±1, ±1)
    [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
    [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
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
