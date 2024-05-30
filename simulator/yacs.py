#!/usr/bin/env python3

# Importar librerías necesarias
import string
import simpy
import numpy as np
import argparse

# Listas para almacenar tiempos de espera, servicio y finalización
tespera = []
tservicio = []
tfinalizacion = []


# Clase para la depuración
class Debug(object):
    enabled = False

    @classmethod
    def enable(cls):
        cls.enabled = True

    @classmethod
    def log(cls, env: simpy.Environment, msg: str):
        if cls.enabled:
            print(f"{env.now:5.4f}:\t{msg}")


# Clase para manejar los parámetros de entrada
class Parametros(object):
    def __init__(self):
        self.procesos = None
        self.cores = None
        self.L1 = None
        self.L2 = None
        self.elog = False
        self._parsear_argumentos()

    # Método para parsear los argumentos de la línea de comandos
    def _parsear_argumentos(self):
        parser = argparse.ArgumentParser(description="Descripción del script.")
        parser.add_argument("--procesos", type=self.validar_no_negativo,
                            required=True, help="Procesos a simular.")
        parser.add_argument("--cores", type=self.validar_cores,
                            required=True, help="Número de cores.")
        parser.add_argument("--L1", type=self.validar_no_negativo,
                            required=True, help="L1 tamaño de la memoria caché.")
        parser.add_argument("--L2", type=self.validar_no_negativo,
                            required=True, help="L2 tamaño de la memoria caché.")
        parser.add_argument("--elog", action='store_true',
                            help="Habilitar logging de depuración.")

        args = parser.parse_args()

        self.procesos = args.procesos
        self.cores = args.cores
        self.L1 = args.L1
        self.L2 = args.L2
        self.elog = args.elog

    # Validar que el número de cores sea correcto
    def validar_cores(self, value):
        cores = int(value)
        if cores == 1 or (cores % 2 == 0 and 1 <= cores <= 64):
            return cores
        else:
            raise argparse.ArgumentTypeError(
                f"{value} no es un valor válido para --cores. Debe ser 1 o un número par hasta 64.")

    # Validar que un valor no sea negativo
    def validar_no_negativo(self, value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                f"{value} no puede ser negativo o igual a 0")
        return ivalue

     # Obtener los parámetros y validar que L1 sea menor que L2
    def obtener_parametros(self):
        if self.L1 >= self.L2:
            raise argparse.ArgumentTypeError("L1 debe ser menor que L2")
        return self.procesos, self.cores, self.L1, self.L2, self.elog

# Clase para representar un proceso


class Proceso(object):
    def __init__(self, idProceso: int, num_datos: int):
        if not (1 <= num_datos <= 25):
            raise ValueError("El número de datos debe estar entre 1 y 25")
        self.idProceso = idProceso
        self.num_datos = num_datos
        self.datos = {
            letra: False for letra in string.ascii_lowercase[:num_datos]}


# Clase para representar un core
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
        self.tUtilizado = 0
        self.procesos_resueltos = 0
        self.cL1 = 0
        self.cL2 = 0
        self.cRam = 0
        self.tCore = []


# Clase para representar el computador
class Computador(object):
    def __init__(self, env: simpy.Environment, numCores: int, L1: int, L2: int, totalprocesos: int):
        self.env = env
        self.totalprocesos = totalprocesos
        self.pCompletados = 0
        self.tRam = 200
        self.coresLibres = simpy.Container(
            self.env, capacity=numCores, init=numCores)
        self.cores = [Core(id, L1, L2) for id in range(numCores)]
        self.env.process(self.run())

    # Método para simular los procesos
    def procesos(self, proceso: Proceso):
        Debug.log(self.env, f"Proceso {proceso.idProceso}: llega")
        itEspera = self.env.now
        yield self.coresLibres.get(1)

        core = self.asignar_core()
        Debug.log(self.env, f"Proceso {proceso.idProceso}: Asignado al core {
                  core.idCore}, con {proceso.num_datos} datos.")
        ftEspera = self.env.now
        tespera.append(ftEspera - itEspera)
        itServicio = self.env.now

        itCore = self.env.now
        for dato in proceso.datos:
            tAcceso = self.leer_dato(core, dato)
            Debug.log(self.env, f"Proceso {proceso.idProceso}: Ocupando core: {
                      core.idCore} Leyendo dato: {dato}, tiempo de acceso: {tAcceso}.")
            yield self.env.timeout(tAcceso)
        ftCore = self.env.now
        core.tUtilizado += (ftCore - itCore)
        core.procesos_resueltos += 1
        core.tCore.append(ftCore - itCore)

        self.liberar_core(core)
        yield self.coresLibres.put(1)
        Debug.log(self.env, f"Proceso {
                  proceso.idProceso} liberó el core {core.idCore}")

        ftServicio = self.env.now
        tservicio.append(ftServicio - itServicio)
        tfinalizacion.append(ftServicio - itEspera)

        self.pCompletados += 1

    # Método para generar los procesos
    def run(self):
        for i in range(1, self.totalprocesos + 1):
            tLlegada = np.random.exponential(scale=1)
            yield self.env.timeout(delay=tLlegada)

            num_datos = np.random.randint(low=1, high=25)
            proceso = Proceso(idProceso=i, num_datos=num_datos)
            self.env.process(self.procesos(proceso=proceso))

     # Método para leer datos del core
    def leer_dato(self, core, dato):
        if dato in core.datosL1:
            core.cL1 += 1
            return core.tL1
        elif dato in core.datosL2:
            core.datosL1.append(dato)
            if len(core.datosL1) > core.L1:
                core.datosL1.pop(0)
            core.cL2 += 1
            return core.tL2 + core.tL1
        else:
            core.datosL2.append(dato)
            if len(core.datosL2) > core.L2:
                core.datosL2.pop(0)
            core.datosL1.append(dato)
            if len(core.datosL1) > core.L1:
                core.datosL1.pop(0)
            core.cRam += 1
            return self.tRam + core.tL2 + core.tL1

    # Método para asignar un core libre
    def asignar_core(self):
        for core in self.cores:
            if not core.ocupado:
                core.ocupado = True
                return core
        raise RuntimeError(
            "No se pudo encontrar un core libre después de haberlo reservado")

    # Método para liberar un core
    def liberar_core(self, core):
        core.ocupado = False

# Función principal del script


def main():
    parametros = Parametros()
    procesos, numCores, L1, L2, elog = parametros.obtener_parametros()

    if elog:
        Debug.enable()

    env = simpy.Environment()
    computador = Computador(env=env, numCores=numCores,
                            L1=L1, L2=L2, totalprocesos=procesos)

    env.run()

    tsimulacion = env.now
    throughput = computador.pCompletados / tsimulacion

    print(f"Throughput: {throughput} procesos/segundo")
    print(f"Tiempo de espera promedio de cada tarea: {np.mean(tespera)}")
    print(f"Tiempo de servicio promedio de cada tarea: {np.mean(tservicio)}")

    for i in range(numCores):
        core = computador.cores[i]
        print(f"Core {i}: Tiempo de uso: {core.tUtilizado}, Promedio tiempo de uso: {np.mean(core.tCore)} Procesos resueltos: {
              core.procesos_resueltos}, Accesos a L1: {core.cL1}, Accesos a L2: {core.cL2}, Accesos a RAM: {core.cRam}")

    print(f"Tiempo de finalización promedio de cada tarea: {
          np.mean(tfinalizacion)}")


if __name__ == "__main__":
    main()
