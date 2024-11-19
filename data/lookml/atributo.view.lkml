view: atributo

dimension: id {
  type: string
  sql: ${TABLE}.id ;; ;;
}

dimension: producto_id {
  type: string
  sql: ${TABLE}.producto_id ;; ;;
}

dimension: nombre {
  type: string
  sql: ${TABLE}.nombre ;; ;;
}

dimension: valor {
  type: string
  sql: ${TABLE}.valor ;; ;;
}

dimension: fuente {
  type: number
  sql: ${TABLE}.fuente ;; ;;
}