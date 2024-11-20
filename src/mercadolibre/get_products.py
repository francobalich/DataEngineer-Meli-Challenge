import requests

class getProducts:
    def __init__(self, base_url="https://api.mercadolibre.com/sites/MLA/search"):
        """
        Inicializa la clase con la URL base de la API.
        """
        self.base_url = base_url

    def fetch_products(self, query="chromecast", limit=50):
        """
        Realiza una solicitud GET a la API para obtener productos.

        Args:
            query (str): El término de búsqueda para los productos.
            limit (int): Límite de resultados a obtener.

        Returns:
            dict: Datos de los productos en formato JSON si la solicitud es exitosa.
            None: Si ocurre algún error en la solicitud.
        """
        params = {
            "q": query,
            "limit": limit
        }

        try:
            response = requests.get(self.base_url, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error en la solicitud: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud:", e)
            return None
