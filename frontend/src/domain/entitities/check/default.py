import datetime
import math
# Modulos de terceros
import pandas as pd
# Modulos locales

class DefaultCheck:
    # Constructor que asigna el nombre de algorithm_name y los fichero en formato: [[nombre, contenido], [nombre, contenido]]
    def __init__(self, filenames: list[str], content_files: list[pd.DataFrame], configuration_file: dict):
        self.filenames = filenames
        self.content_files = content_files
        self.configuration_file = configuration_file


    ''' Se comprueban las configuraciones por defecto definidas en los ficheros de configuracion.'''
    def start(self) -> None:
        configuration_file = self.configuration_file
        for current_content_file in range(len(self.content_files)):
            file = self.content_files[current_content_file]
            n_cols = configuration_file["n_cols"][current_content_file]
            col_type = configuration_file["cols_types"][current_content_file]
            nulls = configuration_file["allowed_nulls"][current_content_file]
            try:
                self.check_n_cols(n_cols, file)
                self.types(col_type, file)
                self.nulls(nulls, file)
            except Exception as error:
                raise Exception(f"En el fichero {self.filenames[current_content_file]}: {str(error)}")


    # Comprueba que el numero de columnas del file seleccionado es igual al configurado.
    def check_n_cols(self, n_cols, file):
        if not file.shape[1] == int(n_cols):
            raise Exception(f"El número de columnas del fichero es incorreccto.")

    # Dado un file, compruebe que en ningun lugar hay una celda nula, si la hay devolver False.
    def nulls(self, nulls, file):
        if nulls == '0':
            if file.isnull().any().any():
                raise Exception("Hay nulls en el fichero y no estan permitidos.")
            
    # Tipos soportados: int, str, float, datetime.
    def types(self, types, file):
        # Si no se indican todos los types de las columnas, se le indica al usuario.
        if (file.shape[1] != len(types)):
            raise Exception(f"En el fichero de configuración, no ha indicado el número correcto de types,\
                porfavor revise el campo cols_types y asegurese que define el tipo de todas las columnas.")
        # Comprobar que todos los datos de la columna son del tipo indicado en 'tipo' en caso de que alguno
        # no lo sea retornar una string diciendo la columna y fila donde el dato no es del tipo indicado.
        for column in range(file.shape[1]):
            columna = file.iloc[:, column]
            tipo = types[column]
            if (tipo == 'str'):
                for fila, valor in enumerate(columna):
                    try:
                        str(valor)
                    except:
                        raise Exception(f"En la columna {column + 1}, fila {fila + 1}, el valor {valor} no es del tipo 'str'")
            elif (tipo == 'int'):
                for fila, valor in enumerate(columna):
                    if math.isnan(valor):
                        continue
                    try:
                        int(valor)
                    except:
                        raise Exception(f"En la columna {column + 1}, fila {fila + 1}, el valor {valor} no es del tipo 'int'")
            elif (tipo == 'float'):
                for fila, valor in enumerate(columna):
                    if math.isnan(valor):
                        continue
                    try:
                        float(valor)
                    except:
                        raise Exception(f"En la columna {column + 1}, fila {fila + 1}, el valor {valor} no es del tipo 'float'")
            elif tipo == 'Datetime':
                for fila, valor in enumerate(columna):
                    try:
                        pd.to_datetime(valor)
                    except:
                        raise Exception(f"En la columna {column + 1}, fila {fila + 1}, el valor {valor} no es una fecha y hora válida")
            else:
                raise Exception(f"En la columna {column + 1}, el tipo '{tipo}' es inválido. {type(valor)}")
    
