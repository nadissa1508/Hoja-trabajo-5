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

def proceso(env, nombre, RAM, CPU, tiempos_procesos, tiempo_inicio):
    instrucciones_totales = random.randint(1, 10)
    memoria_necesaria = random.randint(1, 10)

    print(str(nombre) +"  Solicitando " + str(memoria_necesaria) + " de RAM en tiempo " + str(env.now) )
    yield RAM.get(memoria_necesaria)

    print(str(nombre) +" Asignando " + str(memoria_necesaria) + " de RAM en tiempo " + str(env.now))
    instrucciones_restantes = instrucciones_totales 

    while instrucciones_restantes > 0:
        with CPU.request() as req:
            print(str(nombre) +" Solicitando ejecución del CPU en tiempo " + str(env.now))
            yield req

            print(str(nombre) +" Obteniendo ejecución del CPU  en tiempo " + str(env.now))
            yield env.timeout(1)  # Simular 1 unidad de tiempo de CPU
            instrucciones_restantes -= instrucciones_CPU

            if instrucciones_restantes <= 0:
                tiempo_fin = env.now
                tiempo_proceso = tiempo_fin - tiempo_inicio
                print(str(nombre) +" Proceso completado en tiempo " + str(env.now))
                tiempos_procesos.append(tiempo_proceso)
                break

            print(str(nombre) +"  Procesando en CPU en tiempo " + str(env.now))
            esperar = random.randint(1, 2)

            if esperar == 1:
                tiempo_esperar = random.randint(1, 10)
                print(str(nombre) +"  Esperando por I/O durante " + str(tiempo_esperar) + " unidades de tiempo en t: " + str(env.now))
                yield env.timeout(tiempo_esperar)
            elif esperar == 2:
                print(str(nombre) +"  Listo para ejecutar (ir a ready) nuevamente en t: " + str(env.now))
                continue

    print(str(nombre) +" Proceso terminado, liberando " + str(memoria_necesaria) + " de RAM en tiempo " + str(env.now))
    yield RAM.put(memoria_necesaria)

if __name__ == '__main__':
    main()
