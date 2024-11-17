import json
import os
from datetime import datetime

class ProductProcessor:
    def __init__(self, input_file="productos.json", path_base="data/conversions"):
        """
        Inicializa la clase con el archivo de entrada JSON y la ruta base para guardar los archivos procesados.
        """
        self.input_file = input_file
        self.path_base = path_base
        os.makedirs(self.path_base, exist_ok=True)
        self.productos = self._load_products()
        self.productos_json = []
        self.vendedores_json = []
        self.envios_json = []
        self.atributos_json = []
        self.cuotas_json = []

    def _load_products(self):
        """
        Carga los productos desde el archivo JSON.

        Returns:
            list: Lista de productos cargados desde el archivo JSON.
        """
        try:
            with open(self.input_file, "r", encoding="utf-8", errors="replace") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: El archivo {self.input_file} no se encontró.")
            return []
        except json.JSONDecodeError:
            print(f"Error: No se pudo decodificar el archivo JSON {self.input_file}.")
            return []

    def process_products(self):
        """
        Procesa los productos para extraer los datos de cada tabla.
        """
        for producto in self.productos:
            # Producto
            self.productos_json.append({
                "id": producto["id"],
                "titulo": producto["title"],
                "condicion": producto["condition"],
                "permalink": producto["permalink"],
                "dominio_id": producto["domain_id"],
                "categoria_id": producto["category_id"],
                "vendedor_id": producto["seller"]["id"],
                "envio_id": producto["id"],  # Usamos el ID del producto como referencia para el envio
                "precio": producto["price"],
                "precio_original": producto.get("original_price"),
                "cantidad_disponible": producto["available_quantity"],
                "acepta_mercadopago": producto["accepts_mercadopago"],
                "fecha_limite": datetime.strptime(producto["stop_time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                "tipo_listado": producto["listing_type_id"],
                "modo_compra": producto["buying_mode"]
            })

            # Vendedor
            self.vendedores_json.append({
                "id": producto["seller"]["id"],
                "nickname": producto["seller"].get("nickname")
            })

            # Envío
            self.envios_json.append({
                "id": producto["id"],
                "envio_gratis": producto["shipping"]["free_shipping"],
                "tipo_logistica": producto["shipping"]["logistic_type"],
                "modo_envio": producto["shipping"]["mode"],
                "etiquetas": producto["shipping"].get("tags", [])
            })

            # Atributos
            for atributo in producto.get("attributes", []):
                self.atributos_json.append({
                    "id": atributo["id"],
                    "producto_id": producto["id"],
                    "nombre": atributo["name"],
                    "valor": atributo["value_name"],
                    "fuente": atributo["source"]
                })

            # Cuotas
            if "installments" in producto:
                self.cuotas_json.append({
                    "id": producto["id"],
                    "producto_id": producto["id"],
                    "cantidad": producto["installments"]["quantity"],
                    "monto_por_cuota": producto["installments"]["amount"],
                    "tasa_interes": producto["installments"]["rate"],
                    "moneda": producto["installments"]["currency_id"]
                })

    def save_json_files(self):
        """
        Guarda los datos procesados en archivos JSON.
        """
        with open(os.path.join(self.path_base, "productos.json"), "w") as file:
            json.dump(self.productos_json, file, indent=4)

        with open(os.path.join(self.path_base, "vendedores.json"), "w") as file:
            json.dump(self.vendedores_json, file, indent=4)

        with open(os.path.join(self.path_base, "envios.json"), "w") as file:
            json.dump(self.envios_json, file, indent=4)

        with open(os.path.join(self.path_base, "atributos.json"), "w") as file:
            json.dump(self.atributos_json, file, indent=4)

        with open(os.path.join(self.path_base, "cuotas.json"), "w") as file:
            json.dump(self.cuotas_json, file, indent=4)

        print("Archivos JSON generados exitosamente.")


if __name__ == "__main__":
    processor = ProductProcessor()
    processor.process_products()
    processor.save_json_files()
