import numpy as np
import matplotlib.pyplot as plt

def crear_mosaico(imagenes, color_marco='red', tamano_marco=9):
    """
    Crea un mosaico de 4 i
   
    Args:
        imagenes: Lista de 4 rutas a imágenes,
        color_marco: Color del marco ('black'', etc.),
        tamaño de marco
   
    Returns:
        str: Ruta donde se guardó la imagen resultante
    """
    # Validar número de imágenes
    if len(imagenes) != 4:
        raise ValueError("Se requieren exactamente 4 imágenes")
    
    # Cargar y redimensionar las imágenes usando matplotlib
    imagenes_cargadas = []
    for imageningresada in imagenes:
        img = plt.imread(imageningresada)
        #redimensionar imagen una por una 
        if img.ndim == 3:  # Imagen a color
            img_resized = np.zeros((300, 300, img.shape[2]))
        else:  # Imagen en escala de grises
            img_resized = np.zeros((300, 300))
        
        # aplicacion de interpolación simple
        x_ratio = img.shape[1] / 300
        y_ratio = img.shape[0] / 300
        
        for y in range(300):
            for x in range(300):
                px = int(x * x_ratio)
                py = int(y * y_ratio)
                px = min(px, img.shape[1] - 1)
                py = min(py, img.shape[0] - 1)
                img_resized[y, x] = img[py, px]
        
        imagenes_cargadas.append(img_resized)
    
    # calulo de este vlor = 2 imagenes respecto a x + el tamaño del marco
    tamano_total = 300 * 2 + tamano_marco * 3  # 3 marcos en total (bordes y centro)
    
    # Crear el lienzo con el color del marco
    mosaico = np.zeros((tamano_total, tamano_total, 3))
    
    # Convertir nombre de color a RGB usando matplotlib
    rgb_color = plt.cm.colors.to_rgb(color_marco)
    
    # Rellenar todo el lienzo con el color del marco
    mosaico[:, :, 0] = rgb_color[0]
    mosaico[:, :, 1] = rgb_color[1]
    mosaico[:, :, 2] = rgb_color[2]
    
    # Insertar imgs en la matriz
    for i in range(4):
        fila = i // 2
        col = i % 2
        pos_x = col * (300 + tamano_marco) + tamano_marco
        pos_y = fila * (300 + tamano_marco) + tamano_marco
        
        img = imagenes_cargadas[i]
        
        #imagen de 3 canales
        if img.ndim == 2:  # Si es escala de grises
            img_rgb = np.stack([img, img, img], axis=2)
        else:
            img_rgb = img
            
        # Normalizar valores si es necesario
        if img_rgb.max() > 1.0:
            img_rgb = img_rgb / 255.0
            
        # posicionar la imagen en el mosaico
        mosaico[pos_y:pos_y+300, pos_x:pos_x+300] = img_rgb
    
    #guardar 
    nombre_archivo = 'mosaico.jpg'
    plt.imsave(nombre_archivo, mosaico)
    
    # Mostrar el mosaico (opcional)
    plt.figure(figsize=(10, 10))
    plt.imshow(mosaico)
    plt.axis('off')
    plt.tight_layout()
    
    return nombre_archivo

rutas_imagenes = ['./img1.jpg', './img2.jpg', './img1.jpg', './img2.jpg']
resultado = crear_mosaico(rutas_imagenes, color_marco='white')
print(f'Mosaico guardado como: {resultado}')