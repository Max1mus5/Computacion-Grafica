"""
Pygame Drawing Library (Versión orientada a objetos)

Esta biblioteca contiene clases para dibujar diferentes formas geométricas utilizando Pygame.
Las funciones están extraídas del proyecto CG-Graficador y adaptadas para ser utilizadas
de manera independiente con un enfoque orientado a objetos.

Autor: Basado en el proyecto CG-Graficador (https://github.com/porgetit/CG-Graficador)
"""

import pygame
import math
from abc import ABC, abstractmethod

class DrawingAlgorithm(ABC):
    """Clase base abstracta para todos los algoritmos de dibujo."""
    
    def __init__(self, algorithm_type="BASIC"):
        """
        Inicializa un algoritmo de dibujo.
        
        Args:
            algorithm_type (str): Tipo de algoritmo ("BASIC" o "PYGAME").
        """
        self.algorithm_type = algorithm_type
    
    @abstractmethod
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Método abstracto para dibujar una forma.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos de la forma a dibujar.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        pass

class LineAlgorithm(DrawingAlgorithm):
    """Clase base para algoritmos de dibujo de líneas."""
    pass

class DDALineAlgorithm(LineAlgorithm):
    """Implementación del algoritmo DDA para dibujar líneas."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja una línea utilizando el algoritmo DDA.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos de la línea (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        x1, y1 = points[0]
        x2, y2 = points[1]
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            if canvas_rect is None or canvas_rect.collidepoint(round(x1), round(y1)):
                pygame.draw.circle(surface, color, (round(x1), round(y1)), max(1, line_width // 2))
            return
        
        x_increment = dx / steps
        y_increment = dy / steps
        x, y = x1, y1
        
        for _ in range(steps + 1):
            if canvas_rect is None or canvas_rect.collidepoint(round(x), round(y)):
                pygame.draw.circle(surface, color, (round(x), round(y)), max(1, line_width // 2))
            x += x_increment
            y += y_increment

class PygameLineAlgorithm(LineAlgorithm):
    """Utiliza la función integrada de Pygame para dibujar líneas."""
    
    def __init__(self):
        super().__init__("PYGAME")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja una línea utilizando la función integrada de Pygame.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos de la línea (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        if canvas_rect is not None:
            # Verificar si al menos un extremo de la línea está dentro del canvas
            if not (canvas_rect.collidepoint(points[0]) or canvas_rect.collidepoint(points[1])):
                return
        
        pygame.draw.line(surface, color, points[0], points[1], line_width)

class CircleAlgorithm(DrawingAlgorithm):
    """Clase base para algoritmos de dibujo de círculos."""
    pass

class MidpointCircleAlgorithm(CircleAlgorithm):
    """Implementación del algoritmo del punto medio para dibujar círculos."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un círculo utilizando el algoritmo del punto medio.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del círculo (center, radius, color).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        
        if len(points) < 2:
            return
        
        center = points[0]
        radius = int(math.hypot(points[1][0] - center[0], points[1][1] - center[1]))
        
        x_center, y_center = center
        x = 0
        y = radius
        d = 1 - radius
        
        self._draw_circle_points(surface, x_center, y_center, x, y, color, canvas_rect)
        
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
            self._draw_circle_points(surface, x_center, y_center, x, y, color, canvas_rect)
    
    def _draw_circle_points(self, surface, xc, yc, x, y, color, canvas_rect=None):
        """
        Función auxiliar para dibujar los puntos de un círculo.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujarán los puntos.
            xc, yc (int): Coordenadas del centro del círculo.
            x, y (int): Coordenadas relativas al centro.
            color (tuple): Color de los puntos en formato RGB.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            if canvas_rect is None or canvas_rect.collidepoint(px, py):
                surface.set_at((px, py), color)

class PygameCircleAlgorithm(CircleAlgorithm):
    """Utiliza la función integrada de Pygame para dibujar círculos."""
    
    def __init__(self):
        super().__init__("PYGAME")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un círculo utilizando la función integrada de Pygame.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del círculo (center, radius, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        center = points[0]
        radius = int(math.hypot(points[1][0] - center[0], points[1][1] - center[1]))
        
        if canvas_rect is not None:
            # Verificar si el círculo está al menos parcialmente dentro del canvas
            circle_rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
            if not canvas_rect.colliderect(circle_rect):
                return
        
        pygame.draw.circle(surface, color, center, radius, line_width)

class PygameCirclePointsAlgorithm(CircleAlgorithm):
    """Dibuja un círculo utilizando puntos con la función de círculo de Pygame."""
    
    def __init__(self):
        super().__init__("PYGAME")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un círculo utilizando puntos con la función de círculo de Pygame.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del círculo (center, radius, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        center = points[0]
        radius = int(math.hypot(points[1][0] - center[0], points[1][1] - center[1]))
        
        x_center, y_center = center
        x = 0
        y = radius
        d = 1 - radius
        
        self._draw_circle_points(surface, x_center, y_center, x, y, color, line_width, canvas_rect)
        
        while x < y:
            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
            self._draw_circle_points(surface, x_center, y_center, x, y, color, line_width, canvas_rect)
    
    def _draw_circle_points(self, surface, xc, yc, x, y, color, line_width, canvas_rect=None):
        """
        Función auxiliar para dibujar los puntos de un círculo utilizando círculos pequeños de Pygame.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujarán los puntos.
            xc, yc (int): Coordenadas del centro del círculo.
            x, y (int): Coordenadas relativas al centro.
            color (tuple): Color de los puntos en formato RGB.
            line_width (int): Grosor de los puntos.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            if canvas_rect is None or canvas_rect.collidepoint(px, py):
                pygame.draw.circle(surface, color, (px, py), max(1, line_width // 2))

class RectangleAlgorithm(DrawingAlgorithm):
    """Clase base para algoritmos de dibujo de rectángulos."""
    pass

class BasicRectangleAlgorithm(RectangleAlgorithm):
    """Dibuja un rectángulo utilizando líneas individuales."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un rectángulo utilizando líneas.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del rectángulo (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        x1, y1 = points[0]
        x2, y2 = points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        
        if canvas_rect is not None:
            rect = rect.clip(canvas_rect)
        
        pygame.draw.line(surface, color, (rect.left, rect.top), (rect.right, rect.top), line_width)
        pygame.draw.line(surface, color, (rect.right, rect.top), (rect.right, rect.bottom), line_width)
        pygame.draw.line(surface, color, (rect.right, rect.bottom), (rect.left, rect.bottom), line_width)
        pygame.draw.line(surface, color, (rect.left, rect.bottom), (rect.left, rect.top), line_width)

class PygameRectangleAlgorithm(RectangleAlgorithm):
    """Utiliza la función integrada de Pygame para dibujar rectángulos."""
    
    def __init__(self):
        super().__init__("PYGAME")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un rectángulo utilizando la función integrada de Pygame.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del rectángulo (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        x1, y1 = points[0]
        x2, y2 = points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        
        if canvas_rect is not None:
            # Verificar si el rectángulo está al menos parcialmente dentro del canvas
            if not canvas_rect.colliderect(rect):
                return
            rect = rect.clip(canvas_rect)
        
        pygame.draw.rect(surface, color, rect, line_width)

class PolygonAlgorithm(DrawingAlgorithm):
    """Clase base para algoritmos de dibujo de polígonos."""
    pass

class BasicPolygonAlgorithm(PolygonAlgorithm):
    """Dibuja un polígono utilizando líneas individuales."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un polígono utilizando líneas.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del polígono (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        if canvas_rect is not None:
            filtered_points = [p for p in points if canvas_rect.collidepoint(p)]
        else:
            filtered_points = points
        
        if len(filtered_points) < 2:
            return
        
        for i in range(len(filtered_points) - 1):
            pygame.draw.line(surface, color, filtered_points[i], filtered_points[i + 1], line_width)

class PygamePolygonAlgorithm(PolygonAlgorithm):
    """Utiliza la función integrada de Pygame para dibujar polígonos."""
    
    def __init__(self):
        super().__init__("PYGAME")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja un polígono utilizando la función integrada de Pygame.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos del polígono (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 3:
            if len(points) == 2:
                pygame.draw.line(surface, color, points[0], points[1], line_width)
            return
        
        if canvas_rect is not None:
            # Verificar si al menos un punto está dentro del canvas
            if not any(canvas_rect.collidepoint(p) for p in points):
                return
        
        pygame.draw.polygon(surface, color, points, line_width)

class CurveAlgorithm(DrawingAlgorithm):
    """Clase base para algoritmos de dibujo de curvas."""
    pass

class BezierCurveAlgorithm(CurveAlgorithm):
    """Implementación del algoritmo para dibujar curvas de Bézier cuadráticas."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja una curva de Bézier cuadrática.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos de la curva (points, color, line_width, steps).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        steps = shape_data.get('steps', 100)
        
        if len(points) < 3:
            return
        
        p0, p1, p2 = points[0], points[1], points[2]
        curve_points = []
        
        try:
            for i in range(steps + 1):
                t = i / steps
                x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                curve_points.append((int(x), int(y)))
            
            for i in range(len(curve_points) - 1):
                if canvas_rect is None or canvas_rect.collidepoint(curve_points[i]) or canvas_rect.collidepoint(curve_points[i + 1]):
                    pygame.draw.line(surface, color, curve_points[i], curve_points[i + 1], line_width)
        except Exception as e:
            print(f"Error al dibujar la curva Bézier: {e}")

class PygameBezierCurveAlgorithm(CurveAlgorithm):
    """Utiliza la función integrada de Pygame para dibujar curvas de Bézier."""
    
    def __init__(self):
        super().__init__("PYGAME")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja una curva de Bézier cuadrática utilizando pygame.draw.lines.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos de la curva (points, color, line_width, steps).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        steps = shape_data.get('steps', 100)
        
        if len(points) < 3:
            return
        
        p0, p1, p2 = points[0], points[1], points[2]
        curve_points = []
        
        try:
            for i in range(steps + 1):
                t = i / steps
                x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                curve_points.append((int(x), int(y)))
            
            if len(curve_points) > 1:
                if canvas_rect is not None:
                    # Verificar si al menos un punto está dentro del canvas
                    if not any(canvas_rect.collidepoint(p) for p in curve_points):
                        return
                
                pygame.draw.lines(surface, color, False, curve_points, line_width)
        except Exception as e:
            print(f"Error al dibujar la curva Bézier: {e}")

class EraseAlgorithm(DrawingAlgorithm):
    """Clase base para algoritmos de borrado."""
    pass

class EraseAreaAlgorithm(EraseAlgorithm):
    """Algoritmo para borrar un área rectangular."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Borra un área rectangular.
        
        Args:
            surface (pygame.Surface): Superficie donde se borrará.
            shape_data (dict): Datos del área (points, erase_color).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        erase_color = shape_data.get('erase_color', (255, 255, 255))
        
        if len(points) < 2:
            return
        
        x1, y1 = points[0]
        x2, y2 = points[1]
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        
        if canvas_rect is not None:
            rect = rect.clip(canvas_rect)
        
        pygame.draw.rect(surface, erase_color, rect)

class FreehandEraseAlgorithm(EraseAlgorithm):
    """Algoritmo para borrar siguiendo una línea a mano alzada."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Borra siguiendo una línea a mano alzada.
        
        Args:
            surface (pygame.Surface): Superficie donde se borrará.
            shape_data (dict): Datos de la línea (points, erase_color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        erase_color = shape_data.get('erase_color', (255, 255, 255))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        if canvas_rect is not None:
            filtered_points = [p for p in points if canvas_rect.collidepoint(p)]
        else:
            filtered_points = points
        
        if len(filtered_points) > 1:
            pygame.draw.lines(surface, erase_color, False, filtered_points, line_width)

class FreehandDrawAlgorithm(DrawingAlgorithm):
    """Algoritmo para dibujar a mano alzada."""
    
    def __init__(self):
        super().__init__("BASIC")
    
    def draw(self, surface, shape_data, canvas_rect=None):
        """
        Dibuja una línea a mano alzada.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            shape_data (dict): Datos de la línea (points, color, line_width).
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        points = shape_data.get('points', [])
        color = shape_data.get('color', (0, 0, 0))
        line_width = shape_data.get('line_width', 1)
        
        if len(points) < 2:
            return
        
        if canvas_rect is not None:
            filtered_points = [p for p in points if canvas_rect.collidepoint(p)]
        else:
            filtered_points = points
        
        # Dibujar puntos individuales para trazos más precisos
        for i in range(len(filtered_points) - 1):
            x1, y1 = filtered_points[i]
            x2, y2 = filtered_points[i + 1]
            
            # Usar DDA para dibujar líneas entre puntos consecutivos
            dx = x2 - x1
            dy = y2 - y1
            steps = max(abs(dx), abs(dy))
            
            if steps == 0:
                pygame.draw.circle(surface, color, (round(x1), round(y1)), max(1, line_width // 2))
                continue
                
            x_increment = dx / steps
            y_increment = dy / steps
            x, y = x1, y1
            
            for _ in range(steps + 1):
                pygame.draw.circle(surface, color, (round(x), round(y)), max(1, line_width // 2))
                x += x_increment
                y += y_increment

class Shape:
    """Clase base para todas las formas geométricas."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1, algorithm=None):
        """
        Inicializa una forma geométrica.
        
        Args:
            points (list): Lista de puntos que definen la forma.
            color (tuple): Color de la forma en formato RGB.
            line_width (int): Grosor de las líneas.
            algorithm (DrawingAlgorithm): Algoritmo de dibujo a utilizar.
        """
        self.points = points or []
        self.color = color
        self.line_width = line_width
        self.algorithm = algorithm
    
    def draw(self, surface, canvas_rect=None):
        """
        Dibuja la forma en la superficie.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        if self.algorithm:
            shape_data = {
                'points': self.points,
                'color': self.color,
                'line_width': self.line_width
            }
            self.algorithm.draw(surface, shape_data, canvas_rect)
    
    def update_points(self, new_points):
        """
        Actualiza los puntos de la forma.
        
        Args:
            new_points (list): Nueva lista de puntos.
        """
        self.points = new_points

class Line(Shape):
    """Representa una línea."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1, algorithm_type="BASIC"):
        """
        Inicializa una línea.
        
        Args:
            points (list): Lista de dos puntos [start_point, end_point].
            color (tuple): Color de la línea en formato RGB.
            line_width (int): Grosor de la línea.
            algorithm_type (str): Tipo de algoritmo a utilizar ("BASIC" o "PYGAME").
        """
        algorithm = DDALineAlgorithm() if algorithm_type == "BASIC" else PygameLineAlgorithm()
        super().__init__(points, color, line_width, algorithm)

class Circle(Shape):
    """Representa un círculo."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1, algorithm_type="BASIC"):
        """
        Inicializa un círculo.
        
        Args:
            points (list): Lista de dos puntos [center, point_on_circumference].
            color (tuple): Color del círculo en formato RGB.
            line_width (int): Grosor de la línea.
            algorithm_type (str): Tipo de algoritmo a utilizar ("BASIC" o "PYGAME").
        """
        if algorithm_type == "BASIC":
            algorithm = MidpointCircleAlgorithm()
        else:
            algorithm = PygameCircleAlgorithm() if line_width > 0 else PygameCirclePointsAlgorithm()
        super().__init__(points, color, line_width, algorithm)

class Rectangle(Shape):
    """Representa un rectángulo."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1, algorithm_type="BASIC"):
        """
        Inicializa un rectángulo.
        
        Args:
            points (list): Lista de dos puntos [top_left, bottom_right].
            color (tuple): Color del rectángulo en formato RGB.
            line_width (int): Grosor de las líneas.
            algorithm_type (str): Tipo de algoritmo a utilizar ("BASIC" o "PYGAME").
        """
        algorithm = BasicRectangleAlgorithm() if algorithm_type == "BASIC" else PygameRectangleAlgorithm()
        super().__init__(points, color, line_width, algorithm)

class Polygon(Shape):
    """Representa un polígono."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1, algorithm_type="BASIC"):
        """
        Inicializa un polígono.
        
        Args:
            points (list): Lista de puntos que forman el polígono.
            color (tuple): Color del polígono en formato RGB.
            line_width (int): Grosor de las líneas.
            algorithm_type (str): Tipo de algoritmo a utilizar ("BASIC" o "PYGAME").
        """
        algorithm = BasicPolygonAlgorithm() if algorithm_type == "BASIC" else PygamePolygonAlgorithm()
        super().__init__(points, color, line_width, algorithm)

class Curve(Shape):
    """Representa una curva de Bézier cuadrática."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1, algorithm_type="BASIC", steps=100):
        """
        Inicializa una curva de Bézier.
        
        Args:
            points (list): Lista de tres puntos [p0, p1, p2] que definen la curva.
            color (tuple): Color de la curva en formato RGB.
            line_width (int): Grosor de la línea.
            algorithm_type (str): Tipo de algoritmo a utilizar ("BASIC" o "PYGAME").
            steps (int): Número de segmentos para aproximar la curva.
        """
        algorithm = BezierCurveAlgorithm() if algorithm_type == "BASIC" else PygameBezierCurveAlgorithm()
        super().__init__(points, color, line_width, algorithm)
        self.steps = steps
    
    def draw(self, surface, canvas_rect=None):
        """
        Dibuja la curva en la superficie.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        if self.algorithm:
            shape_data = {
                'points': self.points,
                'color': self.color,
                'line_width': self.line_width,
                'steps': self.steps
            }
            self.algorithm.draw(surface, shape_data, canvas_rect)

class EraseArea(Shape):
    """Representa un área rectangular para borrar."""
    
    def __init__(self, points=None, erase_color=(255, 255, 255), line_width=1):
        """
        Inicializa un área de borrado.
        
        Args:
            points (list): Lista de dos puntos [top_left, bottom_right].
            erase_color (tuple): Color de borrado (generalmente el color de fondo).
            line_width (int): No se utiliza, pero se mantiene por consistencia.
        """
        algorithm = EraseAreaAlgorithm()
        super().__init__(points, erase_color, line_width, algorithm)
        self.erase_color = erase_color
    
    def draw(self, surface, canvas_rect=None):
        """
        Borra un área en la superficie.
        
        Args:
            surface (pygame.Surface): Superficie donde se borrará.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        if self.algorithm:
            shape_data = {
                'points': self.points,
                'erase_color': self.erase_color
            }
            self.algorithm.draw(surface, shape_data, canvas_rect)

class EraseFree(Shape):
    """Representa una línea a mano alzada para borrar."""
    
    def __init__(self, points=None, erase_color=(255, 255, 255), line_width=10):
        """
        Inicializa una línea de borrado a mano alzada.
        
        Args:
            points (list): Lista de puntos que forman la línea.
            erase_color (tuple): Color de borrado (generalmente el color de fondo).
            line_width (int): Grosor de la línea de borrado.
        """
        algorithm = FreehandEraseAlgorithm()
        super().__init__(points, erase_color, line_width, algorithm)
        self.erase_color = erase_color
    
    def draw(self, surface, canvas_rect=None):
        """
        Borra siguiendo una línea en la superficie.
        
        Args:
            surface (pygame.Surface): Superficie donde se borrará.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        if self.algorithm:
            shape_data = {
                'points': self.points,
                'erase_color': self.erase_color,
                'line_width': self.line_width
            }
            self.algorithm.draw(surface, shape_data, canvas_rect)

class Freehand(Shape):
    """Representa una línea a mano alzada."""
    
    def __init__(self, points=None, color=(0, 0, 0), line_width=1):
        """
        Inicializa una línea a mano alzada.
        
        Args:
            points (list): Lista de puntos que forman la línea.
            color (tuple): Color de la línea en formato RGB.
            line_width (int): Grosor de la línea.
        """
        algorithm = FreehandDrawAlgorithm()
        super().__init__(points, color, line_width, algorithm)
    
    def draw(self, surface, canvas_rect=None):
        """
        Dibuja una línea a mano alzada en la superficie.
        
        Args:
            surface (pygame.Surface): Superficie donde se dibujará.
            canvas_rect (pygame.Rect, optional): Rectángulo que define el área de dibujo.
        """
        if self.algorithm:
            shape_data = {
                'points': self.points,
                'color': self.color,
                'line_width': self.line_width
            }
            self.algorithm.draw(surface, shape_data, canvas_rect)

class ShapeFactory:
    """Fábrica para crear diferentes tipos de formas."""
    
    @staticmethod
    def create_shape(shape_type, points=None, color=(0, 0, 0), line_width=1, algorithm_type="BASIC"):
        """
        Crea una forma del tipo especificado.
        
        Args:
            shape_type (str): Tipo de forma ("LINE", "CIRCLE", "RECTANGLE", "POLYGON", "CURVE", "FREEHAND", "ERASE_AREA", "ERASE_FREE").
            points (list): Lista de puntos que definen la forma.
            color (tuple): Color de la forma en formato RGB.
            line_width (int): Grosor de las líneas.
            algorithm_type (str): Tipo de algoritmo a utilizar ("BASIC" o "PYGAME").
        
        Returns:
            Shape: Una instancia de la forma creada.
        
        Raises:
            ValueError: Si el tipo de forma o algoritmo no es reconocido.
        """
        if shape_type == "LINE":
            return Line(points, color, line_width, algorithm_type)
        elif shape_type == "CIRCLE":
            return Circle(points, color, line_width, algorithm_type)
        elif shape_type == "RECTANGLE":
            return Rectangle(points, color, line_width, algorithm_type)
        elif shape_type == "POLYGON":
            return Polygon(points, color, line_width, algorithm_type)
        elif shape_type == "CURVE":
            return Curve(points, color, line_width, algorithm_type)
        elif shape_type == "FREEHAND":
            return Freehand(points, color, line_width)
        elif shape_type == "ERASE_AREA":
            return EraseArea(points, color, line_width)
        elif shape_type == "ERASE_FREE":
            return EraseFree(points, color, line_width)
        else:
            raise ValueError(f"Tipo de forma no reconocido: {shape_type}")

class Canvas:
    """Representa un lienzo donde se dibujan las formas."""
    
    def __init__(self, width=800, height=600, background_color=(255, 255, 255)):
        """
        Inicializa un lienzo.
        
        Args:
            width (int): Ancho del lienzo.
            height (int): Alto del lienzo.
            background_color (tuple): Color de fondo del lienzo en formato RGB.
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.shapes = []
        self.surface = pygame.Surface((width, height))
        self.surface.fill(background_color)
        self.rect = pygame.Rect(0, 0, width, height)
    
    def add_shape(self, shape):
        """
        Añade una forma al lienzo.
        
        Args:
            shape (Shape): Forma a añadir.
        """
        self.shapes.append(shape)
        shape.draw(self.surface, self.rect)
    
    def remove_shape(self, shape):
        """
        Elimina una forma del lienzo.
        
        Args:
            shape (Shape): Forma a eliminar.
        """
        if shape in self.shapes:
            self.shapes.remove(shape)
            self.redraw()
    
    def clear(self):
        """Limpia el lienzo, eliminando todas las formas."""
        self.shapes.clear()
        self.surface.fill(self.background_color)
    
    def redraw(self):
        """Vuelve a dibujar todas las formas en el lienzo."""
        self.surface.fill(self.background_color)
        for shape in self.shapes:
            shape.draw(self.surface, self.rect)
    
    def resize(self, width, height):
        """
        Cambia el tamaño del lienzo.
        
        Args:
            width (int): Nuevo ancho.
            height (int): Nuevo alto.
        """
        new_surface = pygame.Surface((width, height))
        new_surface.fill(self.background_color)
        new_surface.blit(self.surface, (0, 0))
        self.surface = new_surface
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.redraw()
    
    def get_surface(self):
        """
        Obtiene la superficie del lienzo.
        
        Returns:
            pygame.Surface: Superficie del lienzo.
        """
        return self.surface
    
    def save_to_file(self, filename):
        """
        Guarda el lienzo como una imagen.
        
        Args:
            filename (str): Nombre del archivo donde guardar.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            pygame.image.save(self.surface, filename)
            return True
        except Exception as e:
            print(f"Error al guardar la imagen: {e}")
            return False

# Funciones auxiliares
def calculate_distance(point1, point2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        point1 (tuple): Primer punto (x, y).
        point2 (tuple): Segundo punto (x, y).
    
    Returns:
        float: Distancia entre los puntos.
    """
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

def get_circle_radius(center, point):
    """
    Calcula el radio de un círculo dado su centro y un punto en la circunferencia.
    
    Args:
        center (tuple): Centro del círculo (x, y).
        point (tuple): Punto en la circunferencia (x, y).
    
    Returns:
        int: Radio del círculo.
    """
    return int(calculate_distance(center, point))