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
        from matplotlib import transforms
        
        # Creamos una figura y un eje con el tamaño adecuado
        height, width = image.shape[:2]
        fig = plt.figure(figsize=(width/100, height/100), dpi=100)
        ax = fig.add_subplot(111)
        
        # Desactivamos los ejes y establecemos los límites
        ax.set_axis_off()
        ax.set_xlim([0, width])
        ax.set_ylim([height, 0])
        
        # Calculamos el centro de la imagen
        center = (width/2, height/2)
        
        # Aplicamos la transformación de rotación
        tr = transforms.Affine2D().rotate_deg_around(center[0], center[1], angle) + ax.transData
        
        # Mostramos la imagen con la transformación aplicada
        ax.imshow(image, transform=tr)
        
        # Renderizamos la figura
        fig.canvas.draw()
        
        # Obtenemos la imagen del canvas como un array
        rotated_image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        rotated_image = rotated_image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        
        plt.close(fig)
        
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
        result = image.copy()
        if not red:
            result[:, :, 0] = 0
        if not green:
            result[:, :, 1] = 0
        if not blue:
            result[:, :, 2] = 0
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
        result = image.copy()
        # Cian es la ausencia de rojo
        if not cyan:
            result[:, :, 0] = 255
        # Magenta es la ausencia de verde
        if not magenta:
            result[:, :, 1] = 255
        # Amarillo es la ausencia de azul
        if not yellow:
            result[:, :, 2] = 255
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
        height, width = image.shape[:2]
        
        # Calculamos el tamaño de la región para el zoom
        zoom_width = int(width / scale)
        zoom_height = int(height / scale)
        
        # Calculamos las coordenadas de la región
        half_w = zoom_width // 2
        half_h = zoom_height // 2
        
        # Aseguramos que las coordenadas estén dentro de los límites
        x = max(half_w, min(x, width - half_w))
        y = max(half_h, min(y, height - half_h))
        
        # Recortamos la región
        x1, y1 = x - half_w, y - half_h
        x2, y2 = x + half_w, y + half_h
        
        # Aseguramos que no nos salgamos de los límites
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)
        
        # Extraemos la región y la redimensionamos
        region = image[y1:y2, x1:x2]
        from skimage.transform import resize
        zoomed = resize(region, (height, width), mode='reflect', preserve_range=True)
        
        return zoomed.astype(np.uint8)
    
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
    def generate_histogram(image):
        """
        Genera el histograma de la imagen para cada canal de color.
        :param image: Imagen en formato numpy array (H, W, C)
        :return: Figura de matplotlib con el histograma
        """
        if len(image.shape) == 3 and image.shape[2] == 3:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            
            # Histograma de intensidad
            gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
            axes[0, 0].hist(gray.ravel(), bins=256, color='gray', alpha=0.7)
            axes[0, 0].set_title('Intensidad')
            axes[0, 0].set_xlim([0, 256])
            
            # Histograma de canal rojo
            axes[0, 1].hist(image[..., 0].ravel(), bins=256, color='red', alpha=0.7)
            axes[0, 1].set_title('Canal Rojo')
            axes[0, 1].set_xlim([0, 256])
            
            # Histograma de canal verde
            axes[1, 0].hist(image[..., 1].ravel(), bins=256, color='green', alpha=0.7)
            axes[1, 0].set_title('Canal Verde')
            axes[1, 0].set_xlim([0, 256])
            
            # Histograma de canal azul
            axes[1, 1].hist(image[..., 2].ravel(), bins=256, color='blue', alpha=0.7)
            axes[1, 1].set_title('Canal Azul')
            axes[1, 1].set_xlim([0, 256])
            
            plt.tight_layout()
            return fig
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(image.ravel(), bins=256, color='gray', alpha=0.7)
            ax.set_title('Histograma de Intensidad')
            ax.set_xlim([0, 256])
            return fig