#ESTE MÉTODO ES EL CIENTÍFICO (scene/Plotting) Y NO UTILIZA OpenGL; NO ES EL ADECUADO PARA LOS GRÁFICOS BUSCADOS
from vispy import scene

# Crear el canvas
canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))

# Añadir vista
view = canvas.central_widget.add_view()

# Configurar una cámara
view.camera = 'turntable' # otras opciones posibles: 'arcball'(más libertad, estilo solidWorks?) , 'fly', 'panzoom'(2D), etc.
view.camera.fov = 30       # campo de visión (opcional)
view.camera.distance = 5   # distancia inicial desde el origen

# Añadir los ejes XYZ
axis = scene.visuals.XYZAxis(parent=view.scene)
axis.transform = scene.transforms.STTransform(scale=(1, 1, 1))  # asegura tamaño visible

# Opcional: añadir malla para referencia
grid = scene.visuals.GridLines(parent=view.scene)

# ¡Importante! Esto mantiene la ventana abierta
canvas.app.run()