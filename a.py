
# class Proceso:
#     def __init__(self, ID, tespera, tfinalizacion, datos):
#         self.ID = ID
#         self.tespera = tespera
#         self.tfinalizacion = tfinalizacion
#         self.datos = datos


# class Core:
#     def __init__(self, ID):
#         self.ID = ID
#         self.ocupado = False
#         self.tiempo_utilizacion = 0

#     def asignar_proceso(self, proceso, tiempo):
#         self.ocupado = True
#         self.proceso_actual = proceso
#         self.tiempo_utilizacion += tiempo

#     def liberar(self):
#         self.ocupado = False
#         self.proceso_actual = None


# class MemoriaCache:
#     def __init__(self, tamaño, tiempo_acceso):
#         self.tamaño = tamaño
#         self.tiempo_acceso = tiempo_acceso
#         self.datos = []

#     def leer_dato(self, dato):
#         if dato in self.datos:
#             return self.tiempo_acceso
#         else:
#             return None

#     def escribir_dato(self, dato):
#         if len(self.datos) >= self.tamaño:
#             self.datos.pop(0)
#         self.datos.append(dato)


# class RAM:
#     def __init__(self, tiempo_acceso):
#         self.tiempo_acceso = tiempo_acceso

#     def leer_dato(self, dato):
#         return self.tiempo_acceso


# class Simulador:
#     def __init__(self, num_cores, tamaño_L1, tamaño_L2, tiempo_L1, tiempo_L2, tiempo_RAM):
#         self.cores = [Core(i) for i in range(num_cores)]
#         self.L1 = MemoriaCache(tamaño_L1, tiempo_L1)
#         self.L2 = MemoriaCache(tamaño_L2, tiempo_L2)
#         self.RAM = RAM(tiempo_RAM)

#     def asignar_proceso_a_core(self, proceso):
#         for core in self.cores:
#             if not core.ocupado:
#                 core.asignar_proceso(
#                     proceso, self.calcular_tiempo_servicio(proceso))
#                 return
#         raise Exception("No hay cores disponibles.")

#     def calcular_tiempo_servicio(self, proceso):
#         tiempo_total = 0
#         for dato in proceso.datos:
#             tiempo_acceso = self.L1.leer_dato(dato)
#             if tiempo_acceso is None:
#                 tiempo_acceso = self.L2.leer_dato(dato)
#                 if tiempo_acceso is None:
#                     tiempo_acceso = self.RAM.leer_dato(dato)
#                     self.L2.escribir_dato(dato)
#                 self.L1.escribir_dato(dato)
#             tiempo_total += tiempo_acceso
#         return tiempo_total

#     def simular(self, procesos):
#         for proceso in procesos:
#             self.asignar_proceso_a_core(proceso)

#         # Liberar cores y calcular métricas
#         for core in self.cores:
#             core.liberar()

#         # Calcular throughput y utilización de cores
#         throughput = sum(
#             [core.tiempo_utilizacion for core in self.cores]) / len(procesos)
#         utilizacion_cores = [(core.ID, core.tiempo_utilizacion)
#                              for core in self.cores]

#         return throughput, utilizacion_cores


# # Ejemplo de uso:
# procesos = [
#     Proceso(1, 0, 10, ['a', 'b', 'c']),
#     Proceso(2, 0, 15, ['d', 'e', 'f']),
#     Proceso(3, 0, 20, ['g', 'h', 'i']),
# ]

# simulador = Simulador(num_cores=4, tamaño_L1=5, tamaño_L2=10,
#                       tiempo_L1=4, tiempo_L2=10, tiempo_RAM=200)
# throughput, utilizacion_cores = simulador.simular(procesos)

# print(f"Throughput: {throughput}")
# print("Utilización de cores:")
# for core_id, tiempo in utilizacion_cores:
#     print(f"Core {core_id}: {tiempo} ciclos")
