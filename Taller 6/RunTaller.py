# Taller número 6: Análisis Numérico y Visualización con NumPy y Matplotlib
# Solución completa con todos los ejercicios en un mismo archivo

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

print("=" * 80)
print("TALLER 6: ANÁLISIS NUMÉRICO Y VISUALIZACIÓN CON NUMPY Y MATPLOTLIB")
print("=" * 80)

# Ejercicio 1: Creación y Manipulación de Arrays
print("\nEjercicio 1: Creación y Manipulación de Arrays")
print("-" * 50)

# Crear un array A con valores del 1 al 15
A = np.arange(1, 16)
print("Array original A:")
print(A)

# Redimensionar el array a una matriz de 3x5
A = A.reshape(3, 5)
print("\nArray A redimensionado a 3x5:")
print(A)


# Ejercicio 2: Operaciones Básicas
print("\n\nEjercicio 2: Operaciones Básicas")
print("-" * 50)

# Calcular la suma de todos los elementos
suma = np.sum(A)
print(f"Suma de los elementos: {suma}")

# Calcular la media de todos los elementos
media = np.mean(A)
print(f"Media de los elementos: {media}")

# Calcular el producto de todos los elementos
producto = np.prod(A)
print(f"Producto de los elementos: {producto}")


# Ejercicio 3: Acceso y Slicing
print("\n\nEjercicio 3: Acceso y Slicing")
print("-" * 50)

# Seleccionar el segundo y tercer elemento de la segunda fila
# En Python, los índices comienzan en 0, por lo que:
# - La segunda fila tiene índice 1
# - El segundo elemento tiene índice 1
# - El tercer elemento tiene índice 2
elementos_seleccionados = A[1, 1:3]

print("Segundo y tercer elemento de la segunda fila:")
print(elementos_seleccionados)


# Ejercicio 4: Indexación Booleana
print("\n\nEjercicio 4: Indexación Booleana")
print("-" * 50)

# Crear una máscara booleana para elementos mayores que 7
mascara = A > 7

# Crear el array B con los elementos que cumplen la condición
B = A[mascara]

print("Máscara booleana (elementos > 7):")
print(mascara)

print("\nArray B (elementos de A mayores que 7):")
print(B)


# Ejercicio 5: Álgebra Lineal
print("\n\nEjercicio 5: Álgebra Lineal")
print("-" * 50)

# Para el álgebra lineal, necesitamos una matriz cuadrada
# Vamos a crear una matriz cuadrada C de 3x3 a partir de los primeros 9 elementos de A
C = A.flatten()[:9].reshape(3, 3)
print("Matriz C (3x3 a partir de los primeros 9 elementos de A):")
print(C)

# Calcular el determinante de C
determinante = np.linalg.det(C)
print(f"\nDeterminante de C: {determinante}")

# Verificar si la matriz es invertible (determinante != 0)
if determinante != 0:
    # Calcular la inversa de C
    inversa = np.linalg.inv(C)
    print("\nInversa de C:")
    print(inversa)
    
    # Verificar la inversa multiplicando C * C^-1
    print("\nVerificación (C * C^-1 ≈ I):")
    print(np.round(np.dot(C, inversa), decimals=10))  # Redondear para manejar errores de punto flotante
else:
    print("\nLa matriz C no es invertible (determinante = 0)")


# Ejercicio 6: Estadísticas con NumPy
print("\n\nEjercicio 6: Estadísticas con NumPy")
print("-" * 50)

# Crear un array D con 100 números aleatorios (distribución normal)
np.random.seed(42)  # Para reproducibilidad
D = np.random.normal(loc=0, scale=1, size=100)

print(f"Array D (mostrando primeros 10 elementos):\n{D[:10]} ...")

# Calcular el valor máximo
maximo = np.max(D)
print(f"\nValor máximo: {maximo}")

# Calcular el valor mínimo
minimo = np.min(D)
print(f"Valor mínimo: {minimo}")

# Calcular la media
media_d = np.mean(D)
print(f"Media: {media_d}")

# Calcular la desviación estándar
desviacion_estandar = np.std(D)
print(f"Desviación estándar: {desviacion_estandar}")


# Ejercicio 7: Gráfico Básico
print("\n\nEjercicio 7: Gráfico Básico")
print("-" * 50)
print("Graficando funciones seno y coseno en el rango -2π a 2π...")

# Crear un array de valores x en el rango de -2π a 2π
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# Calcular los valores de seno y coseno
seno = np.sin(x)
coseno = np.cos(x)

# Crear la figura y los ejes
plt.figure(figsize=(10, 6))

# Graficar seno y coseno
plt.plot(x, seno, label='sen(x)', color='blue')
plt.plot(x, coseno, label='cos(x)', color='red')

# Añadir una línea horizontal en y=0
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

# Configurar etiquetas y título
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Funciones Seno y Coseno en el rango de -2π a 2π')

# Configurar los ticks del eje x para mostrar múltiplos de π
plt.xticks(
    [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    [r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$']
)

# Añadir leyenda y cuadrícula
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

# Ajustar los límites del eje y
plt.ylim(-1.5, 1.5)

# Guardar la figura (opcional)
plt.savefig('funciones_trigonometricas.png', dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.show()


# Ejercicio 8: Gráficos de Dispersión
print("\n\nEjercicio 8: Gráficos de Dispersión")
print("-" * 50)
print("Creando gráfico de dispersión con los valores de D...")

# Crear el índice para el eje x
indices = np.arange(len(D))

# Crear la figura y los ejes
plt.figure(figsize=(12, 6))

# Crear el gráfico de dispersión
plt.scatter(indices, D, color='blue', alpha=0.7, label='Valores de D')

# Añadir una línea horizontal en y=0
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

# Configurar etiquetas y título
plt.xlabel('Índice')
plt.ylabel('Valor')
plt.title('Gráfico de Dispersión del Array D')

# Añadir leyenda y cuadrícula
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

# Guardar la figura (opcional)
plt.savefig('grafico_dispersion.png', dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.show()


# Ejercicio 9: Histogramas
print("\n\nEjercicio 9: Histogramas")
print("-" * 50)
print("Creando histograma de los valores de D...")

# Crear la figura y los ejes
plt.figure(figsize=(12, 6))

# Calcular el número óptimo de bins usando la regla de Sturges
n_bins = int(np.ceil(np.log2(len(D)) + 1))
print(f"Número de bins según regla de Sturges: {n_bins}")

# Crear el histograma
hist_counts, bin_edges, patches = plt.hist(D, bins=n_bins, alpha=0.7, 
                                         color='skyblue', edgecolor='black',
                                         label=f'Histograma ({n_bins} bins)')

# Añadir una curva de distribución normal teórica
x = np.linspace(min(D), max(D), 100)
y = stats.norm.pdf(x, np.mean(D), np.std(D)) * len(D) * (bin_edges[1] - bin_edges[0])
plt.plot(x, y, 'r-', linewidth=2, label='Distribución Normal Teórica')

# Configurar etiquetas y título
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma del Array D')

# Añadir leyenda y cuadrícula
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

# Guardar la figura (opcional)
plt.savefig('histograma.png', dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.show()


# Ejercicio 10: Manipulación de Imágenes con Matplotlib
print("\n\nEjercicio 10: Manipulación de Imágenes con Matplotlib")
print("-" * 50)
print("Creando y manipulando una imagen sintética...")

# Crear una imagen de muestra con patrones simples
def create_sample_image(size=128):
    """Crear una imagen de muestra con patrones simples"""
    # Crear una rejilla de coordenadas
    y, x = np.ogrid[-size/2:size/2, -size/2:size/2]
    
    # Crear canales RGB con patrones diferentes
    r = np.sin(0.1 * np.sqrt(x**2 + y**2))
    g = np.sin(0.2 * x) * np.cos(0.2 * y)
    b = np.cos(0.1 * np.sqrt(x**2 + y**2 + 100))
    
    # Normalizar a [0, 1]
    r = (r - r.min()) / (r.max() - r.min())
    g = (g - g.min()) / (g.max() - g.min())
    b = (b - b.min()) / (b.max() - b.min())
    
    # Combinar canales
    rgb = np.stack([r, g, b], axis=2)
    return rgb

# Crear imagen de muestra
img_original = create_sample_image(256)

# Convertir a escala de grises usando el método de luminosidad ponderada
# Fórmula: 0.299*R + 0.587*G + 0.114*B
img_gris = np.dot(img_original[..., :3], [0.299, 0.587, 0.114])

# Crear la figura y los subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Mostrar la imagen original
axes[0].imshow(img_original)
axes[0].set_title('Imagen Original')
axes[0].axis('off')

# Mostrar la imagen en escala de grises
axes[1].imshow(img_gris, cmap='gray')
axes[1].set_title('Imagen en Escala de Grises')
axes[1].axis('off')

# Guardar la figura (opcional)
plt.savefig('manipulacion_imagen.png', dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.tight_layout()
plt.show()

