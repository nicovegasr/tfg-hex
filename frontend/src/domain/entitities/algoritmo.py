import os
import importlib
import datetime

from servicios.funciones.procesar_archivos import procesar_archivos

'''Clase que se encarga de llamar al algoritmo dependiendo del nombre que se le haya asignado'''

class Algoritmo:
    def __init__(self, algoritmo, ficheros):
      self.nombre = algoritmo
      self.archivos = procesar_archivos([ficheros[i][0] for i in range(len(ficheros))], [
                                          ficheros[i][1] for i in range(len(ficheros))])
      self.resultado = None
      self.nombres_ficheros = [ficheros[i][0] for i in range(len(ficheros))]
    
    def iniciar(self):
      module = importlib.import_module(f"servicios.algoritmos.{self.nombre}.algoritmo")
      self.resultado = module.algoritmo(self.archivos)
      self.formatear_archivos()
      self.guardar_resultado()
      return self.resultado

    # Es muy importante que el algoritmo siempre devuelve un array de ficheros resultados, aunque sea solo 1. Además debe devolverlos
    # en el orden que se los pasaron para asignar bien el nombre del archivo de origen.
    def formatear_archivos(self):
      if len(self.nombres_ficheros) < len(self.resultado):
        self.nombres_ficheros.append("Nuevo_Fichero_Generado")

      resultado = []
      for i in range(len(self.resultado)):
        archivo = self.resultado[i]
        nombre_fichero = self.nombres_ficheros[i]
        hora_ejecucion = datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
        archivo['Fichero_Origen'] = nombre_fichero
        archivo['Hora_ejecucion'] = hora_ejecucion
        resultado.append(archivo)
      self.resultado = resultado

    # Guarda en la carpeta "resultados" los archivos que devuelva el algoritmo.    
    def guardar_resultado(self):
      path = os.path.dirname(os.path.realpath(__file__))
      parent_dir = path.rsplit("\src", 1)[0] + '/src/resultados/'
      directory = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
      path = os.path.join(parent_dir, directory)
      os.mkdir(path)
      i = 0
      for archivo in self.resultado:
        archivo.to_excel(f"{path}/resultado{i}.xlsx", index=False)
        i += 1
