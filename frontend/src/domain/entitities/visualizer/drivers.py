import pandas as pd
import plotly.express as px
from dash import dcc, html


def visualizer(files: list[pd.DataFrame]):
    file = files[0]
    df = pd.DataFrame()  # Crear dataframe vacío
    for i in range(file.shape[0]):
        hora_inicio = file["Fecha_Salida"][i]
        hora_final = file["Fecha_Llegada"][i]
        conductor = file["conductor_id"][i]
        if file["Direccion"][i] == 11:
            estacion_salida = " Estacion de Salida: A"
        else:
            estacion_salida = "Estacion de Salida: B"
        row = {
            "Hora de salida": hora_inicio,
            "Hora de llegada": hora_final,
            "Estacion de salida": estacion_salida,
            "Conductor": conductor,
        }
        # Agregar la fila al dataframe
        df = pd.concat([df, pd.DataFrame.from_records([row])])

    fig = px.timeline(
        df,
        x_start="Hora de salida",
        x_end="Hora de llegada",
        y="Conductor",
        color="Conductor",
        hover_name="Estacion de salida",
        title="Viajes",
    )

    # Siguiente file.
    file = files[1]
    df = pd.DataFrame()  # Crear dataframe vacío
    for i in range(file.shape[0]):
        hora_inicio = pd.to_datetime(file["Inicio_Descanso"][i], errors="coerce")
        hora_final = pd.to_datetime(file["Final_Descanso"][i], errors="coerce")
        conductor = file["Conductor"][i]
        row = {
            "Inicio de descanso": hora_inicio,
            "Final de descanso": hora_final,
            "Conductor": conductor,
        }
        # Agregar la fila al dataframe
        df = pd.concat([df, pd.DataFrame.from_records([row])])

    fig2 = px.timeline(
        df,
        x_start="Inicio de descanso",
        x_end="Final de descanso",
        y="Conductor",
        color="Conductor",
        title="Descansos",
    )

    return [
        html.Div(
            className="gantt-chart-container",
            children=[dcc.Graph(className="gantt-chart", figure=fig)],
        ),
        html.Div(
            className="gantt-chart-container-2",
            children=[dcc.Graph(className="gantt-chart", figure=fig2)],
        ),
    ]
