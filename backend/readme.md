# Estructura de los archivos de configuración:

```json
 { 
  "name": "Nombre del archivo de configuracion",
  "num_excel": "Numero de ficheros a subir, excel o csv.",
  "num_columnas": ["Primer nº de columnas para el archivo nº1", "Segundo nº de columna para el archivo nº2"],  
  "tipos_columnas": [["Tipo de la primera columna del primer archivo", "..."], ["Tipo de la primera columna del segundo archivo", "..."]],
  "nulls_permitidos": ["0: No se permiten nulls en el primer archivo", "1: Se permiten nulls en el segundo archivo"],
  "descripcion_adicional": "Descripcion aicional que se quiera proporcionar en formato texto"
} 
```
