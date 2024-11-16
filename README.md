# MercadoLibre API Challenge

## Descripción
Este proyecto consiste en desarrollar un conjunto de scripts o una API en Python para interactuar con la API de MercadoLibre, procesar los datos obtenidos, y modelar una solución analítica que permita visualizarlos utilizando LookML. 

A continuación, se describen los pasos y entregables requeridos.

---

## Pasos

### 1. Descargar la data
**Objetivo:** Obtener 500 resultados de la API de MercadoLibre utilizando el endpoint de búsqueda.

- **URL de la API:** `https://api.mercadolibre.com/sites/MLA/search?q=chromecast&limit=50`
- **Descripción:** Se realizarán múltiples llamadas al endpoint con el fin de acumular los 500 resultados.
- **Entregable:**
  - Código para descargar los datos.
  - Archivo JSON con los datos obtenidos.

---

### 2. Modelar
**Objetivo:** Diseñar un modelo relacional con al menos 3 tablas que pueda ser creado en BigQuery (DDL).

- **Requisitos:**
  - Modelo relacional con un mínimo de 3 tablas.
  - Se permite utilizar campos anidados.
  - Justificar la selección de tablas y su relación.
- **Entregable:**
  - Script DDL para la creación de las tablas en BigQuery.
  - Documentación que explique la estructura del modelo y las decisiones tomadas.

---

### 3. Parsear
**Objetivo:** Transformar los datos descargados para adaptarlos al modelo relacional diseñado.

- **Requisitos:**
  - Parsear los datos para que coincidan con las tablas del modelo.
  - Exportar los archivos en formato JSON listos para ser importados.
- **Entregable:**
  - Código de parsing.
  - Archivos JSON con los datos parseados.

---

### 4. Looker
**Objetivo:** Crear archivos LookML que definan una vista por cada tabla y un explore que relacione las vistas.

- **Requisitos:**
  - Utilizar el SDK LookML.
  - Crear una vista (`view`) para cada tabla del modelo.
  - Crear un `explore` que relacione las vistas.
- **Entregable:**
  - Archivos LookML (`.lkml`) con las vistas y el explore.
  - Código utilizado para generar los archivos LookML.

---

## Extras
1. **POO (Programación Orientada a Objetos):** Se valorará la estructuración del código utilizando principios de POO.
2. **Coverage:** Proveer tests que cubran el mayor porcentaje de código posible.
3. **Uso de GenAI:** Si se utilizan herramientas de Generación de Inteligencia Artificial, detallar:
   - Prompts utilizados.
   - Proceso de refinamiento y aprendizaje de la herramienta.
4. **Repositorio GitHub:** Entregar el proyecto organizado en un repositorio público o privado de GitHub.

---