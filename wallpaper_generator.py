import os
import random
import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np

class WallpaperGenerator:
    """
    Clase para generar fondos de pantalla de alta definición (1920x1080) 
    a partir de múltiples imágenes con transformaciones aleatorias.
    """
    
    def __init__(self, output_width=1920, output_height=1080):
        """
        Inicializa el generador de fondos de pantalla.
        
        Args:
            output_width: Ancho de la imagen de salida en píxeles
            output_height: Alto de la imagen de salida en píxeles
        """
        self.output_width = output_width
        self.output_height = output_height
        self.base_canvas = Image.new('RGBA', (output_width, output_height), (0, 0, 0, 255))
        
    def load_images(self, input_directory):
        """
        Carga todas las imágenes desde un directorio.
        
        Args:
            input_directory: Ruta al directorio que contiene las imágenes
            
        Returns:
            Lista de objetos PIL.Image
        """
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        images = []
        
        for filename in os.listdir(input_directory):
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                try:
                    img_path = os.path.join(input_directory, filename)
                    img = Image.open(img_path).convert('RGBA')
                    images.append(img)
                    print(f"Cargada imagen: {filename}")
                except Exception as e:
                    print(f"Error al cargar {filename}: {e}")
        
        if not images:
            raise ValueError("No se encontraron imágenes válidas en el directorio especificado")
        
        return images
    
    def apply_random_scale(self, img):
        """
        Aplica un escalado aleatorio a la imagen, manteniendo la proporción.
        
        Args:
            img: Objeto PIL.Image
            
        Returns:
            Imagen escalada
        """
        # Calculamos un factor de escala aleatorio entre 0.2 y 1.5
        scale_factor = random.uniform(0.2, 1.5)
        
        # Calculamos las nuevas dimensiones
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        
        # Nos aseguramos de que al menos una dimensión sea mayor que el 15% del tamaño final
        min_dimension = min(self.output_width, self.output_height) * 0.15
        
        if new_width < min_dimension and new_height < min_dimension:
            scale_factor = min_dimension / min(img.width, img.height)
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            
        # Redimensionamos la imagen manteniendo la proporción
        return img.resize((new_width, new_height), Image.LANCZOS)
    
    def apply_random_rotation(self, img):
        """
        Aplica una rotación aleatoria leve a la imagen.
        
        Args:
            img: Objeto PIL.Image
            
        Returns:
            Imagen rotada
        """
        # Rotación aleatoria entre -15 y 15 grados
        angle = random.uniform(-15, 15)
        # Expandimos para no perder contenido en las esquinas
        return img.rotate(angle, expand=True, resample=Image.BICUBIC)
    
    def apply_random_color_filter(self, img):
        """
        Aplica filtros de color aleatorios a la imagen.
        
        Args:
            img: Objeto PIL.Image
            
        Returns:
            Imagen con filtro aplicado
        """
        # Guardamos el canal alfa si existe
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            rgb_img = Image.merge('RGB', (r, g, b))
        else:
            rgb_img = img.convert('RGB')
            a = None
        
        # Elegimos un filtro aleatorio
        filter_choice = random.choice([
            'original', 'grayscale', 'sepia', 'enhance_color', 
            'enhance_contrast', 'blur', 'sharpen'
        ])
        
        if filter_choice == 'original':
            filtered_img = rgb_img
        elif filter_choice == 'grayscale':
            filtered_img = ImageOps.grayscale(rgb_img).convert('RGB')
        elif filter_choice == 'sepia':
            # Filtro sepia
            sepia_data = np.array(rgb_img)
            sepia_arr = np.array([
                [ 0.393, 0.769, 0.189],
                [ 0.349, 0.686, 0.168],
                [ 0.272, 0.534, 0.131]
            ])
            sepia_data = np.dot(sepia_data, sepia_arr.T)
            sepia_data[sepia_data > 255] = 255
            filtered_img = Image.fromarray(sepia_data.astype(np.uint8))
        elif filter_choice == 'enhance_color':
            enhancer = ImageEnhance.Color(rgb_img)
            filtered_img = enhancer.enhance(random.uniform(0.5, 2.0))
        elif filter_choice == 'enhance_contrast':
            enhancer = ImageEnhance.Contrast(rgb_img)
            filtered_img = enhancer.enhance(random.uniform(0.7, 1.8))
        elif filter_choice == 'blur':
            filtered_img = rgb_img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 2.0)))
        elif filter_choice == 'sharpen':
            filtered_img = rgb_img.filter(ImageFilter.SHARPEN)
        
        # Recomponemos la imagen con el canal alfa original si existía
        if a:
            return Image.merge('RGBA', (*filtered_img.split(), a))
        else:
            return filtered_img
    
    def apply_random_opacity(self, img):
        """
        Aplica una opacidad aleatoria a la imagen.
        
        Args:
            img: Objeto PIL.Image en modo RGBA
            
        Returns:
            Imagen con opacidad aplicada
        """
        # Aseguramos que la imagen esté en modo RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Aplicamos una opacidad aleatoria entre 40% y 100%
        opacity = random.uniform(0.4, 1.0)
        
        # Extraemos los canales
        r, g, b, a = img.split()
        
        # Modificamos el canal alfa
        a = a.point(lambda x: int(x * opacity))
        
        # Reconstruimos la imagen
        return Image.merge('RGBA', (r, g, b, a))
    
    def get_random_position(self, img):
        """
        Calcula una posición aleatoria para colocar la imagen en el lienzo.
        
        Args:
            img: Objeto PIL.Image
            
        Returns:
            Tupla (x, y) con la posición
        """
        max_x = self.output_width - int(img.width * 0.3)  # Permitimos que parte de la imagen quede fuera
        max_y = self.output_height - int(img.height * 0.3)
        
        # Si la imagen es más grande que el lienzo, aún permitimos posicionarla
        if max_x < 0:
            max_x = 0
        if max_y < 0:
            max_y = 0
            
        x = random.randint(-int(img.width * 0.3), max_x)
        y = random.randint(-int(img.height * 0.3), max_y)
        
        return (x, y)
    
    def apply_transformations(self, img):
        """
        Aplica todas las transformaciones aleatorias a una imagen.
        
        Args:
            img: Objeto PIL.Image
            
        Returns:
            Imagen transformada
        """
        img = self.apply_random_scale(img)
        img = self.apply_random_rotation(img)
        img = self.apply_random_color_filter(img)
        img = self.apply_random_opacity(img)
        
        return img
    
    def generate_wallpaper(self, images, num_layers=None):
        """
        Genera un fondo de pantalla a partir de las imágenes proporcionadas.
        
        Args:
            images: Lista de objetos PIL.Image
            num_layers: Número de capas de imágenes a usar (por defecto: aleatorio entre 5 y 15)
            
        Returns:
            Imagen final del fondo de pantalla
        """
        # Si no se especifica número de capas, usamos un número aleatorio
        if num_layers is None:
            num_layers = random.randint(5, min(15, len(images) * 2))
        
        # Creamos un nuevo lienzo
        canvas = self.base_canvas.copy()
        
        # Primero colocamos un fondo aleatorio
        background = random.choice(images).copy()
        background = background.resize((self.output_width, self.output_height), Image.LANCZOS)
        background = self.apply_random_color_filter(background)
        canvas.paste(background, (0, 0), background)
        
        # Añadimos capas aleatorias
        for _ in range(num_layers):
            # Seleccionamos una imagen aleatoria
            img = random.choice(images).copy()
            
            # Aplicamos transformaciones
            transformed_img = self.apply_transformations(img)
            
            # Colocamos la imagen en una posición aleatoria
            position = self.get_random_position(transformed_img)
            
            # Pegamos la imagen en el lienzo
            canvas.alpha_composite(transformed_img, dest=position)
        
        # Convertimos a RGB para guardar como JPG
        return canvas.convert('RGB')
    
    def save_wallpaper(self, wallpaper, output_path, quality=95):
        """
        Guarda el fondo de pantalla generado.
        
        Args:
            wallpaper: Objeto PIL.Image
            output_path: Ruta donde guardar la imagen
            quality: Calidad de la imagen (para formatos con compresión)
        """
        wallpaper.save(output_path, quality=quality)
        print(f"Fondo de pantalla guardado en: {output_path}")


def main():
    """
    Función principal que procesa los argumentos de línea de comandos
    y genera el fondo de pantalla.
    """
    parser = argparse.ArgumentParser(description='Generador de fondos de pantalla a partir de imágenes')
    parser.add_argument('input_dir', help='Directorio que contiene las imágenes de entrada')
    parser.add_argument('--output', '-o', default='wallpaper.jpg', help='Ruta de salida para el fondo de pantalla')
    parser.add_argument('--width', '-w', type=int, default=1920, help='Ancho de la imagen de salida')
    # Cambiamos -h por -ht para evitar el conflicto con la opción de ayuda
    parser.add_argument('--height', '-ht', type=int, default=1080, help='Alto de la imagen de salida')
    parser.add_argument('--layers', '-l', type=int, help='Número de capas de imágenes a usar')
    parser.add_argument('--quality', '-q', type=int, default=95, help='Calidad de la imagen de salida (1-100)')
    
    args = parser.parse_args()
    
    try:
        # Creamos el generador de fondos de pantalla
        generator = WallpaperGenerator(args.width, args.height)
        
        # Cargamos las imágenes
        images = generator.load_images(args.input_dir)
        print(f"Se cargaron {len(images)} imágenes")
        
        # Generamos el fondo de pantalla
        wallpaper = generator.generate_wallpaper(images, args.layers)
        
        # Guardamos el resultado
        generator.save_wallpaper(wallpaper, args.output, args.quality)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())