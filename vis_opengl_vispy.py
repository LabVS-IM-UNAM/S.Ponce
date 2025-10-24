#MODERN OpenGL (Shaders & Buffers) [https://vispy.org/getting_started/modern-gl.html]
import vispy
import  numpy


#CPU buffer:
#numpy.zeros := genera vectores con todas sus componentes en zero (4 VECTORES)
#np.float32 := número racional usando numpy
#posición=(x,y,z) & color=(r,g,b,opacidad)
data = numpy.zeros(4, dtype = [ ("position", np.float32, 2), ("color", np.float32, 4)] )


#Shader:
#uniforms that may be considered as constant values (across all the vertices)
#attributes are meant for changing slightly our vertex
#varying type is used to pass information between the vertex stage (form) and the fragment stage (shade). 
uniform float scale;
attribute vec2 position;
attribute vec4 color;
#output the vertex position on screen:
void main()
{
    gl_Position = vec4(position*scale, 0.0, 1.0);
}

