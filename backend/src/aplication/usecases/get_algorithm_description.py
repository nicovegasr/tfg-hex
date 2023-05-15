from aplication.usecases.get_configuration_file import get_configuration_file


def get_algorithm_description(configuration_file: dict) -> list:
    try:
        description = f'Descripcion: Para que el algoritmo funcione debe introducir {configuration_file["n_files"]} archivos. '
        for file_number in range(int(configuration_file["n_files"])):
            nulls = "permitidos"
            if configuration_file["allowed_nulls"][file_number] == 0:
                nulls = "prohibidos"
            description += f'El fichero  numero {file_number + 1}: debe tener {configuration_file["n_cols"][file_number]} columna(s). Los tipos deben ser: {configuration_file["cols_types"][file_number]} y los nulos estan {nulls}. '
            aditional_description = (
                f'Descripcion adicional: {configuration_file["aditional_description"]}'
            )
        return [description, aditional_description]
    except:
        raise ValueError("There is a problem with configuration file.")
