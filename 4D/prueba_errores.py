from vispy import scene, app, keys

# Crear canvas
canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='black', size=(700,700))
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(fov=45, distance=5)

# Crear cubo
cube = scene.visuals.Box(width=1, height=1, depth=1, color='white', edge_color='black', parent=view.scene)

# Función para controlar rotación y zoom con teclas
@canvas.events.key_press.connect
def on_key(event):
    if event.key == keys.W:
        view.camera.elevation += 5
    elif event.key == keys.S:
        view.camera.elevation -= 5
    elif event.key == keys.A:
        view.camera.azimuth -= 5
    elif event.key == keys.D:
        view.camera.azimuth += 5
    elif event.key == keys.I:
        view.camera.distance = max(1, view.camera.distance - 0.2)
    elif event.key == keys.O:
        view.camera.distance += 0.2

app.run()
