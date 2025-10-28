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
varying vec4 v_color;
#output the vertex position on screen:
#vertex shader
void main()
{
    gl_Position = vec4(position*scale, 0.0, 1.0);
    v_color = color;
}

#fragment shader
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}

#What is the color of each individual fragment? The answer is the interpolation of all vertices color. This interpolation is made using distance of the fragment to each individual vertex.


#PROJECTION MATRIX
#We need first to define what do we want to view, that is, we need to define a viewing volume such that any object within the volume (even partially) will be rendered while objects outside won’t.

#We’ll only use the perspective projection (distant objects appear smaller) [2 OPTIONS] and the orthographic projection which is a parallel projection (distant objects have the same size as closer ones) 

#We’ll use a view matrix that will map the the world space to camera space

#Model matrix will map the object’s local coordinate space into world space. For example, this will be useful for rotating an object around its center [¡POLITOPOS R4!]


#SUMMARY:
#Model matrix maps from an object’s local coordinate space into world space

#View matrix maps from world space to camera space

#Projection matrix maps from camera to screen space

#When reading documentation, if you’ve found other resources, make sure they deal with the dynamic rendering pipeline and not the fixed one.