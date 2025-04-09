import pygame
import sys
import math
from abc import ABC, abstractmethod

# -----------------------------
# Interfaz y Clases de Algoritmos de Dibujo
# -----------------------------
class LineDrawer(ABC):
    @abstractmethod
    def draw_line(self, surface, start, end, color):
        pass

class DDALineDrawer(LineDrawer):
    def draw_line(self, surface, start, end, color):
        x0, y0 = start
        x1, y1 = end
        dx = x1 - x0
        dy = y1 - y0

        # Determinar la cantidad de pasos necesarios
        steps = int(max(abs(dx), abs(dy)))
        if steps == 0:
            surface.set_at((int(x0), int(y0)), color)
            return

        # Calcular el incremento en cada paso
        x_increment = dx / steps
        y_increment = dy / steps

        # Dibujar la línea paso a paso
        x, y = x0, y0
        for _ in range(steps):
            surface.set_at((int(round(x)), int(round(y))), color)
            x += x_increment
            y += y_increment

class PygameLineDrawer(LineDrawer):
    def draw_line(self, surface, start, end, color):
        pygame.draw.line(surface, color, start, end)

# -----------------------------
# Factory para Seleccionar Algoritmo
# -----------------------------
class LineDrawerFactory:
    @staticmethod
    def get_line_drawer(method: str) -> LineDrawer:
        if method == 'DDA':
            return DDALineDrawer()
        elif method == 'PYGAME':
            return PygameLineDrawer()
        else:
            raise ValueError(f"Método desconocido: {method}")

# -----------------------------
# Botón para Cambiar el Método
# -----------------------------
class Button:
    def __init__(self, rect, text, font, inactive_color, active_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.current_color = inactive_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.current_color = self.active_color
        else:
            self.current_color = self.inactive_color

    def check_click(self, mouse_pos):
        return self.is_hovered(mouse_pos)

# -----------------------------
# Clase Principal de la Aplicación
# -----------------------------
class LineDrawingApp:
    WIDTH, HEIGHT = 800, 600
    BG_COLOR = (30, 30, 30)
    LINE_COLOR = (0, 255, 0)  # Parámetro para ajustar el color de la línea

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dibujo de Líneas: DDA vs pygame.draw.line()")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
        # Inicialmente se selecciona el método DDA
        self.current_method = 'DDA'
        self.line_drawer = LineDrawerFactory.get_line_drawer(self.current_method)
        
        # Botón para cambiar el algoritmo
        self.button = Button(rect=(10, 10, 200, 40),
                             text=f"Método: {self.current_method}",
                             font=self.font,
                             inactive_color=(70, 70, 70),
                             active_color=(100, 100, 100))
        
        self.points = []  # Lista para almacenar los puntos seleccionados

    def toggle_method(self):
        # Cambia entre DDA y PYGAME
        self.current_method = 'PYGAME' if self.current_method == 'DDA' else 'DDA'
        self.line_drawer = LineDrawerFactory.get_line_drawer(self.current_method)
        self.button.text = f"Método: {self.current_method}"

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Si se hace clic en el botón, cambiar el método
                    if self.button.check_click(mouse_pos):
                        self.toggle_method()
                    else:
                        # Registrar los puntos del ratón
                        if len(self.points) < 2:
                            self.points.append(mouse_pos)
                        else:
                            # Reiniciar si ya hay dos puntos
                            self.points = [mouse_pos]

            # Actualizar el estado del botón
            self.button.update(mouse_pos)

            # Dibujar el fondo
            self.screen.fill(self.BG_COLOR)
            
            # Dibujar el botón
            self.button.draw(self.screen)
            
            # Si se han seleccionado dos puntos, dibujar la línea con el método actual
            if len(self.points) == 2:
                self.line_drawer.draw_line(self.screen, self.points[0], self.points[1], self.LINE_COLOR)
                # Mostrar los puntos como círculos para visualización
                for point in self.points:
                    pygame.draw.circle(self.screen, (255, 0, 0), point, 5)
            
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = LineDrawingApp()
    app.run()