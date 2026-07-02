MAPA DE NAVEGACIÓN

+ [OpenCV] : Proyecto alterno software sonorización
+ [4D] : Proyecto de sonorización CCD
  ++ [Diseño Gráfico] : Archivos utilizados, modificados y generados para la producción del material (.pdf) de presentación y difusión.
  ++ [Hecatonicosacoron] *
  ++ [Hexacosicoron] *
  ++ [Hexadecacoro] *
  ++ [Icositetracoron] *
  ++ [Pentacoro] *
  ++ [Teseracto] : Carpeta que contiene archivos elementales para generar la figura (igual que *)
    +++ {ext_proyectando_sage_sch.py} : Obtener la información de las figuras 4-dimensionales desde SageMath, las proyecta a 3 dimensiones y las exporta como archivo json.
    +++ {hypercube_sage.json} : Coordenadas en 4D, 3D y orden de vértices para generar aristas. Este archivo se utliza para generar cada figura en TouchDesigner dentro de un "Text DAT" bajo el nombre "local_data".
    +++ {4D_gloo_reading.py} : Visualización local y programación reactiva utilizando python gloo.
  ++ [Pruebas audios] : Limpieza y procesamiento de audios para obtener información.
    +++ {texto_audacity_limpieza_regulación.txt} :  Instrucciones para limpieza de audios utilizando Audacity.
    +++ {texto_análisis_voz.txt} : Descripición de las propiedades de la voz.
    +++ [analisis_voz]
      ++++ [audios_limpios] : Archivos .wav limpios de ruido y regulados en volumen.
      ++++ {analizador_voz.py} : Código de python que analiza los archivos de audio y regresa los datos de su voz (utilizando la biblioteca librosa) en archivos .csv.
      ++++ [resultados_csv] : Tablas con todos los datos numéricos de la voz obtenidos por frame (60fps).
  ++ [Touch Designer] : Documentos de formato .toe
