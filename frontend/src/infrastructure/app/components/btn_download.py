from dash import callback, Input, Output, dcc, ALL
from infrastructure.storage.algorithm_repository import AlgorithmRepository
# Descarga los archivos de resultados en un zip.
@callback(
    Output('descarga', 'data'),
    Input({'type': 'btn-descarga', 'index': ALL}, 'n_clicks'),
    )
def boton(click):
  if click != [] and click[0] > 0:
    return dcc.send_file( AlgorithmRepository.get_last_result())