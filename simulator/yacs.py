#!/usr/bin/env python3

import string
import simpy
import numpy
import argparse
from typing import List


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


class Proceso(object):
    def __init__(self, ID: int, num_datos: int):
        if not (1 <= num_datos <= 25):
            raise ValueError("El número de datos debe estar entre 1 y 25")

        self.ID = ID
        self.tespera = None  # Inicializado a None, se calculará durante la simulación
        self.tfinalizacion = None  # Inicializado a None, se calculará durante la simulación
        self.num_datos = num_datos
        # Diccionario para seguir el estado de lectura de los datos
        self.datos = {
            letra: False for letra in string.ascii_lowercase[:num_datos]}
        self.datos_leidos = 0  # Contador de datos leídos

    def leer_dato(self, dato):
        if dato in self.datos and not self.datos[dato]:
            self.datos[dato] = True
            self.datos_leidos += 1
        elif dato not in self.datos:
            raise ValueError(
                f"El dato {dato} no es requerido por este proceso.")
        elif self.datos[dato]:
            raise ValueError(f"El dato {dato} ya ha sido leído.")

    def todos_datos_leidos(self):
        return self.datos_leidos == self.num_datos

    def actualizar_tiempos(self, tespera, tfinalizacion):
        self.tespera = tespera
        self.tfinalizacion = tfinalizacion


class MemoriaCache(object):
    def __init__(self, env: simpy.Environment, memoria: int, tiempo_acceso: int):
        self.env = env
        self.memoria = simpy.Resource(env, capacity=memoria)
        self.tiempo_acceso = tiempo_acceso
        self.datos = []


class Ram(object):
    def __init__(self, tiempo_acceso):
        self.tiempo_acceso = tiempo_acceso


class Core(object):
    def __init__(self, env: simpy.Environment, idCore: int, memoriaL1: MemoriaCache, memoriaL2: MemoriaCache):
        self.env = env
        self.idCore = idCore
        self.ocupado = False
        self.tiempo_utilizacion = 0
        self.memoriaL1 = memoriaL1
        self.memoriaL2 = memoriaL2

    def cargarDatosL1(self, proceso: Proceso):
        pass

    def cicloCore(self, idCore: int, proceso: Proceso):
        pass

    def asignar_proceso(self, proceso, tiempo_servicio):
        self.ocupado = True
        yield self.env.timeout(tiempo_servicio)
        self.tiempo_utilizacion += tiempo_servicio
        self.ocupado = False

    def liberar(self):
        self.ocupado = False
        self.tiempo_utilizacion = 0


class Computador(object):
    def __init__(self,
                 env: simpy.Environment,
                 cores: List[Core],
                 memoriaRam: Ram
                 ):
        self.env = env
        self.cores = cores
        self.memoriaRam = memoriaRam


def crear_cores(env: simpy.Environment, num_cores: int, memoriaL1: int, memoriaL2: int, tiempo_acceso_L1: int, tiempo_acceso_L2: int,):
    cores = []
    for i in range(num_cores):
        coreMemoriaL1 = MemoriaCache(
            env=env, memoria=memoriaL1,
            tiempo_acceso=tiempo_acceso_L1)
        coreMemoriaL2 = MemoriaCache(
            env=env, memoria=memoriaL2,
            tiempo_acceso=tiempo_acceso_L2)
        core = Core(env=env,
                    idCore=i,
                    memoriaL1=coreMemoriaL1,
                    memoriaL2=coreMemoriaL2)
        cores.append(core)
    return cores


def crear_procesos(cantidad: int):
    procesos = []
    for i in range(cantidad):
        num_datos = numpy.random.randint(low=1, high=25)
        proceso = Proceso(ID=i, num_datos=num_datos)
        procesos.append(proceso)
    return procesos


def simuladorComputador(env: simpy.Environment, computador: Computador, procesos: int):
    yield env.timeout(1)


# Cinta 
# La ram necesita los valores

def main():
    # Crea una instancia de la clase Parametros
    parametros = Parametros()

    # Obtiene los parámetros
    procesos, cores, L1, L2 = parametros.obtener_parametros()

    # Testeto de los parámetros
    # L1 = 5
    # L2 = 10

    print(f"El valor de Procesos es: {procesos}")
    print(f"El valor de Cores es: {cores}")
    print(f"El valor de L1 es: {L1}")
    print(f"El valor de L2 es: {L2}")

    env = simpy.Environment()

    memoriaRamComputador = Ram(tiempo_acceso=200)

    
    coresComputador = crear_cores(env=env, num_cores=cores, memoriaL1=L1,
                                  memoriaL2=L2, tiempo_acceso_L1=4, tiempo_acceso_L2=10)

    procesosComputador = crear_procesos(cantidad=procesos)

    computador = Computador(env=env, cores=coresComputador,
                            memoriaRam=memoriaRamComputador)

    env.process(simuladorComputador(env=env, computador=computador,
                                    procesos=procesosComputador))

    env.run(until=480)

    for i in procesosComputador:
        print(i.ID, i.num_datos, i.datos,
              i.datos_leidos, i.tespera, i.tfinalizacion)

    # for i in cores:
    #     print(i.ID, i.memoriaL1.memoria, i.memoriaL2.memoria,
    #           i.memoriaL1.tiempo_acceso, i.memoriaL2.tiempo_acceso)

    # computador = Computador(env=env, num_cores=cores)

    env.run()


if __name__ == "__main__":
    main()
