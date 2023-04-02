# **Trabajo final de grado**

![Planteamieto de la arquitectura hexagonal en el backend](./docs/images/backend_hex.png)

![Flujo de endpoints para la conexcion con el frontend](./docs/images/flujo_front.png)


## **Explicacion general**

## **Trazabilidad añadiendo nuevo algoritmo**

## **Testing**
![Flujo de endpoints para la conexcion con el frontend](./docs/images/test.png)

## **Estructura de los archivos de configuración**
```json
 { 
  "name": "Nombre del archivo de configuracion",
  "n_files": "Numero de ficheros a subir, excel o csv.",
  "n_cols": ["Primer nº de columnas para el archivo nº1", "Segundo nº de columna para el archivo nº2"],  
  "cols_types": [["Tipo de la primera columna del primer archivo", "..."], ["Tipo de la primera columna del segundo archivo", "..."]],
  "allowed_nulls": ["0: No se permiten nulls en el primer archivo", "1: Se permiten nulls en el segundo archivo"],
  "aditional_description": "Descripcion aicional que se quiera proporcionar en formato texto"
} 
```


