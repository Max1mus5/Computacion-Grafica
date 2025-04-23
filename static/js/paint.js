/**
 * Paint Web - Aplicación de dibujo para navegador
 * Basado en la biblioteca PygameDrawLibrary
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const canvas = document.getElementById('paint-canvas');
    const ctx = canvas.getContext('2d');
    const coordinatesDisplay = document.getElementById('coordinates');
    const currentToolDisplay = document.getElementById('current-tool');
    const currentColorDisplay = document.getElementById('current-color');
    const colorPicker = document.getElementById('color-picker');
    const lineWidthInput = document.getElementById('line-width');
    const lineWidthValue = document.getElementById('line-width-value');
    const algorithmSelect = document.getElementById('algorithm-select');
    const clearCanvasBtn = document.getElementById('clear-canvas');
    const saveBtn = document.getElementById('save-btn');
    const loadBtn = document.getElementById('load-btn');
    
    // Herramientas
    const toolButtons = {
        pencil: document.getElementById('pencil-tool'),
        line: document.getElementById('line-tool'),
        rectangle: document.getElementById('rectangle-tool'),
        circle: document.getElementById('circle-tool'),
        polygon: document.getElementById('polygon-tool'),
        curve: document.getElementById('curve-tool'),
        eraser: document.getElementById('eraser-tool')
    };
    
    // Estado de la aplicación
    const state = {
        currentTool: 'pencil',
        currentColor: '#000000',
        backgroundColor: '#ffffff',
        lineWidth: 2,
        algorithm: 'BASIC',
        isDrawing: false,
        points: [],
        shapes: [],
        currentShape: null,
        undoStack: [],
        redoStack: []
    };
    
    // Inicializar el canvas
    ctx.fillStyle = state.backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
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
        
        // Función para dibujar una línea con la API de Canvas
        drawLinePygame: function(x1, y1, x2, y2, color, lineWidth) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar un círculo con el algoritmo del punto medio
        drawCircleMidpoint: function(centerX, centerY, radius, color) {
            let x = 0;
            let y = radius;
            let d = 1 - radius;
            
            this.drawCirclePoints(centerX, centerY, x, y, color);
            
            while (x < y) {
                if (d < 0) {
                    d = d + 2 * x + 3;
                } else {
                    d = d + 2 * (x - y) + 5;
                    y--;
                }
                x++;
                this.drawCirclePoints(centerX, centerY, x, y, color);
            }
        },
        
        // Función auxiliar para dibujar los puntos de un círculo
        drawCirclePoints: function(xc, yc, x, y, color) {
            const points = [
                [xc + x, yc + y], [xc - x, yc + y], [xc + x, yc - y], [xc - x, yc - y],
                [xc + y, yc + x], [xc - y, yc + x], [xc + y, yc - x], [xc - y, yc - x]
            ];
            
            for (const [px, py] of points) {
                ctx.fillStyle = color;
                ctx.fillRect(px, py, 1, 1);
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
        
        // Función para dibujar un rectángulo con líneas básicas
        drawRectangleBasic: function(x1, y1, x2, y2, color, lineWidth) {
            const left = Math.min(x1, x2);
            const top = Math.min(y1, y2);
            const right = Math.max(x1, x2);
            const bottom = Math.max(y1, y2);
            
            // Dibujar las cuatro líneas del rectángulo
            this.drawLinePygame(left, top, right, top, color, lineWidth);
            this.drawLinePygame(right, top, right, bottom, color, lineWidth);
            this.drawLinePygame(right, bottom, left, bottom, color, lineWidth);
            this.drawLinePygame(left, bottom, left, top, color, lineWidth);
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
        
        // Función para dibujar un polígono con líneas básicas
        drawPolygonBasic: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            for (let i = 0; i < points.length - 1; i++) {
                this.drawLinePygame(
                    points[i][0], points[i][1],
                    points[i + 1][0], points[i + 1][1],
                    color, lineWidth
                );
            }
        },
        
        // Función para dibujar un polígono con la API de Canvas
        drawPolygonPygame: function(points, color, lineWidth) {
            if (points.length < 2) return;
            
            ctx.beginPath();
            ctx.moveTo(points[0][0], points[0][1]);
            
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i][0], points[i][1]);
            }
            
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        },
        
        // Función para dibujar una curva de Bézier cuadrática
        drawBezierCurve: function(p0, p1, p2, color, lineWidth, steps = 100) {
            const curvePoints = [];
            
            for (let i = 0; i <= steps; i++) {
                const t = i / steps;
                const x = Math.pow(1 - t, 2) * p0[0] + 2 * (1 - t) * t * p1[0] + Math.pow(t, 2) * p2[0];
                const y = Math.pow(1 - t, 2) * p0[1] + 2 * (1 - t) * t * p1[1] + Math.pow(t, 2) * p2[1];
                curvePoints.push([Math.round(x), Math.round(y)]);
            }
            
            if (state.algorithm === 'BASIC') {
                this.drawPolygonBasic(curvePoints, color, lineWidth);
            } else {
                this.drawPolygonPygame(curvePoints, color, lineWidth);
            }
        },
        
        // Función para borrar un área
        eraseArea: function(x1, y1, x2, y2) {
            const left = Math.min(x1, x2);
            const top = Math.min(y1, y2);
            const width = Math.abs(x2 - x1);
            const height = Math.abs(y2 - y1);
            
            ctx.fillStyle = state.backgroundColor;
            ctx.fillRect(left, top, width, height);
        },
        
        // Función para borrar a mano alzada
        eraseFreehand: function(points, lineWidth) {
            if (points.length < 2) return;
            
            ctx.beginPath();
            ctx.moveTo(points[0][0], points[0][1]);
            
            for (let i = 1; i < points.length; i++) {
                ctx.lineTo(points[i][0], points[i][1]);
            }
            
            ctx.strokeStyle = state.backgroundColor;
            ctx.lineWidth = lineWidth;
            ctx.stroke();
        }
    };
    
    // Función para dibujar una forma
    function drawShape(shape, preview = false) {
        const { type, points, color, lineWidth, algorithm } = shape;
        
        switch (type) {
            case 'pencil':
                if (algorithm === 'BASIC') {
                    for (let i = 0; i < points.length - 1; i++) {
                        drawingFunctions.drawLineDDA(
                            points[i][0], points[i][1],
                            points[i + 1][0], points[i + 1][1],
                            color, lineWidth
                        );
                    }
                } else {
                    drawingFunctions.drawPolygonPygame(points, color, lineWidth);
                }
                break;
                
            case 'line':
                if (points.length >= 2) {
                    const [x1, y1] = points[0];
                    const [x2, y2] = points[points.length - 1];
                    
                    if (algorithm === 'BASIC') {
                        drawingFunctions.drawLineDDA(x1, y1, x2, y2, color, lineWidth);
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
                        drawingFunctions.drawCircleMidpoint(centerX, centerY, radius, color);
                    } else {
                        drawingFunctions.drawCirclePygame(centerX, centerY, radius, color, lineWidth);
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
                
            case 'polygon':
                if (algorithm === 'BASIC') {
                    drawingFunctions.drawPolygonBasic(points, color, lineWidth);
                } else {
                    drawingFunctions.drawPolygonPygame(points, color, lineWidth);
                }
                break;
                
            case 'curve':
                if (points.length >= 3) {
                    drawingFunctions.drawBezierCurve(
                        points[0], points[1], points[2],
                        color, lineWidth
                    );
                }
                break;
                
            case 'eraser':
                if (preview) {
                    // Para la vista previa, solo dibujamos un círculo que sigue al cursor
                    const [x, y] = points[points.length - 1];
                    ctx.beginPath();
                    ctx.arc(x, y, lineWidth / 2, 0, Math.PI * 2);
                    ctx.fillStyle = state.backgroundColor;
                    ctx.fill();
                } else {
                    drawingFunctions.eraseFreehand(points, lineWidth);
                }
                break;
        }
    }
    
    // Función para redibujarlo todo
    function redrawCanvas() {
        // Limpiar el canvas
        ctx.fillStyle = state.backgroundColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar todas las formas
        for (const shape of state.shapes) {
            drawShape(shape);
        }
        
        // Dibujar la forma actual si estamos dibujando
        if (state.isDrawing && state.currentShape) {
            drawShape(state.currentShape, true);
        }
    }
    
    // Función para cambiar la herramienta activa
    function setActiveTool(tool) {
        // Desactivar todos los botones
        Object.values(toolButtons).forEach(button => {
            button.classList.remove('active');
        });
        
        // Activar el botón de la herramienta seleccionada
        toolButtons[tool].classList.add('active');
        
        // Actualizar el estado
        state.currentTool = tool;
        currentToolDisplay.textContent = `Herramienta: ${tool.charAt(0).toUpperCase() + tool.slice(1)}`;
    }
    
    // Inicializar la herramienta activa
    setActiveTool('pencil');
    
    // Eventos para los botones de herramientas
    Object.entries(toolButtons).forEach(([tool, button]) => {
        button.addEventListener('click', () => {
            setActiveTool(tool);
        });
    });
    
    // Evento para el selector de color
    colorPicker.addEventListener('input', (e) => {
        state.currentColor = e.target.value;
        currentColorDisplay.textContent = `Color: ${state.currentColor}`;
    });
    
    // Eventos para los swatches de colores
    document.querySelectorAll('.color-swatch').forEach(swatch => {
        swatch.addEventListener('click', () => {
            const color = swatch.getAttribute('data-color');
            state.currentColor = color;
            colorPicker.value = color;
            currentColorDisplay.textContent = `Color: ${color}`;
        });
    });
    
    // Evento para el control de grosor de línea
    lineWidthInput.addEventListener('input', (e) => {
        state.lineWidth = parseInt(e.target.value);
        lineWidthValue.textContent = `${state.lineWidth}px`;
    });
    
    // Evento para el selector de algoritmo
    algorithmSelect.addEventListener('change', (e) => {
        state.algorithm = e.target.value;
    });
    
    // Evento para limpiar el canvas
    clearCanvasBtn.addEventListener('click', () => {
        if (confirm('¿Estás seguro de que quieres limpiar el lienzo?')) {
            state.shapes = [];
            state.undoStack = [];
            state.redoStack = [];
            redrawCanvas();
        }
    });
    
    // Evento para guardar la imagen
    saveBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = 'paint-web.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
    
    // Evento para cargar una imagen
    loadBtn.addEventListener('click', () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const img = new Image();
                    img.onload = () => {
                        // Limpiar el canvas
                        state.shapes = [];
                        
                        // Dibujar la imagen cargada
                        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        };
        
        input.click();
    });
    
    // Eventos del mouse para el canvas
    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        state.isDrawing = true;
        
        // Crear una nueva forma
        state.currentShape = {
            type: state.currentTool,
            points: [[x, y]],
            color: state.currentColor,
            lineWidth: state.lineWidth,
            algorithm: state.algorithm
        };
        
        // Para el polígono y la curva, necesitamos manejar clics múltiples
        if (state.currentTool === 'polygon' || state.currentTool === 'curve') {
            // Si ya hay una forma en progreso, añadir el punto
            if (state.shapes.length > 0 && 
                (state.shapes[state.shapes.length - 1].type === state.currentTool) &&
                !state.shapes[state.shapes.length - 1].completed) {
                
                state.shapes[state.shapes.length - 1].points.push([x, y]);
                state.currentShape = state.shapes[state.shapes.length - 1];
                
                // Para la curva, completarla después de 3 puntos
                if (state.currentTool === 'curve' && state.currentShape.points.length >= 3) {
                    state.currentShape.completed = true;
                    state.isDrawing = false;
                }
                
                redrawCanvas();
                return;
            }
        }
    });
    
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Actualizar las coordenadas
        coordinatesDisplay.textContent = `X: ${Math.round(x)}, Y: ${Math.round(y)}`;
        
        if (state.isDrawing && state.currentShape) {
            // Para herramientas que necesitan seguimiento continuo
            if (['pencil', 'eraser'].includes(state.currentTool)) {
                state.currentShape.points.push([x, y]);
            } else {
                // Para herramientas que solo necesitan el punto inicial y final
                if (state.currentShape.points.length > 1) {
                    state.currentShape.points[state.currentShape.points.length - 1] = [x, y];
                } else {
                    state.currentShape.points.push([x, y]);
                }
            }
            
            // Redibujar el canvas con la vista previa
            redrawCanvas();
        }
    });
    
    canvas.addEventListener('mouseup', (e) => {
        if (state.isDrawing && state.currentShape) {
            // Para el polígono, no completamos la forma hasta que se haga doble clic
            if (state.currentTool === 'polygon') {
                if (!state.shapes.includes(state.currentShape)) {
                    state.shapes.push(state.currentShape);
                }
                state.isDrawing = false;
                return;
            }
            
            // Para la curva, necesitamos 3 puntos
            if (state.currentTool === 'curve') {
                if (!state.shapes.includes(state.currentShape)) {
                    state.shapes.push(state.currentShape);
                }
                
                if (state.currentShape.points.length < 3) {
                    state.isDrawing = false;
                    return;
                }
            }
            
            // Para las demás herramientas, completamos la forma
            if (!state.shapes.includes(state.currentShape)) {
                state.shapes.push(state.currentShape);
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
        
        // Cancelar dibujo actual con Escape
        if (e.key === 'Escape') {
            if (state.isDrawing) {
                state.isDrawing = false;
                state.currentShape = null;
                redrawCanvas();
            }
        }
    });
});