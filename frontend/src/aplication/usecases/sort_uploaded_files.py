def body_of_uploading_files(filenames: list, files_content: list) -> dict:
    files_dict = {}
    for num_file, (filename, file_content) in enumerate(zip(filenames, files_content)):
        files_dict[f"file_{num_file+1}"] = {
            "filename": filename,
            "file_content": file_content,
        }
    return files_dict
