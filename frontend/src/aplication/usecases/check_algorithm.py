import json

from domain.entities.check import Check

def split_files_and_filenames(files: dict):
    filenames = []
    file_contents = []
    for file_key in files:
        file = files[file_key]
        filenames.append(file['filename'])
        file_contents.append(file['file_content'])
    print(filenames)
    return filenames, file_contents

def check_algorithm(files: dict, configuration_file: dict) -> None:
    filenames, files_contents = split_files_and_filenames(files)
    checker = Check(filenames, files_contents, configuration_file)
    return None 
