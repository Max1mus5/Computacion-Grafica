import os
import markdown
from django.shortcuts import render
from django.conf import settings

def docs_view(request):
    """
    Vista para mostrar la documentación del proyecto.
    Lee el archivo docs.md y lo convierte a HTML para mostrarlo en la plantilla.
    """
    # Ruta al archivo de documentación
    docs_path = os.path.join(settings.BASE_DIR, 'docspage', 'docs.md')
    
    # Leer el contenido del archivo
    try:
        with open(docs_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Convertir Markdown a HTML
        html_content = markdown.markdown(
            content,
            extensions=['extra', 'codehilite', 'toc']
        )
    except FileNotFoundError:
        html_content = "<p>El archivo de documentación no se encuentra.</p>"
    except Exception as e:
        html_content = f"<p>Error al leer la documentación: {str(e)}</p>"
    
    return render(request, 'docspage/docs.html', {
        'content': html_content
    })