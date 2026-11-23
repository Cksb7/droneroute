from droneroute.algorithms.ant_colony.aco_01_feromonios import (
    criar_matriz_feromonios
)

from droneroute.algorithms.ant_colony.aco_03_rota import (
    construir_rota,
    calcular_energia_rota
)

from droneroute.algorithms.ant_colony.aco_04_atualizacao import (
    atualizar_feromonios
)

from droneroute.models.drone import Drone
from droneroute.models.client import Client


def otimizar_rota(
    distancias: list[list[float]],
    clientes: list[Client],
    drone: Drone,
    quantidade_formigas: int = 10,
    quantidade_iteracoes: int = 20
) -> tuple[list[int], float]:

    if quantidade_formigas < 1 or quantidade_iteracoes < 1:
        raise ValueError(
            "Formigas e iteracoes devem ser maiores que zero."
        )

    if not clientes:
        return [0], 0.0

    if len(distancias) != len(clientes) + 1:
        raise ValueError(
            "A matriz deve conter o deposito e todos os clientes."
        )

    feromonios = criar_matriz_feromonios(
        len(distancias)
    )

    melhor_rota = []
    melhor_energia = float("inf")

    # Cada iteracao representa uma rodada do ACO.
    for _ in range(quantidade_iteracoes):

        resultados = []

        # Cada formiga constroi uma rota.
        for _ in range(quantidade_formigas):

            rota = construir_rota(
                distancias,
                feromonios
            )

            energia = calcular_energia_rota(
                rota,
                distancias,
                clientes,
                drone
            )

            resultados.append((rota, energia))

            # Guarda a melhor rota encontrada ate agora.
            if energia < melhor_energia:

                melhor_energia = energia
                melhor_rota = rota.copy()

        # Atualiza os feromonios uma vez por rodada.
        feromonios = atualizar_feromonios(
            feromonios,
            resultados
        )

    return melhor_rota, melhor_energia