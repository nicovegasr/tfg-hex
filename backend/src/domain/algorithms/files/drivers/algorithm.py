import pandas as pd

from entities.driver import Driver
from entities.travel import Travel

def timetable_drivers(available_drivers):
    drivers_working = []
    for conductor in available_drivers:
        if conductor.hora_inicio_jornada != None:
            drivers_working.append(conductor)
    # Creamos las columnas del nuevo dataframe que tendrá el horario de los conductores:
    columnas = ["Conductor", "Inicio_Descanso", "Final_Descanso"]
    drivers_timetable = pd.DataFrame(
        columns=columnas, index=range(len(drivers_working)))
    for i in range(len(drivers_working)):
        drivers_timetable["Conductor"][i] = drivers_working[i].id
        drivers_timetable["Inicio_Descanso"][i] = drivers_working[i].descanso_inicio
        drivers_timetable["Final_Descanso"][i] = drivers_working[i].descanso_final
    return drivers_timetable


def get_dataframe(files: dict):
    json_dataframe =  files["file_1"]["file_content"]
    dataframe = pd.read_json(json_dataframe)
    return dataframe
 
def format_and_sort_dataframe(file: pd) -> pd:
    file.columns = ["Dia", "Linea", "Fecha_Salida", "Fecha_Llegada", "Direccion"]
    date_columns = ["Fecha_Salida", "Fecha_Llegada"]
    file[date_columns] = file[date_columns].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S')
    file = file.sort_index(axis=1).sort_values(by=['Fecha_Salida'], ascending=True)
    file['conductor_id'] = ""
    return file

def result_response(filename, driver_result, driver_timetable):
    response_1 = {"file_1" : {"filename": filename, "content": driver_result}}
    response_2 = {"file_2" : {"filename": "Nuevo_archivo_generado", "content": driver_timetable}}
    json_response = {**response_1, **response_2}
    return json_response

def algorithm(files):
    filename = files["file_1"]["filename"]
    file = get_dataframe(files)  
    sorted_file = format_and_sort_dataframe(file)
    available_drivers = [Driver(i) for i in range(1, 50)]
    # Recorremos todos los viajes.
    for i in range(sorted_file.shape[0]):
        # calculamos el tiempo del viaje.
        travel_time = sorted_file['Fecha_Llegada'][i] - \
            sorted_file['Fecha_Salida'][i]

        # Obtenemos la hora de inicio y final de los viajes en buen formato y los pasamos a su tipo correspondiente.

        # hora_inicio_str = sorted_file['Fecha_Salida'].dt.strftime('%H:%M:%S')[i]
        # hora_final_str = sorted_file['Fecha_Llegada'].dt.strftime('%H:%M:%S')[i]
        hora_inicio = sorted_file['Fecha_Salida'][i]
        hora_final = sorted_file['Fecha_Llegada'][i]
        # Obtenemos la dirección del viaje y creamos nuestro viaje.
        lugar = sorted_file['Direccion'][i]
        viaje_actual = Travel(
            i, hora_inicio, hora_final, travel_time, lugar)

        # Seleccionamos el primer conductor disponible.
        for conductor in available_drivers:
            if conductor.viaje_disponible(viaje_actual):
                conductor.asginar_viaje(viaje_actual)
                sorted_file.at[i, 'conductor_id'] = conductor.id
                break
    # Creamos un file con los descansos de los conductores .
    timetable = timetable_drivers(available_drivers)    
    response = result_response(filename, sorted_file.to_json(), timetable.to_json())
    return response