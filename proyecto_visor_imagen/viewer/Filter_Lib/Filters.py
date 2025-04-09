import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

class ImageFilters:
    @staticmethod
    def adjust_brightness(image, factor):
        """
        Ajusta el brillo de la imagen.
        :param image: Imagen en formato numpy array (H, W, C)
        :param factor: Factor de brillo (>1 para aumentar, <1 para disminuir)
        :return: Imagen con brillo ajustado
        """
        # Aseguramos que la imagen esté en formato float para evitar problemas de desbordamiento
        img_float = image.astype(np.float32)
        adjusted = img_float * factor
        # Recortamos los valores para que estén en el rango válido [0, 255]
        return np.clip(adjusted, 0, 255).astype(np.uint8)
    
    @staticmethod
    def adjust_contrast(image, factor):
        """
        Ajusta el contraste de la imagen.
        :param image: Imagen en formato numpy array (H, W, C)
        :param factor: Factor de contraste (>1 para aumentar, <1 para disminuir)
        :return: Imagen con contraste ajustado
        """
        img_float = image.astype(np.float32)
        # Aplicamos la fórmula: (img - 128) * factor + 128
        mean = 128
        adjusted = (img_float - mean) * factor + mean
        return np.clip(adjusted, 0, 255).astype(np.uint8)
    
    @staticmethod
    def rotate_image(image, angle):
        """
        Rota la imagen el ángulo especificado.
        :param image: Imagen en formato numpy array (H, W, C)
        :param angle: Ángulo de rotación en grados (0-360)
        :return: Imagen rotada
        """
        # Usamos scikit-image para rotar la imagen en lugar de matplotlib
        # Esto evita problemas con el hilo principal y tkinter
        from skimage.transform import rotate
        
        # Aseguramos que la imagen esté en formato float para evitar pérdida de datos
        img_float = image.astype(np.float32) / 255.0
        
        # Rotamos la imagen
        # preserve_range=True mantiene los valores en el rango original
        # resize=True ajusta el tamaño del lienzo para que no se recorte la imagen
        rotated = rotate(img_float, angle, resize=True, mode='constant', 
                         cval=0, clip=False, preserve_range=False)
        
        # Convertimos de vuelta a uint8
        rotated_image = (rotated * 255).astype(np.uint8)
        
        return rotated_image
    
    @staticmethod
    def highlight_zones(image, mode='light'):
        """
        Resalta las zonas claras u oscuras de la imagen.
        :param image: Imagen en formato numpy array (H, W, C)
        :param mode: 'light' para resaltar zonas claras, 'dark' para zonas oscuras
        :return: Imagen con zonas resaltadas
        """
        if mode == 'light':
            # Resaltar zonas claras: potenciamos los valores altos
            mask = image > 128
            result = image.copy()
            result[mask] = np.clip(result[mask] * 1.5, 0, 255)
            return result
        elif mode == 'dark':
            # Resaltar zonas oscuras: aumentamos el valor de los píxeles oscuros
            mask = image < 128
            result = image.copy()
            result[mask] = np.clip(result[mask] * 2, 0, 255)
            return result
        else:
            return image
    
    @staticmethod
    def apply_rgb_filter(image, red=True, green=True, blue=True):
        """
        Aplica filtro RGB activando o desactivando canales.
        :param image: Imagen en formato numpy array (H, W, C)
        :param red: Booleano que indica si el canal rojo está activado
        :param green: Booleano que indica si el canal verde está activado
        :param blue: Booleano que indica si el canal azul está activado
        :return: Imagen con filtro RGB aplicado
        """
        # Verificar que la imagen tenga 3 canales
        if len(image.shape) != 3 or image.shape[2] < 3:
            # Si no es una imagen RGB, devolver la imagen original
            return image
            
        # Crear una copia para no modificar la original
        result = image.copy()
        
        # Convertir los parámetros a booleanos explícitos
        red_active = bool(red)
        green_active = bool(green)
        blue_active = bool(blue)
        
        # Aplicar filtros de canal
        try:
            if not red_active:
                result[:, :, 0] = 0
            if not green_active:
                result[:, :, 1] = 0
            if not blue_active:
                result[:, :, 2] = 0
        except Exception as e:
            # En caso de error, registrar y devolver la imagen original
            print(f"Error al aplicar filtro RGB: {e}")
            return image
            
        return result
    
    @staticmethod
    def apply_cmy_filter(image, cyan=True, magenta=True, yellow=True):
        """
        Aplica filtro CMY activando o desactivando canales.
        :param image: Imagen en formato numpy array (H, W, C)
        :param cyan: Booleano que indica si el canal cian está activado
        :param magenta: Booleano que indica si el canal magenta está activado
        :param yellow: Booleano que indica si el canal amarillo está activado
        :return: Imagen con filtro CMY aplicado
        """
        # Verificar que la imagen tenga 3 canales
        if len(image.shape) != 3 or image.shape[2] < 3:
            # Si no es una imagen RGB, devolver la imagen original
            return image
            
        # Crear una copia para no modificar la original
        result = image.copy()
        
        # Convertir los parámetros a booleanos explícitos
        cyan_active = bool(cyan)
        magenta_active = bool(magenta)
        yellow_active = bool(yellow)
        
        try:
            # Cian es la ausencia de rojo
            if not cyan_active:
                result[:, :, 0] = 255
            # Magenta es la ausencia de verde
            if not magenta_active:
                result[:, :, 1] = 255
            # Amarillo es la ausencia de azul
            if not yellow_active:
                result[:, :, 2] = 255
        except Exception as e:
            # En caso de error, registrar y devolver la imagen original
            print(f"Error al aplicar filtro CMY: {e}")
            return image
            
        return result
    
    @staticmethod
    def negative_image(image):
        """
        Invierte los colores de la imagen para obtener el negativo.
        :param image: Imagen en formato numpy array (H, W, C)
        :return: Negativo de la imagen
        """
        return 255 - image
    
    @staticmethod
    def zoom_image(image, x, y, scale):
        """
        Aplica zoom a una región de la imagen.
        :param image: Imagen en formato numpy array (H, W, C)
        :param x: Coordenada x del centro de la región
        :param y: Coordenada y del centro de la región
        :param scale: Factor de escala del zoom (>1 para acercar, <1 para alejar)
        :return: Imagen con zoom aplicado
        """
        try:
            # Verificar que la imagen sea válida
            if image is None or len(image.shape) < 2:
                print("Imagen inválida para aplicar zoom")
                return image
                
            # Obtener dimensiones
            height, width = image.shape[:2]
            
            # Convertir coordenadas a enteros
            x = int(x)
            y = int(y)
            
            # Asegurar que scale sea positivo
            scale = max(0.1, float(scale))
            
            # Calculamos el tamaño de la región para el zoom
            zoom_width = max(1, int(width / scale))
            zoom_height = max(1, int(height / scale))
            
            # Calculamos las coordenadas de la región
            half_w = zoom_width // 2
            half_h = zoom_height // 2
            
            # Aseguramos que las coordenadas estén dentro de los límites
            x = max(half_w, min(x, width - half_w))
            y = max(half_h, min(y, height - half_h))
            
            # Recortamos la región
            x1, y1 = max(0, x - half_w), max(0, y - half_h)
            x2, y2 = min(width, x + half_w), min(height, y + half_h)
            
            # Verificar que la región sea válida
            if x2 <= x1 or y2 <= y1:
                print("Región de zoom inválida")
                return image
                
            # Extraemos la región
            region = image[y1:y2, x1:x2]
            
            # Redimensionamos usando scikit-image
            from skimage.transform import resize
            zoomed = resize(
                region, 
                (height, width), 
                mode='edge',  # Usar 'edge' en lugar de 'reflect' para evitar artefactos
                anti_aliasing=True,  # Aplicar anti-aliasing para mejor calidad
                preserve_range=True  # Mantener el rango de valores
            )
            
            return zoomed.astype(np.uint8)
            
        except Exception as e:
            print(f"Error al aplicar zoom: {e}")
            return image
    
    @staticmethod
    def binarize_image(image, threshold=128):
        """
        Convierte la imagen a blanco y negro usando un umbral.
        :param image: Imagen en formato numpy array (H, W, C)
        :param threshold: Umbral de binarización (0-255)
        :return: Imagen binarizada
        """
        # Convertimos a escala de grises si la imagen es a color
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
        else:
            gray = image.copy()
        
        # Aplicamos umbral
        binary = np.zeros_like(gray)
        binary[gray > threshold] = 255
        
        # Si la imagen original era a color, convertimos el resultado a 3 canales
        if len(image.shape) == 3 and image.shape[2] == 3:
            binary = np.stack([binary, binary, binary], axis=-1)
        
        return binary.astype(np.uint8)
    
    @staticmethod
    def merge_images(image1, image2, alpha=0.5):
        """
        Fusiona dos imágenes con un factor de transparencia.
        :param image1: Primera imagen en formato numpy array (H, W, C)
        :param image2: Segunda imagen en formato numpy array (H, W, C)
        :param alpha: Factor de transparencia (0-1)
        :return: Imagen fusionada
        """
        # Redimensionamos la segunda imagen al tamaño de la primera si es necesario
        if image1.shape[:2] != image2.shape[:2]:
            from skimage.transform import resize
            image2 = resize(image2, image1.shape[:2], mode='reflect', preserve_range=True).astype(np.uint8)
        
        # Fusionamos las imágenes: image1 * (1-alpha) + image2 * alpha
        merged = image1.astype(np.float32) * (1 - alpha) + image2.astype(np.float32) * alpha
        
        return np.clip(merged, 0, 255).astype(np.uint8)
    
    @staticmethod
    def watermark_merge_images(image1, image2):
        """
        Fusiona dos imágenes de diferentes tamaños usando el método de marca de agua.
        :param image1: Primera imagen en formato numpy array (H, W, C)
        :param image2: Segunda imagen en formato numpy array (H, W, C)
        :return: Imagen fusionada
        """
        try:
            # Normalizar valores a rango [0, 1]
            img1 = image1.astype(np.float32) / 255
            img2 = image2.astype(np.float32) / 255
            
            # Determinar cuál imagen es más grande
            tamano1 = img1.shape[0] * img1.shape[1]
            tamano2 = img2.shape[0] * img2.shape[1]
            
            # Identificar la imagen más grande y la más pequeña
            if tamano1 >= tamano2:
                img_grande = img1.copy()
                img_pequena = img2.copy()
            else:
                img_grande = img2.copy()
                img_pequena = img1.copy()
            
            # Cálculo de alto y ancho de dimensiones finales
            altura_final = max(img_grande.shape[0], img_pequena.shape[0])
            anchura_final = max(img_grande.shape[1], img_pequena.shape[1])
            
            # Matriz nueva para añadir imágenes
            resultado = np.zeros((altura_final, anchura_final, 3))
            
            # Posición central para la imagen más pequeña
            centro_altura = altura_final // 2
            centro_anchura = anchura_final // 2
            
            # Insertar imagen más pequeña en el centro
            inicio_altura = centro_altura - img_pequena.shape[0] // 2
            inicio_anchura = centro_anchura - img_pequena.shape[1] // 2
            
            resultado[inicio_altura:inicio_altura + img_pequena.shape[0],
                     inicio_anchura:inicio_anchura + img_pequena.shape[1]] += img_pequena
            
            # Aplicar efecto de marca de agua
            img_marca_agua = img_grande * 1
            
            # Insertar la imagen con marca de agua
            resultado[:img_marca_agua.shape[0], :img_marca_agua.shape[1]] += img_marca_agua
            
            # Normalizar valores
            resultado = np.clip(resultado, 0, 1)
            
            # Convertir de vuelta a rango [0, 255]
            return (resultado * 255).astype(np.uint8)
            
        except Exception as e:
            print(f"Error en watermark_merge_images: {e}")
            # En caso de error, devolver la primera imagen
            return image1
    
    @staticmethod
    def generate_histogram(image):
        """
        Genera el histograma de la imagen para cada canal de color.
        :param image: Imagen en formato numpy array (H, W, C)
        :return: Figura de matplotlib con el histograma
        """
        # Configurar matplotlib para no usar GUI
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        # Crear figura sin usar tkinter
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Crear figura
            fig = plt.figure(figsize=(12, 10))
            
            # Crear subplots manualmente
            ax1 = fig.add_subplot(2, 2, 1)
            ax2 = fig.add_subplot(2, 2, 2)
            ax3 = fig.add_subplot(2, 2, 3)
            ax4 = fig.add_subplot(2, 2, 4)
            
            # Histograma de intensidad
            gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
            ax1.hist(gray.ravel(), bins=256, color='gray', alpha=0.7)
            ax1.set_title('Intensidad')
            ax1.set_xlim([0, 256])
            
            # Histograma de canal rojo
            ax2.hist(image[..., 0].ravel(), bins=256, color='red', alpha=0.7)
            ax2.set_title('Canal Rojo')
            ax2.set_xlim([0, 256])
            
            # Histograma de canal verde
            ax3.hist(image[..., 1].ravel(), bins=256, color='green', alpha=0.7)
            ax3.set_title('Canal Verde')
            ax3.set_xlim([0, 256])
            
            # Histograma de canal azul
            ax4.hist(image[..., 2].ravel(), bins=256, color='blue', alpha=0.7)
            ax4.set_title('Canal Azul')
            ax4.set_xlim([0, 256])
            
            plt.tight_layout()
        else:
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(1, 1, 1)
            ax.hist(image.ravel(), bins=256, color='gray', alpha=0.7)
            ax.set_title('Histograma de Intensidad')
            ax.set_xlim([0, 256])
        
        # Guardar la figura en un buffer de memoria
        from io import BytesIO
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)  # Cerrar la figura para liberar memoria
        
        # Crear una nueva figura con la imagen guardada
        buf.seek(0)
        img = plt.imread(buf)
        new_fig = plt.figure(figsize=(12, 10))
        ax = new_fig.add_subplot(1, 1, 1)
        ax.imshow(img)
        ax.axis('off')
        
        return new_fig