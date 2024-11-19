import json
import os
import lkml

class LookMLGenerator:
    def __init__(self, jsonl_path, output_path=""):
        """
        Inicializa el generador de LookML con una ruta base para los archivos JSONL.
        """
        self.jsonl_path = jsonl_path
        self.output_path = output_path

    def infer_columns_from_jsonl(self, file_path):
        """
        Infiera las columnas y sus tipos desde un archivo JSONL.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            first_row = json.loads(next(file))
            columns = []
            for key, value in first_row.items():
                if isinstance(value, str):
                    col_type = "string"
                elif isinstance(value, int):
                    col_type = "number"
                elif isinstance(value, float):
                    col_type = "number"
                elif isinstance(value, bool):
                    col_type = "yesno"
                elif isinstance(value, list):
                    col_type = "array"
                elif isinstance(value, dict):
                    col_type = "string"
                else:
                    col_type = "string"
                columns.append({"name": key, "type": col_type})
        return columns

    def generate_view_from_jsonl(self, jsonl_file, table_name):
        """
        Genera un archivo LookML .view.lkml basado en un archivo JSONL.
        """
        full_path = os.path.join(self.jsonl_path, jsonl_file)
        columns = self.infer_columns_from_jsonl(full_path)
        view = {
            "view": table_name,
            "dimensions": [
                {"name": col["name"], "type": col["type"], "sql": f"${{TABLE}}.{col['name']} ;;"}
                for col in columns
            ]
        }

        file_name = f"{table_name}.view.lkml"
        output_path = os.path.join(self.output_path, file_name)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(lkml.dump(view))
        return file_name

    def generate_explore(self, joins, base_table="producto"):
        """
        Genera un archivo LookML .explore.lkml basado en las relaciones entre tablas.
        """
        explore = {
            "explore": base_table,
            "joins": [
                {
                    "name": join["table"],
                    "sql_on": join["sql_on"],
                    "relationship": join["relationship"]
                }
                for join in joins
            ]
        }

        file_name = f"{base_table}.explore.lkml"
        output_path = os.path.join(self.output_path, file_name)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(lkml.dump(explore))
        return file_name
