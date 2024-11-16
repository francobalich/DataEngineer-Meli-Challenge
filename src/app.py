from flask import Flask, request, jsonify
from src.mercadolibre.api import getProducts
import json

app = Flask(__name__)

product_manager = getProducts()

user_state = {
    "count": 0,
    "categories": {}
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
            if product not in user_state["categories"]:
                user_state["categories"][product] = []
            user_state["categories"][product].extend(fetched["results"])

            user_state["count"] += len(fetched["results"])

        if user_state["count"] >= 500:
            with open("resultados_api.json", "w", encoding="utf-8") as file:
                json.dump(user_state, file, indent=4, ensure_ascii=False)

            response = {
                "message": "Se alcanzaron los 500 productos. Los datos se han guardado.",
                "categories": user_state["categories"],
                "count": user_state["count"]
            }

            user_state["count"] = 0
            user_state["categories"] = {}

            return jsonify(response), 200

        response = {
            "current_count": user_state["count"],
            "target_count": 500,
            "categories": user_state["categories"]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
