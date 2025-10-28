#The gloo layer of VisPy is the lowest level interface and is the closest thing to OpenGL that VisPy provides. This also means it is the most complicated. While OpenGL is complicated, gloo tries to provide a simple to use object-oriented layer on top of that.

#Two things that are common across all of the VisPy interfaces (gloo included): APPLICATION instance & CANVAS (or subclass instance)

#Application object wraps the high-level event loop logic of the VisPy backend you use (PyQt6). In most cases you don’t have to know too much about this, but you do need to create and run the application to be able to process events and run properly.

#Canvas object will be your main way of using and controlling VisPy; you’ll either be using the Canvas, SceneCanvas, or creating Figure objects. They will almost never be used in the same application (although are built on each other). To help keep your code easy to understand it is best not to mix these in the same application.

import sys
#To access system-specific variables and functions, allowing interaction with the Python interpreter and the operating system.
from vispy import app, gloo

canvas = app.Canvas(keys='interactive')
#Object representing the overall space where our visualization will take place.

@canvas.connect
#decorator method to attach this method to any “draw” events coming from the canvas. When using this technique the function must be named on_<event>
def on_draw(event):
#function telling OpenGL to fill the Canvas with a specific RGBA
    #gloo.set_clear_color((0.2, 0.4, 0.6, 1.0)) #Azul Claro (Ejemplo)
    gloo.set_clear_color((1, 0, 0.517, 1.0)) #Rosa Mexicano (255,0,132,0.7)
    gloo.clear()


canvas.show()
#display the Canvas object on the screen, talking to the underlying GUI backend (PyQt6) to construct a native GUI “widget” with our OpenGL visualization inside.

if __name__ == '__main__' and sys.flags.interactive == 0:
#The if statement here is a common occurrence in VisPy example scripts so that the Application is only started when the code is run as a script (instead of imported). This also helps with more advanced usage where we run this script in an interactive Python interpreter.
    app.run()
    #running a default VisPy Application object