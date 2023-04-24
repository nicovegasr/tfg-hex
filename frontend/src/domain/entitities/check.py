import datetime
import math
# Modulos de terceros
import pandas as pd
# Modulos locales

class Check:
    # Constructor que asigna el nombre de algorithm_name y los fichero en formato: [[nombre, contenido], [nombre, contenido]]
    def __init__(self, filenames: list(str), files: list(pd.DataFrame), configuration_file: dict):
        self.filenames = filenames
        self.files = files
        self.configuration_file = configuration_file

    ''' Se comprueban las configuraciones por defecto, en caso de querer comprobar cosas propias de cada algorithm_name se llamaria a otro metodo
     en caso de estar definido que tendria el mismo nombre que el algorimto seleccionado '''

    def start(self) -> None:
        configuration_file = self.configuration_file
        for current_file in range(len(self.files)):
            file = self.files[current_file]
            n_cols = configuration_file["num_columnas"][current_file]
            tipo_col = configuration_file["tipos_columnas"][current_file]
            nulls = configuration_file["nulls_permitidos"][current_file]
            if not (self.num_columnas(n_cols, file)):
                return f"El número de columnas del fichero {self.filenames[current_file]} es incorreccto."
            if (self.types(tipo_col, file) != 0):
                mensaje = self.types(tipo_col, file)
                return f"En el fichero {self.filenames[current_file]}: {mensaje}"
            if not (self.nulls(nulls, file)):
                return f"En el fichero {self.filenames[current_file]} hay celdas vacías. Por favor revise el fichero."
        return 0

    # Comprueba que el numero de columnas del file seleccionado es igual al configurado.
    def num_columnas(self, n_cols, file):
        if (file.shape[1] == int(n_cols)):
            return True
        else:
            return False

    # Tipos soportados: int, str, float, datetime.
    def types(self, types, file):
        # Si no se indican todos los types de las columnas, se le indica al usuario.
        if (file.shape[1] != len(types)):
            return f"En el fichero de configuración, no ha indicado el número correcto de types,\
                porfavor revise el campo tipos_columnas y asegurese que define el tipo de todas las columnas."
        # Comprobar que todos los datos de la columna son del tipo indicado en 'tipo' en caso de que alguno
        # no lo sea retornar una string diciendo la columna y fila donde el dato no es del tipo indicado.
        for current_file in range(file.shape[1]):
            columna = file.iloc[:, current_file]
            tipo = types[current_file]
            if (tipo == 'str'):
                for j, valor in enumerate(columna):
                    try:
                        str(valor)
                    except:
                        return f"En la columna {current_file + 1}, fila {j + 1}, el valor {valor} no es del tipo 'str'"
            elif (tipo == 'int'):
                for j, valor in enumerate(columna):
                    if math.isnan(valor):
                        continue
                    try:
                        int(valor)
                    except:
                        return f"En la columna {current_file + 1}, fila {j + 1}, el valor {valor} no es del tipo 'int'"
            elif (tipo == 'float'):
                for j, valor in enumerate(columna):
                    if math.isnan(valor):
                        continue
                    try:
                        float(valor)
                    except:
                        return f"En la columna {current_file + 1}, fila {j + 1}, el valor {valor} no es del tipo 'float'"
            elif tipo == 'Datetime':
                for j, valor in enumerate(columna):
                    try:
                        pd.to_datetime(valor)
                    except ValueError:
                        return f"En la columna {current_file + 1}, fila {j + 1}, el valor {valor} no es una fecha y hora válida"
            else:
                return f"En la columna {current_file + 1}, el tipo '{tipo}' es inválido. {type(valor)}"
        return 0
    
    # Dado un file, compruebe que en ningun lugar hay una celda nula, si la hay devolver False.
    def nulls(self, nulls, file):
        if nulls == '0':
            if file.isnull().any().any():
                return False
            else:
                return True
        else:
            return True