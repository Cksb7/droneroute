
from droneroute.models.drone import Drone
from droneroute.models.client import Client

from droneroute.algorithms.genetic_algorithm.ag_02_fitness import (
    calcular_fitness,
    distribuicao_respeita_carga
)

from droneroute.algorithms.ant_colony.aco_05_otimizacao import (
    otimizar_rota
)


def avaliar_cromossomo(
    cromossomo: list[int],
    clientes: list[Client],
    drones: list[Drone],
    distancias: list[list[float]]
) -> tuple[float, float, list[list[int]]]:

    quantidade_pontos = len(clientes) + 1

    if (
        len(distancias) != quantidade_pontos
        or any(len(linha) != quantidade_pontos for linha in distancias)
    ):
        raise ValueError("Matriz de distancias invalida.")

    # 1. Verifica se a distribuicao respeita a carga.
    if not distribuicao_respeita_carga(
        cromossomo, clientes, drones
    ):
        return 0.0, float("inf"), []

    energia_total = 0.0
    rotas = []

    # 2. Avalia os clientes atribuidos a cada drone.
    for numero_drone, drone in enumerate(drones, start=1):

        indices_clientes = [
            i
            for i, atribuido in enumerate(cromossomo)
            if atribuido == numero_drone
        ]

        # Drone sem clientes nao precisa realizar voo.
        if not indices_clientes:
            rotas.append([0])
            continue

        clientes_drone = [
            clientes[i] for i in indices_clientes
        ]

        # Indices dos pontos na matriz original.
        pontos_globais = [0] + [
            i + 1 for i in indices_clientes
        ]

        # Matriz contendo apenas os pontos deste drone.
        distancias_drone = [
            [
                distancias[origem][destino]
                for destino in pontos_globais
            ]
            for origem in pontos_globais
        ]

        # 3. O ACO encontra a melhor rota deste drone.
        rota_local, energia = otimizar_rota(
            distancias_drone,
            clientes_drone,
            drone
        )

        # 4. Verifica se a bateria permite a viagem.
        if energia > drone.current_battery_wh:
            return 0.0, float("inf"), []

        energia_total += energia

        # Converte os indices locais para os originais.
        rota_global = [
            pontos_globais[ponto]
            for ponto in rota_local
        ]

        rotas.append(rota_global)

    # 5. Calcula a qualidade da distribuicao completa.
    fitness = calcular_fitness(
        energia_total,
        viavel=True
    )

    return fitness, energia_total, rotas
