from vispy import app, gloo
from vispy.gloo import Program, IndexBuffer
from vispy.util.transforms import perspective, translate, rotate
import numpy as np

# ==================== SHADERS ====================
vertex = """
    attribute vec3 position;
    attribute vec4 color;   
    varying vec4 v_color;
    uniform mat4 u_mvp;
    void main()
    {
        gl_Position = u_mvp * vec4(position, 1.0);
        v_color = color;
    } """
    #"mat4 u_mvp":= Model-View-Projection Matrix (4x4)

fragment = """
    varying vec4 v_color;
    void main()
    {
        gl_FragColor = v_color;
    } """

# ==================== CANVAS ====================
class Canvas(app.Canvas):
    def __init__(self):
        super().__init__(size=(700, 700), title='3D Cube', keys='interactive')
        
        self.program = Program(vertex, fragment)

        #VERTICES
        vertices = np.array([
                            (-0.5, -0.5, -0.5),
                            (+0.5, -0.5, -0.5),
                            (-0.5, +0.5, -0.5),
                            (-0.5, -0.5, +0.5),
                            (+0.5, +0.5, -0.5),
                            (+0.5, -0.5, +0.5),
                            (-0.5, +0.5, +0.5),
                            (+0.5, +0.5, +0.5),
                        ], dtype=np.float32)

        #EDGES
        # Define as 2D for readability, then flatten
        edge_pairs = np.array([
                            (0, 1),  # bottom front edge
                            (0, 2),  # bottom left edge  
                            (0, 3),  # left front edge
                            (1, 4),  # bottom right edge
                            (1, 5),  # right front edge
                            (2, 4),  # top left edge
                            (2, 6),  # left back edge
                            (3, 5),  # right front vertical
                            (3, 6),  # left back vertical
                            (4, 7),  # top right edge
                            (5, 7),  # right back edge
                            (6, 7)   # top back edge
                        ], dtype=np.uint32)

        # Convert to 1D: [0, 1, 0, 2, 0, 3, ...] FOR PROGRAM
        edge_indices = edge_pairs.flatten()

        #COLORS 
        colors = np.array([
                        (1, 1, 1, 1),
                        (1, 1, 1, 1),
                        (1, 1, 1, 1),
                        (1, 1, 1, 1),
                        (1, 1, 1, 1),
                        (1, 1, 1, 1),
                        (1, 1, 1, 1),
                        (1, 1, 1, 1)
                    ], dtype=np.float32)

        #DEFINE PROGRAM VARIABLES   
        self.program['position'] = vertices
        self.program['color'] = colors
        self.indices = IndexBuffer(edge_indices)

        #ROTATION & ZOOM STATE
        self.theta = 0.0
        self.phi = 0.0
            #around Z??? (q/e)
        self.distance = 5.0

        gloo.set_viewport(0, 0, *self.physical_size) 
        gloo.set_clear_color('black')
        self.show()
    
    # ========== MATRIX CREATION ==========
    def _get_mvp(self):
        proj = perspective(45.0, self.size[0] / self.size[1], 0.1, 100.0)
        view = translate((0, 0, -self.distance))

        model = np.eye(4, dtype=np.float32)
        model = rotate(self.theta, (1, 0, 0)) @ model
        model = rotate(self.phi, (0, 1, 0)) @ model

        return proj @ view @ model

    # ========== DRAW ==========
    def on_draw(self, event):
        gloo.clear()
        self.program['u_mvp'] = self._get_mvp()
        self.program.draw('lines', self.indices)

    # ========== RESIZE ==========
    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)
    
    # ========== KEYPRESS ==========
    def on_key_press(self, event):
        key = event.key.name.upper() if hasattr(event.key, "name") else str(event.key).upper()

        if key == 'W':
            self.theta -= 5
        elif key == 'S':
            self.theta += 5
        elif key == 'A':
            self.phi -= 5
        elif key == 'D':
            self.phi += 5
        elif key == 'I':
            self.distance = max(1.0, self.distance - 0.2)
        elif key == 'O':
            self.distance += 0.2

        # redraw only after keypress
        self.update()
    

if __name__ == '__main__':
    c = Canvas()
    app.run()