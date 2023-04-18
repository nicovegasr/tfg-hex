# Librerias de terceras partes.
from dash import html, callback, Input, Output, ALL
from infrastructure.utils.uploadfile_sort import body_of_uploading_files

@callback(
    Output('upload-message', 'children'),
    Input({'type': 'upload-file', 'index': ALL}, 'filename'),
)
def PostFileDrivers(filename):
    if (filename[0] is  None):
        return html.P('Ningún archivo seleccionado.'),
    ficheros = ", ".join(filename[0]) + "."
    return html.P(children=[ficheros]),


#   Input({'type': 'upload-file', 'index': ALL}, 'contents'),
#   Input('algorithm_selected', 'data')
#        print(algorithm_selected['data'])
#        print(body_of_uploading_files(filename[0], contents[0]))
