import pandas as pd


def format_and_sort_dataframe(file: pd.DataFrame) -> pd.DataFrame:
    file.columns = ["Dia", "Linea", "Fecha_Salida", "Fecha_Llegada", "Direccion"]
    date_columns = ["Fecha_Salida", "Fecha_Llegada"]
    file[date_columns] = file[date_columns].apply(
        pd.to_datetime
    )
    file = file.sort_index(axis=1).sort_values(by=["Fecha_Salida"], ascending=True)
    file["conductor_id"] = ""
    return file
