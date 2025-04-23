# Graficador Pygame - Computación Gráfica

Este proyecto implementa un graficador utilizando algoritmos de dibujo propios, sin depender de las funciones prediseñadas de Pygame. La aplicación permite dibujar diferentes formas geométricas y curvas utilizando algoritmos como DDA, Bresenham, y Bézier.

## Características

- **Algoritmos de dibujo implementados:**
  - Líneas: DDA y Bresenham
  - Circunferencias: Bresenham para círculos
  - Curvas: Bézier cúbica (4 puntos de control)
  - Figuras: triángulos, rectángulos, polígonos, elipses
  - Trazo libre: dibujo a mano alzada siguiendo el movimiento del mouse

- **Interfaz gráfica:**
  - Ventana principal con lienzo de dibujo
  - Sistema de selección de figuras (teclado o botones)
  - Colores específicos para cada tipo de figura
  - Opciones para limpiar pantalla y reiniciar

- **Estructura del programa:**
  - División en módulos: lógica de dibujo (PygameDrawLibrary.py) e interfaz
  - Uso apropiado de estructuras de datos
  - Código documentado y organizado

## Requisitos

- Python 3.8 o superior
- Django 3.2 o superior
- Pygame 2.0 o superior
- Pillow

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/Max1mus5/Computacion-Grafica.git
   cd Computacion-Grafica
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r GraphicatorProjectDjango/requirements.txt
   ```

3. Ejecuta el servidor Django:
   ```
   cd GraphicatorProjectDjango
   python manage.py runserver
   ```

4. Abre tu navegador y visita `http://localhost:8000`

## Uso

- **Trazo Libre (F)**: Dibuja a mano alzada siguiendo el movimiento del mouse
- **Línea (L)**: Dibuja una línea recta entre dos puntos
- **Círculo (C)**: Dibuja un círculo con centro y radio definidos
- **Curva Bézier (B)**: Dibuja una curva Bézier cúbica con 4 puntos de control
- **Rectángulo (R)**: Dibuja un rectángulo definido por dos esquinas opuestas
- **Triángulo (T)**: Dibuja un triángulo definido por tres puntos
- **Polígono (P)**: Dibuja un polígono definido por múltiples puntos (doble clic para cerrar)
- **Elipse (E)**: Dibuja una elipse con centro y radios definidos

## Estructura del Proyecto

- `GraphicatorProjectDjango/`: Proyecto Django principal
  - `GraphicatorProject/`: Configuración del proyecto Django
    - `Lib/`: Bibliotecas propias
      - `PygameDrawLibrary.py`: Implementación de algoritmos de dibujo
  - `static/`: Archivos estáticos (CSS, JavaScript)
  - `templates/`: Plantillas HTML

## Implementación de Algoritmos

### Algoritmo DDA para Líneas

El algoritmo DDA (Digital Differential Analyzer) es un algoritmo simple para dibujar líneas. Calcula los puntos intermedios entre dos puntos dados utilizando incrementos constantes.

### Algoritmo de Bresenham para Líneas

El algoritmo de Bresenham para líneas es más eficiente que DDA y utiliza solo operaciones enteras, lo que lo hace más rápido.

### Algoritmo de Bresenham para Círculos

Este algoritmo dibuja círculos utilizando simetría de octantes para reducir los cálculos necesarios.

### Algoritmo para Curvas de Bézier

Las curvas de Bézier se implementan utilizando la fórmula paramétrica con 4 puntos de control.

## Rendimiento y Optimización

### Causas del Retraso (Lag) al Dibujar

Cuando se dibuja intensivamente en el canvas, especialmente con la herramienta de trazo libre, puede experimentarse un retraso (lag) que aumenta a medida que se añaden más elementos. Esto se debe a varios factores:

1. **Acumulación de formas en memoria**: 
   - Cada trazo se almacena en el array `state.shapes`
   - Cada forma contiene todos sus puntos, color, grosor y algoritmo usado
   - Para el trazo libre, se guardan TODOS los puntos por los que pasa el cursor

2. **Redibujo completo del canvas**: 
   - Cada vez que se mueve el mouse o se añade un nuevo punto, la función `redrawCanvas()` se ejecuta
   - Esta función borra todo el canvas y vuelve a dibujar TODAS las formas desde cero
   - Cuantas más formas haya dibujadas, más tiempo toma este proceso

3. **Algoritmo DDA para trazo libre**:
   - El trazo libre usa el algoritmo DDA que dibuja círculos en cada punto
   - Para cada punto en un trazo libre, se crea un círculo con `ctx.arc()` y `ctx.fill()`
   - Esto es computacionalmente costoso, especialmente con muchos puntos

4. **Falta de optimización para trazos largos**:
   - No hay ninguna optimización para reducir la cantidad de puntos en trazos largos
   - Cada movimiento del mouse genera un nuevo punto que se almacena y procesa

### Posibles Mejoras Futuras

Para mejorar el rendimiento se podrían implementar:

1. **Capas de canvas**: Usar un canvas para dibujo activo y otro para formas completadas
2. **Simplificación de trazos**: Reducir la cantidad de puntos en trazos largos usando algoritmos de simplificación
3. **Renderizado parcial**: Solo redibujar las áreas afectadas, no todo el canvas
4. **Optimización del almacenamiento**: Convertir trazos completados en imágenes o paths optimizados

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

Desarrollado por Jerónimo Riveros para el curso de Computación Gráfica.