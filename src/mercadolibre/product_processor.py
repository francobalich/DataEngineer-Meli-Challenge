import json
import os
from datetime import datetime


class ProductProcessor:
    def __init__(self, input_file="data/productos.jsonl", path_base="data/conversions"):
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
        self.promociones_json = []
        self.categorias_json = []
        self.dominios_json = []

    def _load_products(self):
        """
        Carga los productos desde el archivo JSONL.

        Returns:
            list: Lista de productos cargados desde el archivo JSONL.
        """
        productos = []
        try:
            with open(self.input_file, "r", encoding="utf-8", errors="replace") as file:
                for line in file:
                    productos.append(json.loads(line))
            return productos
        except FileNotFoundError:
            print(f"Error: El archivo {self.input_file} no se encontró.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error: No se pudo decodificar el archivo JSONL {self.input_file}: {e}")
            return []

    def process_products(self):
        """
        Procesa los productos para extraer los datos de cada tabla.
        """
        categorias = set()
        dominios = set()

        for producto in self.productos:
            if producto is None:
                continue

            # Convertir `stop_time` a cadena si existe
            fecha_limite = None
            if producto.get("stop_time"):
                try:
                    fecha_limite = datetime.strptime(producto["stop_time"], "%Y-%m-%dT%H:%M:%S.%fZ").isoformat()
                except ValueError:
                    fecha_limite = datetime.strptime(producto["stop_time"], "%Y-%m-%dT%H:%M:%S.%fZ").isoformat()

            # Producto
            self.productos_json.append({
                "id": producto.get("id"),
                "titulo": producto.get("title"),
                "condicion": producto.get("condition"),
                "permalink": producto.get("permalink"),
                "dominio_id": producto.get("domain_id"),
                "categoria_id": producto.get("category_id"),
                "vendedor_id": producto.get("seller", {}).get("id") if producto.get("seller") else None,
                "envio_id": producto.get("id"),  # Usamos el ID del producto como referencia para el envio
                "precio": producto.get("price"),
                "precio_original": producto.get("original_price"),
                "cantidad_disponible": producto.get("available_quantity"),
                "acepta_mercadopago": producto.get("accepts_mercadopago"),
                "fecha_limite": fecha_limite,
                "tipo_listado": producto.get("listing_type_id"),
                "modo_compra": producto.get("buying_mode")
            })

            # Vendedor
            if producto.get("seller"):
                self.vendedores_json.append({
                    "id": producto["seller"].get("id"),
                    "nickname": producto["seller"].get("nickname")
                })

            # Envío
            if producto.get("shipping"):
                self.envios_json.append({
                    "id": producto.get("id"),
                    "envio_gratis": producto["shipping"].get("free_shipping"),
                    "tipo_logistica": producto["shipping"].get("logistic_type"),
                    "modo_envio": producto["shipping"].get("mode"),
                    "etiquetas": producto["shipping"].get("tags", [])
                })

            # Atributos
            for atributo in producto.get("attributes", []):
                self.atributos_json.append({
                    "id": atributo.get("id"),
                    "producto_id": producto.get("id"),
                    "nombre": atributo.get("name"),
                    "valor": atributo.get("value_name"),
                    "fuente": atributo.get("source")
                })

            # Cuotas
            if producto.get("installments"):
                self.cuotas_json.append({
                    "id": producto.get("id"),
                    "producto_id": producto.get("id"),
                    "cantidad": producto["installments"].get("quantity"),
                    "monto_por_cuota": producto["installments"].get("amount"),
                    "tasa_interes": producto["installments"].get("rate"),
                    "moneda": producto["installments"].get("currency_id")
                })

            # Promociones
            if producto.get("promotions"):
                for promo in producto["promotions"]:
                    self.promociones_json.append({
                        "id": promo.get("id"),
                        "producto_id": producto.get("id"),
                        "tipo_promocion": promo.get("type"),
                        "descuento_porcentaje": promo.get("discount_percentage"),
                        "descuento_monto": promo.get("discount_amount"),
                        "fecha_inicio": promo.get("start_date"),
                        "fecha_fin": promo.get("end_date"),
                        "metadatos": promo.get("metadata", {})
                    })

            # Categorías (sin duplicados)
            categorias.add((producto.get("category_id"), producto.get("category_name")))

            # Dominios (sin duplicados)
            dominios.add((producto.get("domain_id"), producto.get("domain_name")))

        # Generar listas finales para categorías y dominios
        for id_cat, nombre_cat in categorias:
            self.categorias_json.append({"id": id_cat, "nombre": nombre_cat})

        for id_dom, nombre_dom in dominios:
            self.dominios_json.append({"id": id_dom, "nombre": nombre_dom})

    def save_jsonl_files(self):
        """
        Guarda los datos procesados en archivos JSONL.
        """
        def save_to_file(data, filename):
            with open(os.path.join(self.path_base, filename), "w", encoding="utf-8") as file:
                for record in data:
                    file.write(json.dumps(record, ensure_ascii=False) + "\n")

        save_to_file(self.productos_json, "producto.jsonl")
        save_to_file(self.vendedores_json, "vendedor.jsonl")
        save_to_file(self.envios_json, "envio.jsonl")
        save_to_file(self.atributos_json, "atributo.jsonl")
        save_to_file(self.cuotas_json, "cuota.jsonl")
        save_to_file(self.promociones_json, "promocion.jsonl")
        save_to_file(self.categorias_json, "categoria.jsonl")
        save_to_file(self.dominios_json, "dominio.jsonl")

        print("Archivos JSONL generados exitosamente.")


if __name__ == "__main__":
    processor = ProductProcessor()
    processor.process_products()
    processor.save_jsonl_files()
