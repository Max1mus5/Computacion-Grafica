import pygame
import sys

# Inicializa
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click Listener")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Lista almacenar posiciones de los círculos
puntos = []
MAX_PUNTOS = 40  # Max Putnos

# Radio 
RADIO = 5

# Bucle principal del juego
def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Detectar clic del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                # obtener posición del ratón
                pos = pygame.mouse.get_pos()
                
                print(pos)
                # agregar punto a la lista FIFO
                puntos.append(pos)
                
                # eliminar primer elemento si la lista excede el tamaño máximo
                if len(puntos) > MAX_PUNTOS:
                    puntos.pop(0)

        # pantalla limpia
        screen.fill(WHITE)

        # dibujar ciruclos y conectar
        for i, punto in enumerate(puntos):
            # en posiciones dibujar un círculo
            pygame.draw.circle(screen, RED, punto, RADIO)
            
            # conectar
            if i > 0:
                pygame.draw.line(screen, BLACK, puntos[i-1], punto, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()