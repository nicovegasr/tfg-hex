class Travel:
  def __init__(self, id, hora_inicio, hora_final, tiempo_viaje, direccion):
    self.id = id
    self.hora_inicio = hora_inicio
    self.hora_final = hora_final
    self.tiempo_viaje = tiempo_viaje
    self.direccion = direccion
    self.estacion_salida = 'A' if direccion == 11 else 'B'
    self.estacion_llegada = 'A' if direccion == 12 else 'B'
    