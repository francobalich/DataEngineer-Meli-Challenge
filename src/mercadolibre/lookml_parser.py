import json
import os
import lkml


def infer_columns_from_jsonl(file_path):
    """
    Infiera las columnas y sus tipos desde un archivo JSONL.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        # Lee la primera fila para inferir los nombres y tipos de columnas
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
                col_type = "string"  # Maneja dicts como JSON si es necesario
            else:
                col_type = "string"
            columns.append({"name": key, "type": col_type})
    return columns


def generate_view_from_jsonl(jsonl_path, table_name):
    """
    Genera un archivo LookML .view.lkml basado en un archivo JSONL.
    """
    columns = infer_columns_from_jsonl(jsonl_path)
    view = {
        "view": table_name,
        "dimensions": [
            {"name": col["name"], "type": col["type"], "sql": f"${{TABLE}}.{col['name']} ;;"}
            for col in columns
        ]
    }

    # Escribir el archivo .view.lkml
    file_name = f"{table_name}.view.lkml"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(lkml.dump(view))
    print(f"Archivo {file_name} generado.")


def generate_explore(joins, base_table="producto"):
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

    # Escribir el archivo .explore.lkml
    file_name = f"{base_table}.explore.lkml"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(lkml.dump(explore))
    print(f"Archivo {file_name} generado.")


# Ruta base donde se encuentran los archivos JSONL
jsonl_path = "data/conversions"

# Diccionario de archivos JSONL y sus nombres de tablas en BigQuery
jsonl_to_tables = {
    "producto.jsonl": "producto",
    "vendedor.jsonl": "vendedor",
    "envio.jsonl": "envio",
    "atributo.jsonl": "atributo",
    "categoria.jsonl": "categoria",
}

# Relación entre las tablas (para el archivo explore)
joins = [
    {"table": "vendedor", "sql_on": "${producto.vendedor_id} = ${vendedor.id} ;;", "relationship": "many_to_one"},
    {"table": "envio", "sql_on": "${producto.envio_id} = ${envio.id} ;;", "relationship": "many_to_one"},
    {"table": "atributo", "sql_on": "${producto.id} = ${atributo.producto_id} ;;", "relationship": "one_to_many"},
    {"table": "categoria", "sql_on": "${producto.categoria_id} = ${categoria.id} ;;", "relationship": "many_to_one"},
]

# Generar las views para todas las tablas
for jsonl_file, table_name in jsonl_to_tables.items():
    full_path = os.path.join(jsonl_path, jsonl_file)
    generate_view_from_jsonl(full_path, table_name)

# Generar el explore
generate_explore(joins)
