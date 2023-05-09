import datetime
import os


class AlgorithmRepository:
    @staticmethod
    def save(files: dict):
        path = os.path.dirname(os.path.realpath(__file__))
        parent_dir = path.rsplit("/storage", 1)[0] + "/storage/results"
        directory = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        for file_number, file in enumerate(files):
            file.to_csv(f"{path}/resultado{file_number}.csv", index=False)

    @staticmethod
    def get_last_result():
        pass
