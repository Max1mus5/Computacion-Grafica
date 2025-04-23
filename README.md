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

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

Desarrollado por Jerónimo Riveros para el curso de Computación Gráfica.