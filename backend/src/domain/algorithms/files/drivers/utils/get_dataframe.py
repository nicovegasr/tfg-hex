import pandas as pd

def get_dataframe(files: dict):
    json_dataframe =  files["file_1"]["file_content"]
    dataframe = pd.read_json(json_dataframe)
    return dataframe
 