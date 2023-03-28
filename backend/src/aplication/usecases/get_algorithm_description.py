from get_configuration_file import get_configuration_file

def get_algorithm_description(algorithm_name: str) -> list:
    data = get_configuration_file(algorithm_name)
    if (not (data == "")):
        description = f'Descripcion: Para que el algoritmo funcione debe introducir {data["n_files"]} archivos. '
        for i in range(int(data["n_files"])):
            description += f'El fichero  numero {i+1}: debe tener {data["n_cols"][i]} columna(s) y los tipos deben ser: {data["cols_types"][i]}. '
            aditional_description = f'Descripcion adicional: {data["aditional_description"]}'
        return [description, aditional_description]
    return []