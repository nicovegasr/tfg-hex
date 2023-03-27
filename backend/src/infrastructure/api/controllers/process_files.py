
from flask import make_response, request
from src.aplication.usecases.process_algorithm_files import process_algorithm_files

def sort_files(files):
    files_list = []
    for key in sorted(files.keys()):
        file_info = files[key]
        file_content = file_info["file_content"]
        files_list.append(file_content)
    return files_list

def process_files():
    files = request.data
    sorted_files = sort_files(files)
    print(files, "################", sorted_files)
    return 0