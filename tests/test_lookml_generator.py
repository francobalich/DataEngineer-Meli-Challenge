import unittest
import os
from src.mercadolibre.lookml_generator import LookMLGenerator

class TestLookMLGenerator(unittest.TestCase):

    def setUp(self):
        # Crea un archivo JSONL de prueba
        self.jsonl_path = "test_jsonl"
        self.output_path = "test_lookml"
        os.makedirs(self.jsonl_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)

        with open(os.path.join(self.jsonl_path, "producto.jsonl"), "w") as f:
            f.write('{"id": "1", "title": "Producto 1"}\n')

    def tearDown(self):
        # Elimina los directorios de prueba
        for path in [self.jsonl_path, self.output_path]:
            if os.path.exists(path):
                for file in os.listdir(path):
                    os.remove(os.path.join(path, file))
                os.rmdir(path)

    def test_infer_columns_from_jsonl(self):
        generator = LookMLGenerator(self.jsonl_path, self.output_path)
        columns = generator.infer_columns_from_jsonl(os.path.join(self.jsonl_path, "producto.jsonl"))
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0]["name"], "id")
        self.assertEqual(columns[0]["type"], "string")

    def test_generate_view_from_jsonl(self):
        generator = LookMLGenerator(self.jsonl_path, self.output_path)
        file_name = generator.generate_view_from_jsonl("producto.jsonl", "producto")
        self.assertTrue(os.path.exists(os.path.join(self.output_path, file_name)))

    def test_generate_explore(self):
        generator = LookMLGenerator(self.jsonl_path, self.output_path)
        joins = [{"table": "vendedor", "sql_on": "${producto.vendedor_id} = ${vendedor.id} ;;", "relationship": "many_to_one"}]
        file_name = generator.generate_explore(joins)
        self.assertTrue(os.path.exists(os.path.join(self.output_path, file_name)))