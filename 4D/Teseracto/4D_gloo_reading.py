from vispy import app, gloo
from vispy.gloo import Program, VertexBuffer, IndexBuffer
from vispy.util.transforms import perspective, translate, rotate
import numpy as np
import json

# =================== READ DATA ===================
with open('hypercube_4d_3.json', 'r') as f:
    data = json.load(f)

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
        super().__init__(size=(700, 700), title='4D Teseracto', keys='interactive')
        
        #VERTICES
        vertices = np.array(data['vertices_3d'], dtype=np.float32)

        
        #EDGES-INDICES
        edges = np.array(data['edges'], dtype=np.uint32)

        flattened_edges = edges.flatten().tolist()

        # COLORS
        colors = np.ones((16, 4), dtype=np.float32)

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

        gloo.set_state(clear_color=(0.07843, 0.07843, 0.07843, 1.0), depth_test=True)
        self.show()
        self.update()  #Forces the 1st on_draw
    

    # ========== DRAW ==========
    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        self.program.draw('lines', self.indices)

    # ========== RESIZE ==========
    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)

    #=======KEYPRESS EVENTS========
    def on_key_press(self, event):
        #ROTATE
        if event.text == 'w':
            self.alpha += 15

        elif event.text == 's':
            self.alpha -= 15

        elif event.text == 'a':
            self.beta -= 15
        
        elif event.text == 'd':
            self.beta += 15
        
        elif event.text == 'q':
            self.gamma -= 15
        
        elif event.text == 'e':
            self.gamma += 15

        #ZOOM
        elif event.text == 'i':  # zoom in 
            #self.camera_z += 1.0
            self.camera_z = min(self.camera_z + 1.0, -3.0)  #NO MORE THAN -1
        elif event.text == 'o':  # zoom out
            self.camera_z = max(self.camera_z - 1.0, -33.0)  #NOT LESS THAN -50
        
        #UPDATE IF ROTATION
        if event.text in ('w', 's', 'a', 'd', 'q', 'e'):
            model = np.eye(4, dtype=np.float32)
            model = rotate(self.alpha, (1, 0, 0)) @ model
            model = rotate(self.beta, (0, 1, 0)) @ model
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