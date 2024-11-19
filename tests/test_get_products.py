import unittest
from src.mercadolibre.api import getProducts
import responses

class TestGetProducts(unittest.TestCase):

    @responses.activate
    def test_fetch_products_success(self):
        base_url = "https://api.mercadolibre.com/sites/MLA/search"
        query = "chromecast"
        limit = 50

        # Simula una respuesta exitosa de la API
        responses.add(
            responses.GET,
            base_url,
            json={"results": [{"id": "123", "title": "Chromecast"}]},
            status=200,
        )

        api = getProducts(base_url)
        result = api.fetch_products(query=query, limit=limit)

        # Verificaciones
        self.assertIsNotNone(result)
        self.assertIn("results", result)
        self.assertEqual(result["results"][0]["id"], "123")
        self.assertEqual(result["results"][0]["title"], "Chromecast")

    @responses.activate
    def test_fetch_products_failure(self):
        base_url = "https://api.mercadolibre.com/sites/MLA/search"
        # Simula una respuesta fallida de la API
        responses.add(
            responses.GET,
            base_url,
            json={"error": "Bad Request"},
            status=400,
        )

        api = getProducts(base_url)
        result = api.fetch_products(query="chromecast", limit=50)

        # Verificaciones
        self.assertIsNone(result)
