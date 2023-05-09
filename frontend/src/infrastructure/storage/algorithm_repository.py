import datetime
import os
import pandas as pd
import zipfile
import io

class AlgorithmRepository:
    storage_dir = os.path.dirname(os.path.realpath(__file__)) + "/results"

    @staticmethod
    def save(files: list[dict]):
        directory_name = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        with zipfile.ZipFile(f'{AlgorithmRepository.storage_dir}/{directory_name}.zip', 'w') as myzip:
            for file_index, file in enumerate(files):
                dataframe_json = pd.read_json(file)
                csv_buffer = pd.DataFrame.to_csv(dataframe_json, index=False)
                myzip.writestr(f'file_{file_index + 1}.csv', csv_buffer)
    
    @staticmethod
    def get_last_result():
        return (AlgorithmRepository.storage_dir + "/" + os.listdir(AlgorithmRepository.storage_dir)[-1])
        