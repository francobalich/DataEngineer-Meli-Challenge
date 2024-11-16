from flask import Flask, request, jsonify
from src.mercadolibre.api import getProducts
import json

app = Flask(__name__)

product_manager = getProducts()

DEFAULT_PRODUCTS = [
    "notebook", "celular", "tablet", "electronica", "monitor",
    "teclado", "camara", "tv", "rgb", "luz"
]

@app.route('/getproducts', methods=['POST'])
def get_products():
    """
    Endpoint para obtener productos desde la API de MercadoLibre.
    """
    try:
        data = request.get_json()

        product_list = data.get('products') if data and 'products' in data else DEFAULT_PRODUCTS

        if len(product_list) == 10:
            results = {
                "products": DEFAULT_PRODUCTS,
                "count": 0,
                "categories": {}
            }

            for product in product_list:
                fetched = product_manager.fetch_products(query=product, limit=50) 
                if fetched and "results" in fetched and fetched["results"]:
                    if product not in results["categories"]:
                        results["categories"][product] = []
                    results["categories"][product].extend(fetched["results"])

                    results["count"] += len(fetched["results"])


            return jsonify(results), 200
        else:
            return jsonify({"error": "El array de productos debe tener exactamente 10 elementos."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
