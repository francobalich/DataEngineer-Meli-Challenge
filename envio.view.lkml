view: envio

dimension: id {
  type: string
  sql: ${TABLE}.id ;; ;;
}

dimension: envio_gratis {
  type: number
  sql: ${TABLE}.envio_gratis ;; ;;
}

dimension: tipo_logistica {
  type: string
  sql: ${TABLE}.tipo_logistica ;; ;;
}

dimension: modo_envio {
  type: string
  sql: ${TABLE}.modo_envio ;; ;;
}

dimension: etiquetas {
  type: array
  sql: ${TABLE}.etiquetas ;; ;;
}