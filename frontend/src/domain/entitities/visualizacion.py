
from dash import dash_table, html, dcc
import plotly.express as px
import pandas as pd

class Visualizacion:
    def __init__(self, archivos, algoritmo_seleccionado):
        self.archivos = archivos
        self.algoritmo = algoritmo_seleccionado

    # Importante que el resultado se devuelva como una lista.
    def iniciar(self):
        if hasattr(Visualizacion, self.algoritmo):
            resultado = getattr(self, self.algoritmo)()
        else:
            resultado = self.default()
        resultado.append(html.Button('Descargar', id={
                         'type': 'btn-descarga', 'index': 'btn-descarga'}, className="boton-descarga", n_clicks=0))
        return resultado

    # Por defecto se mostrarán las tablas en la app web.
    def default(self):
        tablas = []
        for archivo in self.archivos:
            tabla = dash_table.DataTable(
                data=archivo.to_dict('records'),
                columns=[{"name": i, "id": i} for i in archivo.columns],
                style_header={
                    'backgroundColor': 'rgb(62, 62, 62)',
                    'color': "white",
                    'fontWeight': 'bold'
                },
                style_cell={'textAlign': 'left'}
            )
            tabla_div = html.Div(children=tabla, style={
                                 'margin': '.375rem', 'overflow': 'scroll'})
            tablas.append(tabla_div)
        return tablas


    def conductores(self):
        archivo = self.archivos[0]
        df = pd.DataFrame() # Crear dataframe vacío
        for i in range(archivo.shape[0]):
            hora_inicio = archivo["Fecha_Salida"][i]
            hora_final = archivo["Fecha_Llegada"][i]
            conductor = archivo["conductor_id"][i]
            if archivo["Direccion"][i] == 11:
                estacion_salida = ' Estacion de Salida: A'
            else:
                estacion_salida = 'Estacion de Salida: B'
            row = {"Hora de salida": hora_inicio, "Hora de llegada": hora_final, "Estacion de salida" : estacion_salida, "Conductor" : conductor}
            df = pd.concat([df, pd.DataFrame.from_records([row])]) # Agregar la fila al dataframe
        
        fig = px.timeline(df, x_start="Hora de salida", x_end="Hora de llegada", y="Conductor", color="Conductor", hover_name="Estacion de salida", title="Viajes")
        # Siguiente archivo.
        archivo = self.archivos[1]
        df = pd.DataFrame() # Crear dataframe vacío
        for i in range(archivo.shape[0]):
            hora_inicio = archivo["Inicio_Descanso"][i]
            hora_final = archivo["Final_Descanso"][i]
            conductor = archivo["Conductor"][i]
            row = {"Inicio de descanso": hora_inicio, "Final de descanso": hora_final, "Conductor": conductor}
            df = pd.concat([df, pd.DataFrame.from_records([row])]) # Agregar la fila al dataframe
        
        fig2 = px.timeline(df, x_start="Inicio de descanso", x_end="Final de descanso", y="Conductor", color="Conductor", title="Descansos")
        return [html.Div(className="gantt-chart-container",children=[dcc.Graph(className='gantt-chart', figure=fig)]), html.Div(className="gantt-chart-container-2",children=[dcc.Graph(className='gantt-chart', figure=fig2)])]

'''
DESCARGAR LAS GRAFICAS:

import plotly.graph_objs as go
import plotly.io as pio

fig = go.Figure(data=[go.Bar(x=[1, 2, 3], y=[4, 5, 6])])

# Descargar la gráfica en formato de imagen
pio.write_image(fig, 'grafica.png')

# Descargar la gráfica en formato interactivo
pio.write_html(fig, 'grafica.html')
'''