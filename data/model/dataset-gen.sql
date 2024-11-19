-- Crear la tabla de Producto
CREATE TABLE `dataengineer-meli-challenge.challenge.producto` (
  id STRING NOT NULL,
  titulo STRING,
  condicion STRING,
  permalink STRING,
  dominio_id STRING,
  categoria_id STRING,
  vendedor_id STRING,
  envio_id STRING,
  precio FLOAT64,
  precio_original FLOAT64,
  cantidad_disponible INT64,
  acepta_mercadopago BOOL,
  fecha_limite TIMESTAMP,
  tipo_listado STRING,
  modo_compra STRING
);

-- Crear la tabla de Vendedor
CREATE TABLE `dataengineer-meli-challenge.challenge.vendedor` (
  id STRING NOT NULL,
  nickname STRING
);

-- Crear la tabla de Envío
CREATE TABLE `dataengineer-meli-challenge.challenge.envio` (
  id STRING NOT NULL,
  envio_gratis BOOL,
  tipo_logistica STRING,
  modo_envio STRING,
  etiquetas ARRAY<STRING>
);

-- Crear la tabla de Atributo
CREATE TABLE `dataengineer-meli-challenge.challenge.atributo` (
  id STRING NOT NULL,
  producto_id STRING NOT NULL,
  nombre STRING,
  valor STRING,
  fuente INT64
);

-- Crear la tabla de Cuota (Financiamiento)
CREATE TABLE `dataengineer-meli-challenge.challenge.cuota` (
  id STRING NOT NULL,
  producto_id STRING NOT NULL,
  cantidad INT64,
  monto_por_cuota FLOAT64,
  tasa_interes FLOAT64,
  moneda STRING
);
