from dash import dash_table, html
import pandas as pd

def visualizer(files: list[pd.DataFrame]):
    tables = []
    for file in files:
        table = dash_table.DataTable(
            data=file.to_dict("records"),
            columns=[
                {"name": column_value, "id": column_value}
                for column_value in file.columns
            ],
            style_header={
                "backgroundColor": "rgb(62, 62, 62)",
                "color": "white",
                "fontWeight": "bold",
            },
            style_cell={"textAlign": "left"},
        )
        div_table = html.Div(
            children=table, style={"margin": ".375rem", "overflow": "scroll"}
        )
        tables.append(div_table)
    return tables
