Importante:

Si se añaden algoritmos con tipos no añadidos (soportados) en los archivos de configuracion del backend tendra que modificarse en el usecase del frontend que crear el pandera shcema y valida que los dataframe de los archivos procesados sigan dicho schema. 


Deudas técnicas:
* El Datetime en el check por default tiene problemas con enteros ya que considera enteros como posibles datetime, el problema si se define un formato en especifico perderiamos muchos posibles formatos de datetime.
