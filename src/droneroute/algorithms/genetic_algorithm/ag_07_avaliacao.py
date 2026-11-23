
import numpy as np

from collections.abc import Sequence

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
    distancias: np.ndarray | Sequence[Sequence[float]],
    quantidade_formigas_aco: int = 10,
    quantidade_iteracoes_aco: int = 20
) -> tuple[float, float, list[list[int]]]:

    quantidade_pontos = len(clientes) + 1

    # 1. Converte as distancias para uma matriz NumPy.

    try:
        matriz_distancias = np.asarray(
            distancias,
            dtype=np.float64
        )

    except (TypeError, ValueError) as erro:
        raise ValueError(
            "A matriz de distancias deve conter valores numericos."
        ) from erro

    # 2. Valida as dimensoes da matriz.

    if matriz_distancias.shape != (
        quantidade_pontos,
        quantidade_pontos
    ):
        raise ValueError("Matriz de distancias invalida.")

    if not np.isfinite(matriz_distancias).all():
        raise ValueError(
            "A matriz de distancias deve conter valores finitos."
        )

    if np.any(matriz_distancias < 0):
        raise ValueError(
            "As distancias nao podem ser negativas."
        )

    # 3. Verifica se a distribuicao respeita a carga.

    if not distribuicao_respeita_carga(
        cromossomo,
        clientes,
        drones
    ):
        return 0.0, float("inf"), []

    energia_total = 0.0
    rotas = []

    # 4. Avalia os clientes atribuidos a cada drone.

    for numero_drone, drone in enumerate(drones, start=1):

        indices_clientes = [
            indice
            for indice, atribuido in enumerate(cromossomo)
            if atribuido == numero_drone
        ]

        # Drone sem clientes nao precisa realizar voo.

        if not indices_clientes:
            rotas.append([0])
            continue

        clientes_drone = [
            clientes[indice]
            for indice in indices_clientes
        ]

        # Indices dos pontos na matriz original.
        # O indice 0 representa o deposito.

        pontos_globais = [0] + [
            indice + 1
            for indice in indices_clientes
        ]

        # 5. Extrai a matriz de distancias deste drone.
        # np.ix_ seleciona simultaneamente linhas e colunas.

        distancias_drone = matriz_distancias[
            np.ix_(
                pontos_globais,
                pontos_globais
            )
        ]

        # 6. O ACO encontra a melhor rota deste drone.

        rota_local, energia = otimizar_rota(
            distancias_drone,
            clientes_drone,
            drone,
            quantidade_formigas=quantidade_formigas_aco,
            quantidade_iteracoes=quantidade_iteracoes_aco
        )

        # 7. Verifica se a bateria permite a viagem.

        if energia > drone.current_battery_wh:
            return 0.0, float("inf"), []

        energia_total += energia

        # 8. Converte os indices locais para os originais.

        rota_global = [
            pontos_globais[ponto]
            for ponto in rota_local
        ]

        rotas.append(rota_global)

    # 9. Calcula a qualidade da distribuicao completa.

    fitness = calcular_fitness(
        energia_total,
        viavel=True
    )

    return fitness, energia_total, rotas
