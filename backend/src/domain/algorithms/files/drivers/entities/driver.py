from datetime import datetime, timedelta


class Driver:
  def __init__(self, id):
    self.id = id
    self.hora_inicio_jornada = None
    self.hora_final_jornada = None
    self.estacion_salida_inicial = None
    # Asignamos la jornada reduciendo el toma y deje de 15 minutos cada uno.
    self.jornada = timedelta(hours=8) - timedelta(minutes=30)
    # Los conductores por defecto iniciaran en la estacion que se les asigne en el primer viaje.
    self.lugar = None
    # Lista de viajes asignados.
    self.viajes = []
    # Cada conductor debe descansar 30 minutos que se les asignaran entre la 3ra y 5ta hora de trabajo, es decir, cuando la jornada baje de 5 horas.
    self.descanso_inicio = None
    self.descanso_final = None
    # Hora final y tiempo del ultimo viaje o del viaje que está realizando actualmente:
    self.hora_final_anterior = None
    self.tiempo_ultimo_viaje = None

  # El conductor descansa si la jornada:
  #   Baja de 5 horas (Pasan 3 horas)
  #   Importante:  Y si no se le ha asignado previamente.
  def valorar_descanso(self, viaje):
    if (self.jornada <= timedelta(hours=5)) and (self.descanso_inicio == None):
      self.asignar_hora_descanso(viaje.hora_final)

  # Se establece la hora de descanso inicial, final y se descuentan los 30 minutos de la jornada.
  def asignar_hora_descanso(self, hora):
    self.descanso_inicio = hora
    self.descanso_final = hora + timedelta(minutes=30)
    self.jornada = self.jornada - timedelta(minutes=30)

  def esta_descansando(self, viaje):
    # La hora de inicio no se ha setteado
    if self.descanso_inicio == None:
      return False
    # Si la hora de inicio del viaje es mas tarde que el final del descanso, ya descansó.
    if viaje.hora_inicio > self.descanso_final:
      return False
    # En caso contrario, está descansando
    return True

  # En caso de que el conductor tenga tiempo en su jornada laboral y se encuentre en el sitio correspondiente, se asigna el viaje.
  def viaje_disponible(self, viaje):
    if not (self.esta_descansando(viaje)):
    # Si la jornada que le queda al conductor es mayor que el tiempo del viaje.
      if self.jornada >= viaje.tiempo_viaje:
        # Si el conductor está en el lugar correspondiente o no se le a asignado un lugar, está disponible en dicha estación. O si puede hacer un viaje en vacio para llegar a la estacion
        if (self.lugar == None) or (self.lugar == viaje.estacion_salida) or (self.puede_viaje_vacío(viaje)):
          # Si el conductor no ha sido asignado a una hora o si esta es mas temprana que la hora de inico del viaje actual, el conductor está disponiible
          if (self.hora_final_anterior == None) or (self.hora_final_anterior <= viaje.hora_inicio):
            return True
          else:
            return False
        else:
          return False
      else:
        return False
    # 
  def puede_viaje_vacío(self, viaje):
    # Si aun no ha hecho ningun viaje, se devuelve True sin hacer nada ya que no tiene sentido hacer viajes en vacio.
    if self.tiempo_ultimo_viaje == None:
      return False
    tiempo_aumentado = (0.60 * self.tiempo_ultimo_viaje)  + viaje.tiempo_viaje
    if (self.jornada >= tiempo_aumentado):
      return True
    
    return False
  
  def asginar_viaje(self, viaje):
    if self.hora_inicio_jornada == None:
      self.hora_inicio_jornada = viaje.hora_inicio
      self.hora_final_jornada = viaje.hora_inicio + timedelta(hours=7, minutes=30)
      self.hora_final_anterior = viaje.hora_inicio
      self.estacion_salida_inicial = viaje.estacion_salida
    # El tiempo transcurrido es desde la hora de inicio de la jornada hasta la del viaje actual que se quiere poner.
    tiempo_transcurrido = (viaje.hora_inicio - self.hora_final_anterior) + viaje.tiempo_viaje
    self.jornada = self.jornada - tiempo_transcurrido
    # Se asigna el lugar al que llegará el conductor
    self.lugar = viaje.estacion_llegada
    self.hora_final_anterior = viaje.hora_final
    self.viajes.append(viaje)
    self.tiempo_ultimo_viaje = viaje.tiempo_viaje
    # Se valora si el conductor descansará luego de realizar el viaje
    self.valorar_descanso(viaje)