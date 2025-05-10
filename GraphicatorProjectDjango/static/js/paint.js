/**
 * Graficador Pygame - Aplicación de dibujo para navegador
 * Integrado con la biblioteca PygameDrawLibrary
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const canvas = document.getElementById('paint-canvas');
    const ctx = canvas.getContext('2d');
    const coordinatesDisplay = document.querySelector('.coordinates-display');
    const currentToolDisplay = document.getElementById('current-tool');
    const currentColorDisplay = document.getElementById('current-color');
    const currentStrokeDisplay = document.getElementById('current-stroke');
    const colorDisplay = document.getElementById('color-display');
    const colorPicker = document.getElementById('color-picker');
    const customColorInput = document.getElementById('custom-color-input');
    const strokeWidthInput = document.getElementById('stroke-width');
    const strokeWidthValue = document.querySelector('.stroke-value');
    const clearCanvasBtn = document.getElementById('clear-canvas');
    const saveImageBtn = document.getElementById('save-image');
    const fullscreenToggleBtn = document.getElementById('fullscreen-toggle');
    
    // Pestañas
    const drawTab = document.getElementById('draw-tab');
    const shapesTab = document.getElementById('shapes-tab');
    const drawTools = document.getElementById('draw-tools');
    const shapesTools = document.getElementById('shapes-tools');
    
    // Herramientas
    const toolButtons = {
        freehand: document.getElementById('freehand-tool'),
        line: document.getElementById('line-tool'),
        circle: document.getElementById('circle-tool'),
        bezier: document.getElementById('bezier-tool'),
        'bezier-closed': document.getElementById('bezier-closed-tool'),
        'erase-free': document.getElementById('erase-free-tool'),
        'erase-area': document.getElementById('erase-area-tool'),
        grid: document.getElementById('grid-tool'),
        rectangle: document.getElementById('rectangle-tool'),
        triangle: document.getElementById('triangle-tool'),
        polygon: document.getElementById('polygon-tool'),
        ellipse: document.getElementById('ellipse-tool')
    };
    
    // Estado de la aplicación
    const state = {
        currentTool: 'freehand',
        currentColor: '#FFBF00',
        backgroundColor: '#1A1A24',
        lineWidth: 2,
        algorithm: 'BASIC',
        isDrawing: false,
        points: [],
        shapes: [],
        currentShape: null,
        undoStack: [],
        redoStack: [],
        showGrid: true,
        isFullscreen: false,
        activeTab: 'draw'
    };
    
    // Ajustar el tamaño del canvas al tamaño de la ventana
    function resizeCanvas() {
        const canvasArea = document.querySelector('.canvas-area');
        canvas.width = canvasArea.clientWidth;
        canvas.height = canvasArea.clientHeight;
        redrawCanvas();
    }
    
    // Inicializar el canvas
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Funciones de dibujo
    const drawingFunctions = {
        // Función para dibujar una línea con el algoritmo DDA
        drawLineDDA: function(x1, y1, x2, y2, color, lineWidth) {
            const dx = x2 - x1;
            const dy = y2 - y1;
            const steps = Math.max(Math.abs(dx), Math.abs(dy));
            
            if (steps === 0) {
                ctx.beginPath();
                ctx.arc(Math.round(x1), Math.round(y1), Math.max(1, lineWidth / 2), 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
                return;
            }
            
            const xIncrement = dx / steps;
            const yIncrement = dy / steps;
            let x = x1;
            let y = y1;
            
            for (let i = 0; i <= steps; i++) {
                ctx.beginPath();
                ctx.arc(Math.round(x), Math.round(y), Math.max(1, lineWidth / 2), 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
                x += xIncrement;
                y += yIncrement;
            }
        },
        
        // Función para dibujar una línea con el algoritmo de Bresenham
        drawLineBresenham: function(x1, y1, x2, y2, color, lineWidth) {
            let x = Math.round(x1);
            let y = Math.round(y1);
            const dx = Math.abs(Math.round(x2) - x);
            const dy = Math.abs(Math.round(y2) - y);
            const sx = (x < Math.round(x2)) ? 1 : -1;
            const sy = (y < Math.round(y2)) ? 1 : -1;
            let err = dx - dy;
            
            while (true) {
                ctx.beginPath();
                ctx.arc(x, y, Math.max(1, lineWidth / 2), 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
                
                if (x === Math.round(x2) && y === Math.round(y2)) break;
                
                const e2 = 2 * err;
                if (e2 > -dy) {
                    err -= dy;
                    x += sx;
                }
                if (e2 < dx) {
                    err += dx;
                    y += sy;
                }
            }
        },
        
        // Función para dibujar una línea con la API de Canvas
        drawLinePygame: function(x1, y1, x2, y2, color, lineWidth) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar un círculo con el algoritmo de Bresenham
        drawCircleBresenham: function(centerX, centerY, radius, color, lineWidth) {
            let x = 0;
            let y = radius;
            let d = 3 - 2 * radius;
            
            const drawPixel = (x, y) => {
                ctx.beginPath();
                ctx.arc(x, y, Math.max(1, lineWidth / 2), 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
            };
            
            const drawCirclePoints = (cx, cy, x, y) => {
                drawPixel(cx + x, cy + y);
                drawPixel(cx - x, cy + y);
                drawPixel(cx + x, cy - y);
                drawPixel(cx - x, cy - y);
                drawPixel(cx + y, cy + x);
                drawPixel(cx - y, cy + x);
                drawPixel(cx + y, cy - x);
                drawPixel(cx - y, cy - x);
            };
            
            drawCirclePoints(centerX, centerY, x, y);
            
            while (y >= x) {
                x++;
                
                if (d > 0) {
                    y--;
                    d = d + 4 * (x - y) + 10;
                } else {
                    d = d + 4 * x + 6;
                }
                
                drawCirclePoints(centerX, centerY, x, y);
            }
        },
        
        // Función para dibujar un círculo con la API de Canvas
        drawCirclePygame: function(centerX, centerY, radius, color, lineWidth) {
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar una elipse con el algoritmo de Bresenham
        drawEllipseBresenham: function(centerX, centerY, radiusX, radiusY, color, lineWidth) {
            let x = 0;
            let y = radiusY;
            
            // Parámetros iniciales de la región 1
            let d1 = (radiusY * radiusY) - (radiusX * radiusX * radiusY) + (0.25 * radiusX * radiusX);
            let dx = 2 * radiusY * radiusY * x;
            let dy = 2 * radiusX * radiusX * y;
            
            const drawPixel = (x, y) => {
                ctx.beginPath();
                ctx.arc(x, y, Math.max(1, lineWidth / 2), 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
            };
            
            // Región 1
            while (dx < dy) {
                drawPixel(centerX + x, centerY + y);
                drawPixel(centerX - x, centerY + y);
                drawPixel(centerX + x, centerY - y);
                drawPixel(centerX - x, centerY - y);
                
                x++;
                dx += 2 * radiusY * radiusY;
                
                if (d1 < 0) {
                    d1 += dx + radiusY * radiusY;
                } else {
                    y--;
                    dy -= 2 * radiusX * radiusX;
                    d1 += dx - dy + radiusY * radiusY;
                }
            }
            
            // Parámetros iniciales de la región 2
            let d2 = ((radiusY * radiusY) * ((x + 0.5) * (x + 0.5))) + 
                     ((radiusX * radiusX) * ((y - 1) * (y - 1))) - 
                     (radiusX * radiusX * radiusY * radiusY);
            
            // Región 2
            while (y >= 0) {
                drawPixel(centerX + x, centerY + y);
                drawPixel(centerX - x, centerY + y);
                drawPixel(centerX + x, centerY - y);
                drawPixel(centerX - x, centerY - y);
                
                y--;
                dy -= 2 * radiusX * radiusX;
                
                if (d2 > 0) {
                    d2 += radiusX * radiusX - dy;
                } else {
                    x++;
                    dx += 2 * radiusY * radiusY;
                    d2 += dx - dy + radiusX * radiusX;
                }
            }
        },
        
        // Función para dibujar una elipse con la API de Canvas
        drawEllipsePygame: function(centerX, centerY, radiusX, radiusY, color, lineWidth) {
            ctx.beginPath();
            ctx.ellipse(centerX, centerY, radiusX, radiusY, 0, 0, Math.PI * 2);
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar un rectángulo con líneas básicas
        drawRectangleBasic: function(x1, y1, x2, y2, color, lineWidth) {
            const left = Math.min(x1, x2);
            const top = Math.min(y1, y2);
            const right = Math.max(x1, x2);
            const bottom = Math.max(y1, y2);
            
            // Dibujar las cuatro líneas del rectángulo usando Bresenham
            this.drawLineBresenham(left, top, right, top, color, lineWidth);
            this.drawLineBresenham(right, top, right, bottom, color, lineWidth);
            this.drawLineBresenham(right, bottom, left, bottom, color, lineWidth);
            this.drawLineBresenham(left, bottom, left, top, color, lineWidth);
        },
        
        // Función para dibujar un rectángulo con la API de Canvas
        drawRectanglePygame: function(x1, y1, x2, y2, color, lineWidth) {
            const left = Math.min(x1, x2);
            const top = Math.min(y1, y2);
            const width = Math.abs(x2 - x1);
            const height = Math.abs(y2 - y1);
            
            ctx.beginPath();
            ctx.rect(left, top, width, height);
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar un triángulo
        drawTriangle: function(points, color, lineWidth) {
            if (points.length < 3) return;
            
            if (state.algorithm === 'BASIC') {
                this.drawLineBresenham(points[0][0], points[0][1], points[1][0], points[1][1], color, lineWidth);
                this.drawLineBresenham(points[1][0], points[1][1], points[2][0], points[2][1], color, lineWidth);
                this.drawLineBresenham(points[2][0], points[2][1], points[0][0], points[0][1], color, lineWidth);
            } else {
                ctx.beginPath();
                ctx.moveTo(points[0][0], points[0][1]);
                ctx.lineTo(points[1][0], points[1][1]);
                ctx.lineTo(points[2][0], points[2][1]);
                ctx.lineTo(points[0][0], points[0][1]);
                ctx.strokeStyle = color;
                ctx.lineWidth = lineWidth;
                ctx.stroke();
            }
        },
        
        // Función para dibujar un polígono con líneas básicas
        drawPolygonBasic: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            for (let i = 0; i < points.length - 1; i++) {
                this.drawLineBresenham(
                    points[i][0], points[i][1],
                    points[i + 1][0], points[i + 1][1],
                    color, lineWidth
                );
            }
            
            // Cerrar el polígono si tiene más de 2 puntos
            if (points.length > 2) {
                this.drawLineBresenham(
                    points[points.length - 1][0], points[points.length - 1][1],
                    points[0][0], points[0][1],
                    color, lineWidth
                );
            }
        },
        
        // Función para dibujar una curva abierta con líneas básicas (sin cerrar)
        drawCurveBasic: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            for (let i = 0; i < points.length - 1; i++) {
                this.drawLineBresenham(
                    points[i][0], points[i][1],
                    points[i + 1][0], points[i + 1][1],
                    color, lineWidth
                );
            }
            // No cerramos la curva, dejándola abierta
        },
        
        // Función para dibujar un polígono con la API de Canvas
        drawPolygonPygame: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            ctx.beginPath();
            ctx.moveTo(points[0][0], points[0][1]);
            
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i][0], points[i][1]);
            }
            
            // Cerrar el polígono si tiene más de 2 puntos
            if (points.length > 2) {
                ctx.closePath();
            }
            
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar una curva abierta con la API de Canvas (sin cerrar)
        drawCurvePygame: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            ctx.beginPath();
            ctx.moveTo(points[0][0], points[0][1]);
            
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i][0], points[i][1]);
            }
            
            // No cerramos la curva, dejándola abierta
            
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar una curva de Bézier cúbica (4 puntos de control)
        drawBezierCurve: function(points, color, lineWidth, steps = 100, closeCurve = false) {
            if (points.length < 4) return;
            
            const p0 = points[0];
            const p1 = points[1];
            const p2 = points[2];
            const p3 = points[3];
            
            const curvePoints = [];
            
            for (let i = 0; i <= steps; i++) {
                const t = i / steps;
                const t2 = t * t;
                const t3 = t2 * t;
                const mt = 1 - t;
                const mt2 = mt * mt;
                const mt3 = mt2 * mt;
                
                // Fórmula de Bézier cúbica: B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
                const x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0];
                const y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1];
                
                curvePoints.push([Math.round(x), Math.round(y)]);
            }
            
            if (closeCurve) {
                // Si se quiere cerrar la curva, usar las funciones de polígono
                if (state.algorithm === 'BASIC') {
                    this.drawPolygonBasic(curvePoints, color, lineWidth);
                } else {
                    this.drawPolygonPygame(curvePoints, color, lineWidth);
                }
            } else {
                // Si no se quiere cerrar la curva, usar las funciones de curva abierta
                if (state.algorithm === 'BASIC') {
                    this.drawCurveBasic(curvePoints, color, lineWidth);
                } else {
                    this.drawCurvePygame(curvePoints, color, lineWidth);
                }
            }
        },
        
        // Función para dibujar a mano alzada
        drawFreehand: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            if (state.algorithm === 'BASIC') {
                // Usar DDA para dibujar líneas entre puntos consecutivos
                for (let i = 0; i < points.length - 1; i++) {
                    this.drawLineDDA(
                        points[i][0], points[i][1],
                        points[i + 1][0], points[i + 1][1],
                        color, lineWidth
                    );
                }
            } else {
                ctx.beginPath();
                ctx.moveTo(points[0][0], points[0][1]);
                
                for (let i = 1; i < points.length; i++) {
                    ctx.lineTo(points[i][0], points[i][1]);
                }
                
                ctx.strokeStyle = color;
                ctx.lineWidth = lineWidth;
                ctx.stroke();
            }
        }
    };
    
    // Función para dibujar una forma
    function drawShape(shape, preview = false) {
        const { type, points, color, lineWidth, algorithm } = shape;
        
        switch (type) {
            case 'freehand':
                drawingFunctions.drawFreehand(points, color, lineWidth);
                break;
                
            case 'line':
                if (points.length >= 2) {
                    const [x1, y1] = points[0];
                    const [x2, y2] = points[points.length - 1];
                    
                    if (algorithm === 'BASIC') {
                        drawingFunctions.drawLineBresenham(x1, y1, x2, y2, color, lineWidth);
                    } else {
                        drawingFunctions.drawLinePygame(x1, y1, x2, y2, color, lineWidth);
                    }
                }
                break;
                
            case 'circle':
                if (points.length >= 2) {
                    const [centerX, centerY] = points[0];
                    const [pointX, pointY] = points[1];
                    const radius = Math.hypot(pointX - centerX, pointY - centerY);
                    
                    if (algorithm === 'BASIC') {
                        drawingFunctions.drawCircleBresenham(centerX, centerY, radius, color, lineWidth);
                    } else {
                        drawingFunctions.drawCirclePygame(centerX, centerY, radius, color, lineWidth);
                    }
                }
                break;
                
            case 'ellipse':
                if (points.length >= 2) {
                    const [centerX, centerY] = points[0];
                    const [pointX, pointY] = points[1];
                    const radiusX = Math.abs(pointX - centerX);
                    const radiusY = Math.abs(pointY - centerY);
                    
                    if (algorithm === 'BASIC') {
                        drawingFunctions.drawEllipseBresenham(centerX, centerY, radiusX, radiusY, color, lineWidth);
                    } else {
                        drawingFunctions.drawEllipsePygame(centerX, centerY, radiusX, radiusY, color, lineWidth);
                    }
                }
                break;
                
            case 'rectangle':
                if (points.length >= 2) {
                    const [x1, y1] = points[0];
                    const [x2, y2] = points[1];
                    
                    if (algorithm === 'BASIC') {
                        drawingFunctions.drawRectangleBasic(x1, y1, x2, y2, color, lineWidth);
                    } else {
                        drawingFunctions.drawRectanglePygame(x1, y1, x2, y2, color, lineWidth);
                    }
                }
                break;
                
            case 'triangle':
                if (points.length >= 3) {
                    drawingFunctions.drawTriangle(points, color, lineWidth);
                } else if (preview && points.length === 2) {
                    // Para la vista previa, calcular el tercer punto del triángulo
                    const [x1, y1] = points[0];
                    const [x2, y2] = points[1];
                    const x3 = x1 + (x2 - x1) * 2;
                    const y3 = y1;
                    drawingFunctions.drawTriangle([points[0], points[1], [x3, y3]], color, lineWidth);
                }
                break;
                
            case 'polygon':
                if (algorithm === 'BASIC') {
                    drawingFunctions.drawPolygonBasic(points, color, lineWidth);
                } else {
                    drawingFunctions.drawPolygonPygame(points, color, lineWidth);
                }
                break;
                
            case 'bezier':
                if (points.length >= 4) {
                    // Por defecto, no cerramos la curva (curva abierta)
                    drawingFunctions.drawBezierCurve(points, color, lineWidth, 100, false);
                } else if (preview) {
                    // Para la vista previa, mostrar los puntos de control
                    for (let i = 0; i < points.length - 1; i++) {
                        drawingFunctions.drawLinePygame(
                            points[i][0], points[i][1],
                            points[i+1][0], points[i+1][1],
                            color, 1
                        );
                    }
                }
                break;
                
            case 'bezier-closed':
                if (points.length >= 4) {
                    // Curva cerrada (conecta el punto final con el inicial)
                    drawingFunctions.drawBezierCurve(points, color, lineWidth, 100, true);
                } else if (preview) {
                    // Para la vista previa, mostrar los puntos de control
                    for (let i = 0; i < points.length - 1; i++) {
                        drawingFunctions.drawLinePygame(
                            points[i][0], points[i][1],
                            points[i+1][0], points[i+1][1],
                            color, 1
                        );
                    }
                }
                break;
                
            case 'erase-free':
                // No necesitamos hacer nada especial aquí, se maneja en los eventos del mouse
                break;
                
            case 'erase-area':
                if (points.length >= 2) {
                    const [x1, y1] = points[0];
                    const [x2, y2] = points[1];
                    
                    // Dibujar un rectángulo con línea punteada para mostrar el área a borrar
                    if (preview) {
                        ctx.setLineDash([5, 5]);
                        ctx.strokeStyle = '#FF0000';
                        ctx.lineWidth = 1;
                        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
                        ctx.setLineDash([]);
                    }
                }
                break;
        }
    }
    
    // Función para comunicarse con la API de dibujo
    async function callDrawingAPI(action, data = {}) {
        try {
            const response = await fetch('/paint/api/draw/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    action: action,
                    ...data
                })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Error al comunicarse con la API de dibujo:', error);
            return { success: false, error: error.message };
        }
    }
    
    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Función para redibujarlo todo
    function redrawCanvas() {
        // Limpiar el canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar todas las formas
        for (const shape of state.shapes) {
            drawShape(shape);
        }
        
        // Dibujar la forma actual si estamos dibujando
        if (state.isDrawing && state.currentShape) {
            drawShape(state.currentShape, true);
        }
        
        // Dibujar puntos de control para formas en progreso
        if (state.isDrawing && state.currentShape && state.currentTool !== 'freehand') {
            state.currentShape.points.forEach(point => {
                ctx.beginPath();
                ctx.arc(point[0], point[1], 4, 0, Math.PI * 2);
                ctx.fillStyle = state.currentColor;
                ctx.fill();
            });
        }
    }
    
    // Función para cambiar la herramienta activa
    function setActiveTool(tool) {
        // Desactivar todos los botones
        Object.values(toolButtons).forEach(button => {
            if (button) button.classList.remove('active');
        });
        
        // Activar el botón de la herramienta seleccionada
        if (toolButtons[tool]) {
            toolButtons[tool].classList.add('active');
        }
        
        // Actualizar el estado
        if (tool === 'grid') {
            // Si es la herramienta de cuadrícula, solo activamos/desactivamos la cuadrícula
            toggleGrid();
            // Mantenemos la herramienta actual
            if (toolButtons[state.currentTool]) {
                toolButtons[state.currentTool].classList.add('active');
            }
        } else {
            state.currentTool = tool;
        }
        
        // Actualizar el texto en español
        let toolName = '';
        switch (tool) {
            case 'freehand': toolName = 'Trazo Libre'; break;
            case 'line': toolName = 'Línea'; break;
            case 'circle': toolName = 'Círculo'; break;
            case 'bezier': toolName = 'Curva Bézier Abierta'; break;
            case 'bezier-closed': toolName = 'Curva Bézier Cerrada'; break;
            case 'erase-free': toolName = 'Borrador a Mano Alzada'; break;
            case 'erase-area': toolName = 'Borrador de Área'; break;
            case 'grid': toolName = 'Cuadrícula'; break;
            case 'rectangle': toolName = 'Rectángulo'; break;
            case 'triangle': toolName = 'Triángulo'; break;
            case 'polygon': toolName = 'Polígono'; break;
            case 'ellipse': toolName = 'Elipse'; break;
            default: toolName = tool.charAt(0).toUpperCase() + tool.slice(1);
        }
        
        currentToolDisplay.textContent = `Herramienta: ${toolName}`;
    }
    
    // Función para mostrar/ocultar la cuadrícula
    function toggleGrid() {
        state.showGrid = !state.showGrid;
        const gridBackground = document.querySelector('.grid-background');
        if (state.showGrid) {
            gridBackground.style.display = 'block';
        } else {
            gridBackground.style.display = 'none';
        }
    }
    
    // Función para cambiar el color activo
    function setActiveColor(color) {
        state.currentColor = color;
        
        // Actualizar la visualización del color
        document.querySelector('.color-preview').style.backgroundColor = color;
        document.querySelector('.color-value').textContent = color;
        customColorInput.value = color;
        
        // Actualizar el estado
        currentColorDisplay.textContent = `Color: ${color}`;
        
        // Actualizar la selección visual
        document.querySelectorAll('.color-swatch').forEach(swatch => {
            swatch.classList.remove('selected');
            if (swatch.getAttribute('data-color') === color) {
                swatch.classList.add('selected');
            }
        });
    }
    
    // Función para cambiar el grosor de línea
    function setStrokeWidth(width) {
        state.lineWidth = width;
        strokeWidthValue.textContent = `${width}px`;
        currentStrokeDisplay.textContent = `Grosor: ${width}px`;
    }
    
    // Función para cambiar la pestaña activa
    function setActiveTab(tab) {
        state.activeTab = tab;
        
        // Actualizar las clases de las pestañas
        drawTab.classList.toggle('active', tab === 'draw');
        shapesTab.classList.toggle('active', tab === 'shapes');
        
        // Mostrar/ocultar las herramientas correspondientes
        drawTools.style.display = tab === 'draw' ? 'grid' : 'none';
        shapesTools.style.display = tab === 'shapes' ? 'grid' : 'none';
    }
    
    // Función para alternar el modo de pantalla completa
    function toggleFullscreen() {
        const appContainer = document.querySelector('.app-container');
        
        if (!state.isFullscreen) {
            if (appContainer.requestFullscreen) {
                appContainer.requestFullscreen();
            } else if (appContainer.mozRequestFullScreen) {
                appContainer.mozRequestFullScreen();
            } else if (appContainer.webkitRequestFullscreen) {
                appContainer.webkitRequestFullscreen();
            } else if (appContainer.msRequestFullscreen) {
                appContainer.msRequestFullscreen();
            }
            fullscreenToggleBtn.innerHTML = '<i class="fas fa-compress"></i>';
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
            fullscreenToggleBtn.innerHTML = '<i class="fas fa-expand"></i>';
        }
        
        state.isFullscreen = !state.isFullscreen;
    }
    
    // Inicializar la herramienta activa
    setActiveTool('freehand');
    
    // Inicializar el color activo
    setActiveColor('#FFBF00');
    
    // Inicializar el grosor de línea
    setStrokeWidth(2);
    
    // Inicializar la pestaña activa
    setActiveTab('draw');
    
    // Inicializar la cuadrícula
    const gridBackground = document.querySelector('.grid-background');
    if (state.showGrid) {
        gridBackground.style.display = 'block';
    } else {
        gridBackground.style.display = 'none';
    }
    
    // Eventos para los botones de herramientas
    Object.entries(toolButtons).forEach(([tool, button]) => {
        if (button) {
            button.addEventListener('click', () => {
                setActiveTool(tool);
            });
        }
    });
    
    // Eventos para las pestañas
    drawTab.addEventListener('click', () => setActiveTab('draw'));
    shapesTab.addEventListener('click', () => setActiveTab('shapes'));
    
    // Evento para el selector de color
    colorDisplay.addEventListener('click', () => {
        colorPicker.style.display = colorPicker.style.display === 'grid' ? 'none' : 'grid';
    });
    
    // Eventos para los swatches de colores
    document.querySelectorAll('.color-swatch').forEach(swatch => {
        if (!swatch.classList.contains('custom')) {
            swatch.addEventListener('click', () => {
                const color = swatch.getAttribute('data-color');
                setActiveColor(color);
                colorPicker.style.display = 'none';
            });
        }
    });
    
    // Evento para el selector de color personalizado
    customColorInput.addEventListener('input', (e) => {
        setActiveColor(e.target.value);
    });
    
    // Evento para el control de grosor de línea
    strokeWidthInput.addEventListener('input', (e) => {
        setStrokeWidth(parseInt(e.target.value));
    });
    
    // Evento para limpiar el canvas
    clearCanvasBtn.addEventListener('click', async () => {
        if (confirm('¿Estás seguro de que quieres limpiar el lienzo?')) {
            // Limpiar el estado local
            state.shapes = [];
            state.undoStack = [];
            state.redoStack = [];
            
            // Usar la API para limpiar el lienzo en el servidor
            const result = await callDrawingAPI('clear');
            
            if (result.success && result.image) {
                // Actualizar el canvas con la imagen devuelta por la API
                const img = new Image();
                img.onload = function() {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0);
                };
                img.src = result.image;
            } else {
                // Si hay un error, al menos limpiar el canvas local
                redrawCanvas();
            }
        }
    });
    
    // Evento para guardar la imagen
    saveImageBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = 'graficador-pygame.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
    
    // Evento para alternar el modo de pantalla completa
    fullscreenToggleBtn.addEventListener('click', toggleFullscreen);
    
    // Eventos del mouse para el canvas
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        state.isDrawing = true;
        
        // Manejar herramientas de borrado
        if (state.currentTool === 'erase-free' || state.currentTool === 'erase-area') {
            state.currentShape = {
                type: state.currentTool,
                points: [[x, y]],
                color: '#ffffff', // Color blanco para borrar
                lineWidth: state.currentTool === 'erase-free' ? state.lineWidth * 2 : state.lineWidth,
                algorithm: 'erase'
            };
            
            if (state.currentTool === 'erase-free') {
                // Para el borrador a mano alzada, añadimos la forma inmediatamente
                if (!state.shapes.includes(state.currentShape)) {
                    state.shapes.push(state.currentShape);
                }
                
                // Llamar a la API para borrar
                callDrawingAPI('erase', {
                    erase_data: {
                        type: 'free',
                        point: [x, y],
                        size: state.lineWidth * 2
                    }
                });
                
                redrawCanvas();
            }
            return;
        }
        
        // Crear una nueva forma para herramientas de dibujo
        state.currentShape = {
            type: state.currentTool,
            points: [[x, y]],
            color: state.currentColor,
            lineWidth: state.lineWidth,
            algorithm: state.algorithm
        };
        
        // Para el trazo libre, añadimos la forma inmediatamente
        if (state.currentTool === 'freehand') {
            if (!state.shapes.includes(state.currentShape)) {
                state.shapes.push(state.currentShape);
            }
            redrawCanvas();
            return;
        }
        
        // Para el polígono, necesitamos manejar clics múltiples
        if (state.currentTool === 'polygon') {
            // Si ya hay una forma en progreso, añadir el punto
            if (state.shapes.length > 0 &&
                (state.shapes[state.shapes.length - 1].type === 'polygon') &&
                !state.shapes[state.shapes.length - 1].completed) {
                
                state.shapes[state.shapes.length - 1].points.push([x, y]);
                state.currentShape = state.shapes[state.shapes.length - 1];
                
                redrawCanvas();
                return;
            }
        }
        
        // Para el triángulo, necesitamos 3 puntos
        if (state.currentTool === 'triangle') {
            if (state.shapes.length > 0 &&
                (state.shapes[state.shapes.length - 1].type === 'triangle') &&
                state.shapes[state.shapes.length - 1].points.length < 3) {
                
                state.shapes[state.shapes.length - 1].points.push([x, y]);
                state.currentShape = state.shapes[state.shapes.length - 1];
                
                if (state.currentShape.points.length >= 3) {
                    state.currentShape.completed = true;
                    state.isDrawing = false;
                }
                
                redrawCanvas();
                return;
            }
        }
        
        // Para la curva de Bézier, necesitamos 4 puntos
        if (state.currentTool === 'bezier' || state.currentTool === 'bezier-closed') {
            if (state.shapes.length > 0 &&
                (state.shapes[state.shapes.length - 1].type === state.currentTool) &&
                state.shapes[state.shapes.length - 1].points.length < 4) {
                
                state.shapes[state.shapes.length - 1].points.push([x, y]);
                state.currentShape = state.shapes[state.shapes.length - 1];
                
                if (state.currentShape.points.length >= 4) {
                    state.currentShape.completed = true;
                    state.isDrawing = false;
                }
                
                redrawCanvas();
                return;
            }
        }
    });
    
    canvas.addEventListener('mousemove', async (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Actualizar las coordenadas
        coordinatesDisplay.textContent = `X: ${Math.round(x)}, Y: ${Math.round(y)}`;
        
        if (state.isDrawing && state.currentShape) {
            // Para las herramientas de borrado
            if (state.currentTool === 'erase-free') {
                state.currentShape.points.push([x, y]);
                
                // Llamar a la API para borrar
                const result = await callDrawingAPI('erase', {
                    erase_data: {
                        type: 'free',
                        point: [x, y],
                        size: state.lineWidth * 2
                    }
                });
                
                if (result.success && result.image) {
                    const img = new Image();
                    img.onload = function() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0);
                    };
                    img.src = result.image;
                } else {
                    redrawCanvas();
                }
                return;
            }
            
            // Para el trazo libre, añadir el punto actual
            if (state.currentTool === 'freehand') {
                state.currentShape.points.push([x, y]);
                redrawCanvas();
                return;
            }
            
            // Para herramientas que solo necesitan el punto inicial y final
            if (state.currentShape.points.length > 1 &&
                !['polygon', 'triangle', 'bezier'].includes(state.currentTool)) {
                state.currentShape.points[state.currentShape.points.length - 1] = [x, y];
            } else if (!['polygon', 'triangle', 'bezier'].includes(state.currentTool)) {
                state.currentShape.points.push([x, y]);
            }
            
            // Redibujar el canvas con la vista previa
            redrawCanvas();
        }
    });
    
    canvas.addEventListener('mouseup', async (e) => {
        if (state.isDrawing && state.currentShape) {
            // Para las herramientas de borrado
            if (state.currentTool === 'erase-free') {
                state.currentShape.completed = true;
                state.isDrawing = false;
                state.currentShape = null;
                
                // Limpiar la pila de rehacer cuando se borra algo
                state.redoStack = [];
                return;
            }
            
            if (state.currentTool === 'erase-area') {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                // Obtener los puntos inicial y final para definir el área
                const startPoint = state.currentShape.points[0];
                const endPoint = [x, y];
                
                // Llamar a la API para borrar un área
                const result = await callDrawingAPI('erase', {
                    erase_data: {
                        type: 'area',
                        start_point: startPoint,
                        end_point: endPoint
                    }
                });
                
                if (result.success && result.image) {
                    const img = new Image();
                    img.onload = function() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0);
                    };
                    img.src = result.image;
                }
                
                state.currentShape.completed = true;
                state.isDrawing = false;
                state.currentShape = null;
                
                // Limpiar la pila de rehacer cuando se borra algo
                state.redoStack = [];
                return;
            }
            
            // Para el trazo libre, completar la forma
            if (state.currentTool === 'freehand') {
                state.currentShape.completed = true;
                
                // Usar la API para dibujar con PygameDrawLibrary
                const result = await callDrawingAPI('draw', {
                    shape: {
                        type: 'freehand',
                        points: state.currentShape.points,
                        color: state.currentShape.color,
                        line_width: state.currentShape.lineWidth
                    }
                });
                
                if (result.success && result.image) {
                    // Actualizar el canvas con la imagen devuelta por la API
                    const img = new Image();
                    img.onload = function() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0);
                    };
                    img.src = result.image;
                }
                
                state.isDrawing = false;
                state.currentShape = null;
                
                // Limpiar la pila de rehacer cuando se dibuja algo nuevo
                state.redoStack = [];
                return;
            }
            
            // Para el polígono, no completamos la forma hasta que se haga doble clic
            if (state.currentTool === 'polygon') {
                if (!state.shapes.includes(state.currentShape)) {
                    state.shapes.push(state.currentShape);
                }
                state.isDrawing = false;
                return;
            }
            
            // Para el triángulo y la curva de Bézier, necesitamos puntos adicionales
            if (state.currentTool === 'triangle' || state.currentTool === 'bezier' || state.currentTool === 'bezier-closed') {
                if (!state.shapes.includes(state.currentShape)) {
                    state.shapes.push(state.currentShape);
                }
                
                if ((state.currentTool === 'triangle' && state.currentShape.points.length < 3) ||
                    ((state.currentTool === 'bezier' || state.currentTool === 'bezier-closed') && state.currentShape.points.length < 4)) {
                    state.isDrawing = false;
                    return;
                }
                
                // Si tenemos suficientes puntos, dibujar con la API
                if ((state.currentTool === 'triangle' && state.currentShape.points.length >= 3) ||
                    ((state.currentTool === 'bezier' || state.currentTool === 'bezier-closed') && state.currentShape.points.length >= 4)) {
                    
                    const result = await callDrawingAPI('draw', {
                        shape: {
                            type: state.currentTool,
                            points: state.currentShape.points,
                            color: state.currentShape.color,
                            line_width: state.currentShape.lineWidth
                        }
                    });
                    
                    if (result.success && result.image) {
                        const img = new Image();
                        img.onload = function() {
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            ctx.drawImage(img, 0, 0);
                        };
                        img.src = result.image;
                    }
                }
            }
            
            // Para las demás herramientas, completamos la forma
            if (!state.shapes.includes(state.currentShape)) {
                state.shapes.push(state.currentShape);
                
                // Usar la API para dibujar con PygameDrawLibrary
                const result = await callDrawingAPI('draw', {
                    shape: {
                        type: state.currentTool,
                        points: state.currentShape.points,
                        color: state.currentShape.color,
                        line_width: state.currentShape.lineWidth
                    }
                });
                
                if (result.success && result.image) {
                    const img = new Image();
                    img.onload = function() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0);
                    };
                    img.src = result.image;
                }
            }
            
            state.currentShape.completed = true;
            state.isDrawing = false;
            state.currentShape = null;
            
            // Limpiar la pila de rehacer cuando se dibuja algo nuevo
            state.redoStack = [];
        }
    });
    
    canvas.addEventListener('dblclick', (e) => {
        // Completar un polígono con doble clic
        if (state.currentTool === 'polygon' &&
            state.shapes.length > 0 &&
            state.shapes[state.shapes.length - 1].type === 'polygon' &&
            !state.shapes[state.shapes.length - 1].completed) {
            
            state.shapes[state.shapes.length - 1].completed = true;
            redrawCanvas();
        }
    });
    
    // Eventos de teclado
    document.addEventListener('keydown', (e) => {
        // Deshacer con Ctrl+Z
        if (e.ctrlKey && e.key === 'z') {
            if (state.shapes.length > 0) {
                const lastShape = state.shapes.pop();
                state.undoStack.push(lastShape);
                redrawCanvas();
            }
        }
        
        // Rehacer con Ctrl+Y
        if (e.ctrlKey && e.key === 'y') {
            if (state.undoStack.length > 0) {
                const shape = state.undoStack.pop();
                state.shapes.push(shape);
                redrawCanvas();
            }
        }
        
        // Mostrar/ocultar cuadrícula con G
        if (e.key.toLowerCase() === 'g') {
            toggleGrid();
        }
        
        // Borrador a mano alzada con E
        if (e.key.toLowerCase() === 'e') {
            setActiveTool('erase-free');
        }
        
        // Borrador de área con A
        if (e.key.toLowerCase() === 'a') {
            setActiveTool('erase-area');
        }
        
        // Guardar con Ctrl+S
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveImageBtn.click();
        }
        
        // Cancelar dibujo actual con Escape
        if (e.key === 'Escape') {
            if (state.isDrawing) {
                state.isDrawing = false;
                state.currentShape = null;
                redrawCanvas();
            }
        }
        
        // Limpiar canvas con Delete
        if (e.key === 'Delete') {
            clearCanvasBtn.click();
        }
        
        // Atajos de teclado para herramientas
        switch (e.key.toLowerCase()) {
            case 'f':
                setActiveTab('draw');
                setActiveTool('freehand');
                break;
            case 'l':
                setActiveTab('draw');
                setActiveTool('line');
                break;
            case 'c':
                setActiveTab('draw');
                setActiveTool('circle');
                break;
            case 'b':
                setActiveTab('draw');
                setActiveTool('bezier');
                break;
            case 'z':
                setActiveTab('draw');
                setActiveTool('bezier-closed');
                break;
            case 'g':
                setActiveTab('draw');
                setActiveTool('grid');
                break;
            case 'r':
                setActiveTab('shapes');
                setActiveTool('rectangle');
                break;
            case 't':
                setActiveTab('shapes');
                setActiveTool('triangle');
                break;
            case 'p':
                setActiveTab('shapes');
                setActiveTool('polygon');
                break;
            case 'e':
                setActiveTab('shapes');
                setActiveTool('ellipse');
                break;
        }
    });
    
    // Ocultar el selector de color al hacer clic fuera de él
    document.addEventListener('click', (e) => {
        if (!colorDisplay.contains(e.target) && !colorPicker.contains(e.target)) {
            colorPicker.style.display = 'none';
        }
    });
});