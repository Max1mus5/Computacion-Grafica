import numpy as np
import matplotlib.pyplot as plt

def taylor_exp(x, n_terms=10):
    """
    Aproxima la función exponencial e^x usando series de Taylor.
    
    Args:
        x: Valor o array de valores para evaluar
        n_terms: Número de términos a usar en la serie
        
    Returns:
        Aproximación de e^x usando series de Taylor
    """
    result = np.zeros_like(x, dtype=float)
    for i in range(n_terms):
        # e^x = Σ (x^n / n!) desde n=0 hasta infinito
        result += (x**i) / np.math.factorial(i)
    return result

def factorial(n):
    """
    Calcula el factorial de un número.
    """
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def taylor_exp(x, n_terms=10):
    """
    Aproxima la función exponencial e^x usando series de Taylor.
    
    Args:
        x: Valor o array de valores para evaluar
        n_terms: Número de términos a usar en la serie
        
    Returns:
        Aproximación de e^x usando series de Taylor
    """
    result = np.zeros_like(x, dtype=float)
    for i in range(n_terms):
        # e^x = Σ (x^n / n!) desde n=0 hasta infinito
        result += (x**i) / factorial(i)
    return result

def taylor_sin(x, n_terms=10):
    """
    Aproxima la función seno usando series de Taylor.
    
    Args:
        x: Valor o array de valores para evaluar
        n_terms: Número de términos a usar en la serie
        
    Returns:
        Aproximación de sin(x) usando series de Taylor
    """
    result = np.zeros_like(x, dtype=float)
    for i in range(n_terms):
        # sin(x) = Σ ((-1)^n * x^(2n+1) / (2n+1)!) desde n=0 hasta infinito
        term = ((-1)**i) * (x**(2*i+1)) / factorial(2*i+1)
        result += term
    return result

def taylor_cos(x, n_terms=10):
    """
    Aproxima la función coseno usando series de Taylor.
    
    Args:
        x: Valor o array de valores para evaluar
        n_terms: Número de términos a usar en la serie
        
    Returns:
        Aproximación de cos(x) usando series de Taylor
    """
    result = np.zeros_like(x, dtype=float)
    for i in range(n_terms):
        # cos(x) = Σ ((-1)^n * x^(2n) / (2n)!) desde n=0 hasta infinito
        term = ((-1)**i) * (x**(2*i)) / factorial(2*i)
        result += term
    return result

def taylor_tan(x, n_terms=10):
    """
    Aproxima la función tangente usando la relación tan(x) = sin(x)/cos(x).
    Utiliza las aproximaciones de taylor_sin y taylor_cos.
    
    Args:
        x: Valor o array de valores para evaluar
        n_terms: Número de términos a usar en las series para sin y cos
        
    Returns:
        Aproximación de tan(x) usando series de Taylor
    """
    sin_x = taylor_sin(x, n_terms)
    cos_x = taylor_cos(x, n_terms)
    # Evitar división por cero
    cos_x = np.where(np.abs(cos_x) < 1e-10, 1e-10, cos_x)
    return sin_x / cos_x

def taylor_ln(x, n_terms=50):
    """
    Aproxima el logaritmo natural usando series de Taylor.
    La serie es válida para |x-1| < 1, así que ajustamos para otros valores.
    
    Args:
        x: Valor o array de valores para evaluar (debe ser positivo)
        n_terms: Número de términos a usar en la serie
        
    Returns:
        Aproximación de ln(x) usando series de Taylor
    """
    # Aseguramos que x sea positivo
    if np.any(x <= 0):
        raise ValueError("El logaritmo natural está definido solo para valores positivos")
    
    # La serie de Taylor para ln(x) alrededor de x=1 es:
    # ln(x) = Σ ((-1)^(n+1) * (x-1)^n / n) desde n=1 hasta infinito
    result = np.zeros_like(x, dtype=float)
    t = x - 1  # Cambio de variable para la serie centrada en 1
    
    for i in range(1, n_terms + 1):
        term = ((-1)**(i+1)) * (t**i) / i
        result += term
    
    return result

# Función para comparar visualmente todas las aproximaciones
def plot_taylor_approximations():
    # Configuración de subplots
    fig, axs = plt.subplots(5, 1, figsize=(12, 15))
    plt.subplots_adjust(hspace=0.4)
    
    # 1. Función Exponencial
    x_exp = np.linspace(-2, 2, 1000)
    terms = [1, 2, 3, 5, 10]
    
    axs[0].plot(x_exp, np.exp(x_exp), 'k-', linewidth=2, label='exp(x) real')
    for n in terms:
        axs[0].plot(x_exp, taylor_exp(x_exp, n), '--', label=f'Taylor ({n} términos)')
    
    axs[0].set_title('Aproximación de la Función Exponencial')
    axs[0].legend()
    axs[0].grid(True)
    
    # 2. Función Seno
    x_trig = np.linspace(-2*np.pi, 2*np.pi, 1000)
    
    axs[1].plot(x_trig, np.sin(x_trig), 'k-', linewidth=2, label='sin(x) real')
    for n in terms:
        axs[1].plot(x_trig, taylor_sin(x_trig, n), '--', label=f'Taylor ({n} términos)')
    
    axs[1].set_title('Aproximación de la Función Seno')
    axs[1].legend()
    axs[1].grid(True)
    
    # 3. Función Coseno
    axs[2].plot(x_trig, np.cos(x_trig), 'k-', linewidth=2, label='cos(x) real')
    for n in terms:
        axs[2].plot(x_trig, taylor_cos(x_trig, n), '--', label=f'Taylor ({n} términos)')
    
    axs[2].set_title('Aproximación de la Función Coseno')
    axs[2].legend()
    axs[2].grid(True)
    
    # 4. Función Tangente
    # Limitamos el dominio para evitar asíntotas
    x_tan = np.linspace(-1.5, 1.5, 1000)
    
    axs[3].plot(x_tan, np.tan(x_tan), 'k-', linewidth=2, label='tan(x) real')
    for n in terms:
        axs[3].plot(x_tan, taylor_tan(x_tan, n), '--', label=f'Taylor ({n} términos)')
    
    axs[3].set_title('Aproximación de la Función Tangente')
    axs[3].set_ylim(-10, 10)  # Limitamos el rango para mejor visualización
    axs[3].legend()
    axs[3].grid(True)
    
    # 5. Función Logaritmo Natural
    x_ln = np.linspace(0.1, 3, 1000)
    
    axs[4].plot(x_ln, np.log(x_ln), 'k-', linewidth=2, label='ln(x) real')
    terms_ln = [5, 10, 20, 50]
    for n in terms_ln:
        axs[4].plot(x_ln, taylor_ln(x_ln, n), '--', label=f'Taylor ({n} términos)')
    
    axs[4].set_title('Aproximación del Logaritmo Natural')
    axs[4].legend()
    axs[4].grid(True)
    
    plt.tight_layout()
    plt.show()

# Ejecutar la función para visualizar todas las aproximaciones
plot_taylor_approximations()

# Función para evaluar la precisión de las aproximaciones
def evaluate_precision():
    """
    Evalúa la precisión de las aproximaciones de Taylor comparándolas
    con las funciones reales de NumPy.
    """
    print("Evaluación de la precisión de las aproximaciones de Taylor:")
    
    # Puntos de prueba
    test_points = [-2, -1, -0.5, 0, 0.5, 1, 2]
    
    # 1. Exponencial
    print("\nFunción Exponencial:")
    print(f"{'x':^10} | {'exp(x) real':^15} | {'Taylor (10 términos)':^20} | {'Error Absoluto':^15} | {'Error Relativo %':^15}")
    print("-" * 80)
    
    for x in test_points:
        real = np.exp(x)
        approx = taylor_exp(x, 10)
        abs_error = abs(real - approx)
        rel_error = abs_error / abs(real) * 100 if real != 0 else 0
        print(f"{x:^10.2f} | {real:^15.6f} | {approx:^20.6f} | {abs_error:^15.6f} | {rel_error:^15.6f}")
    
    # 2. Seno
    print("\nFunción Seno:")
    print(f"{'x':^10} | {'sin(x) real':^15} | {'Taylor (10 términos)':^20} | {'Error Absoluto':^15} | {'Error Relativo %':^15}")
    print("-" * 80)
    
    for x in test_points:
        real = np.sin(x)
        approx = taylor_sin(x, 10)
        abs_error = abs(real - approx)
        rel_error = abs_error / abs(real) * 100 if real != 0 else 0
        print(f"{x:^10.2f} | {real:^15.6f} | {approx:^20.6f} | {abs_error:^15.6f} | {rel_error:^15.6f}")
    
    # 3. Coseno
    print("\nFunción Coseno:")
    print(f"{'x':^10} | {'cos(x) real':^15} | {'Taylor (10 términos)':^20} | {'Error Absoluto':^15} | {'Error Relativo %':^15}")
    print("-" * 80)
    
    for x in test_points:
        real = np.cos(x)
        approx = taylor_cos(x, 10)
        abs_error = abs(real - approx)
        rel_error = abs_error / abs(real) * 100 if real != 0 else 0
        print(f"{x:^10.2f} | {real:^15.6f} | {approx:^20.6f} | {abs_error:^15.6f} | {rel_error:^15.6f}")
    
    # 4. Tangente (evitando puntos problemáticos)
    print("\nFunción Tangente:")
    print(f"{'x':^10} | {'tan(x) real':^15} | {'Taylor (10 términos)':^20} | {'Error Absoluto':^15} | {'Error Relativo %':^15}")
    print("-" * 80)
    
    tan_points = [-0.5, -0.25, 0, 0.25, 0.5]
    for x in tan_points:
        real = np.tan(x)
        approx = taylor_tan(x, 10)
        abs_error = abs(real - approx)
        rel_error = abs_error / abs(real) * 100 if real != 0 else 0
        print(f"{x:^10.2f} | {real:^15.6f} | {approx:^20.6f} | {abs_error:^15.6f} | {rel_error:^15.6f}")
    
    # 5. Logaritmo Natural (evitando puntos negativos)
    print("\nFunción Logaritmo Natural:")
    print(f"{'x':^10} | {'ln(x) real':^15} | {'Taylor (50 términos)':^20} | {'Error Absoluto':^15} | {'Error Relativo %':^15}")
    print("-" * 80)
    
    ln_points = [0.5, 0.75, 1, 1.25, 1.5, 2]
    for x in ln_points:
        real = np.log(x)
        approx = taylor_ln(x, 50)
        abs_error = abs(real - approx)
        rel_error = abs_error / abs(real) * 100 if real != 0 else 0
        print(f"{x:^10.2f} | {real:^15.6f} | {approx:^20.6f} | {abs_error:^15.6f} | {rel_error:^15.6f}")

# Ejecutar la función para evaluar la precisión
evaluate_precision()