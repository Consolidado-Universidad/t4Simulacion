#!/usr/bin/env python3
import numpy
import simpy


autosEnFila = []


class Debug(object):
    @classmethod
    def log(self, env: simpy.Environment, msg: str):
        print(f"{env.now:5.4f}:\t{msg}")


class Estacionamiento(object):
    def __init__(self,
                 env: simpy.Environment,
                 capacidad: int,
                 totalAutos: int,
                 tMedioLlegada: float):
        self.env = env
        self.capacidad = capacidad

        self.totalAutos = totalAutos
        self.tMedioLlegada = tMedioLlegada

        self.espaciosLibres = simpy.Container(self.env, capacity=capacidad,
                                              init=capacidad)

        procesoSim = self.env.process(self.run())
        procesoSnitch = self.env.process(self.snitch())

    def autos(self, id: int):

        # Llega al estacionamiento
        Debug.log(self.env, f"auto {id} llega")

        # Revisa que exista un espacio libre
        yield self.espaciosLibres.get(1)

        Debug.log(self.env, f"auto {id} se estaciona")
        # Se estaciona por cierta cantidad de tiempo
        tEstacionado = numpy.random.randint(20, 180)
        yield self.env.timeout(delay=tEstacionado)

        # Sale del estacionamiento
        yield self.espaciosLibres.put(1)
        Debug.log(self.env, f"auto {id} sale")

    def run(self):
        for idAuto in range(0, self.totalAutos):
            tLlegada = numpy.random.exponential(self.tMedioLlegada)
            yield self.env.timeout(delay=tLlegada)
            self.env.process(self.autos(id=idAuto))

    def snitch(self):
        while True:
            autosEnFilaGet = len(self.espaciosLibres.get_queue)
            dato = (self.env.now, autosEnFilaGet)
            autosEnFila.append(dato)
            yield self.env.timeout(delay=1)


def main():
    env = simpy.Environment()
    estacionamiento = Estacionamiento(
        env, capacidad=2, totalAutos=10, tMedioLlegada=3)
    env.run(until=600)

    print(autosEnFila)


if __name__ == "__main__":
    main()
