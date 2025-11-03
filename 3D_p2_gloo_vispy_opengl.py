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
        super().__init__(size=(700, 700), title='3D Octa', keys='interactive')
        
        #VERTICES
        vertices = np.array([
                            [ 0,  +1 / np.sqrt(2),  0],  # V0
                            [ 0, -1 / np.sqrt(2),  0],  # V1
                            [ +1 / np.sqrt(2),  0,  0],  # V2
                            [-1 / np.sqrt(2),  0,  0],  # V3
                            [ 0,  0, +1 / np.sqrt(2)],  # V4
                            [ 0,  0, -1 / np.sqrt(2)]   # V5
                        ], dtype=np.float32)

        #EDGES-INDICES
        edges = np.array([
                        0, 2, 
                        0, 3, 
                        0, 4, 
                        0, 5,
                        1, 2, 
                        1, 3, 
                        1, 4, 
                        1, 5,
                        2, 4, 
                        2, 5,
                        3, 4, 
                        3, 5
                    ], dtype=np.uint32)

        # COLORS
        colors = np.ones((6, 4), dtype=np.float32)

        #DEFINE PROGRAM VARIABLES
        self.program = Program(vertex, fragment)
        self.program['position'] = VertexBuffer(vertices)
        self.program['color'] = VertexBuffer(colors)
        self.indices = IndexBuffer(edges)

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