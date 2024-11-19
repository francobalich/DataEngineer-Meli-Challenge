view: producto

dimension: id {
  type: string
  sql: ${TABLE}.id ;; ;;
}

dimension: titulo {
  type: string
  sql: ${TABLE}.titulo ;; ;;
}

dimension: condicion {
  type: string
  sql: ${TABLE}.condicion ;; ;;
}

dimension: permalink {
  type: string
  sql: ${TABLE}.permalink ;; ;;
}

dimension: dominio_id {
  type: string
  sql: ${TABLE}.dominio_id ;; ;;
}

dimension: categoria_id {
  type: string
  sql: ${TABLE}.categoria_id ;; ;;
}

dimension: vendedor_id {
  type: number
  sql: ${TABLE}.vendedor_id ;; ;;
}

dimension: envio_id {
  type: string
  sql: ${TABLE}.envio_id ;; ;;
}

dimension: precio {
  type: number
  sql: ${TABLE}.precio ;; ;;
}

dimension: precio_original {
  type: number
  sql: ${TABLE}.precio_original ;; ;;
}

dimension: cantidad_disponible {
  type: number
  sql: ${TABLE}.cantidad_disponible ;; ;;
}

dimension: acepta_mercadopago {
  type: number
  sql: ${TABLE}.acepta_mercadopago ;; ;;
}

dimension: fecha_limite {
  type: string
  sql: ${TABLE}.fecha_limite ;; ;;
}

dimension: tipo_listado {
  type: string
  sql: ${TABLE}.tipo_listado ;; ;;
}

dimension: modo_compra {
  type: string
  sql: ${TABLE}.modo_compra ;; ;;
}