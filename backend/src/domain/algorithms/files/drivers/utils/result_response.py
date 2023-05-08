def result_response(filename, driver_result, driver_timetable):
    response_1 = {"file_1": {"filename": filename, "file_content": driver_result}}
    response_2 = {
        "file_2": {
            "filename": "Nuevo_archivo_generado",
            "file_content": driver_timetable,
        }
    }
    json_response = {**response_1, **response_2}
    return json_response
