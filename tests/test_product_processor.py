import unittest
import os
from src.mercadolibre.product_processor import ProductProcessor

class TestProductProcessor(unittest.TestCase):

    def setUp(self):
        # Crea un archivo de prueba JSONL
        self.input_file = "test_productos.jsonl"
        self.output_path = "test_output"
        os.makedirs(self.output_path, exist_ok=True)
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write('{"id": "1", "title": "Producto 1", "seller": {"id": "100"}, "shipping": {"free_shipping": true}}\n')

    def tearDown(self):
        # Limpia los archivos generados
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_path):
            for file in os.listdir(self.output_path):
                os.remove(os.path.join(self.output_path, file))
            os.rmdir(self.output_path)

    def test_process_products(self):
        processor = ProductProcessor(input_file=self.input_file, path_base=self.output_path)
        processor.process_products()

        self.assertEqual(len(processor.productos_json), 1)
        self.assertEqual(processor.productos_json[0]["id"], "1")

    def test_save_jsonl_files(self):
        processor = ProductProcessor(input_file=self.input_file, path_base=self.output_path)
        processor.process_products()
        processor.save_jsonl_files()

        output_files = os.listdir(self.output_path)
        self.assertIn("producto.jsonl", output_files)
