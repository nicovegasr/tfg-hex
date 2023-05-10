import base64
import requests
import pandas as pd
from infrastructure.storage.algorithm_repository import AlgorithmRepository
import numpy as np
import threading
import multiprocessing
import geopandas
import json
import os
import dash

import plotly.graph_objects as go
from dash import html, callback

from infrastructure.http_requesters.algorithm_http_requester import AlgorithmHttpRequester

TOKEN = "pk.eyJ1IjoiY3Jpc3RvbSIsImEiOiJjbDZveG9jYjEwMG5wM2trNnlkZzFtZ3YyIn0.DSX5UzfvOxANpHMRca4Wvw"
geopandas_path = os.getcwd() + "/src/infrastructure/app/dynamic_visualizers/zones/geopandas/zonas.shp"
df_zonas = geopandas.read_file(geopandas_path).to_crs("WGS84")

lineas = []

def jsonOptimization(profile, coordinates):
    """
    Consulta a la API de Mapbox para obtener la ruta óptima entre varios puntos.
    :param profile:     tipo de  desplazamiento ("walking", "driving", "driving-traffic", "cycling")
    :param coordinates: lista de puntos del trazado (LON,LAT)
    :return:            json con los puntos del trazado óptimo en el sentido especificado sin vuelta
    """
    coords = ";".join(coordinates)
    petition = f"https://api.mapbox.com/optimized-trips/v1/mapbox/{profile}/{coords}?geometries=geojson&roundtrip=false&source=first&destination=last&access_token={TOKEN}"
    response = requests.get(petition)
    return response.json()


@callback(
    dash.Output("graph", "figure"),
    dash.Input("passenger_threshold", "value"),
    dash.Input("max_km_h", "value"),
    dash.Input("ratio_time_pass_thres", "value"),
    dash.Input("tmax", "value"),
    dash.Input("segs_parada", "value"),
    dash.Input("algorithm_request_body", "data"),
)
def get_map(
    passenger_threshold,
    max_km_h,
    ratio_time_pass_thres,
    tmax,
    segs_parada,
    algorithm_request_body
):
    if algorithm_request_body["data"] is not None:
      algorithm_body = algorithm_request_body["data"]
      parameters = {
                      "passenger_threshold": passenger_threshold,
                      "max_km_h": max_km_h, 
                      "ratio_time_pass_thres": ratio_time_pass_thres,
                      "tmax": tmax, 
                      "segs_parada": segs_parada
                   }
      data_in_dataframe = pd.DataFrame([(key, value) for key, value in parameters.items()], columns=['parameter', 'value'])
      data_in_csv = data_in_dataframe.to_csv(index=False)
      file_content_encode =  "data:;base64," + base64.b64encode(str(data_in_csv).encode('utf-8')).decode('utf-8')
      set_parameters = {"file_3": { "filename": "set_parameters" ,
                                    "file_content": file_content_encode
                                  }
                        }
      algorithm_body = {**algorithm_body, **set_parameters}      
      algorithm_request = AlgorithmHttpRequester.get_algorithm_result(algorithm_body).content.decode("utf-8")    

      AlgorithmRepository.save(json.loads(algorithm_request))
      
      df_lin = json.loads(algorithm_request)
      df_lin = pd.read_json(df_lin[0])
      layout = go.Layout(
          margin={"l": 0, "t": 0, "b": 0, "r": 0},
          mapbox={
              "accesstoken": TOKEN,
              "style": "light",
              "center": {"lat": 28.3, "lon": -16.5},
              "zoom": 9,
              "layers": [
                  {
                      "source": json.loads(df_zonas.geometry.to_json()),
                      "below": "traces",
                      "type": "line",
                      "color": "rgba(0,0,0,0.5)",
                      "line": {"width": 1},
                  }
              ],
          },
          autosize=False,
      )
      my_map = go.Figure(layout=layout)

      stops_lon_lat, lons_lats = point_requests(df_lin)

      global lineas
      lineas = sorted(lineas, key=lambda x: x["demanda_total"])[::-1]
      my_map.add_trace(
          go.Scattermapbox(
              mode="markers",
              lon=[x_ for x in stops_lon_lat for x_ in x["lon"]],
              lat=[x_ for x in stops_lon_lat for x_ in x["lat"]],
              hoverinfo="none",
              marker={"size": 10, "symbol": "bus", "allowoverlap": True},
              name="Paradas",
              showlegend=False,
          )
      )

      for idx, lon_lat in enumerate(
          sorted(lons_lats, key=lambda x: x["demanda_total"])[::-1]
      ):
          my_map.add_trace(
              go.Scattermapbox(
                  mode="markers+lines+text",
                  lon=lon_lat["lon"],
                  lat=lon_lat["lat"],
                  hovertext=[
                      f"Demanda: {d}pers<br>"
                      + f"Tiempo: {t}mins<br>"
                      + f"Demanda Total: {lon_lat['demanda_total']}pers<br>"
                      f"Tiempo Total: {lon_lat['tiempo_total']}mins<br>"
                      for d, t in zip(lon_lat["demanda"], lon_lat["tiempo"])
                  ],
                  text=[i for i in range(len(lon_lat["lon"]))],
                  name=f"{'{:{}}'.format(idx+1, 3)}, {lon_lat['name']}",
                  legendgrouptitle={"text": "Nº, Salida-Fin, Demanda Total, Min, Max"},
                  showlegend=True,
              )
          )
      return my_map

@callback(
    dash.Output("line_information", "children"),
    dash.Input("graph", "restyleData"),
)
def legend_value(value):
    if value is None:
        return ""
    if len(value[1]) == 1 and value[0]["visible"] == [True]:
        return get_line(value[1][0] - 1)


def get_line(index):
    linea = lineas[index]
    trayecto = linea["trayecto"]
    children = [
        html.Div(children=["Origen"]),
        html.Div(children=["Destino"]),
        html.Div(children=["Demanda"]),
        html.Div(children=["Tiempo"]),
    ]
    for i, (first, second) in enumerate(zip(trayecto[:-1], trayecto[1:])):
        children.append(html.Div(children=[first]))
        children.append(html.Div(children=[second]))
        children.append(html.Div(children=[round(linea["demanda"][i])]))
        children.append(html.Div(children=[round(linea["tiempo"][i] / 60, 2)]))
    children.append(html.Div(children=["Total:"]))
    children.append(html.Div(children=[""]))
    children.append(html.Div(children=[linea["demanda_total"]]))
    children.append(html.Div(children=[linea["tiempo_total"]]))
    return children


def point_requests(df_lin):
    stops_lon_lat, lons_lats = [], []
    n_lineas = len(df_lin.LINEA.unique())
    threads = []
    n_threads = multiprocessing.cpu_count()
    lines_per_thread = n_lineas // n_threads
    for i in range(n_threads):
        line_range = range(i * lines_per_thread, lines_per_thread * (i + 1))
        thread = threading.Thread(
            target=point_request, args=(df_lin, line_range, stops_lon_lat, lons_lats)
        )
        threads.append(thread)
        thread.start()
    remainder = lines_per_thread * n_threads
    if remainder != n_lineas:
        line_range = range(remainder, n_lineas)
        thread = threading.Thread(
            target=point_request, args=(df_lin, line_range, stops_lon_lat, lons_lats)
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return stops_lon_lat, lons_lats


def point_request(df_lin, line_range, stops_lon_lat, lons_lats):
    for i in line_range:
        linea = df_lin[df_lin.LINEA == i]
        coords = [
            f"{linea['ORIGEN_LONGITUD'].values[0]},"
            + f"{linea['ORIGEN_LATITUD'].values[0]}"
        ]
        for _, row in linea.iterrows():
            coords.append(f"{row['DESTINO_LONGITUD']},{row['DESTINO_LATITUD']}")

        demanda, tiempos, lon, lat = make_requests(linea, coords)

        demanda_total = round(linea.DEMANDA.sum())
        lons_lats.append(
            {
                "lon": lon,
                "lat": lat,
                "name": (
                    f"{linea.ORIGEN.values[0]} -> {linea.DESTINO.values[-1]},  "
                    + f"{'{:{}}'.format(demanda_total, 4)},  "
                    + f"{'{:{}}'.format(min(demanda), 3)},  "
                    + f"{'{:{}}'.format(max(demanda), 3)}"
                ),
                "demanda": demanda,
                "demanda_total": demanda_total,
                "tiempo": tiempos,
                "tiempo_total": round(linea.TIEMPO.sum() / 60, 2),
            }
        )
        stops_lon_lat.append(
            {
                "lon": np.append(
                    linea.ORIGEN_LONGITUD.values[:1], linea.DESTINO_LONGITUD.values
                ),
                "lat": np.append(
                    linea.ORIGEN_LATITUD.values[:1], linea.DESTINO_LATITUD.values
                ),
            }
        )
        lineas.append(
            {
                "trayecto": np.append(linea.ORIGEN.values[:1], linea.DESTINO.values),
                "demanda": linea.DEMANDA.values,
                "demanda_total": round(linea.DEMANDA.sum()),
                "tiempo": linea.TIEMPO.values,
                "tiempo_total": round(linea.TIEMPO.sum() / 60, 2),
            }
        )


def make_requests(linea, coords):
    demanda, tiempos, lon, lat = [], [], [], []
    for j in range(len(coords) // 13 + 1):
        response = jsonOptimization("driving", coords[j * 12 : j * 12 + 12])
        if "message" not in response.keys():
            waypoints = sorted(response["waypoints"], key=lambda x: x["waypoint_index"])
            puntos = response["trips"][0]["geometry"]["coordinates"]
            count = 0
            for punto in puntos:
                lon.append(punto[0])
                lat.append(punto[1])
                demanda.append(round(linea.DEMANDA.values[count + j * 12]))
                tiempos.append(round(linea.TIEMPO.values[count + j * 12] / 60, 2))
                if punto == waypoints[count + 1]["location"]:
                    count += 1
        else:
            raise Exception("Error API")
    return demanda, tiempos, lon, lat