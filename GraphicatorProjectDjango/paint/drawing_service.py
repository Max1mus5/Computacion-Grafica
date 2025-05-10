"""
Servicio de dibujo que utiliza la biblioteca PygameDrawLibrary para realizar operaciones de dibujo.
Este servicio actúa como puente entre la interfaz web y la biblioteca de dibujo.
"""

import base64
import io
import json
import os
import sys
from django.http import JsonResponse
import pygame

# Añadir la ruta de la librería al path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'GraphicatorProject', 'Lib'))
from PygameDrawLibrary import PygameDrawLibrary

class DrawingService:
    """Servicio para manejar operaciones de dibujo utilizando PygameDrawLibrary."""
    
    def __init__(self, width=800, height=600):
        """
        Inicializa el servicio de dibujo con un lienzo de tamaño específico.
        
        Args:
            width (int): Ancho del lienzo
            height (int): Alto del lienzo
        """
        self.width = width
        self.height = height
        self.surface = None
        self.draw_lib = None
        self.initialize()
    
    def initialize(self):
        """
        Inicializa la superficie de dibujo y la librería PygameDrawLibrary.
        """
        pygame.init()
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))  # Fondo blanco
        self.draw_lib = PygameDrawLibrary(self.surface)
    
    def draw_shape(self, shape_data):
        """
        Dibuja una forma en la superficie utilizando PygameDrawLibrary.
        
        Args:
            shape_data (dict): Datos de la forma a dibujar
                - type: Tipo de forma (line, circle, freehand, etc.)
                - points: Lista de puntos que definen la forma
                - color: Color de la forma en formato hexadecimal
                - line_width: Ancho de línea
        
        Returns:
            dict: Respuesta con el estado de la operación y la imagen resultante
        """
        try:
            shape_type = shape_data.get('type')
            points = shape_data.get('points', [])
            color_hex = shape_data.get('color', '#000000')
            line_width = shape_data.get('line_width', 1)
            
            # Convertir color hexadecimal a RGB
            color = self._hex_to_rgb(color_hex)
            
            # Dibujar según el tipo de forma
            if shape_type == 'line':
                if len(points) >= 2:
                    start_point = points[0]
                    end_point = points[-1]
                    self.draw_lib.draw_line(start_point, end_point, color, line_width)
            
            elif shape_type == 'circle':
                if len(points) >= 2:
                    center = points[0]
                    end_point = points[-1]
                    # Calcular el radio
                    radius = int(((end_point[0] - center[0]) ** 2 + (end_point[1] - center[1]) ** 2) ** 0.5)
                    self.draw_lib.draw_circle(center, radius, color, line_width)
            
            elif shape_type == 'rectangle':
                if len(points) >= 2:
                    start_point = points[0]
                    end_point = points[-1]
                    self.draw_lib.draw_rectangle(start_point, end_point, color, line_width)
            
            elif shape_type == 'triangle':
                if len(points) >= 3:
                    self.draw_lib.draw_polygon(points, color, line_width)
            
            elif shape_type == 'polygon':
                if len(points) >= 3:
                    self.draw_lib.draw_polygon(points, color, line_width)
            
            elif shape_type == 'ellipse':
                if len(points) >= 2:
                    start_point = points[0]
                    end_point = points[-1]
                    # Calcular el centro y los radios
                    center_x = (start_point[0] + end_point[0]) // 2
                    center_y = (start_point[1] + end_point[1]) // 2
                    radius_x = abs(end_point[0] - start_point[0]) // 2
                    radius_y = abs(end_point[1] - start_point[1]) // 2
                    self.draw_lib.draw_ellipse((center_x, center_y), radius_x, radius_y, color, line_width)
            
            elif shape_type == 'bezier' or shape_type == 'bezier-closed':
                if len(points) >= 4:
                    is_closed = shape_type == 'bezier-closed'
                    self.draw_lib.draw_bezier_curve(points, color, line_width, is_closed)
            
            elif shape_type == 'freehand':
                if len(points) >= 2:
                    for i in range(len(points) - 1):
                        start = points[i]
                        end = points[i + 1]
                        self.draw_lib.draw_line(start, end, color, line_width)
            
            # Actualizar la pantalla y devolver la imagen
            pygame.display.flip()
            return {
                'success': True,
                'image': self._surface_to_base64()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_canvas(self):
        """
        Limpia todo el lienzo.
        
        Returns:
            dict: Respuesta con el estado de la operación y la imagen resultante.
        """
        try:
            self.surface.fill((255, 255, 255))  # Fondo blanco
            pygame.display.flip()
            return {
                'success': True,
                'image': self._surface_to_base64()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def resize_canvas(self, width, height):
        """
        Cambia el tamaño del lienzo.
        
        Args:
            width (int): Nuevo ancho.
            height (int): Nuevo alto.
            
        Returns:
            dict: Respuesta con el estado de la operación y la imagen resultante.
        """
        try:
            # Crear una nueva superficie con el nuevo tamaño
            new_surface = pygame.Surface((width, height))
            new_surface.fill((255, 255, 255))
            
            # Copiar el contenido de la superficie actual a la nueva
            new_surface.blit(self.surface, (0, 0))
            
            # Actualizar las propiedades
            self.width = width
            self.height = height
            self.surface = new_surface
            self.draw_lib = PygameDrawLibrary(self.surface)
            
            pygame.display.flip()
            return {
                'success': True,
                'image': self._surface_to_base64()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_canvas(self, filename):
        """
        Guarda el lienzo como una imagen.
        
        Args:
            filename (str): Nombre del archivo donde guardar.
            
        Returns:
            dict: Respuesta con el estado de la operación.
        """
        try:
            pygame.image.save(self.surface, filename)
            return {
                'success': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _hex_to_rgb(self, hex_color):
        """
        Convierte un color hexadecimal a RGB.
        
        Args:
            hex_color (str): Color en formato hexadecimal (#RRGGBB)
        
        Returns:
            tuple: Color en formato RGB (r, g, b)
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _surface_to_base64(self):
        """
        Convierte la superficie de pygame a una imagen base64.
        
        Returns:
            str: Imagen codificada en base64
        """
        # Crear un archivo temporal para guardar la imagen
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            pygame.image.save(self.surface, temp_file.name)
            temp_file_path = temp_file.name
        
        # Leer la imagen y convertirla a base64
        with open(temp_file_path, 'rb') as img_file:
            img_data = img_file.read()
        
        # Eliminar el archivo temporal
        os.unlink(temp_file_path)
        
        # Codificar en base64
        base64_data = base64.b64encode(img_data).decode('utf-8')
        return f"data:image/png;base64,{base64_data}"


class DrawingServiceExtended(DrawingService):
    def erase(self, erase_data):
        """
        Borra una parte del lienzo.
        
        Args:
            erase_data (dict): Datos para la operación de borrado
                - type: Tipo de borrado ('free' o 'area')
                - point: Punto actual para borrado libre
                - size: Tamaño del borrador
                - start_point: Punto inicial para borrado de área
                - end_point: Punto final para borrado de área
        
        Returns:
            dict: Respuesta con el estado de la operación y la imagen resultante
        """
        try:
            erase_type = erase_data.get('type', 'free')
            
            if erase_type == 'free':
                point = erase_data.get('point', [0, 0])
                size = erase_data.get('size', 10)
                # Dibujar un círculo blanco para simular el borrado
                self.draw_lib.draw_circle(point, size // 2, (255, 255, 255), 0)
            
            elif erase_type == 'area':
                start_point = erase_data.get('start_point', [0, 0])
                end_point = erase_data.get('end_point', [100, 100])
                # Dibujar un rectángulo blanco para borrar el área
                self.draw_lib.draw_rectangle(start_point, end_point, (255, 255, 255), 0)
            
            # Actualizar la pantalla y devolver la imagen
            pygame.display.flip()
            return {
                'success': True,
                'image': self._surface_to_base64()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Instancia global del servicio de dibujo
drawing_service = DrawingServiceExtended()

def handle_draw_request(request):
    """
    Maneja una solicitud de dibujo.
    
    Args:
        request (HttpRequest): Solicitud HTTP.
        
    Returns:
        JsonResponse: Respuesta JSON con el resultado de la operación.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'draw':
                shape_data = data.get('shape')
                result = drawing_service.draw_shape(shape_data)
                return JsonResponse(result)
            
            elif action == 'erase':
                erase_data = data.get('erase_data', {})
                result = drawing_service.erase(erase_data)
                return JsonResponse(result)
            
            elif action == 'clear':
                result = drawing_service.clear_canvas()
                return JsonResponse(result)
            
            elif action == 'resize':
                width = data.get('width', 800)
                height = data.get('height', 600)
                result = drawing_service.resize_canvas(width, height)
                return JsonResponse(result)
            
            elif action == 'save':
                filename = data.get('filename', 'canvas.png')
                result = drawing_service.save_canvas(filename)
                return JsonResponse(result)
            
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Acción no reconocida'
                })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })