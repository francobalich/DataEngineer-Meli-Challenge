
# MercadoLibre API Challenge

## Descripción
Este proyecto consiste en el desarrollo de una API en Python para interactuar con la API de MercadoLibre, procesar los datos obtenidos, y modelar una solución analítica que permita visualizarlos utilizando LookML.

A continuación, se describen los pasos y entregables requeridos.

---

## Solución

### 1. Descargar la data
**Objetivo:** Obtener 500 resultados de la API de MercadoLibre utilizando el endpoint de búsqueda.

- **URL de la API:** `https://api.mercadolibre.com/sites/MLA/search?q=chromecast&limit=50`
- **Descripción:** Se realizarán múltiples llamadas al endpoint con el fin de acumular los 500 resultados.
- **Código disponible en:** `src/mercadolibre/get_products.py`
- **Modo de uso:** 
  - Probar el script para obtener los productos en un archivo JSONL ubicado en `data/origin/productos.jsonl`.
  - Realizar las llamadas al endpoint `/getproducts`:
    ```bash
    curl --location 'http://127.0.0.1:5000/getproducts' \
    --header 'Content-Type: application/json' \
    --data '{ 
        "product": "pc" 
    }'
    ```
  - Se pueden realizar las llamadas con el mismo producto o productos distintos.
- **Entregable:**
  - Código para descargar los datos.
  - Archivo `JSONL` con los datos obtenidos.

---

### 2. Modelar
**Objetivo:** Diseñar un modelo relacional con al menos 3 tablas que pueda ser creado en BigQuery (DDL).

- **Decisiones tomadas:**
  - Se analizaron las respuestas de la API para incluir en el modelo solo los datos relevantes.
  - Se excluyeron tablas para `Dominio` y `Categoría` debido a la falta de contenido en los IDs, pero se dejaron los IDs en la tabla `Producto` para futuras expansiones.
  - No se creó una tabla adicional para `Promoción` debido a su baja recurrencia en los productos.
- **Modelo orientado a análisis como:**
  - Comparativa de precios entre productos.
  - Identificación del vendedor con más productos.
  - Productos con más atributos en sus publicaciones.
  - Cantidad de cuotas más recurrente.
  - Proporción de envíos gratis vs. pagos.
- **Código disponible en:** `data/model/dataset-gen.sql`
- **Entregable:**
  - Script DDL para la creación de las tablas en BigQuery.
  - Documentación explicativa sobre la estructura del modelo y las decisiones tomadas.

---

### 3. Parsear
**Objetivo:** Transformar los datos descargados para adaptarlos al modelo relacional diseñado.

- **Código disponible en:** `src/mercadolibre/product_processor.py`
- **Datos generados:**
  - `data/conversions/atributo.jsonl`
  - `data/conversions/cuota.jsonl`
  - `data/conversions/envio.jsonl`
  - `data/conversions/producto.jsonl`
  - `data/conversions/vendedor.jsonl`
- **Modo de uso:**
  - Ejecutar el siguiente comando para procesar los datos:
    ```bash
    curl --location --request POST 'http://localhost:5000/convertdata' \
    --data ''
    ```
- **Entregable:**
  - Código de parsing.
  - Archivos `JSONL` con los datos procesados.

---

### 4. Looker
**Objetivo:** Crear archivos LookML que definan una vista por cada tabla y un explore que relacione las vistas.

- **Código disponible en:** `src/mercadolibre/lookml_generator.py`
- **Archivos generados:**
  - `data/lookml/atributo.view.lkml`
  - `data/lookml/envio.view.lkml`
  - `data/lookml/producto.view.lkml`
  - `data/lookml/vendedor.view.lkml`
  - `data/lookml/producto.explore.lkml`
- **Modo de uso:**
  - Ejecutar el siguiente comando para generar los archivos LookML:
    ```bash
    curl --location --request POST 'http://localhost:5000/genlookml' \
    --data ''
    ```
- **Entregable:**
  - Archivos LookML (`.lkml`) con las vistas y el explore.
  - Código utilizado para generar los archivos LookML.

---

## Implementación técnica

### Requerimientos
Este proyecto utiliza las siguientes dependencias, listadas en el archivo `requirements.txt`:
- Flask
- lkml
- requests
- Otros necesarios para pruebas y funcionalidad.

Instalación:
```bash
pip install -r requirements.txt
```

### Tests y cobertura
- **Tests disponibles en:** Carpeta `tests`.
- **Ejecución de los tests:**
  ```bash
  python -m unittest discover -s tests
  ```
- **Reporte de cobertura:** Archivo HTML disponible en `report/index.html`.

### Ejecución del servidor
Para ejecutar la API localmente:
```bash
python main.py
```

---
