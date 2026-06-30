# Invoca SageMath
from sage.all import *

# Crear el objeto 4D
P = polytopes.simplex(4)

# Generar la proyección 3D
plot = P.plot()


# Mostrar con Jmol (ventana interactiva)
plot.show(viewer='jmol')

#Descargué SageMath p   ara correr localmente
#Se requiere Ubuntu Server para instalar SageMath
#Abres Ubuntu Server y de ahí cambias el directorio Y corres sage con "conda activate sage"
#Windows X Server para la visualizacion (VcSxrv)
#NO CORRE LA VISUALIZACION (descargado el tachyon)
#Cambiamos de tachyon a Jmol (JAVA), buscamos imagenes interactivas NO el raytracing

#CAMBIO DEPLANES///SAGE NO ES VIABLE PARA CAMBIOS A TIEMPO REAL
