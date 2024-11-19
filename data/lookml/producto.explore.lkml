explore: producto

join: vendedor {
  sql_on: ${producto.vendedor_id} = ${vendedor.id} ;; ;;
  relationship: many_to_one
}

join: envio {
  sql_on: ${producto.envio_id} = ${envio.id} ;; ;;
  relationship: many_to_one
}

join: atributo {
  sql_on: ${producto.id} = ${atributo.producto_id} ;; ;;
  relationship: one_to_many
}