# Mapa de navegación

* **OpenCV**
  *Proyecto alterno de software de sonorización.*

* **4D**
  *Proyecto de sonorización CCD.*

  * **Diseño Gráfico:**
    Archivos utilizados, modificados y generados para la producción del material de presentación y difusión (`.pdf`).

  * **Hecatonicosacoron** *

  * **Hexacosicoron** *

  * **Hexadecacoro** *

  * **Icositetracoron** *

  * **Pentacoro** *

  * **Teseracto:**
    Carpeta que contiene archivos elementales para generar la figura (igual que `*`).

    * `ext_proyectando_sage_sch.py`
      Obtener la información de las figuras 4-dimensionales desde SageMath, proyectarlas a 3 dimensiones y exportarlas como archivo `.json`.

    * `hypercube_sage.json`
      Coordenadas en 4D, 3D y orden de vértices para generar aristas. Este archivo se utiliza para generar cada figura en TouchDesigner dentro de un **Text DAT** con el nombre `local_data`.

    * `4D_gloo_reading.py`
      Visualización local y programación reactiva utilizando Python Gloo.

  * **Pruebas audios:**
    Limpieza y procesamiento de audios para obtener información.

    * `texto_audacity_limpieza_regulación.txt`
      Instrucciones para limpieza de audios utilizando Audacity.

    * `texto_análisis_voz.txt`
      Descripción de las propiedades de la voz.

    * **analisis_voz:**

      * **audios_limpios**
        Archivos `.wav` limpios de ruido y regulados en volumen.

      * `analizador_voz.py`
        Código en Python que analiza los archivos de audio y regresa los datos de la voz (utilizando la biblioteca **librosa**) en archivos `.csv`.

      * **resultados_csv**
        Tablas con todos los datos numéricos de la voz obtenidos por frame (60 FPS).

  * **Touch Designer:**
    Documentos en formato `.toe`.
