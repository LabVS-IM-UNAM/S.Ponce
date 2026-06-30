# visualizar.py
import pyvista as pv
import json
import numpy as np

# Cargar datos
with open("polytope.json") as f:
    data = json.load(f)

vertices = np.array(data["vertices"])
edges = data["edges"]

# Formato de líneas para PyVista
lines = []
for i, j in edges:
    lines.extend([2, i, j])
lines = np.array(lines, dtype=int)

# Crear y mostrar
poly = pv.PolyData(vertices, lines=lines)
plotter = pv.Plotter()
plotter.add_mesh(poly, color="white", line_width=2)
plotter.set_background("black")
plotter.show()  # ← Esto abre una ventana INTERACTIVA (ratón: rotar, zoom, pan)
