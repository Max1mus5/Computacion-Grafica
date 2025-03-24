import numpy as np
import matplotlib.pyplot as plt

def fusionar_imagenes(ruta_img1, ruta_img2):
    """
    Fusiona dos imágenes de diferentes tamaños usando el método de marca de agua.
    
    argumentos:
        1)ruta de imagen 1 
        2)ruta ruta de imagen 2
    
    retoro
        imagen fusionada
    """
    # Leer imágenes y normalizar valores
    img1 = plt.imread(ruta_img1) / 255
    img2 = plt.imread(ruta_img2) / 255
    
    #  imagen es mas grande
    tamano1 = img1.shape[0] * img1.shape[1]
    tamano2 = img2.shape[0]* img2.shape[1]
    
    #Identificar la imagen mas grande y la mas pequeña
    if tamano1 >= tamano2:
        img_grande = img1.copy()
        img_pequeña = img2.copy()
    else:
        img_grande = img2.copy()
        img_pequeña = img1.copy()
    
    # calculo de alto y ancho de dimensiones
    altura_final = max(img_grande.shape[0], img_pequeña.shape[0])
    anchura_final = max(img_grande.shape[1], img_pequeña.shape[1])
    
    #martiz nueva para añair imagenes
    resultado = np.zeros((altura_final, anchura_final, 3))
    
    # posocion central para la imagen mas pequeña
    centro_altura = altura_final // 2
    centro_anchura = anchura_final // 2
    
    # Isertar imagen mas pequeña en el centro
    inicio_altura = centro_altura - img_pequeña.shape[0] // 2
    inicio_anchura = centro_anchura - img_pequeña.shape[1] // 2
    #nsertar imagen mas pequeña en el centro
    resultado[inicio_altura:inicio_altura + img_pequeña.shape[0],
             inicio_anchura:inicio_anchura + img_pequeña.shape[1]] += img_pequeña
    
    # Aplicar efecto de marca de agua 
    img_marca_agua = img_grande * 1
    
    # Insertar la imagen con marca de agua
    resultado[:img_marca_agua.shape[0], :img_marca_agua.shape[1]] += img_marca_agua
    
    # mormalizar valores
    resultado = np.clip(resultado, 0, 1)
    
    # Guardar la imagen resultante
    nombre_salida = 'fusion_resultado.jpg'
    plt.imsave(nombre_salida, resultado)
    return nombre_salida

# Ejemplo de uso
resultado = fusionar_imagenes('./img1.jpg', './img2.jpg')
#rint('Imagen guardada como: {resultado}')