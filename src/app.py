from flask import Flask, request, jsonify
from src.mercadolibre.api import getProducts

app = Flask(__name__)

product_manager = getProducts()

@app.route('/test', methods=['GET'])
def check_stats():
    """
    Endpoint para probar la API de MercadoLibre.
    """
    try:
        query = request.args.get('query', 'chromecast')
        limit = int(request.args.get('limit', 50))

        products = product_manager.fetch_products(query=query, limit=limit)

        if products:
            return jsonify(products), 200
        else:
            return jsonify({"error": "No se pudieron obtener productos."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
