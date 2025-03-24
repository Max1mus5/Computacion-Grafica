import pygame
import math
import sys

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Suma Vectorial")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Función para convertir coordenadas cartesianas a coordenadas de pantalla
def cartesian_to_screen(x, y):
    # Ajustar el origen al centro de la pantalla
    screen_x = WIDTH // 2 + x
    screen_y = HEIGHT // 2 - y  # Invertir el eje Y
    return int(screen_x), int(screen_y)

# Función para dibujar una línea usando el algoritmo DDA
def draw_line_dda(surface, color, start_cart, end_cart, width=1):
    start_x, start_y = cartesian_to_screen(start_cart[0], start_cart[1])
    end_x, end_y = cartesian_to_screen(end_cart[0], end_cart[1])

    dx = end_x - start_x
    dy = end_y - start_y
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        if 0 <= start_x < surface.get_width() and 0 <= start_y < surface.get_height():
            if width == 1:
                surface.set_at((start_x, start_y), color)
            else:
                pygame.draw.circle(surface, color, (start_x, start_y), width // 2)
        return

    x_increment = dx / steps
    y_increment = dy / steps

    x = start_x
    y = start_y

    for _ in range(int(steps) + 1):
        if 0 <= int(x) < surface.get_width() and 0 <= int(y) < surface.get_height():
            if width == 1:
                surface.set_at((int(x), int(y)), color)
            else:
                pygame.draw.circle(surface, color, (int(x), int(y)), width // 2)
        x += x_increment
        y += y_increment

# Función para dibujar los ejes cartesianos
def draw_axes(surface):
    draw_line_dda(surface, BLACK, (-WIDTH // 2, 0), (WIDTH // 2, 0), 1)
    draw_line_dda(surface, BLACK, (0, -HEIGHT // 2), (0, HEIGHT // 2), 1)

    # Marcas en los ejes (cada 50 píxeles)
    for i in range(-WIDTH // 2, WIDTH // 2, 50):
        if i != 0:
            draw_line_dda(surface, BLACK, (i, -5), (i, 5), 1)
    for i in range(-HEIGHT // 2, HEIGHT // 2, 50):
        if i != 0:
            draw_line_dda(surface, BLACK, (-5, i), (5, i), 1)

# Función principal
def main():
    clock = pygame.time.Clock()

    # Datos del problema (magnitud y ángulo en grados)
    vectors_data = [
        {"magnitude": 10, "angle": 20, "color": RED},      # A
        {"magnitude": 12, "angle": 36, "color": GREEN},     # B
        {"magnitude": 8, "angle": 180 - 30, "color": BLUE}, # C (ajustado a la referencia del oeste)
        {"magnitude": 18, "angle": 180, "color": (255, 165, 0)},   # D (naranja)
        {"magnitude": 24, "angle": 180 + 26, "color": (128, 0, 128)} # E (púrpura)
    ]

    # Calcular los puntos finales de los vectores
    points = [(0, 0)]  # Punto inicial en el origen
    for vector in vectors_data:
        magnitude = vector["magnitude"]
        angle_rad = math.radians(vector["angle"])
        last_x, last_y = points[-1]
        new_x = last_x + magnitude * math.cos(angle_rad)
        new_y = last_y + magnitude * math.sin(angle_rad)
        points.append((new_x, new_y))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        draw_axes(screen)

        # Dibujar los vectores
        for i, vector in enumerate(vectors_data):
            start_point = points[i]
            end_point = points[i + 1]
            draw_line_dda(screen, vector["color"], start_point, end_point, 2)

        # Dibujar el vector resultante (desde el origen hasta el punto final del último vector)
        draw_line_dda(screen, BLACK, (0, 0), points[-1], 3)

        # Mostrar información en pantalla
        font = pygame.font.SysFont('Arial', 14)
        info_text = font.render("Pantalla: 800x600 | Origen en centro | ESC para salir", True, BLACK)
        screen.blit(info_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()