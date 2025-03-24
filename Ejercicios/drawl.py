# drawl.py - Módulo para funciones de dibujo de líneas

def cartesian_to_screen(x, y, width=800, height=600):
    """Convierte coordenadas cartesianas a coordenadas de pantalla"""
    screen_x = width // 2 + x
    screen_y = height // 2 - y  # Restamos porque el eje Y está invertido
    return int(screen_x), int(screen_y)

def draw_line_dda(surface, color, start_cart, end_cart, width=1):
    """
    Implementación del algoritmo DDA para dibujar líneas
    Recibe coordenadas cartesianas y las convierte a coordenadas de pantalla
    """
    import pygame
    
    # Convertir coordenadas cartesianas a coordenadas de pantalla
    start_x, start_y = cartesian_to_screen(start_cart[0], start_cart[1])
    end_x, end_y = cartesian_to_screen(end_cart[0], end_cart[1])
    
    # Implementación del algoritmo DDA (Digital Differential Analyzer)
    dx = end_x - start_x
    dy = end_y - start_y
    
    # Determinar el número de pasos
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        # Dibujar un solo punto si start y end son iguales
        if 0 <= start_x < surface.get_width() and 0 <= start_y < surface.get_height():
            if width == 1:
                surface.set_at((start_x, start_y), color)
            else:
                pygame.draw.circle(surface, color, (start_x, start_y), width // 2)
        return
    
    # Calcular incrementos
    x_increment = dx / steps
    y_increment = dy / steps
    
    # Valores iniciales
    x = start_x
    y = start_y
    
    # Dibujar cada punto
    for i in range(steps + 1):
        # Comprobamos que el punto está dentro de la superficie
        if 0 <= int(x) < surface.get_width() and 0 <= int(y) < surface.get_height():
            if width == 1:
                surface.set_at((int(x), int(y)), color)
            else:
                pygame.draw.circle(surface, color, (int(x), int(y)), width // 2)
        
        # Avanzar al siguiente punto
        x += x_increment
        y += y_increment

def draw_axes(surface, color=(0, 0, 0)):
    """Dibuja los ejes cartesianos en la superficie"""
    width, height = surface.get_width(), surface.get_height()
    
    # Eje X
    draw_line_dda(surface, color, (-width//2, 0), (width//2, 0), 1)
    # Eje Y
    draw_line_dda(surface, color, (0, -height//2), (0, height//2), 1)
    
    # Marcas en los ejes (cada 50 píxeles)
    for i in range(-width//2, width//2, 50):
        if i != 0:
            draw_line_dda(surface, color, (i, -5), (i, 5), 1)
    
    for i in range(-height//2, height//2, 50):
        if i != 0:
            draw_line_dda(surface, color, (-5, i), (5, i), 1)