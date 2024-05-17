# Simulador de Eventos Discretos: yacs.py

Este proyecto consiste en la creación de un simulador de eventos discretos orientado por procesos para analizar el rendimiento de un sistema de cómputo con múltiples cores y memorias cache. El objetivo es determinar el rendimiento del sistema (tiempo de servicio promedio por proceso) y el tiempo de utilización de cada core.

## Características de los Procesos

Cada proceso `k` tiene las siguientes características:

| Atributo                | Descripción                                                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_k`                  | Identificador entero mayor que 0                                                                                                                                             |
| `tespera_k`             | Tiempo que toma el proceso en ser atendido desde que llega al sistema                                                                                                        |
| `tfinalizacion_k`       | Tiempo que demora el proceso en terminar desde que llega al sistema                                                                                                          |
| `[d_1, d_2, ..., d_Nk]` | Datos que deben ser leídos por el proceso antes de completar su ejecución. Representados por las `N_k` primeras letras del abecedario. (`N_k` en el rango `[1, 2, ..., 25]`) |

## Características del Computador

El computador tiene las siguientes características:

| Atributo | Descripción                                                                                                                                                                             |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `C`      | Cantidad de cores (en el rango `[1, 2, ..., 64]`)                                                                                                                                       |
| `L1`     | Memoria cache L1 que puede almacenar hasta `M_L1` datos. La velocidad de acceso a un dato es de `T_L1 = 4` ciclos de reloj.                                                             |
| `L2`     | Memoria cache L2 que puede almacenar hasta `M_L2` datos. Compartida entre los `C` cores. Se tiene que `M_L2 > M_L1`.                                                                    |
| `RAM`    | Memoria principal. Considerada infinita para la simulación y contiene todos los datos que los procesos necesiten. La velocidad de acceso a un dato es de `T_RAM = 200` ciclos de reloj. |

## Requerimientos del Sistema

- Asignar tareas al primer core libre disponible.
- El core no puede ser interrumpido mientras está ejecutando un proceso.
- Si los datos no se encuentran en la cache `L1`, se deben buscar desde la cache `L2`.
- Si los datos no se encuentran en la cache `L2`, se deben buscar desde la `RAM`.
- Ambas memorias cache (`L1` y `L2`) se llenan de forma secuencial:
  - Se comienza de nuevo en la primera posición de memoria cuando se llena la capacidad actual.

## Trabajo a Realizar

Se debe crear un simulador de nombre `yacs.py` basado en el código `yacs-base.py` disponible en el aula virtual. El simulador debe cumplir con los siguientes objetivos:

1. Determinar el throughput del sistema (tiempo de servicio promedio por proceso).
2. Calcular el tiempo de utilización de cada core.
