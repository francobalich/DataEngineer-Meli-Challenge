import lkml
from pprint import pprint

# Asegúrate de que el archivo `orders.view.lkml` existe en el mismo directorio o proporciona la ruta completa.
try:
    with open('src\mercadolibre\orders.view.lkml', 'r') as file:
        # Carga el archivo LookML usando lkml
        result = lkml.load(file)
        # Imprime el resultado en un formato legible
        pprint(result)
except FileNotFoundError:
    print("El archivo 'orders.view.lkml' no existe en el directorio especificado.")
except Exception as e:
    print(f"Ocurrió un error al procesar el archivo: {e}")
