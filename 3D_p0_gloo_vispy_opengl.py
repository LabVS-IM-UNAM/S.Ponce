from vispy import app, gloo
from vispy.gloo import Program

#SHADERS:
vertex = """
    attribute vec3 position;
    attribute vec4 color;
    void main()
    {
        gl_Position = vec4(position, 1.0);
    } """

fragment = """
    attribute vec4 u_color;
    void main()
    {
        gl_FragColor = u_color;
    } """

class Canvas(app.Canvas):
    def __init__(self):
        super().__init__(size=(700, 700), title='3D Cube', keys='interactive')
        
        self.program = Program(vertex, fragment, count=8)

        self.program['position'] = [
                                    (-0.5, -0.5, -0.5),
                                    (+0.5, -0.5, -0.5),
                                    (-0.5, +0.5, -0.5),
                                    (-0.5, -0.5, +0.5),
                                    (+0.5, +0.5, -0.5),
                                    (+0.5, -0.5, +0.5),
                                    (-0.5, +0.5, +0.5),
                                    (+0.5, +0.5, +0.5),
                                    ]
        
        self.program['color'] = [
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1),
                                    (1, 1, 1, 1)
                                    ]

        gloo.set_viewport(0, 0, *self.physical_size)
            
        gloo.set_clear_color('black')

        self.show()

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('line')

if __name__ == '__main__':
    c = Canvas()
    app.run()