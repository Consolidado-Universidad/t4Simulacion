#!/usr/bin/env python3

import numpy
import simpy
import statistics

tiemposRetardo = []

class Cine(object):
    def __init__(self, env: simpy.Environment,  cCajeros: int, cRevisores:int, cVendedores:int ):
        self.env = env
        self.personalCajas   = simpy.Resource(env, capacity=cCajeros)
        self.personalRevisor = simpy.Resource(env, capacity=cRevisores)
        self.personalVentas  = simpy.Resource(env, capacity=cVendedores)

    def comprarTicket(self, persona):
        deltaT = numpy.random.randint(low=1, high=5)
        yield self.env.timeout(deltaT)

    def revisarTicket(self, persona):
        deltaT = numpy.random.randint(low=30/60, high=1)
        yield self.env.timeout(deltaT)

    def comprarComida(self, persona):
        deltaT = numpy.random.randint(low=3, high=10)
        yield self.env.timeout(deltaT)

def cicloPersona(env: simpy.Environment, idPersona: int, cine: Cine):

    # persona llega al cine
    tInicio = env.now

    req = cine.personalCajas.request()
    yield req
    yield env.process(cine.comprarTicket(idPersona))
    cine.personalCajas.release(req)

    req = cine.personalRevisor.request()
    yield req
    yield env.process(cine.revisarTicket(idPersona))
    cine.personalRevisor.release(req)

    if numpy.random.choice([True, False]):
        req = cine.personalVentas.request()
        yield req
        yield env.process(cine.comprarComida(idPersona))
        cine.personalVentas.release(req)

    # persona llega a la entrada de la sala
    tFin = env.now

    tRetardo = tFin - tInicio
    tiemposRetardo.append(tRetardo)

def simularCine(env: simpy.Environment, 
            cPersonalCajas, 
            cPersonalRevisa, 
            cPersonalVentas):
    
    cine = Cine(env, cPersonalCajas, cPersonalRevisa, cPersonalVentas)
    idPersona = 0
    while True:
        tEntreLlegada = numpy.random.exponential(scale=1)
        yield env.timeout(delay=tEntreLlegada)
        env.process(cicloPersona(env, idPersona, cine))
        idPersona += 1


def main():

    personalCajas = 5
    personalRevisor = 4
    personalVentas = 4
    env = simpy.Environment()

    env.process(simularCine(env, personalCajas, personalRevisor, personalVentas))
    
    env.run(until=480)

    tRetardoPromedio = statistics.mean(tiemposRetardo)
    print(tRetardoPromedio)


if __name__ == "__main__":
    main()
