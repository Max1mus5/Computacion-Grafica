# Graphicator - Paint Web

Aplicación web de dibujo desarrollada con Django y JavaScript.

## Requisitos

- Python 3.8 o superior
- Django 5.2
- Pillow 11.1.0
- Pygame 2.5.2

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Max1mus5/Computacion-Grafica.git
cd Computacion-Grafica/GraphicatorProjectDjango
```

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

1. Inicia el servidor de desarrollo:
```bash
python manage.py runserver
```

2. Abre tu navegador y visita:
```
http://127.0.0.1:8000/
```

## Características

- Interfaz gráfica moderna con tema oscuro
- Panel lateral con herramientas de dibujo (20% del ancho)
- Área de canvas para dibujo (80% del ancho)
- Sistema de pestañas para alternar entre herramientas de dibujo y formas
- Selector de color con paleta predefinida y opción personalizada
- Control de grosor de línea con slider
- Biblioteca PygameDrawLibrary para funciones de dibujo

## Estructura del Proyecto

- `GraphicatorProject/`: Configuración principal de Django
- `paint/`: Aplicación principal de dibujo
- `static/`: Archivos estáticos (CSS, JavaScript)
- `templates/`: Plantillas HTML
- `GraphicatorProject/Lib/`: Biblioteca de dibujo con Pygame