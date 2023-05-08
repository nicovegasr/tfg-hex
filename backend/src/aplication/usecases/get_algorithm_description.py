from aplication.usecases.get_configuration_file import get_configuration_file


def get_algorithm_description(algorithm_name: str) -> list:
    try:
        data = get_configuration_file(algorithm_name)
        description = f'Descripcion: Para que el algoritmo funcione debe introducir {data["n_files"]} archivos. '
        for i in range(int(data["n_files"])):
            nulls = "permitidos"
            if data["allowed_nulls"][i] == 0:
                nulls = "prohibidos"
            description += f'El fichero  numero {i+1}: debe tener {data["n_cols"][i]} columna(s). Los tipos deben ser: {data["cols_types"][i]} y los nulos estan {nulls}. '
            aditional_description = (
                f'Descripcion adicional: {data["aditional_description"]}'
            )
        return [description, aditional_description]
    except:
        raise ValueError("There is a problem with configuration file.")
