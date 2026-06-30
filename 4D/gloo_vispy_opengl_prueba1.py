from vispy import app, gloo
from vispy.gloo import Program

#SHADERS:
vertex = """
    uniform float theta;
    attribute vec4 color;
    attribute vec2 position;
    varying vec4 v_color;
    void main()
    {
        float ct = cos(theta);
        float st = sin(theta);
        float x = 0.75* (position.x*ct - position.y*st);
        float y = 0.75* (position.x*st + position.y*ct);
        gl_Position = vec4(x, y, 0.0, 1.0);
        v_color = color;
    } """

fragment = """
    varying vec4 v_color;
    void main()
    {
        gl_FragColor = v_color;
    } """

class Canvas(app.Canvas):
#Create a subclass of the Canvas object to hold on to all of the objects we create.
    def __init__(self):
        super().__init__(size=(512, 512), title='Colored quad',
                         keys='interactive')

        # Build program (defining an OpenGL Program which expects two shaders, simplest case)
        self.program = Program(vertex, fragment, count=4)

        # Set uniforms and attributes (used by the shaders)
        self.program['color'] = [(1, 0, 0, 1), (0, 1, 0, 1),
                                 (0, 0, 1, 1), (1, 1, 0, 1)]
        self.program['position'] = [(-1, -1), (-1, +1),
                                    (+1, -1), (+1, +1)]

        self.program['theta'] = 0.0
        #angle? unifrom

        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.set_clear_color('white')

        self.timer = app.Timer('auto', self.on_timer)
        #'auto' fires timer as quickly it can. We’ve connected this timer to a new on_timer method which will be executed whenever the timer is triggered.
        self.clock = 0
        self.timer.start()

        self.show()
        #.show() call inside the __init__ method so the Canvas is shown as soon as it is created.

    def on_draw(self, event):
        gloo.clear() #white
        self.program.draw('triangle_strip')

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)
    #Event for when the user resizes the Graphical User Interface window we can update the size of the OpenGL canvas (viewport).

    def on_timer(self, event):
        self.clock += 0.001 * 1000.0 / 60.
        #updating our special clock counter variable
        self.program['theta'] = self.clock
        self.update()
        #tells the Canvas to start redrawing itself.

    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()

if __name__ == '__main__':
    c = Canvas()
    app.run()
