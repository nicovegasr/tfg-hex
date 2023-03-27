from datetime import datetime
import pandas as pd

from .entities.driver import Conductor
from .entities.travel import Viaje


def algorithm(archivos):
    archivo = archivos[0].copy()  # Crear una copia del DataFrame original
    archivo.columns = ["Dia", "Linea",
                       "Fecha_Salida", "Fecha_Llegada", "Direccion"]
    archivo['Fecha_Salida'] = pd.to_datetime(
        archivo['Fecha_Salida'], format='%Y-%m-%d %H:%M:%S')
    archivo['Fecha_Llegada'] = pd.to_datetime(
        archivo['Fecha_Llegada'], format='%Y-%m-%d %H:%M:%S')
    # Ordenamos el archivo y ponemos los nuevos indices
    archivo_ordenado = archivo.sort_values(by=['Fecha_Salida'], ascending=True)
    archivo_ordenado = archivo_ordenado.reset_index(drop=True)
    archivo_ordenado = archivo_ordenado.assign(
        conductor_id=pd.Series("", dtype="object"))
    # Creamos muchos conductores
    conductores_disponibles = [Conductor(i) for i in range(1, 50)]
    # Recorremos todos los viajes.
    for i in range(archivo_ordenado.shape[0]):
        # calculamos el tiempo del viaje.
        tiempo_viaje = archivo_ordenado['Fecha_Llegada'][i] - \
            archivo_ordenado['Fecha_Salida'][i]

        # Obtenemos la hora de inicio y final de los viajes en buen formato y los pasamos a su tipo correspondiente.

        # hora_inicio_str = archivo_ordenado['Fecha_Salida'].dt.strftime('%H:%M:%S')[i]
        # hora_final_str = archivo_ordenado['Fecha_Llegada'].dt.strftime('%H:%M:%S')[i]
        hora_inicio = archivo_ordenado['Fecha_Salida'][i]
        hora_final = archivo_ordenado['Fecha_Llegada'][i]
        # Obtenemos la dirección del viaje y creamos nuestro viaje.
        lugar = archivo_ordenado['Direccion'][i]
        viaje_actual = Viaje(
            i, hora_inicio, hora_final, tiempo_viaje, lugar)

        # Seleccionamos el primer conductor disponible.
        for conductor in conductores_disponibles:
            if conductor.viaje_disponible(viaje_actual):
                conductor.asginar_viaje(viaje_actual)
                archivo_ordenado.at[i, 'conductor_id'] = conductor.id
                break

    # Creamos un archivo con los descansos de los conductores .
    conductores_trabajando = []
    for conductor in conductores_disponibles:
        if conductor.hora_inicio_jornada != None:
            conductores_trabajando.append(conductor)
    # Creamos las columnas del nuevo dataframe que tendrá el horario de los conductores:
    columnas = ["Conductor", "Inicio_Descanso", "Final_Descanso"]
    horario_conductores = pd.DataFrame(
        columns=columnas, index=range(len(conductores_trabajando)))
    for i in range(len(conductores_trabajando)):
        horario_conductores["Conductor"][i] = conductores_trabajando[i].id
        horario_conductores["Inicio_Descanso"][i] = conductores_trabajando[i].descanso_inicio
        horario_conductores["Final_Descanso"][i] = conductores_trabajando[i].descanso_final

    archivo_ordenado['Fecha_Salida'] = archivo_ordenado['Fecha_Salida'].astype(
        str)
    archivo_ordenado['Fecha_Llegada'] = archivo_ordenado['Fecha_Llegada'].astype(
        str)

    return [archivo_ordenado, horario_conductores]
