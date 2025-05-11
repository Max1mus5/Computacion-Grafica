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
        # Crear una ventana redimensionable
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Graficador Pygame - Computación Gráfica")
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (51, 51, 51)
        self.DARKER_GRAY = (37, 37, 37)
        self.DARKEST_GRAY = (30, 30, 30)
        self.BACKGROUND = (26, 26, 36)
        self.YELLOW = (255, 191, 0)
        self.ORANGE = (204, 85, 0)
        self.PURPLE = (156, 39, 176)
        
        # Colores de la interfaz web
        self.UI_COLORS = {
            'background': (30, 30, 30),
            'panel': (37, 37, 37),
            'button': (51, 51, 51),
            'text': (255, 255, 255),
            'text_secondary': (153, 153, 153),
            'accent': (255, 191, 0),
            'canvas_bg': (26, 26, 36),
            'grid': (42, 42, 42),
            'status_bar': (37, 37, 37),
            'tool_active': (255, 191, 0, 51),
            'tool_border_active': (255, 191, 0),
            'circle_active': (204, 85, 0, 51),
            'circle_border_active': (204, 85, 0),
            'bezier_active': (156, 39, 176, 51),
            'bezier_border_active': (156, 39, 176),
            'grid_active': (33, 150, 243, 51),
            'grid_border_active': (33, 150, 243),
            'rectangle_active': (76, 175, 80, 51),
            'rectangle_border_active': (76, 175, 80),
            'triangle_active': (33, 150, 243, 51),
            'triangle_border_active': (33, 150, 243),
            'polygon_active': (244, 67, 54, 51),
            'polygon_border_active': (244, 67, 54),
            'developer_link': (76, 175, 80),
            'developer_link_hover': (33, 150, 243)
        }
        
        # Estado de la aplicación
        self.drawing = False
        self.current_tool = "freehand"  # Herramienta por defecto
        self.points = []
        self.current_color = self.YELLOW  # Color amarillo por defecto como en la web
        self.line_width = 2
        self.show_grid = True
        self.active_tab = "draw"  # Pestaña activa por defecto
        
        # Establecer dimensiones del panel y canvas
        self.panel_width = 200  # Ancho fijo del panel lateral
        self.canvas_width = self.width - self.panel_width
        self.canvas_height = self.height  # Usar toda la altura disponible
        
        # Crear superficie para el canvas
        self.canvas_surface = pygame.Surface((self.canvas_width, self.canvas_height))
        self.canvas_surface.fill(self.UI_COLORS['canvas_bg'])
        
        # Inicializar la biblioteca de dibujo para el canvas
        self.draw_lib = PygameDrawLibrary(self.canvas_surface)
        
        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()
        
        # Cargar fuentes
        self.font_small = pygame.font.SysFont("Arial", 12)
        self.font_medium = pygame.font.SysFont("Arial", 14)
        self.font_large = pygame.font.SysFont("Arial", 16)
        self.font_title = pygame.font.SysFont("Arial", 12)
        self.font_title.set_bold(True)
        
        print("DEBUG: Aplicación local inicializada")
    
    def draw_interface(self):
        """Dibuja la interfaz de usuario."""
        # Limpiar la pantalla con el color de fondo
        self.screen.fill(self.UI_COLORS['background'])
        
        # Actualizar dimensiones del canvas en caso de redimensionamiento
        self.canvas_width = max(1, self.width - self.panel_width)
        self.canvas_height = max(1, self.height)
        
        # Si el tamaño del canvas ha cambiado, recrearlo
        if self.canvas_surface.get_width() != self.canvas_width or self.canvas_surface.get_height() != self.canvas_height:
            old_canvas = self.canvas_surface.copy()
            self.canvas_surface = pygame.Surface((self.canvas_width, self.canvas_height))
            self.canvas_surface.fill(self.UI_COLORS['canvas_bg'])
            self.canvas_surface.blit(old_canvas, (0, 0))
            self.draw_lib = PygameDrawLibrary(self.canvas_surface)
        
        # Definir áreas de la interfaz
        panel_width = self.panel_width
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        
        # Dibujar el canvas en la pantalla principal
        self.screen.blit(self.canvas_surface, (panel_width, 0))
        
        # Dibujar cuadrícula si está activada
        if self.show_grid:
            self.draw_grid()
        
        # Dibujar panel de herramientas
        panel_rect = pygame.Rect(0, 0, panel_width, canvas_height)
        pygame.draw.rect(self.screen, self.UI_COLORS['panel'], panel_rect)
        
        # Dibujar pestañas
        tab_height = 40
        draw_tab_rect = pygame.Rect(0, 0, panel_width // 2, tab_height)
        shapes_tab_rect = pygame.Rect(panel_width // 2, 0, panel_width // 2, tab_height)
        
        # Pestaña Dibujar
        tab_color = self.UI_COLORS['button'] if self.active_tab != "draw" else self.DARK_GRAY
        pygame.draw.rect(self.screen, tab_color, draw_tab_rect)
        draw_tab_text = self.font_medium.render("Dibujar", True, 
                                              self.YELLOW if self.active_tab == "draw" else self.UI_COLORS['text_secondary'])
        self.screen.blit(draw_tab_text, (draw_tab_rect.centerx - draw_tab_text.get_width() // 2, 
                                        draw_tab_rect.centery - draw_tab_text.get_height() // 2))
        
        # Pestaña Formas
        tab_color = self.UI_COLORS['button'] if self.active_tab != "shapes" else self.DARK_GRAY
        pygame.draw.rect(self.screen, tab_color, shapes_tab_rect)
        shapes_tab_text = self.font_medium.render("Formas", True, 
                                                self.YELLOW if self.active_tab == "shapes" else self.UI_COLORS['text_secondary'])
        self.screen.blit(shapes_tab_text, (shapes_tab_rect.centerx - shapes_tab_text.get_width() // 2, 
                                          shapes_tab_rect.centery - shapes_tab_text.get_height() // 2))
        
        # Sección de herramientas
        tools_section_y = tab_height + 10
        section_title = self.font_title.render("HERRAMIENTAS", True, self.UI_COLORS['text_secondary'])
        self.screen.blit(section_title, (16, tools_section_y))
        
        # Grid de herramientas
        tools_grid_y = tools_section_y + 30
        tool_size = (panel_width - 40) // 2
        tool_padding = 8
        
        # Herramientas de dibujo
        if self.active_tab == "draw":
            tools = [
                {"id": "freehand", "name": "Trazo Libre", "key": "F"},
                {"id": "line", "name": "Línea", "key": "L"},
                {"id": "circle", "name": "Círculo", "key": "C"},
                {"id": "bezier", "name": "Curva Bézier", "key": "B"},
                {"id": "bezier-closed", "name": "Bézier Cerrada", "key": "Z"},
                {"id": "erase-free", "name": "Borrador", "key": "E"},
                {"id": "erase-area", "name": "Borrador Área", "key": "A"},
                {"id": "grid", "name": "Cuadrícula", "key": "G"}
            ]
        else:  # Pestaña de formas
            tools = [
                {"id": "rectangle", "name": "Rectángulo", "key": "R"},
                {"id": "triangle", "name": "Triángulo", "key": "T"},
                {"id": "polygon", "name": "Polígono", "key": "P"},
                {"id": "ellipse", "name": "Elipse", "key": "E"}
            ]
        
        # Dibujar botones de herramientas
        for i, tool in enumerate(tools):
            row = i // 2
            col = i % 2
            x = 16 + col * (tool_size + tool_padding)
            y = tools_grid_y + row * (tool_size + tool_padding)
            
            # Determinar color del botón según si está activo
            if tool["id"] == self.current_tool:
                if tool["id"] == "circle":
                    bg_color = self.UI_COLORS['circle_active']
                    border_color = self.UI_COLORS['circle_border_active']
                elif tool["id"] in ["bezier", "bezier-closed"]:
                    bg_color = self.UI_COLORS['bezier_active']
                    border_color = self.UI_COLORS['bezier_border_active']
                elif tool["id"] == "grid":
                    bg_color = self.UI_COLORS['grid_active']
                    border_color = self.UI_COLORS['grid_border_active']
                elif tool["id"] == "rectangle":
                    bg_color = self.UI_COLORS['rectangle_active']
                    border_color = self.UI_COLORS['rectangle_border_active']
                elif tool["id"] == "triangle":
                    bg_color = self.UI_COLORS['triangle_active']
                    border_color = self.UI_COLORS['triangle_border_active']
                elif tool["id"] == "polygon":
                    bg_color = self.UI_COLORS['polygon_active']
                    border_color = self.UI_COLORS['polygon_border_active']
                else:
                    bg_color = self.UI_COLORS['tool_active']
                    border_color = self.UI_COLORS['tool_border_active']
            else:
                bg_color = self.UI_COLORS['button']
                border_color = None
            
            # Dibujar botón
            tool_rect = pygame.Rect(x, y, tool_size, tool_size)
            pygame.draw.rect(self.screen, bg_color, tool_rect, border_radius=8)
            if border_color:
                pygame.draw.rect(self.screen, border_color, tool_rect, width=1, border_radius=8)
            
            # Dibujar ícono o texto de la herramienta
            tool_text = self.font_small.render(tool["name"][0], True, 
                                             self.YELLOW if tool["id"] == self.current_tool else self.UI_COLORS['text'])
            self.screen.blit(tool_text, (tool_rect.centerx - tool_text.get_width() // 2, 
                                        tool_rect.centery - tool_text.get_height() // 2))
        
        # Calcular posición de la paleta de colores
        if self.active_tab == "draw":
            tools_count = 8  # Número de herramientas en la pestaña de dibujo
        else:
            tools_count = 4  # Número de herramientas en la pestaña de formas
        
        color_section_y = tools_grid_y + (((tools_count + 1) // 2) * (tool_size + tool_padding)) + 20
        
        # Sección de color
        color_title = self.font_title.render("COLOR", True, self.UI_COLORS['text_secondary'])
        self.screen.blit(color_title, (16, color_section_y))
        
        # Selector de color
        color_display_rect = pygame.Rect(16, color_section_y + 30, panel_width - 32, 40)
        pygame.draw.rect(self.screen, self.UI_COLORS['button'], color_display_rect, border_radius=8)
        
        # Previsualización del color
        color_preview_rect = pygame.Rect(26, color_section_y + 38, 24, 24)
        pygame.draw.ellipse(self.screen, self.current_color, color_preview_rect)
        
        # Valor del color en hexadecimal
        color_hex = f"#{self.current_color[0]:02X}{self.current_color[1]:02X}{self.current_color[2]:02X}"
        color_text = self.font_medium.render(color_hex, True, self.UI_COLORS['text'])
        self.screen.blit(color_text, (60, color_section_y + 42))
        
        # Paleta de colores
        palette_y = color_section_y + 80
        swatch_size = (panel_width - 48) // 4
        swatch_padding = 8
        colors = [
            self.YELLOW,  # #FFBF00
            self.ORANGE,  # #CC5500
            self.PURPLE,  # #9C27B0
            (76, 175, 80),  # #4CAF50
            (33, 150, 243),  # #2196F3
            (244, 67, 54),  # #F44336
            self.WHITE,  # #FFFFFF
            self.BLACK   # #000000
        ]
        
        for i, color in enumerate(colors):
            row = i // 4
            col = i % 4
            x = 16 + col * (swatch_size + swatch_padding)
            y = palette_y + row * (swatch_size + swatch_padding)
            
            # Dibujar muestra de color
            swatch_rect = pygame.Rect(x, y, swatch_size, swatch_size)
            pygame.draw.ellipse(self.screen, color, swatch_rect)
            if color == self.current_color:
                pygame.draw.ellipse(self.screen, self.WHITE, swatch_rect, width=2)
        
        # Sección de grosor de línea
        stroke_section_y = palette_y + 80
        stroke_title = self.font_title.render("GROSOR DE LÍNEA", True, self.UI_COLORS['text_secondary'])
        self.screen.blit(stroke_title, (16, stroke_section_y))
        
        # Control deslizante de grosor
        slider_y = stroke_section_y + 30
        slider_width = panel_width - 32
        slider_height = 4
        slider_rect = pygame.Rect(16, slider_y + 8, slider_width, slider_height)
        pygame.draw.rect(self.screen, self.UI_COLORS['button'], slider_rect, border_radius=2)
        
        # Posición del control deslizante
        slider_pos = 16 + (self.line_width - 1) * (slider_width / 9)
        pygame.draw.circle(self.screen, self.WHITE, (slider_pos, slider_y + 10), 8)
        
        # Valor del grosor
        stroke_value_text = self.font_small.render(f"{self.line_width}px", True, self.UI_COLORS['text_secondary'])
        self.screen.blit(stroke_value_text, (slider_width - stroke_value_text.get_width() + 16, slider_y + 20))
        
        # Sección de acciones
        actions_section_y = slider_y + 50
        actions_title = self.font_title.render("ACCIONES", True, self.UI_COLORS['text_secondary'])
        self.screen.blit(actions_title, (16, actions_section_y))
        
        # Botones de acción
        clear_btn_rect = pygame.Rect(16, actions_section_y + 30, panel_width - 32, 40)
        pygame.draw.rect(self.screen, self.UI_COLORS['button'], clear_btn_rect, border_radius=8)
        clear_text = self.font_medium.render("Limpiar Lienzo", True, self.UI_COLORS['text'])
        self.screen.blit(clear_text, (clear_btn_rect.centerx - clear_text.get_width() // 2, 
                                     clear_btn_rect.centery - clear_text.get_height() // 2))
        
        save_btn_rect = pygame.Rect(16, actions_section_y + 80, panel_width - 32, 40)
        pygame.draw.rect(self.screen, self.UI_COLORS['button'], save_btn_rect, border_radius=8)
        save_text = self.font_medium.render("Guardar Imagen", True, self.UI_COLORS['text'])
        self.screen.blit(save_text, (save_btn_rect.centerx - save_text.get_width() // 2, 
                                    save_btn_rect.centery - save_text.get_height() // 2))
        
        # Visualización de coordenadas
        mouse_pos = pygame.mouse.get_pos()
        canvas_rect = pygame.Rect(panel_width, 0, canvas_width, canvas_height)
        if canvas_rect.collidepoint(mouse_pos):
            canvas_x = mouse_pos[0] - panel_width
            canvas_y = mouse_pos[1]
            coords_text = f"X: {canvas_x}, Y: {canvas_y}"
            coords_bg_rect = pygame.Rect(self.width - 120, self.height - 60, 100, 30)
            pygame.draw.rect(self.screen, (51, 51, 51, 128), coords_bg_rect, border_radius=6)
            coords_render = self.font_medium.render(coords_text, True, self.UI_COLORS['text'])
            self.screen.blit(coords_render, (coords_bg_rect.centerx - coords_render.get_width() // 2, 
                                           coords_bg_rect.centery - coords_render.get_height() // 2))
        
        # Botón de pantalla completa
        fullscreen_btn_rect = pygame.Rect(self.width - 56, 16, 36, 36)
        pygame.draw.rect(self.screen, (51, 51, 51, 128), fullscreen_btn_rect, border_radius=8)
        fullscreen_text = self.font_large.render("⛶", True, self.UI_COLORS['text'])
        self.screen.blit(fullscreen_text, (fullscreen_btn_rect.centerx - fullscreen_text.get_width() // 2, 
                                         fullscreen_btn_rect.centery - fullscreen_text.get_height() // 2))
        
        # Barra de estado
        status_bar_rect = pygame.Rect(0, self.height - 32, self.width, 32)
        pygame.draw.rect(self.screen, self.UI_COLORS['status_bar'], status_bar_rect)
        
        # Información de estado
        tool_names = {
            "freehand": "Trazo Libre",
            "line": "Línea",
            "circle": "Círculo",
            "rectangle": "Rectángulo",
            "triangle": "Triángulo",
            "polygon": "Polígono",
            "ellipse": "Elipse",
            "bezier": "Curva Bézier",
            "bezier-closed": "Bézier Cerrada",
            "erase-free": "Borrador",
            "erase-area": "Borrador de Área",
            "grid": "Cuadrícula"
        }
        
        # Dibujar barra de estado
        status_bar_rect = pygame.Rect(0, self.height - 30, self.width, 30)
        pygame.draw.rect(self.screen, self.UI_COLORS['status_bar'], status_bar_rect)
        
        # Información de herramienta
        tool_status = self.font_small.render(f"Herramienta: {tool_names.get(self.current_tool, self.current_tool)}", 
                                           True, self.UI_COLORS['text_secondary'])
        self.screen.blit(tool_status, (16, self.height - 20))
        
        # Información de color
        color_hex = f"#{self.current_color[0]:02X}{self.current_color[1]:02X}{self.current_color[2]:02X}"
        color_status = self.font_small.render(f"Color: {color_hex}", True, self.UI_COLORS['text_secondary'])
        
        # Posicionar información de color según el ancho de la ventana
        color_x = min(180, max(tool_status.get_width() + 30, self.panel_width + 20))
        self.screen.blit(color_status, (color_x, self.height - 20))
        
        # Información de grosor
        stroke_status = self.font_small.render(f"Grosor: {self.line_width}px", True, self.UI_COLORS['text_secondary'])
        stroke_x = min(300, max(color_x + color_status.get_width() + 30, self.panel_width + 120))
        self.screen.blit(stroke_status, (stroke_x, self.height - 20))
        
        # Información del desarrollador - centrada en la ventana
        dev_text = self.font_small.render("Desarrollado por Jeronimo Riveros Perea", True, self.UI_COLORS['text_secondary'])
        self.screen.blit(dev_text, (self.width - dev_text.get_width() - 16, self.height - 20))
    
    def draw_grid(self):
        """Dibuja la cuadrícula en el área del canvas."""
        panel_width = self.panel_width
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        canvas_rect = pygame.Rect(panel_width, 0, canvas_width, canvas_height)

        # Ajustar el tamaño de la cuadrícula según el tamaño de la ventana
        # Más pequeño para ventanas grandes, más grande para ventanas pequeñas
        base_grid_size = 40
        window_scale = min(1.0, max(0.5, self.width / 1024))  # Escala entre 0.5 y 1.0
        grid_size = int(base_grid_size * window_scale)
        grid_size = max(20, grid_size)  # Asegurar un tamaño mínimo de 20px
        
        # Dibujar líneas verticales
        for x in range(canvas_rect.left, canvas_rect.right, grid_size):
            pygame.draw.line(self.screen, self.UI_COLORS["grid"], (x, canvas_rect.top),
                           (x, canvas_rect.bottom), 1)
        
        # Dibujar líneas horizontales
        for y in range(canvas_rect.top, canvas_rect.bottom, grid_size):
            pygame.draw.line(self.screen, self.UI_COLORS["grid"], (canvas_rect.left, y),
                           (canvas_rect.right, y), 1)
    def handle_events(self):
        """Maneja los eventos de Pygame."""
        # Definir áreas de la interfaz
        panel_width = self.panel_width
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        
        canvas_rect = pygame.Rect(panel_width, 0, canvas_width, canvas_height)
        panel_rect = pygame.Rect(0, 0, panel_width, canvas_height)
        
        # Definir áreas de los botones
        tab_height = 40
        draw_tab_rect = pygame.Rect(0, 0, panel_width // 2, tab_height)
        shapes_tab_rect = pygame.Rect(panel_width // 2, 0, panel_width // 2, tab_height)
        
        # Calcular posición de los botones de herramientas
        tools_section_y = tab_height + 10
        tools_grid_y = tools_section_y + 30
        tool_size = (panel_width - 40) // 2
        tool_padding = 8
        
        # Calcular posición de la paleta de colores
        if self.active_tab == "draw":
            tools_count = 8  # Número de herramientas en la pestaña de dibujo
        else:
            tools_count = 4  # Número de herramientas en la pestaña de formas
        
        color_section_y = tools_grid_y + (((tools_count + 1) // 2) * (tool_size + tool_padding)) + 20
        palette_y = color_section_y + 80
        swatch_size = (panel_width - 48) // 4
        swatch_padding = 8
        
        # Calcular posición del control de grosor
        stroke_section_y = palette_y + 80
        slider_y = stroke_section_y + 30
        slider_width = panel_width - 32
        
        # Calcular posición de los botones de acción
        actions_section_y = slider_y + 50
        clear_btn_rect = pygame.Rect(16, actions_section_y + 30, panel_width - 32, 40)
        save_btn_rect = pygame.Rect(16, actions_section_y + 80, panel_width - 32, 40)
        
        # Botón de pantalla completa
        fullscreen_btn_rect = pygame.Rect(self.width - 56, 16, 36, 36)
        
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Manejo del redimensionamiento de la ventana
            elif event.type == pygame.VIDEORESIZE:
                # Actualizar el tamaño de la ventana
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                
                # Actualizar el tamaño del canvas
                self.canvas_width = max(1, self.width - self.panel_width)
                self.canvas_height = max(1, self.height)
                
                # Crear un nuevo canvas con el tamaño actualizado
                old_canvas = self.canvas_surface.copy()
                self.canvas_surface = pygame.Surface((self.canvas_width, self.canvas_height))
                self.canvas_surface.fill(self.UI_COLORS['canvas_bg'])
                
                # Copiar el contenido del canvas anterior al nuevo, centrado
                old_width, old_height = old_canvas.get_size()
                paste_x = max(0, (self.canvas_width - old_width) // 2)
                paste_y = max(0, (self.canvas_height - old_height) // 2)
                self.canvas_surface.blit(old_canvas, (paste_x, paste_y))
                
                # Actualizar la biblioteca de dibujo con la nueva superficie
                self.draw_lib = PygameDrawLibrary(self.canvas_surface)
                print(f"DEBUG: Ventana redimensionada a {self.width}x{self.height}, canvas: {self.canvas_width}x{self.canvas_height}")
            
            # Manejo de teclas
            elif event.type == pygame.KEYDOWN:
                # Teclas para herramientas de dibujo
                if event.key == pygame.K_f:
                    self.current_tool = "freehand"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Trazo Libre")
                elif event.key == pygame.K_l:
                    self.current_tool = "line"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Línea")
                elif event.key == pygame.K_c:
                    self.current_tool = "circle"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Círculo")
                elif event.key == pygame.K_b:
                    self.current_tool = "bezier"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Curva Bézier")
                elif event.key == pygame.K_z:
                    self.current_tool = "bezier-closed"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Bézier Cerrada")
                elif event.key == pygame.K_e:
                    self.current_tool = "erase-free"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Borrador")
                elif event.key == pygame.K_a:
                    self.current_tool = "erase-area"
                    self.active_tab = "draw"
                    print("DEBUG: Herramienta cambiada a Borrador de Área")
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                    print(f"DEBUG: Cuadrícula {'activada' if self.show_grid else 'desactivada'}")
                
                # Teclas para herramientas de formas
                elif event.key == pygame.K_r:
                    self.current_tool = "rectangle"
                    self.active_tab = "shapes"
                    print("DEBUG: Herramienta cambiada a Rectángulo")
                elif event.key == pygame.K_t:
                    self.current_tool = "triangle"
                    self.active_tab = "shapes"
                    print("DEBUG: Herramienta cambiada a Triángulo")
                elif event.key == pygame.K_p:
                    self.current_tool = "polygon"
                    self.active_tab = "shapes"
                    print("DEBUG: Herramienta cambiada a Polígono")
                
                # Teclas para grosor de línea
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.line_width = min(10, self.line_width + 1)
                    print(f"DEBUG: Grosor de línea aumentado a {self.line_width}")
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.line_width = max(1, self.line_width - 1)
                    print(f"DEBUG: Grosor de línea reducido a {self.line_width}")
                
                # Tecla para limpiar el lienzo
                elif event.key == pygame.K_DELETE:
                    self.canvas_surface.fill(self.UI_COLORS['canvas_bg'])
                    print("DEBUG: Lienzo limpiado")
                
                # Tecla para guardar imagen
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.save_image()
                    print("DEBUG: Imagen guardada")
            
            # Manejo del mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Verificar si se hizo clic en las pestañas
                if draw_tab_rect.collidepoint(mouse_pos):
                    self.active_tab = "draw"
                    print("DEBUG: Pestaña de Dibujo seleccionada")
                elif shapes_tab_rect.collidepoint(mouse_pos):
                    self.active_tab = "shapes"
                    print("DEBUG: Pestaña de Formas seleccionada")
                
                # Verificar si se hizo clic en los botones de herramientas
                elif panel_rect.collidepoint(mouse_pos) and mouse_pos[1] > tools_grid_y and mouse_pos[1] < color_section_y:
                    # Calcular qué herramienta se seleccionó
                    col = (mouse_pos[0] - 16) // (tool_size + tool_padding)
                    row = (mouse_pos[1] - tools_grid_y) // (tool_size + tool_padding)
                    
                    if col >= 0 and col < 2 and row >= 0:
                        tool_index = row * 2 + col
                        
                        if self.active_tab == "draw" and tool_index < 8:
                            tools = ["freehand", "line", "circle", "bezier", "bezier-closed", "erase-free", "erase-area", "grid"]
                            if tool_index == 7:  # Botón de cuadrícula
                                self.show_grid = not self.show_grid
                                print(f"DEBUG: Cuadrícula {'activada' if self.show_grid else 'desactivada'}")
                            else:
                                self.current_tool = tools[tool_index]
                                print(f"DEBUG: Herramienta cambiada a {self.current_tool}")
                        
                        elif self.active_tab == "shapes" and tool_index < 4:
                            tools = ["rectangle", "triangle", "polygon", "ellipse"]
                            self.current_tool = tools[tool_index]
                            print(f"DEBUG: Herramienta cambiada a {self.current_tool}")
                
                # Verificar si se hizo clic en la paleta de colores
                elif panel_rect.collidepoint(mouse_pos) and mouse_pos[1] > palette_y and mouse_pos[1] < stroke_section_y:
                    # Calcular qué color se seleccionó
                    col = (mouse_pos[0] - 16) // (swatch_size + swatch_padding)
                    row = (mouse_pos[1] - palette_y) // (swatch_size + swatch_padding)
                    
                    if col >= 0 and col < 4 and row >= 0 and row < 2:
                        color_index = row * 4 + col
                        colors = [
                            self.YELLOW,  # #FFBF00
                            self.ORANGE,  # #CC5500
                            self.PURPLE,  # #9C27B0
                            (76, 175, 80),  # #4CAF50
                            (33, 150, 243),  # #2196F3
                            (244, 67, 54),  # #F44336
                            self.WHITE,  # #FFFFFF
                            self.BLACK   # #000000
                        ]
                        
                        if color_index < len(colors):
                            self.current_color = colors[color_index]
                            print(f"DEBUG: Color cambiado a {self.current_color}")
                
                # Verificar si se hizo clic en el control deslizante de grosor
                elif panel_rect.collidepoint(mouse_pos) and mouse_pos[1] > slider_y and mouse_pos[1] < slider_y + 20:
                    # Calcular el grosor basado en la posición horizontal
                    slider_pos = (mouse_pos[0] - 16) / slider_width
                    self.line_width = max(1, min(10, int(slider_pos * 10) + 1))
                    print(f"DEBUG: Grosor de línea cambiado a {self.line_width}")
                
                # Verificar si se hizo clic en los botones de acción
                elif clear_btn_rect.collidepoint(mouse_pos):
                    self.canvas_surface.fill(self.UI_COLORS['canvas_bg'])
                    print("DEBUG: Lienzo limpiado")
                elif save_btn_rect.collidepoint(mouse_pos):
                    self.save_image()
                    print("DEBUG: Imagen guardada")
                
                # Verificar si se hizo clic en el botón de pantalla completa
                elif fullscreen_btn_rect.collidepoint(mouse_pos):
                    pygame.display.toggle_fullscreen()
                    print("DEBUG: Pantalla completa alternada")
                
                # Iniciar dibujo si se hizo clic en el área del canvas
                elif canvas_rect.collidepoint(mouse_pos):
                    self.drawing = True
                    # Ajustar las coordenadas al canvas
                    canvas_pos = (mouse_pos[0] - panel_width, mouse_pos[1])
                    self.points = [canvas_pos]
                    
                    # Crear una copia del canvas para poder restaurarlo durante la previsualización
                    self.canvas_backup = self.canvas_surface.copy()
                    
                    if self.current_tool == "freehand":
                        print("DEBUG: Iniciando trazo libre")
                    elif self.current_tool == "erase-free":
                        print("DEBUG: Iniciando borrado libre")
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing and canvas_rect.collidepoint(event.pos):
                    # Ajustar las coordenadas al canvas
                    canvas_pos = (event.pos[0] - panel_width, event.pos[1])
                    self.points.append(canvas_pos)
                    
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
                                'erase_color': self.UI_COLORS['canvas_bg'],
                                'radius': self.line_width * 5
                            }
                            self.draw_lib.draw_shape("erase-free", shape_data)
                    
                    # Previsualización para herramientas que dibujan al soltar el botón
                    elif self.current_tool in ["line", "circle", "rectangle", "triangle", "ellipse", "bezier", "bezier-closed", "polygon", "erase-area"]:
                        # Restaurar el canvas a su estado anterior
                        self.canvas_surface.blit(self.canvas_backup, (0, 0))
                        
                        # Previsualizar la forma según la herramienta
                        if self.current_tool == "line":
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("line", shape_data)
                        
                        elif self.current_tool == "circle":
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("circle", shape_data)
                        
                        elif self.current_tool == "rectangle":
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("rectangle", shape_data)
                        
                        elif self.current_tool == "triangle":
                            # Calcular el tercer punto del triángulo
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            x3 = x1 - (x2 - x1)
                            y3 = y2
                            
                            shape_data = {
                                'points': [[x1, y1], [x2, y2], [x3, y3]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("polygon", shape_data)
                        
                        elif self.current_tool == "ellipse":
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("circle", shape_data)  # Usamos círculo como aproximación
                        
                        elif self.current_tool == "bezier":
                            # Curva de Bézier cúbica abierta
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            
                            # Calcular puntos de control para la curva Bézier
                            # Puntos de control a 1/3 y 2/3 de la distancia
                            cx1 = x1 + (x2 - x1) / 3
                            cy1 = y1 + (y2 - y1) / 3
                            cx2 = x1 + 2 * (x2 - x1) / 3
                            cy2 = y1 + 2 * (y2 - y1) / 3
                            
                            shape_data = {
                                'points': [[x1, y1], [cx1, cy1], [cx2, cy2], [x2, y2]],
                                'color': self.current_color,
                                'line_width': self.line_width,
                                'closed': False
                            }
                            self.draw_lib.draw_shape("curve", shape_data)
                        
                        elif self.current_tool == "bezier-closed":
                            # Curva de Bézier cúbica cerrada
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            
                            # Calcular el ancho y alto del rectángulo
                            width = abs(x2 - x1)
                            height = abs(y2 - y1)
                            
                            # Asegurar que x1,y1 es la esquina superior izquierda
                            if x1 > x2:
                                x1, x2 = x2, x1
                            if y1 > y2:
                                y1, y2 = y2, y1
                            
                            # Crear puntos de control para una curva cerrada suave
                            # Esquinas del rectángulo
                            p1 = [x1, y1]  # Superior izquierda
                            p2 = [x2, y1]  # Superior derecha
                            p3 = [x2, y2]  # Inferior derecha
                            p4 = [x1, y2]  # Inferior izquierda
                            
                            # Puntos de control para cada segmento (para suavizar las esquinas)
                            # Superior: p1 a p2
                            c1 = [x1 + width/3, y1]
                            c2 = [x2 - width/3, y1]
                            
                            # Derecha: p2 a p3
                            c3 = [x2, y1 + height/3]
                            c4 = [x2, y2 - height/3]
                            
                            # Inferior: p3 a p4
                            c5 = [x2 - width/3, y2]
                            c6 = [x1 + width/3, y2]
                            
                            # Izquierda: p4 a p1
                            c7 = [x1, y2 - height/3]
                            c8 = [x1, y1 + height/3]
                            
                            # Dibujar los cuatro segmentos de la curva cerrada
                            segments = [
                                {'points': [p1, c1, c2, p2], 'color': self.current_color, 'line_width': self.line_width},
                                {'points': [p2, c3, c4, p3], 'color': self.current_color, 'line_width': self.line_width},
                                {'points': [p3, c5, c6, p4], 'color': self.current_color, 'line_width': self.line_width},
                                {'points': [p4, c7, c8, p1], 'color': self.current_color, 'line_width': self.line_width}
                            ]
                            
                            for segment in segments:
                                self.draw_lib.draw_shape("curve", segment)
                        
                        elif self.current_tool == "polygon":
                            # Crear un polígono regular de 6 lados
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            
                            # Calcular el centro y el radio
                            center_x = (x1 + x2) / 2
                            center_y = (y1 + y2) / 2
                            radius = math.sqrt((x2 - center_x)**2 + (y2 - center_y)**2)
                            
                            # Generar los puntos del polígono
                            polygon_points = []
                            sides = 6
                            for i in range(sides):
                                angle = 2 * math.pi * i / sides
                                px = center_x + radius * math.cos(angle)
                                py = center_y + radius * math.sin(angle)
                                polygon_points.append([px, py])
                            
                            # Cerrar el polígono
                            polygon_points.append(polygon_points[0])
                            
                            shape_data = {
                                'points': polygon_points,
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("polygon", shape_data)
                        
                        elif self.current_tool == "erase-area":
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'erase_color': self.UI_COLORS['canvas_bg']
                            }
                            self.draw_lib.draw_shape("erase-area", shape_data)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.drawing:
                    self.drawing = False
                    
                    if canvas_rect.collidepoint(event.pos):
                        # Ajustar las coordenadas al canvas
                        canvas_pos = (event.pos[0] - panel_width, event.pos[1])
                        self.points.append(canvas_pos)
                        
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
                        
                        elif self.current_tool == "triangle" and len(self.points) >= 2:
                            print("DEBUG: Dibujando triángulo")
                            # Calcular el tercer punto del triángulo
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            x3 = x1 - (x2 - x1)
                            y3 = y2
                            
                            shape_data = {
                                'points': [[x1, y1], [x2, y2], [x3, y3]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("polygon", shape_data)
                        
                        elif self.current_tool == "ellipse" and len(self.points) >= 2:
                            print("DEBUG: Dibujando elipse")
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("circle", shape_data)  # Usamos círculo como aproximación
                        
                        elif self.current_tool == "bezier" and len(self.points) >= 2:
                            print("DEBUG: Dibujando curva Bézier")
                            # Calcular puntos de control para la curva Bézier
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            
                            # Puntos de control a 1/3 y 2/3 de la distancia
                            cx1 = x1 + (x2 - x1) / 3
                            cy1 = y1 + (y2 - y1) / 3
                            cx2 = x1 + 2 * (x2 - x1) / 3
                            cy2 = y1 + 2 * (y2 - y1) / 3
                            
                            shape_data = {
                                'points': [[x1, y1], [cx1, cy1], [cx2, cy2], [x2, y2]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("curve", shape_data)
                        
                        elif self.current_tool == "bezier-closed" and len(self.points) >= 2:
                            print("DEBUG: Dibujando curva Bézier cerrada")
                            # Calcular puntos para la curva Bézier cerrada
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            
                            # Crear una forma cerrada
                            shape_data = {
                                'points': [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]],
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("polygon", shape_data)
                        
                        elif self.current_tool == "polygon" and len(self.points) >= 2:
                            print("DEBUG: Dibujando polígono")
                            # Crear un polígono regular de 6 lados
                            x1, y1 = self.points[0]
                            x2, y2 = self.points[-1]
                            
                            # Calcular el centro y el radio
                            center_x = (x1 + x2) / 2
                            center_y = (y1 + y2) / 2
                            radius = math.sqrt((x2 - center_x)**2 + (y2 - center_y)**2)
                            
                            # Generar los puntos del polígono
                            polygon_points = []
                            sides = 6
                            for i in range(sides):
                                angle = 2 * math.pi * i / sides
                                px = center_x + radius * math.cos(angle)
                                py = center_y + radius * math.sin(angle)
                                polygon_points.append([px, py])
                            
                            # Cerrar el polígono
                            polygon_points.append(polygon_points[0])
                            
                            shape_data = {
                                'points': polygon_points,
                                'color': self.current_color,
                                'line_width': self.line_width
                            }
                            self.draw_lib.draw_shape("polygon", shape_data)
                        
                        elif self.current_tool == "erase-area" and len(self.points) >= 2:
                            print("DEBUG: Borrando área")
                            shape_data = {
                                'points': [self.points[0], self.points[-1]],
                                'erase_color': self.UI_COLORS['canvas_bg']
                            }
                            self.draw_lib.draw_shape("erase-area", shape_data)
        
        return True
    
    def save_image(self):
        """Guarda el contenido del canvas como una imagen PNG."""
        # Guardar la imagen
        timestamp = pygame.time.get_ticks()
        filename = f"graphicator_image_{timestamp}.png"
        pygame.image.save(self.canvas_surface, filename)
        print(f"DEBUG: Imagen guardada como {filename}")
    
    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        running = True
        
        # Limpiar la pantalla al inicio
        self.screen.fill(self.UI_COLORS['background'])
        
        # Limpiar el área del canvas
        self.canvas_surface.fill(self.UI_COLORS['canvas_bg'])
        
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
    # Iniciar con una resolución estándar, pero permitiendo redimensionamiento
    app = GraphicatorLocalApp(width=1024, height=768)
    app.run()


if __name__ == "__main__":
    run_local_app()