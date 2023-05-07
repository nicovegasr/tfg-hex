import json
import pandas as pd

def split_files_and_filenames(files: dict):
    filenames = []
    file_contents = []
    for file_key in files:
        file = files[file_key]
        filenames.append(file['filename'])
        file_contents.append(pd.DataFrame.from_dict(\
                             json.loads(file['file_content'])))
    return filenames, file_contents