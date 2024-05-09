# Tarea 4: Procesador Multicore

## Objetivo
El objetivo de esta tarea fue diseñar e implementar, utilizando SimPy, un modelo de un computador multicore.

## Descripción del Sistema
Se simuló el procesamiento de K procesos intensivos en la búsqueda de datos en un procesador multicore con C cores. Cada proceso debía acceder a Nk datos antes de finalizar.

### Características de cada Proceso
Cada proceso k tenía las siguientes características:
- **IDk**: Identificador entero mayor que 0.
- **tesperak**: Tiempo que tomó el proceso en ser atendido desde que llegó al sistema.
- **tfinalizacionk**: Tiempo que demoró el proceso en terminar desde que llegó al sistema.
- **[d1, d2, ..., dNk]**: Los datos que debían ser leídos por el proceso antes de completar su ejecución. Estos datos estaban representados por las primeras Nk (1, ..., 25) letras del abecedario.

### Características del Computador
El computador tenía las siguientes características:
- **C**: Cantidad de cores. Valores posibles: {1, 2, 4, 8, ..., 64}.
- **L1**: Memoria caché L1. Podía almacenar hasta ML1 datos. Velocidad de acceso: TL1 = 4 ciclos de reloj.
- **L2**: Memoria caché L2. Podía almacenar hasta ML2 datos. Velocidad de acceso: TL2 = 10 ciclos de reloj. Compartida con todos los cores.
- **RAM**: Memoria principal. Desde el punto de vista de la simulación, era infinita y contenía todos los datos que los procesos necesitaban. Velocidad de acceso: TRAM = 200 ciclos de reloj.

### Asignación de Tareas
Las tareas eran asignadas al primer core libre y no eran interrumpidas. Si ambos cores estaban libres, se seleccionaba uno al azar. La política de búsqueda de datos seguía el siguiente orden:
1. **L1**: Si los datos no estaban en la caché L1, se buscaban en...
2. **L2**: Si los datos no estaban en la caché L2, se buscaban en...
3. **RAM**: Los datos se buscaban finalmente en la RAM.

### Llenado de Memoria Caché
Ambas memorias caché se llenaban en forma secuencial. Al completarse la memoria, se comenzaba nuevamente en la primera posición.

## Trabajo Realizado
Se realizó un simulador (llamado `yacs.py`) de eventos discretos orientado a procesos para el sistema descrito. El objetivo fue determinar:
- **Throughput**
- **Tiempo promedio de servicio por tarea**
- **Tiempo de utilización de cada core**

### Uso del Simulador
El script recibía los parámetros del simulador a través de argumentos de entrada. Por ejemplo, para simular un sistema con 500 procesos, 8 cores, caché L1 de 6 datos, y caché L2 de 18 datos:

```bash
$ yacs.py --procesos 500 --cores 8 --L1 6 --L2 18
```

### Informe Detallado
Se elaboró un informe detallado que incluyó:
1. **Diseño**
   - Descripción del sistema
   - Modelo de filas
   - Variables de estado
   - Salidas que permitieron calcular las métricas solicitadas

2. **Implementación**
   - Modelo lógico basado en un diagrama de clases
   - Herramienta visual para representar entidades y relaciones del sistema
   - Visión sistemática y organizada del trabajo realizado

### Entrega
Se entregó un archivo ZIP (`tarea04-apellido1-apellido2-nombre.zip`) que contenía:
- El código fuente del simulador (`yacs.py`).
- Un archivo PDF con el informe respectivo.

La estructura del archivo ZIP fue como se muestra a continuación:

```
tarea04-apellido1-apellido2-nombre.zip
└── tarea04-apellido1-apellido2-nombre
    ├── yacs.py
    ├── informe.pdf
    └── README.md
```

## Ejemplo de Estructura
```bash
tarea04-apellido1-apellido2-nombre/
│
├── yacs.py
├── informe.pdf
└── README.md
```

### Requisitos Previos
- Python 3.x
- SimPy

### Instalación
Se instaló SimPy utilizando pip:
```bash
pip install simpy
```

### Uso del Simulador
Ejemplo de uso:
```bash
$ yacs.py --procesos 500 --cores 8 --L1 6 --L2 18
```

## Notas
- **yacs-base.py**: Se utilizó el código proporcionado en `yacs-base.py` como base para el desarrollo del simulador.

## Autor
- [Nombre del Estudiante]

## Curso
- ICI515 - Simulación