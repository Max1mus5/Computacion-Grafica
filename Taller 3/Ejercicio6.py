# Ejercicio 6: Trabajo con Datos Faltantes
# Pistas:
# - Utiliza np.nan_to_num(data, nan=0) para reemplazar np.nan por 0.
# - Calcula la media del array resultante con np.mean(data).

import numpy as np

def main():
    print("\n===== Ejercicio 6: Trabajo con Datos Faltantes =====")
    
    # Crear un array con valores faltantes (NaN)
    data = np.array([1.0, 2.0, np.nan, 4.0, 5.0, np.nan, 7.0, 8.0, 9.0, np.nan])
    print(f"\nArray original con valores NaN:")
    print(data)
    
    # Identificar valores NaN
    nan_mask = np.isnan(data)
    print(f"\nMáscara de valores NaN (np.isnan(data)):")
    print(nan_mask)
    print(f"Número de valores NaN: {np.sum(nan_mask)}")
    
    # Reemplazar NaN con ceros
    data_zero = np.nan_to_num(data, nan=0)
    print(f"\nArray con NaN reemplazados por ceros (np.nan_to_num(data, nan=0)):")
    print(data_zero)
    
    # Calcular estadísticas ignorando NaN
    print(f"\nEstadísticas ignorando NaN:")
    print(f"Media (np.nanmean(data)): {np.nanmean(data)}")
    print(f"Suma (np.nansum(data)): {np.nansum(data)}")
    print(f"Mínimo (np.nanmin(data)): {np.nanmin(data)}")
    print(f"Máximo (np.nanmax(data)): {np.nanmax(data)}")
    
    # Eliminar valores NaN
    data_no_nan = data[~np.isnan(data)]
    print(f"\nArray con valores NaN eliminados (data[~np.isnan(data)]):")
    print(data_no_nan)
    
    # Reemplazar NaN con un valor personalizado
    data_custom = np.nan_to_num(data, nan=-1)
    print(f"\nArray con NaN reemplazados por -1 (np.nan_to_num(data, nan=-1)):")
    print(data_custom)
    
    # Interpolación de valores faltantes
    print(f"\nInterpolación de valores faltantes:")
    
    # Crear un array con NaN para interpolación
    data_to_interpolate = np.copy(data)
    
    # Obtener índices de valores no-NaN y sus correspondientes valores
    mask = ~np.isnan(data_to_interpolate)
    indices = np.arange(len(data_to_interpolate))
    values = data_to_interpolate[mask]
    indices_valid = indices[mask]
    
    # Interpolación lineal simple
    data_interpolated = np.interp(indices, indices_valid, values)
    print(f"\nArray con valores interpolados:")
    print(data_interpolated)
    
    # Demostración con arrays multidimensionales
    print(f"\nTrabajo con datos faltantes en arrays multidimensionales:")
    
    # Crear una matriz 3x3 con algunos valores NaN
    matrix_with_nan = np.array([
        [1.0, 2.0, np.nan],
        [4.0, np.nan, 6.0],
        [np.nan, 8.0, 9.0]
    ])
    print(f"\nMatriz con valores NaN:")
    print(matrix_with_nan)
    
    # Reemplazar NaN con ceros
    matrix_zero = np.nan_to_num(matrix_with_nan, nan=0)
    print(f"\nMatriz con NaN reemplazados por ceros:")
    print(matrix_zero)
    
    # Calcular estadísticas por filas y columnas ignorando NaN
    print(f"\nMedia por filas (np.nanmean(matrix_with_nan, axis=1)):")
    print(np.nanmean(matrix_with_nan, axis=1))
    
    print(f"\nMedia por columnas (np.nanmean(matrix_with_nan, axis=0)):")
    print(np.nanmean(matrix_with_nan, axis=0))

if __name__ == "__main__":
    main()