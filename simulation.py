#
# Universidad del Valle de Guatemala
# Angie Nadissa Vela López, 23764
# Simulación de la ejecución de procesos en un CPU
# 27/02/2024
 
import simpy
import random
import numpy as np

random_seed = 42
capacidad_RAM = 200
intervalo_creacion_procesos = 10
instrucciones_CPU = 3
num_procesos = 100   

random.seed(random_seed)

def main():
    tiempos_procesos = []
    for _ in range(num_procesos):
        env = simpy.Environment()
        RAM = simpy.Container(env, init=capacidad_RAM, capacity=capacidad_RAM)
        CPU = simpy.Resource(env, capacity=1)
        env.process(llegada_procesos(env, RAM, CPU, tiempos_procesos))
        env.run(until=1000)  # Tiempo de simulación más largo
    tiempo_promedio = np.mean(tiempos_procesos)
    desviacion_estandar = np.std(tiempos_procesos)
    print(f"Para {num_procesos} procesos:")
    print(f"Tiempo promedio: {tiempo_promedio}")
    print(f"Desviación estándar: {desviacion_estandar}")
    return tiempo_promedio, desviacion_estandar

def llegada_procesos(env, RAM, CPU, tiempos_procesos):
    num_proceso = 0
    while True:
        tiempo_inicio = env.now  # Se actualiza con cada nuevo proceso
        yield env.timeout(random.expovariate(1.0 / intervalo_creacion_procesos))
        num_proceso += 1
        env.process(proceso(env, f"Proceso {num_proceso}", RAM, CPU, tiempos_procesos, tiempo_inicio))

if __name__ == '__main__':
    main()
