from flask import Flask, request, jsonify
from src.mercadolibre.api import getProducts
from src.mercadolibre.product_processor import ProductProcessor

import json

app = Flask(__name__)

product_manager = getProducts()

user_state = {
    "count": 0,
    "products": []
}

@app.route('/getproducts', methods=['POST'])
def get_products():
    """
    Endpoint para obtener productos desde la API de MercadoLibre.
    Permite solicitudes incrementales hasta alcanzar 500 productos.
    """
    try:
        data = request.get_json()

        product = data.get('product')
        if not product:
            return jsonify({"error": "Debes proporcionar un término de búsqueda ('product')."}), 400

        fetched = product_manager.fetch_products(query=product, limit=50)
        if fetched and "results" in fetched and fetched["results"]:
            user_state["products"].extend(fetched["results"])
            user_state["count"] += len(fetched["results"])

        if user_state["count"] >= 500:
            with open("productos.jsonl", "w", encoding="utf-8") as file:
                for product in user_state["products"]:
                    file.write(json.dumps(product, ensure_ascii=False) + "\n")

            response = {
                "message": "Se alcanzaron los 500 productos. Los datos se han guardado en JSONL.",
                "total_products": user_state["count"],
                "file": "productos.jsonl"
            }

            user_state["count"] = 0
            user_state["products"] = []

            return jsonify(response), 200

        response = {
            "current_count": user_state["count"],
            "target_count": 500
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/convertdata', methods=['POST'])
def convert_data():
    """
    Endpoint para procesar los productos guardados en JSONL y convertirlos en JSON para BigQuery.
    """
    try:
        processor = ProductProcessor(input_file="productos.jsonl")
        processor.process_products()
        processor.save_json_files()

        return jsonify({"message": "Los datos se han convertido y guardado en archivos JSON."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
