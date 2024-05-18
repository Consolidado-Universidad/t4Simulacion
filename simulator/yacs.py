#!/usr/bin/env python3

# Importar librerias
import string
import simpy
import numpy
import argparse
from typing import List
# from typing import Dict
import time

thoughput = 0
tiempo_servicio_promedio = 0
tiempo_utilizacion_core = 0


class Debug(object):
    @classmethod
    def log(self, env: simpy.Environment, msg: str):
        print(f"{env.now:5.4f}:\t{msg}")


class Parametros(object):
    def __init__(self):
        self.procesos = None
        self.cores = None
        self.L1 = None
        self.L2 = None
        self._parsear_argumentos()

    def _parsear_argumentos(self):
        parser = argparse.ArgumentParser(description="Descripción del script.")

        # Argumentos obligatorios (posicionales)
        parser.add_argument("--procesos", type=self.validar_no_negativo,
                            required=True, help="Procesos a simular.")
        parser.add_argument("--cores", type=self.validar_cores,
                            required=True, help="Número de cores.")
        parser.add_argument("--L1", type=self.validar_no_negativo,
                            required=True, help="L1 tamaño de la memoria caché.")
        parser.add_argument("--L2", type=self.validar_no_negativo,
                            required=True, help="L2 tamaño de la memoria caché.")

        # Parser de los argumentos
        args = parser.parse_args()

        # Asigna los argumentos a las variables de la clase
        self.procesos = args.procesos
        self.cores = args.cores
        self.L1 = args.L1
        self.L2 = args.L2

    # Validadores de los argumentos
    def validar_cores(self, value):
        cores = int(value)
        if cores == 1 or (cores % 2 == 0 and 1 <= cores <= 64):
            return cores
        else:
            raise argparse.ArgumentTypeError(
                f"{value} no es un valor válido para --cores. Debe ser 1 o un número par hasta 64.")

    # Vaidar no negatividad
    def validar_no_negativo(self, value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                f"{value} no puede ser negativo o igual a 0")
        return ivalue

    # Obtener los parámetros
    def obtener_parametros(self):
        # Devuelve los parámetros como una tupla
        return self.procesos, self.cores, self.L1, self.L2


# Estructura de datos de lo que es un proceso
class Proceso(object):
    def __init__(self, idProceso: int, num_datos: int):
        if not (1 <= num_datos <= 25):
            raise ValueError("El número de datos debe estar entre 1 y 25")

        self.idProceso = idProceso
        self.tespera = None  # Inicializado a None, se calculará durante la simulación
        self.tfinalizacion = None  # Inicializado a None, se calculará durante la simulación
        self.num_datos = num_datos
        # Diccionario para seguir el estado de lectura de los datos
        self.datos = {
            letra: False for letra in string.ascii_lowercase[:num_datos]}
        self.datos_leidos = 0  # Contador de datos leídos


class Core(object):
    def __init__(self, idCore: int, L1: int, L2: int):
        self.idCore = idCore
        self.L1 = L1
        self.L2 = L2
        self.datosL1 = []
        self.datosL2 = []
        self.tL1 = 4
        self.tL2 = 10
        self.ocupado = False


class Computador(object):
    def __init__(self,
                 env: simpy.Environment,
                 numCores: int,
                 L1: int,
                 L2: int,
                 totalprocesos: int
                 ):
        self.env = env
        self.totalprocesos = totalprocesos

        self.tRam = 200

        self.coresLibres = simpy.Container(
            self.env, capacity=numCores, init=numCores)

        self.cores = [Core(id, L1, L2) for id in range(numCores)]

        self.env.process(self.run())
        # procesoSnitch = self.env.process(self.snitch())

    def procesos(self, proceso: Proceso):

        # Proceso llega al computador
        Debug.log(self.env, f"Proceso {proceso.idProceso} llega")

        # Revisa que exista un core libre
        yield self.coresLibres.get(1)

        # Asignar un core al proceso
        core = self.asignar_core()
        Debug.log(self.env, f"Proceso {
                  proceso.idProceso} asignado al core {core.idCore}")

        for dato in proceso.datos:
            tAcceso = self.leer_dato(core, dato)
            Debug.log(self.env, f"tiempo de acceso: {
                      tAcceso},   dato: {dato},")
            yield self.env.timeout(tAcceso)

        # Liberar el core
        self.liberar_core(core)
        yield self.coresLibres.put(1)
        Debug.log(self.env, f"Proceso {
                  proceso.idProceso} liberó el core {core.idCore}")

    def run(self):
        for i in range(1, self.totalprocesos):
            tLlegada = numpy.random.exponential(scale=1)
            yield self.env.timeout(delay=tLlegada)

            # Crear un proceso
            num_datos = numpy.random.randint(low=1, high=25)
            proceso = Proceso(idProceso=i, num_datos=num_datos)

            # Desarrollar el proceso
            self.env.process(self.procesos(proceso=proceso))

    def leer_dato(self, core, dato):
        # Dato encontrado en L1
        if dato in core.datosL1:
            return core.tL1
        # Dato encontrado en L2
        elif dato in core.datosL2:
            core.datosL1.append(dato)
            if len(core.datosL1) > core.L1:
                core.datosL1.pop(0)
            return core.tL2 + core.tL1
        # Buscar en la RAM
        else:
            core.datosL2.append(dato)
            if len(core.datosL2) > core.L2:
                core.datosL2.pop(0)
            core.datosL1.append(dato)
            if len(core.datosL1) > core.L1:
                core.datosL1.pop(0)
            return self.tRam + core.tL2 + core.tL1

    def asignar_core(self):
        for core in self.cores:
            if not core.ocupado:
                core.ocupado = True
                return core
        raise RuntimeError(
            "No se pudo encontrar un core libre después de haberlo reservado")

    def liberar_core(self, core):
        core.ocupado = False


# def cicloProceso(env: simpy.Environment, proceso: Proceso, computador: Computador):
#     # Proceso llega al computador
#     tInicio = env.now

#     # Asignar un core al proceso
#     req = computador.recursoCores.request()

#     core = computador.cores[computador.cores.index(
#         computador.core_mapping[req])]

#     print(f"Proceso {proceso.idProceso} asignado al core {core.idCore}")

#     yield req

#     # Leer los datos del proceso

#     # Proceso termina

#     # Liberar el core


# Cinta
def main():
    # Crea una instancia de la clase Parametros
    parametros = Parametros()

    # Obtiene los parámetros
    procesos, numCores, L1, L2 = parametros.obtener_parametros()

    env = simpy.Environment()

    computador = Computador(env=env,
                            numCores=numCores,
                            L1=L1,
                            L2=L2,
                            totalprocesos=procesos)

    env.run()

    # print(f"Thoughput: {thoughput}")
    # print(f"Tiempo de servicio promedio de cada tarea: {
    #       tiempo_servicio_promedio}")
    # print(f"Tiempo de utilizacion de cada core: {tiempo_utilizacion_core}")


if __name__ == "__main__":
    main()
