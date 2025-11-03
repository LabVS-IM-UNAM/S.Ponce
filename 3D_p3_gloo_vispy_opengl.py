from vispy import app, gloo
from vispy.gloo import Program, VertexBuffer, IndexBuffer
from vispy.util.transforms import perspective, translate, rotate
import numpy as np

# ==================== SHADERS ====================
vertex = """
    uniform float alpha;
    uniform float beta;
    uniform float gamma;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    attribute vec3 position;
    attribute vec4 color;   
    varying vec4 v_color;
    void main()
    {
        gl_Position = projection * view * model * vec4(position, 1.0);
        v_color = color;
    } """

fragment = """
    varying vec4 v_color;
    void main()
    {
        gl_FragColor = v_color;
    } """

# ==================== CANVAS ====================
class Canvas(app.Canvas):
    def __init__(self):
        super().__init__(size=(700, 700), title='3D Dodeca', keys='interactive')
        
        #VERTICES
        phi = 1.618 #Golden ratio
        inv_phi = 0.618 #Inverse Golden ratio

        vertices = np.array([
            # Even permutations of (0, ±1/φ, ±φ)
            [0, inv_phi, phi], [0, inv_phi, -phi], [0, -inv_phi, phi], [0, -inv_phi, -phi],
            [inv_phi, phi, 0], [-inv_phi, phi, 0], [inv_phi, -phi, 0], [-inv_phi, -phi, 0],
            [phi, 0, inv_phi], [-phi, 0, inv_phi], [phi, 0, -inv_phi], [-phi, 0, -inv_phi],
            # Even permutations of (±1, ±1, ±1)
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
        ], dtype=np.float32)

        
        #EDGES-INDICES
        # Compute edges by connecting nearest neighbors
        edges = np.array([(0, 2), (0, 12), (0, 16), (1, 3), (1, 13), (1, 17), (2, 14), (2, 18), (3, 15), (3, 19), (4, 5), (4, 12), (4, 13), (5, 16), (5, 17), (6, 7), (6, 14), (6, 15), (7, 18), (7, 19), (8, 10), (8, 12), (8, 14), (9, 11), (9, 16), (9, 18), (10, 13), (10, 15), (11, 17), (11, 19)])

        flattened_edges = edges.flatten().tolist()

        # COLORS
        colors = np.ones((20, 4), dtype=np.float32)

        #DEFINE PROGRAM VARIABLES
        self.program = Program(vertex, fragment)
        self.program['position'] = VertexBuffer(vertices)
        self.program['color'] = VertexBuffer(colors)
        self.indices = IndexBuffer(flattened_edges)

        #rotation variables
        self.alpha = 0
        self.beta = 0
        self.gamma = 0

        self.model = np.eye(4, dtype=np.float32) #identity matrix np.eye(4)

        #VIEWING DISTANCE
        self.camera_z = -11.0
        self.view = translate((0, 0, self.camera_z))

        self.projection = perspective(45.0, self.size[0]/self.size[1], 1.0, 100.0)

        self.program['model'] = self.model
        self.program['view'] = self.view
        self.program['projection'] = self.projection

        gloo.set_state(clear_color='black', depth_test=True)
        self.show()
        self.update()  #Forces the 1st on_draw
    

    # ========== DRAW ==========
    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        self.program.draw('lines', self.indices)

    # ========== RESIZE ==========
    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_key_press(self, event):
        #ROTATE
        if event.text == 'w':
            self.alpha += 15

        elif event.text == 's':
            self.alpha -= 15

        elif event.text == 'a':
            self.beta += 15
        
        elif event.text == 'd':
            self.beta -= 15
        
        elif event.text == 'q':
            self.gamma += 15
        
        elif event.text == 'e':
            self.gamma -= 15

        #ZOOM
        elif event.text == 'i':  # zoom in 
            #self.camera_z += 1.0
            self.camera_z = min(self.camera_z + 1.0, -3.0)  #NO MORE THAN -1
        elif event.text == 'o':  # zoom out
            self.camera_z = max(self.camera_z - 1.0, -33.0)  #NOT LESS THAN -50
        
        #UPDATE IF ROTATION
        if event.text in ('w', 's', 'a', 'd', 'q', 'e'):
            model = np.eye(4, dtype=np.float32)
            model = rotate(self.alpha, (0, 1, 0)) @ model
            model = rotate(self.beta, (1, 0, 0)) @ model
            model = rotate(self.gamma, (0, 0, 1)) @ model
            self.program['model'] = model

        #UPDATE IF ZOOM
        if event.text in ('i', 'o'):
            self.view = translate((0, 0, self.camera_z))
            self.program['view'] = self.view

        self.update()  #REDRAW FOCED
    

if __name__ == '__main__':
    app.use_app('pyqt5')
    c = Canvas()
    app.run()