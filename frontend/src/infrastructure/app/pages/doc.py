import os
import dash
from dash import dcc, html

dash.register_page(__name__, path="/doc", title="Documentacion")

backend_video = "assets" + "/backend_algorithm_add.mp4"
frontend_video = "assets" + "/frontend_algorithm_add.mp4"

layout = html.Div(
    className="docs-table",
    children=[
    html.Div(
        className="docs",
        children=[
            html.Div(
                className="doc",
                children=[
                    dcc.Markdown(
                        """
                        # Instrucciones para añadir algoritmos.
                        ## Aclaraciones
                        
                        A la hora de añadir cualquier algoritmo hace falta tener diferenciada 2 partes:
                        
                        1. La ejecución del algoritmo que devolverá siempre uno o varios resultados dataframe
                        2. La parte de la visualización aunque hayan valores que se puedan modificar
                        
                        ## ¿Como añadir algortimos con visualizaciones estáticas?

                        Lo primero es aclarar que toda la parte de ejecución se hace en el backend y que las respuestas  
                        de los algoritmos tienen que tener un formato en específico.

                        Además, los algoritmos siempre reciben ficheros con formatos  
                        `{file_i: {filename: name, file_content: content}}` 
                        
                        Entonces, cuando cada algoritmo retorna una respuesta con el mismo formato, la clase algorithm  
                        hace algunas transformaciones y envia un objeto con una lista de los dataframe resultantes.

                        Esto facilita las visualizaicones estáticas ya que en el frontend se pueden crear directamente en la carpeta  
                        correspondiente (más adelante veremos un vídeo de esto)
                        
                        ## ¿Como añadir algortimos con visualizaciones que dependen de parámetros por callbacks?

                        En estos casos hay que crear un ultimo fichero que se encargue de recoger todos estos valores modificables  
                        en el callback (Inputs) y pasarselo al backend para que en el algoritmo correspondiente haga los setter  
                        de esos valores.
                         
                        Como los algoritmos siempre siguen un orden de ficheros y se organizan al llegar al backend  
                        (para eso se usan los indices de file_i), podemos añadir este fichero (es un JSON a efectos prácticos)  
                        e intentar acceer a las variables correspondientes para los algoritmos que necesiten de estos valores. 
                        
                        Para la primera  llamada del algoritmo es importante siempre settear estos valores por defecto.

                        Todo esto se verá mejor en los siguientes vídeos:

                        """
                    ),
                    html.Video(src=backend_video,controls=True, id="backend-video"),
                    html.Video(src=frontend_video,controls=True, id="frontend-video")
                ],
            )
        ])
])
