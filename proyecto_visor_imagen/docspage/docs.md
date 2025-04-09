# Documentación Técnica: Visor de Imágenes

## 1. Descripción General del Sistema

### Propósito

El Visor de Imágenes es una aplicación web diseñada para permitir a los usuarios cargar, visualizar y aplicar diversos filtros y transformaciones a imágenes digitales. La aplicación proporciona una interfaz intuitiva para manipular imágenes y visualizar sus propiedades, como histogramas de color.

### Contexto de Uso

Esta aplicación está pensada para ser utilizada en entornos educativos, específicamente en cursos de computación gráfica, procesamiento de imágenes y desarrollo web. Permite a los estudiantes experimentar con diferentes algoritmos de procesamiento de imágenes y ver los resultados en tiempo real.

### Público Objetivo

- Estudiantes de computación gráfica y procesamiento de imágenes
- Profesores que deseen demostrar conceptos de manipulación de imágenes
- Desarrolladores que busquen ejemplos de implementación de algoritmos de procesamiento de imágenes en web
- Usuarios generales interesados en edición básica de imágenes

## 2. Arquitectura del Sistema

### Tecnologías Utilizadas

#### Backend
- **Django 5.2**: Framework web de Python que proporciona la estructura del proyecto
- **Python 3.x**: Lenguaje de programación principal para el backend
- **NumPy**: Biblioteca para operaciones numéricas, utilizada para manipulación de matrices de imágenes
- **Matplotlib**: Biblioteca para generación de gráficos, utilizada para crear histogramas
- **scikit-image**: Biblioteca para algoritmos avanzados de procesamiento de imágenes

#### Frontend
- **HTML5/CSS3**: Para la estructura y estilo de la interfaz de usuario
- **JavaScript (ES6+)**: Para la interactividad del lado del cliente
- **Chart.js**: Biblioteca para visualización de datos, utilizada para mostrar histogramas
- **Tailwind CSS**: Framework CSS para el diseño de la interfaz de usuario

### Comunicación Cliente-Servidor

La aplicación utiliza un enfoque de comunicación cliente-servidor basado en solicitudes HTTP:

1. **Carga de imágenes**: Las imágenes se cargan desde el cliente al servidor mediante solicitudes POST con datos codificados en base64.
2. **Procesamiento de imágenes**: El servidor procesa las imágenes utilizando las bibliotecas de Python y devuelve los resultados al cliente.
3. **API REST**: Se implementa una API REST simple para las operaciones de procesamiento de imágenes:
   - `/process-image/`: Endpoint para aplicar filtros y transformaciones a las imágenes
   - `/generate-histogram/`: Endpoint para generar histogramas de las imágenes

## 3. Carga y Visualización de Imágenes

### Formatos Aceptados

La aplicación acepta los siguientes formatos de imagen:
- JPEG (.jpg, .jpeg)
- PNG (.png)

### Almacenamiento y Procesamiento

- **Almacenamiento**: Las imágenes no se almacenan permanentemente en el servidor. Se procesan en memoria y se devuelven al cliente.
- **Procesamiento**: El procesamiento se realiza principalmente en el servidor utilizando NumPy, Pillow y scikit-image.

### Gestión en el Navegador

- **Carga**: Las imágenes se cargan utilizando la API `FileReader` de JavaScript para convertirlas a formato base64.
- **Visualización**: Las imágenes se muestran en elementos `<img>` con la fuente establecida como una URL de datos (data URL).
- **Compresión**: Antes de enviar imágenes grandes al servidor, se comprimen utilizando un canvas HTML5 para reducir el tamaño de los datos.

```javascript
// Ejemplo de compresión de imagen antes de enviarla al servidor
const compressImage = (dataUrl) => {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = function() {
            // Crear un canvas para comprimir la imagen
            const canvas = document.createElement('canvas');
            
            // Calcular el nuevo tamaño manteniendo la proporción
            let width = img.width;
            let height = img.height;
            const maxSize = 1200; // Tamaño máximo para cualquier dimensión
            
            if (width > height && width > maxSize) {
                height = Math.round(height * (maxSize / width));
                width = maxSize;
            } else if (height > maxSize) {
                width = Math.round(width * (maxSize / height));
                height = maxSize;
            }
            
            // Establecer el tamaño del canvas
            canvas.width = width;
            canvas.height = height;
            
            // Dibujar la imagen en el canvas con el nuevo tamaño
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            
            // Obtener la imagen comprimida como Data URL (calidad 0.85)
            resolve(canvas.toDataURL('image/jpeg', 0.85));
        };
        
        img.onerror = function() {
            reject(new Error('Error al cargar la imagen para compresión'));
        };
        
        img.src = dataUrl;
    });
};
```

## 4. Edición de Imágenes

### Filtros y Transformaciones Disponibles

La aplicación ofrece los siguientes filtros y transformaciones:

1. **Ajustes básicos**:
   - Brillo
   - Contraste
   - Saturación

2. **Filtros de color**:
   - Escala de grises
   - Negativo
   - Canales RGB individuales
   - Canales CMY

3. **Transformaciones**:
   - Rotación
   - Zoom

4. **Efectos especiales**:
   - Binarización (umbralización)
   - Detección de bordes
   - Resaltado de zonas

5. **Operaciones avanzadas**:
   - Fusión de imágenes (con transparencia o marca de agua)
   - Creación de mosaicos con múltiples imágenes (en desarrollo)

### Implementación de Funciones de Edición

Las funciones de edición están implementadas en la clase `ImageFilters` ubicada en `viewer/Filter_Lib/Filters.py`. Esta clase contiene métodos estáticos para cada tipo de filtro o transformación.

### Algoritmos Utilizados

#### Escala de Grises

La conversión a escala de grises se realiza utilizando la fórmula estándar de luminancia:

```python
def grayscale_image(image):
    """
    Convierte una imagen a escala de grises.
    :param image: Imagen en formato numpy array (H, W, C)
    :return: Imagen en escala de grises
    """
    # Usar la fórmula de luminancia: Y = 0.299R + 0.587G + 0.114B
    grayscale = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    return np.stack([grayscale, grayscale, grayscale], axis=-1).astype(np.uint8)
```

#### Binarización

La binarización se implementa utilizando un umbral definido por el usuario:

```python
def binarize_image(image, threshold=128):
    """
    Convierte una imagen a binaria (blanco y negro) según un umbral.
    :param image: Imagen en formato numpy array (H, W, C)
    :param threshold: Umbral para la binarización (0-255)
    :return: Imagen binarizada
    """
    # Convertir a escala de grises primero
    gray = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    
    # Aplicar umbral
    binary = np.where(gray > threshold, 255, 0)
    
    # Si la imagen original tiene 3 canales, convertir de vuelta a RGB
    if len(image.shape) == 3 and image.shape[2] == 3:
        binary = np.stack([binary, binary, binary], axis=-1)
    
    return binary.astype(np.uint8)
```

#### Fusión de Imágenes

La fusión de imágenes se realiza mediante una combinación ponderada de los valores de píxel:

```python
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
```

### Ejes y Matrices de Referencia

Las operaciones de procesamiento de imágenes utilizan matrices NumPy con la siguiente convención:
- Eje 0: Filas (altura)
- Eje 1: Columnas (anchura)
- Eje 2: Canales de color (R, G, B)

Las imágenes se representan como matrices tridimensionales con forma (altura, anchura, canales), donde los canales típicamente son 3 para imágenes RGB.

## 5. Histograma de la Imagen

### Cálculo del Histograma

El histograma se calcula utilizando NumPy y Matplotlib. Para cada canal de color (R, G, B) y para la luminancia, se cuenta la frecuencia de cada valor de intensidad (0-255):

```python
def generate_histogram(image):
    """
    Genera el histograma de la imagen para cada canal de color.
    :param image: Imagen en formato numpy array (H, W, C)
    :return: Diccionario con los datos del histograma
    """
    # Configurar matplotlib para no usar GUI
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
    
    # Calcular histogramas para cada canal
    hist_r = np.histogram(image[:,:,0], bins=256, range=(0, 256))[0]
    hist_g = np.histogram(image[:,:,1], bins=256, range=(0, 256))[0]
    hist_b = np.histogram(image[:,:,2], bins=256, range=(0, 256))[0]
    
    # Calcular luminancia
    luminance = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    hist_l = np.histogram(luminance, bins=256, range=(0, 256))[0]
    
    # Crear figura para el histograma
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Graficar histogramas
    ax.plot(hist_r, color='red', alpha=0.7)
    ax.plot(hist_g, color='green', alpha=0.7)
    ax.plot(hist_b, color='blue', alpha=0.7)
    ax.plot(hist_l, color='white', alpha=0.7)
    
    # Configurar gráfico
    ax.set_xlim(0, 255)
    ax.set_facecolor('#1e293b')  # Fondo oscuro
    fig.patch.set_facecolor('#1e293b')  # Fondo oscuro para toda la figura
    
    # Guardar figura en formato base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Codificar en base64
    histogram_image = base64.b64encode(image_png).decode('utf-8')
    
    # Devolver datos del histograma y la imagen
    return {
        'histogram_data': {
            'red': hist_r.tolist(),
            'green': hist_g.tolist(),
            'blue': hist_b.tolist(),
            'luminance': hist_l.tolist()
        },
        'histogram_image': f'data:image/png;base64,{histogram_image}'
    }
```

### Renderización del Gráfico

El histograma se renderiza en el cliente utilizando Chart.js, una biblioteca de JavaScript para visualización de datos. Los datos del histograma se envían desde el servidor en formato JSON y se utilizan para crear un gráfico de líneas:

```javascript
// Crear nuevo chart
histogramChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array.from({ length: 256 }, (_, i) => i),
        datasets: [
            {
                label: 'Luminance',
                data: data.histogram_data.luminance,
                borderColor: 'white',
                borderWidth: 1,
                pointRadius: 0,
                fill: false
            },
            {
                label: 'Red',
                data: data.histogram_data.red,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                pointRadius: 0,
                fill: false
            },
            {
                label: 'Green',
                data: data.histogram_data.green,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                pointRadius: 0,
                fill: false
            },
            {
                label: 'Blue',
                data: data.histogram_data.blue,
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                pointRadius: 0,
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                display: false
            },
            y: {
                display: false
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
});
```

### Manejo de Canales RGB y Frecuencia

- Cada canal de color (R, G, B) se procesa por separado para generar su propio histograma.
- La frecuencia se calcula contando el número de píxeles que tienen cada valor de intensidad (0-255).
- También se calcula la luminancia (brillo percibido) utilizando la fórmula: Y = 0.299R + 0.587G + 0.114B.

## 6. Interfaz de Usuario

### Herramientas Disponibles

La interfaz de usuario proporciona las siguientes herramientas:

1. **Página de inicio**:
   - Área de arrastrar y soltar para cargar imágenes
   - Botón para seleccionar archivos del sistema

2. **Editor de imágenes**:
   - Panel de filtros y transformaciones
   - Controles específicos para cada filtro (deslizadores, botones, etc.)
   - Histograma en tiempo real
   - Botón de reinicio para volver a la imagen original
   - Botón de descarga para guardar la imagen procesada

### Flujo de Trabajo

El flujo de trabajo típico de la aplicación es el siguiente:

1. **Carga**: El usuario carga una imagen desde su dispositivo.
2. **Previsualización**: La imagen se muestra en el editor junto con su histograma.
3. **Edición**: El usuario selecciona y aplica diferentes filtros y transformaciones.
4. **Guardado**: El usuario descarga la imagen procesada.

## 7. Gestión de Archivos y Recursos Estáticos

### Ubicación de Recursos

- **CSS**: Los archivos CSS se encuentran en `viewer/static/viewer/css/`
- **JavaScript**: Los archivos JavaScript se encuentran en `viewer/static/viewer/js/`
- **Imágenes**: Las imágenes estáticas se encuentran en `viewer/static/viewer/images/`

### Carga de Recursos

Django se encarga de servir los archivos estáticos utilizando la configuración `STATIC_URL` en `settings.py`. En producción, se recomienda utilizar un servidor web como Nginx para servir los archivos estáticos de manera más eficiente.

## 8. Problemas Encontrados y Soluciones

### Límite de Tamaño de Carga

**Problema**: Django limita el tamaño máximo de las solicitudes POST, lo que causaba errores al cargar imágenes grandes.

**Solución**: Se aumentó el límite de tamaño de carga en `settings.py`:

```python
# Aumentar el límite de tamaño de carga para permitir imágenes grandes
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MB
```

Además, se implementó la compresión de imágenes en el cliente antes de enviarlas al servidor.

### Rendimiento con Imágenes Grandes

**Problema**: El procesamiento de imágenes grandes era lento y consumía mucha memoria.

**Solución**: Se implementó un sistema de redimensionamiento automático para limitar el tamaño máximo de las imágenes procesadas, manteniendo una buena calidad visual.

### Compatibilidad con Navegadores

**Problema**: Algunos navegadores más antiguos no admitían todas las funciones de JavaScript utilizadas.

**Solución**: Se utilizaron polyfills y se implementaron comprobaciones de compatibilidad para garantizar que la aplicación funcionara en la mayoría de los navegadores modernos.

## 9. Información Adicional

### Instalación y Configuración

1. Clonar el repositorio:
   ```
   git clone https://github.com/usuario/proyecto_visor_imagen.git
   ```

2. Crear y activar un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

### Futuras Mejoras

- Implementación de más filtros y efectos
- Soporte para edición de imágenes por lotes