import numpy as np
from collections import Counter

def create_vector(elements):
    """Crea un vector a partir de una lista de elementos."""
    return np.array(elements)

def create_range_vector(start, end):
    """Crea un vector con elementos en un rango específico."""
    return np.array(range(start, end + 1))

def concatenate_vectors(vector1, vector2):
    """Concatena dos vectores en uno solo."""
    return np.concatenate((vector1, vector2))

def find_min(vector):
    """Encuentra el valor mínimo en un vector."""
    return np.min(vector)

def find_max(vector):
    """Encuentra el valor máximo en un vector."""
    return np.max(vector)

def get_length(vector):
    """Obtiene la longitud de un vector."""
    return len(vector)

def calculate_average_manually(vector):
    """Calcula el promedio manualmente usando operaciones elementales."""
    return sum(vector) / len(vector)

def calculate_average(vector):
    """Calcula el promedio usando la función de NumPy."""
    return np.mean(vector)

def calculate_median(vector):
    """Calcula la mediana usando la función de NumPy."""
    return np.median(vector)

def calculate_sum(vector):
    """Calcula la suma de los elementos usando la función de NumPy."""
    return np.sum(vector)

def filter_greater_than(vector, value):
    """Filtra elementos mayores que un valor dado."""
    return vector[vector > value]

def filter_between(vector, min_value, max_value):
    """Filtra elementos entre dos valores dados."""
    return vector[(vector > min_value) & (vector < max_value)]

def replace_element(vector, index, value):
    """Reemplaza un elemento en una posición específica."""
    vector[index] = value
    return vector

def replace_elements(vector, start_index, end_index, value):
    """Reemplaza elementos en un rango de posiciones con un valor específico."""
    vector[start_index:end_index + 1] = value
    return vector

def find_mode(vector):
    """Encuentra la moda de un vector."""
    counts = Counter(vector)
    return counts.most_common(1)[0][0]

def sort_vector(vector):
    """Ordena un vector de menor a mayor."""
    return np.sort(vector)

def multiply_vector(vector, factor):
    """Multiplica un vector por un factor."""
    return vector * factor

def replace_range_with_values(vector, start_index, end_index, values):
    """Reemplaza elementos en un rango con valores específicos."""
    if len(values) != (end_index - start_index + 1):
        raise ValueError("La cantidad de valores no coincide con el rango especificado.")
    vector[start_index:end_index + 1] = values
    return vector