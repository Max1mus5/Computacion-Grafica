import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometric Figures Drawing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Drawing states
DRAW_CIRCLE = 1
DRAW_ELLIPSE = 2
DRAW_RECTANGLE = 3
DRAW_TRIANGLE = 4
DRAW_POLYGON = 5

# Current drawing mode and points
current_mode = None
start_point = None
points = []

def draw_line_dda(surface, start, end, color):
    """
    Digital Differential Analyzer (DDA) line drawing algorithm
    """
    x1, y1 = start
    x2, y2 = end
    
    dx = x2 - x1
    dy = y2 - y1
    
    steps = max(abs(dx), abs(dy))
    
    x_inc = dx / steps
    y_inc = dy / steps
    
    x, y = x1, y1
    
    for _ in range(int(steps) + 1):
        pygame.draw.circle(surface, color, (round(x), round(y)), 1)
        x += x_inc
        y += y_inc

def draw_circle_bresenham(surface, center, radius, color):
    """
    Bresenham's circle drawing algorithm
    """
    x, y = 0, radius
    d = 3 - 2 * radius
    cx, cy = center

    def draw_circle_points(x, y):
        pygame.draw.circle(surface, color, (cx + x, cy + y), 1)
        pygame.draw.circle(surface, color, (cx + x, cy - y), 1)
        pygame.draw.circle(surface, color, (cx - x, cy + y), 1)
        pygame.draw.circle(surface, color, (cx - x, cy - y), 1)
        pygame.draw.circle(surface, color, (cx + y, cy + x), 1)
        pygame.draw.circle(surface, color, (cx + y, cy - x), 1)
        pygame.draw.circle(surface, color, (cx - y, cy + x), 1)
        pygame.draw.circle(surface, color, (cx - y, cy - x), 1)

    while y >= x:
        draw_circle_points(x, y)
        
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6

def draw_ellipse(surface, center, width, height, color):
    """
    Parametric ellipse drawing algorithm
    """
    cx, cy = center
    rx, ry = width // 2, height // 2
    
    for t in range(361):  # 360 degrees
        angle = math.radians(t)
        x = int(cx + rx * math.cos(angle))
        y = int(cy + ry * math.sin(angle))
        pygame.draw.circle(surface, color, (x, y), 1)

def draw_rectangle(surface, start, end, color):
    """
    Rectangle drawing using DDA line algorithm
    """
    x1, y1 = start
    x2, y2 = end
    
    # Create rectangle vertices
    vertices = [
        (x1, y1),  # Top left
        (x2, y1),  # Top right
        (x2, y2),  # Bottom right
        (x1, y2)   # Bottom left
    ]
    
    # Draw lines between vertices
    for i in range(4):
        draw_line_dda(surface, vertices[i], vertices[(i+1) % 4], color)

def draw_triangle(surface, points, color):
    """
    Triangle drawing using DDA line algorithm
    """
    for i in range(3):
        draw_line_dda(surface, points[i], points[(i+1) % 3], color)

def draw_polygon(surface, points, color):
    """
    Polygon drawing using DDA line algorithm
    """
    for i in range(len(points)):
        draw_line_dda(surface, points[i], points[(i+1) % len(points)], color)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Mode selection keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                current_mode = DRAW_CIRCLE
                points = []
            elif event.key == pygame.K_e:
                current_mode = DRAW_ELLIPSE
                points = []
            elif event.key == pygame.K_r:
                current_mode = DRAW_RECTANGLE
                points = []
            elif event.key == pygame.K_t:
                current_mode = DRAW_TRIANGLE
                points = []
            elif event.key == pygame.K_p:
                current_mode = DRAW_POLYGON
                points = []
        
        # Mouse interactions
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_mode == DRAW_CIRCLE:
                if not start_point:
                    start_point = event.pos
                else:
                    radius = int(math.sqrt((event.pos[0] - start_point[0])**2 + 
                                           (event.pos[1] - start_point[1])**2))
                    draw_circle_bresenham(screen, start_point, radius, BLACK)
                    start_point = None
            
            elif current_mode == DRAW_ELLIPSE:
                if not start_point:
                    start_point = event.pos
                else:
                    width = abs(event.pos[0] - start_point[0]) * 2
                    height = abs(event.pos[1] - start_point[1]) * 2
                    draw_ellipse(screen, start_point, width, height, BLACK)
                    start_point = None
            
            elif current_mode == DRAW_RECTANGLE:
                if not start_point:
                    start_point = event.pos
                else:
                    draw_rectangle(screen, start_point, event.pos, BLACK)
                    start_point = None
            
            elif current_mode == DRAW_TRIANGLE:
                points.append(event.pos)
                if len(points) == 3:
                    draw_triangle(screen, points, BLACK)
                    points = []
            
            elif current_mode == DRAW_POLYGON:
                points.append(event.pos)
                if len(points) > 2 and event.button == 3:  # Right click to finish polygon
                    draw_polygon(screen, points, BLACK)
                    points = []
    
    # Draw temporary polygon points
    if current_mode == DRAW_POLYGON and points:
        for point in points:
            pygame.draw.circle(screen, RED, point, 3)
    
    # On-screen instructions
    font = pygame.font.Font(None, 24)
    instructions = [
        "Press keys to select drawing mode:",
        "C - Circle",
        "E - Ellipse",
        "R - Rectangle",
        "T - Triangle",
        "P - Polygon (Right-click to finish)"
    ]
    
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (10, 10 + i * 25))
    
    pygame.display.flip()

pygame.quit()