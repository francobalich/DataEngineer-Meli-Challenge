from flask import Flask, request, jsonify
from src.mercadolibre.get_products import getProducts
from src.mercadolibre.product_processor import ProductProcessor
from src.mercadolibre.lookml_generator import LookMLGenerator

import os
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
            with open("data/origin/productos.jsonl", "w", encoding="utf-8") as file:
                for product in user_state["products"]:
                    file.write(json.dumps(product, ensure_ascii=False) + "\n")

            response = {
                "message": "Se alcanzaron los 500 productos. Los datos se han guardado en JSONL.",
                "total_products": user_state["count"],
                "file": "data/origin/productos.jsonl",
                "data": user_state["products"]
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
    Endpoint para procesar los productos guardados en JSONL y convertirlos en JSONL para BigQuery.
    """
    try:
        processor = ProductProcessor(input_file="data/origin/productos.jsonl")
        processor.process_products()
        processor.save_jsonl_files()

        return jsonify({"message": "Los datos se han convertido y guardado en archivos JSONL."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/genlookml', methods=['POST'])
def convert_lookml():
    """
    Endpoint para crear los .lkml a partir de los JSONL.
    """
    try:
        # Parámetros
        jsonl_path = "data/conversions"
        output_path = "data/lookml"
        jsonl_to_tables = {
            "producto.jsonl": "producto",
            "vendedor.jsonl": "vendedor",
            "envio.jsonl": "envio",
            "atributo.jsonl": "atributo",
        }
        joins = [
            {"table": "vendedor", "sql_on": "${producto.vendedor_id} = ${vendedor.id} ;;", "relationship": "many_to_one"},
            {"table": "envio", "sql_on": "${producto.envio_id} = ${envio.id} ;;", "relationship": "many_to_one"},
            {"table": "atributo", "sql_on": "${producto.id} = ${atributo.producto_id} ;;", "relationship": "one_to_many"},
        ]

        # Verifica si la carpeta de salida existe, si no, la crea
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Directorio '{output_path}' creado.")

        # Inicializa el generador
        generator = LookMLGenerator(jsonl_path=jsonl_path, output_path=output_path)

        # Genera las vistas
        generated_files = []
        for jsonl_file, table_name in jsonl_to_tables.items():
            file_name = generator.generate_view_from_jsonl(jsonl_file, table_name)
            generated_files.append(file_name)

        # Genera el explore
        explore_file = generator.generate_explore(joins)
        generated_files.append(explore_file)

        return jsonify({"message": "Archivos LookML generados exitosamente.", "files": generated_files}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
