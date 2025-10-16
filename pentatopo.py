from sage.all import *

P = polytopes.simplex(4)
plot = P.plot()
plot.show(viewer='tachyon')

#Descargué SageMath para correr localmente
#Se requiere Ubuntu Server para instalar SageMath
#Abres Ubuntu Server y de ahí cambias el directorio Y corres sage con "conda activate sage"
#Windows X Server para la visualizacion (VcSxrv)
#NO CORRE LA VISUALIZACION (descargado el tachyon)
#
