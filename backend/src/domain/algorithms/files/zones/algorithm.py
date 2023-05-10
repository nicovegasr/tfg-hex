import json
import pandas as pd
from .models.solver import solve

# La idea es que en dataframes contents estén los archivos:
# * 1.- full dataframe
# * 2.- paradas_max_pasajeros 
def algorithm(*arguments):
    full_dataframe_json = json.loads(arguments[0][0]["file_1"]["file_content"])
    paradas_max_pasajeros_dataframe_json = json.loads(arguments[0][0]["file_2"]["file_content"])
    try:
        set_values_dataframe_with_no_format = json.loads(arguments[0][0]["file_3"]["file_content"])
        set_values_dataframe = {set_values_dataframe_with_no_format['parameter'][key]: set_values_dataframe_with_no_format['value'][key] for key in set_values_dataframe_with_no_format['parameter']}
        passenger_threshold: float = float(set_values_dataframe["passenger_threshold"])
        max_km_h: int = int(set_values_dataframe["max_km_h"])
        ratio_time_pass_thres: int = int(set_values_dataframe["ratio_time_pass_thres"])
        tmax: int = int(set_values_dataframe["tmax"])
        segs_parada: int = int(set_values_dataframe["segs_parada"])
    except: 
        passenger_threshold: float = 10.0
        max_km_h: int = 17
        ratio_time_pass_thres: int = 200
        tmax: int = 45 * 60
        segs_parada: int = 30

    full_dataset_dataframe = pd.DataFrame.from_dict(full_dataframe_json)
    max_passengers_stop_dataframe = pd.DataFrame.from_dict(paradas_max_pasajeros_dataframe_json)

    df_lin = solve(
        full_dataset_dataframe,
        max_passengers_stop_dataframe,
        passenger_threshold,
        max_km_h,
        ratio_time_pass_thres,
        tmax,
        segs_parada,
    )


    full_dataframe_name = arguments[0][0]["file_1"]["filename"]

    response = {"file_1": {"filename": full_dataframe_name , "file_content": df_lin.to_json()}}

    return response
    

    