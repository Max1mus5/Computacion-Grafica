"""
Aplicación local de Graphicator utilizando Pygame directamente.
Esta versión se ejecuta cuando se usa el comando 'python manage.py runserver local'.
"""

import pygame
import sys
import math
from GraphicatorProject.Lib.PygameDrawLibrary import PygameDrawLibrary

class GraphicatorLocalApp:
    """Aplicación local de Graphicator utilizando Pygame."""
    
    def __init__(self, width=800, height=600):
        """
        Inicializa la aplicación local.
        
        Args:
            width (int): Ancho de la ventana
            height (int): Alto de la ventana
        """
        # Inicializar Pygame
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Graphicator - Versión Local")
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (200, 200, 200)
        
        # Inicializar la biblioteca de dibujo
        self.draw_lib = PygameDrawLibrary(self.screen)
        
        # Estado de la aplicación
        self.drawing = False
        self.current_tool = "freehand"  # Herramienta por defecto
        self.points = []
        self.current_color = self.BLACK
        self.line_width = 2
        
        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()
        
        print("DEBUG: Aplicación local inicializada")
    
    def draw_interface(self):
        """Dibuja la interfaz de usuario."""
        # Dibujar la barra de herramientas
        pygame.draw.rect(self.screen, self.GRAY, (0, 0, self.width, 40))
        
        # Mostrar la herramienta actual
        font = pygame.font.SysFont(None, 24)
        
        # Mapeo de nombres de herramientas para mostrar
        tool_names = {
            "freehand": "Trazo Libre",
            "line": "Línea",
            "circle": "Círculo",
            "rectangle": "Rectángulo",
            "erase-free": "Borrador",
            "erase-area": "Borrador de Área"
        }
        
        tool_text = font.render(f"Herramienta: {tool_names.get(self.current_tool, self.current_tool)}", True, self.BLACK)
        self.screen.blit(tool_text, (10, 10))
        
        # Mostrar el color actual
        color_text = font.render("Color:", True, self.BLACK)
        self.screen.blit(color_text, (200, 10))
        pygame.draw.rect(self.screen, self.current_color, (250, 10, 20, 20))
        
        # Mostrar instrucciones
        instructions = font.render("F: Trazo Libre | L: Línea | C: Círculo | R: Rectángulo | X: Borrador | E: Borrador Área", True, self.BLACK)
        self.screen.blit(instructions, (280, 10))
    
    def handle_events(self):
        """Maneja los eventos de Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Manejo de teclas
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.current_tool = "freehand"
                    print("DEBUG: Herramienta cambiada a Trazo Libre")
                elif event.key == pygame.K_l:
                    self.current_tool = "line"
                    print("DEBUG: Herramienta cambiada a Línea")
                elif event.key == pygame.K_c:
                    self.current_tool = "circle"
                    print("DEBUG: Herramienta cambiada a Círculo")
                elif event.key == pygame.K_r:
                    self.current_tool = "rectangle"
                    print("DEBUG: Herramienta cambiada a Rectángulo")
                elif event.key == pygame.K_x:
                    self.current_tool = "erase-free"
                    print("DEBUG: Herramienta cambiada a Borrador")
                elif event.key == pygame.K_e:
                    self.current_tool = "erase-area"
                    print("DEBUG: Herramienta cambiada a Borrador de Área")
                elif event.key == pygame.K_1:
                    self.current_color = self.BLACK
                    print("DEBUG: Color cambiado a Negro")
                elif event.key == pygame.K_2:
                    self.current_color = self.RED
                    print("DEBUG: Color cambiado a Rojo")
                elif event.key == pygame.K_3:
                    self.current_color = self.GREEN
                    print("DEBUG: Color cambiado a Verde")
                elif event.key == pygame.K_4:
                    self.current_color = self.BLUE
                    print("DEBUG: Color cambiado a Azul")
            
            # Manejo del mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > 40:  # Solo dibujar debajo de la barra de herramientas
                    self.drawing = True
                    self.points = [event.pos]
                    
                    if self.current_tool == "freehand":
                        print("DEBUG: Iniciando trazo libre")
                    elif self.current_tool == "erase-free":
                        print("DEBUG: Iniciando borrado libre")
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing and event.pos[1] > 40:
                    self.points.append(event.pos)
                    
                    # Dibujar en tiempo real
                    if self.current_tool == "freehand":
                        if len(self.points) >= 2:
                            shape_data = {
                                'points': [self.points[-2], self.points[-1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("line", shape_data)
                    
                    elif self.current_tool == "erase-free":
                        if len(self.points) >= 1:
                            shape_data = {
                                'points': [self.points[-1]],
                                'erase_color': self.WHITE,
                                'radius': 10
                            }
                            self.draw_lib.draw_shape("erase-free", shape_data)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.drawing:
                    self.drawing = False
                    
                    if self.current_tool == "line" and len(self.points) >= 2:
                        print("DEBUG: Dibujando línea")
                        shape_data = {
                            'points': [self.points[0], self.points[-1]],
                            'color': self.current_color,
                            'line_width': self.line_width
                        }
                        self.draw_lib.draw_shape("line", shape_data)
                    
                    elif self.current_tool == "circle" and len(self.points) >= 2:
                        print("DEBUG: Dibujando círculo")
                        shape_data = {
                            'points': [self.points[0], self.points[-1]],
                            'color': self.current_color,
                            'line_width': self.line_width
                        }
                        self.draw_lib.draw_shape("circle", shape_data)
                    
                    elif self.current_tool == "rectangle" and len(self.points) >= 2:
                        print("DEBUG: Dibujando rectángulo")
                        shape_data = {
                            'points': [self.points[0], self.points[-1]],
                            'color': self.current_color,
                            'line_width': self.line_width
                        }
                        self.draw_lib.draw_shape("rectangle", shape_data)
                    
                    elif self.current_tool == "erase-area" and len(self.points) >= 2:
                        print("DEBUG: Borrando área")
                        shape_data = {
                            'points': [self.points[0], self.points[-1]],
                            'erase_color': self.WHITE
                        }
                        self.draw_lib.draw_shape("erase-area", shape_data)
        
        return True
    
    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        running = True
        
        # Limpiar la pantalla al inicio
        self.screen.fill(self.WHITE)
        
        print("DEBUG: Iniciando bucle principal de la aplicación local")
        
        while running:
            # Manejar eventos
            running = self.handle_events()
            
            # Dibujar la interfaz
            self.draw_interface()
            
            # Actualizar la pantalla
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        print("DEBUG: Aplicación local cerrada")


def run_local_app():
    """Función para iniciar la aplicación local."""
    print("Iniciando aplicación local con Pygame...")
    app = GraphicatorLocalApp()
    app.run()


if __name__ == "__main__":
    run_local_app()