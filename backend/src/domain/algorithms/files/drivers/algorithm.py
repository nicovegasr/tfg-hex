import json
from .entities.driver import Driver
from .entities.travel import Travel

from .utils.format_and_sort_dataframe import format_and_sort_dataframe
from .utils.get_dataframe import get_dataframe
from .utils.result_response import result_response
from .utils.timetable_drivers import timetable_drivers


def algorithm(*arguments):
    files = (arguments[0][0])
    filename = files["file_1"]["filename"]
    file = get_dataframe(files)
    sorted_file = format_and_sort_dataframe(file)
    available_drivers = [Driver(i) for i in range(1, 50)]
    # Recorremos todos los viajes.
    for i in range(sorted_file.shape[0]):
        # calculamos el tiempo del viaje.
        travel_time = sorted_file["Fecha_Llegada"][i] - sorted_file["Fecha_Salida"][i]

        # Obtenemos la hora de inicio y final de los viajes en buen formato y los pasamos a su tipo correspondiente.

        # hora_inicio_str = sorted_file['Fecha_Salida'].dt.strftime('%H:%M:%S')[i]
        # hora_final_str = sorted_file['Fecha_Llegada'].dt.strftime('%H:%M:%S')[i]
        hora_inicio = sorted_file["Fecha_Salida"][i]
        hora_final = sorted_file["Fecha_Llegada"][i]
        # Obtenemos la dirección del viaje y creamos nuestro viaje.
        lugar = sorted_file["Direccion"][i]
        viaje_actual = Travel(i, hora_inicio, hora_final, travel_time, lugar)

        # Seleccionamos el primer conductor disponible.
        for conductor in available_drivers:
            if conductor.viaje_disponible(viaje_actual):
                conductor.asginar_viaje(viaje_actual)
                sorted_file.at[i, "conductor_id"] = conductor.id
                break
    # Creamos un file con los descansos de los conductores .
    timetable = timetable_drivers(available_drivers)
    sorted_file["Fecha_Salida"] = sorted_file["Fecha_Salida"].astype(str)
    sorted_file["Fecha_Llegada"] = sorted_file["Fecha_Llegada"].astype(str)

    timetable["Inicio_Descanso"] = timetable["Inicio_Descanso"].astype(str)
    timetable["Final_Descanso"] = timetable["Final_Descanso"].astype(str)

    response = result_response(filename, sorted_file.to_json(), timetable.to_json())
    return response
