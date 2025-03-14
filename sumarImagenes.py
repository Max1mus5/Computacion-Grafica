""" suma de 2 imagenes con arrays y numpy 
Computacion Grafica


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2/14/2025   2:41 PM                venv
-a----         2/14/2025   3:21 PM        1300623 image.png
-a----         2/14/2025   3:20 PM        2107167 image1.png
-a----         2/14/2025   2:49 PM            294 numpyExcercise.py
"""
import numpy as numpy
import matplotlib.pyplot as plt

#dejar de un mimso tamaño las imagenes:
image1 = numpy.array(plt.imread('image1.png'))
image = numpy.array(plt.imread('image.png'))

#sumar las imagenes
sumaImagenes = plt.imread('image1.png') + plt.imread('image.png')

#guardar la imagen
plt.imsave('sumaImagenes.png', sumaImagenes)

print("Imagen sumada")
