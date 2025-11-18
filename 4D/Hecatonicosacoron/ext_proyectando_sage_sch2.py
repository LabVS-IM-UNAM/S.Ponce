from sage.all import *
import numpy as np
import json

print("[1/5] Setting up high precision...")
RF = RealField(200)  # ~60 decimal digits

print("[2/5] Loading 120-cell...")
P = polytopes.one_hundred_twenty_cell()
assert P.n_vertices() == 600, "Expected 600 vertices"

# Extract vertices in high precision
sage_vertices_4d = [tuple(vector(RF, v)) for v in P.vertices()]
assert len(set(sage_vertices_4d)) == 600
vertex_to_index = {v: i for i, v in enumerate(sage_vertices_4d)}
vertices_4d = np.array(sage_vertices_4d, dtype=np.float64)
print(f"[✓] Loaded {len(vertices_4d)} 4D vertices")

print("[3/5] Applying generic 4D rotation (to break symmetry)...")
# Random but reproducible SO(4) rotation
np.random.seed(2025)
# Generate random 4x4 matrix and QR-decompose to get orthogonal matrix
A = np.random.randn(4, 4)
Q, _ = np.linalg.qr(A)
# Ensure determinant +1 (proper rotation)
if np.linalg.det(Q) < 0:
    Q[:, 0] = -Q[:, 0]
rotation = Q

# Rotate all vertices
vertices_4d_rot = vertices_4d @ rotation.T
print("[✓] Rotation applied")

print("[4/5] Perspective projection to w=0 hyperplane...")
# Projection point behind the polytope along w-axis
d = 4.0  # polytope fits in [-2,2]^4; d=4 is safely outside
proj_point = np.array([0.0, 0.0, 0.0, d])  # (x,y,z,w) = (0,0,0,d)

vertices_3d = []
tol = 1e-12

for v in vertices_4d_rot:
    # Parametric line: p + t*(v - p)
    # We want w = 0:  d + t*(v[3] - d) = 0  →  t = d / (d - v[3])
    denom = d - v[3]
    if abs(denom) < tol:
        t = 1.0
    else:
        t = d / denom
    # Compute x,y,z at intersection
    x = proj_point[0] + t * (v[0] - proj_point[0])
    y = proj_point[1] + t * (v[1] - proj_point[1])
    z = proj_point[2] + t * (v[2] - proj_point[2])
    vertices_3d.append([x, y, z])

vertices_3d = np.array(vertices_3d)
print(f"[✓] Projected to 3D: {vertices_3d.shape}")

print("[5/5] Validating uniqueness...")
def count_unique(arr, decimals):
    return len(np.unique(np.round(arr, decimals=decimals), axis=0))

for dec in [6, 8, 10, 12]:
    cnt = count_unique(vertices_3d, dec)
    mark = "✅" if cnt == 600 else "❌"
    print(f"  {mark} {cnt} unique vertices (decimals={dec})")

assert count_unique(vertices_3d, 10) == 600, "Projection still collapsed vertices!"

print("[6/6] Extracting edges...")
G = P.graph()
edges = []
for u_vec, v_vec, _ in G.edges():
    u_key = tuple(vector(RF, u_vec))
    v_key = tuple(vector(RF, v_vec))
    i = vertex_to_index[u_key]
    j = vertex_to_index[v_key]
    edges.append((i, j))

assert len(edges) == 1200, f"Expected 1200 edges, got {len(edges)}"

print("Exporting to JSON...")
data = {
    "metadata": {
        "polytope": "120-cell (Sage one_hundred_twenty_cell)",
        "projection": "perspective from (0,0,0,4) onto w=0",
        "rotation_applied": True,
        "vertices_4d": 600,
        "vertices_3d_unique": 600,
        "edges": 1200
    },
    "vertices_4d": np.round(vertices_4d, 12).tolist(),
    "vertices_3d": np.round(vertices_3d, 10).tolist(),  # 10 decimals safe for viewers
    "edges": edges
}

filename = "120cell_perspective.json"
with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n🎉 SUCCESS! All 600 vertices preserved.")
print(f"📁 Output saved to: {filename}")