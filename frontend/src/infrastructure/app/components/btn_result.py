
from dash import html, callback, Input, Output, State, ALL


#TODO: HAcer el callback con varios output y pasarle tanto algorithm selected como el configuration file por Iput del dcc.Store y los files subidos que a lo mejor seria buena idea pasar directamente desde un dcc.Store el formato del body que ya tengo.

# Hacemos visible la parte de la visualización donde tambien se manejaran los errores correspondientes:
@callback(
    Output('visualizacion', 'style'),
    [Input('dropdown-seleccion', 'value'),
     Input({'type': 'upload-file', 'index': ALL}, 'filename'), Input({'type': 'boton', 'index': ALL}, 'n_clicks')]
)
def toggle_visibility(value, filename, n_clicks):
    if value is None:
        return {'visibility': 'hidden'}
    else:
        if filename == [] or filename[0] is None:
            return {'visibility': 'hidden'}
        else:
            if n_clicks == [] or n_clicks[0] == 0:
                return {'visibility': 'hidden'}
            else:
                return {'visibility': 'visible'}


# Seteamos los ficheros con sus nombres, contenido y el nombre de algoritmo para posteriormente inicializar todo.
@callback(
    Output('visualizacion', 'n_clicks'),
    [Input('dropdown-seleccion', 'value'),
     Input({'type': 'upload-file', 'index': ALL}, 'filename'), Input({'type': 'upload-file', 'index': ALL}, 'contents')]
)
def set_var(value, filename, contents):
    global algoritmo_seleccionado, files
    files = []
    if value is None:
        pass
    else:
        if filename == [] or filename[0] is None:
            pass
        else:
            if contents == [] or contents[0] == None:
                pass
            else:
                algoritmo_seleccionado = value
                for i in range(len(filename[0])):
                    files.append([filename[0][i], contents[0][i]])

# Al hacer click llamaremos a Comprobar, al Algoritmo y a Visualizacion.
@callback(
    Output('visualizacion', 'children'),
    Input({'type': 'boton', 'index': 'btn-resultado'}, 'n_clicks'),
    )
def boton(click):
    global algoritmo_seleccionado, files
    if click > 0:
        # Llamamos a comprobaciones.
        comprobaciones = Comprobar(algoritmo_seleccionado, files)
        mensaje = comprobaciones.inciar()
        if mensaje != 0: return html.P(mensaje)
        # Si todo sale bien, llamamos al algoritmo. Llegados a este punto todo acerca del fichero debe ser correcto asi que no deberia de fallar.
        algoritmo = Algoritmo(algoritmo_seleccionado, files)
        archivos = algoritmo.iniciar()
        # Ahora deberia devolver la visualizacion
        visualizacion = Visualizacion(archivos, algoritmo_seleccionado)
        return visualizacion.iniciar()