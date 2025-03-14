import numpy as np
import matplotlib.pyplot as plt
import ProceImg as pi

MiImagen = np.array(plt.imread("Plaza.jpg")) / 255

plt.figure(1)
plt.subplot(2,2,1)
plt.imshow(MiImagen)
plt.title("Imagen Original")

plt.subplot(2,2,2)
BrilloImg = pi.BrilloImg(MiImagen, 0.5)
plt.imshow(BrilloImg)
plt.title("Ajuste de Brillo")

plt.subplot(2,2,3)
AjusteCanal = pi.AjusteCanal(MiImagen, 100, 0)
plt.imshow(AjusteCanal)

plt.subplot(2,2,4)
Contraste = pi.Contraste(MiImagen, 0.5, 1)
plt.imshow(Contraste)

plt.show()
