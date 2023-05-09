import pandas as pd

# Modulos locales


def start(*arguments):
    content_files = arguments[1]
    file = content_files[0].copy()  # Crear una copia del DataFrame original
    file.columns = ["Dia", "Linea", "Fecha_Salida", "Fecha_Llegada", "Direccion"]
    file["Fecha_Salida"] = pd.to_datetime(file["Fecha_Salida"])
    file["Fecha_Llegada"] = pd.to_datetime(file["Fecha_Llegada"])
    sorted_file = file.sort_values(by=["Fecha_Salida"], ascending=True)
    sorted_file = sorted_file.reset_index(drop=True)
    departure_dates = sorted_file.iloc[:, 2]
    arrival_dates = sorted_file.iloc[:, 3]
    for date_value in range(len(departure_dates)):
        if departure_dates[date_value] > arrival_dates[date_value]:
            raise Exception(
                f"La fecha de salida no puede ser mayor que la de llegada, porfavor revise las fechas en la fila con valor fecha de salida: {departure_dates[date_value]}."
            )
