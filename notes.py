# Cada proceso k tiene los siguientes caracteristicas:
# ID_k: Identificador entero mayot que 0
# tespera_k: Tiempo que toma el proceso en ser atendido desde que llega al sistema
# tfinalizacion_k: tiempo que demora el proceso en terminar desde que llega al sistema
# [d_1, d_2, ..., d_Nk]: Son los datos que deben ser leidos por el proceso antes de completar
# su ejecucion. Estos datos son representados por las N_k = [1, 2, ..., 25] primeras letras del abecedario 

# El computador tiene los siguientes caracteristicas:
# C: Cantidad de cores C = [1, 2, ..., 64]
# L1: memoria cache L1. Puede almacenar hasta M_L1 datos. La velocidad 
# de acceso a un dato es de T_L2=4 ciclos de reloj.
# L2 : Memoria cache L2. Puede almacenar hasta M_L2 datos. Esta memoria es compartida
# Con la C cores. Se tiene que M_L2 > M_L1.
# RAM : Memoria principal. Desde el punto de vista de la simulacion, es infinita y contiene
# to todos los datos que los procesos necesiten. La velocidad de acceso a un dato es de T_RAM=200 ciclos de reloj.

# Requerimientos del sistema:
# Asignar tareas al primer core libre
# El core no puede ser interrumpido mientras este ejecutando un proceso
# Si los datos no se encuentran en la cache L1, se deben buscar desde la cache L2
# Si los datos no se encuentran en la cache L2, se deben buscar desde la RAM
# Ambas memorias cache son llenadas en forma secuencial // ¿Que significa esto?
# Se comienza de nuevo en la primera posicion de memoria // ¿Que significa esto?

# Trabahjo a realizar:
# Crear un simulador de nombre "yacs.py" de eventos discretos orientado por procesos para el sistema
# descrito en la seccion anterior
# El obejtivo es determinar el thoughput del sistema (tiempo de servicio promedio por proceso) y el
# Tiempo de utilizacion de cada core
# Se debe utilizar como base el código yacs-base.py disponible en el aula virtual
