import pandas as pd


def timetable_drivers(available_drivers):
    drivers_working = []
    for conductor in available_drivers:
        if conductor.hora_inicio_jornada is not None:
            drivers_working.append(conductor)
    # Creamos las columnas del nuevo dataframe que tendrá el horario de los conductores:
    new_columns = ["Conductor", "Inicio_Descanso", "Final_Descanso"]
    drivers_timetable = pd.DataFrame(
        columns=new_columns, index=range(len(drivers_working))
    )
    for i in range(len(drivers_working)):
        drivers_timetable["Conductor"][i] = drivers_working[i].id
        drivers_timetable["Inicio_Descanso"][i] = drivers_working[i].descanso_inicio
        drivers_timetable["Final_Descanso"][i] = drivers_working[i].descanso_final
    return drivers_timetable
