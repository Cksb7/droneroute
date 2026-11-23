
import numpy as np

from collections.abc import Sequence
from numpy.typing import ArrayLike

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
    distancias: ArrayLike,
    clientes: Sequence[Client],
    drone: Drone,
    quantidade_formigas: int = 10,
    quantidade_iteracoes: int = 20
) -> tuple[list[int], float]:

    if (
        isinstance(quantidade_formigas, (bool, np.bool_))
        or not isinstance(quantidade_formigas, (int, np.integer))
        or quantidade_formigas < 1
    ):
        raise ValueError(
            "A quantidade de formigas deve ser um inteiro positivo."
        )

    if (
        isinstance(quantidade_iteracoes, (bool, np.bool_))
        or not isinstance(quantidade_iteracoes, (int, np.integer))
        or quantidade_iteracoes < 1
    ):
        raise ValueError(
            "A quantidade de iteracoes deve ser um inteiro positivo."
        )

    if len(clientes) == 0:
        return [0], 0.0

    # 1. Prepara e valida a matriz de distancias.
    try:
        matriz_distancias = np.asarray(
            distancias,
            dtype=np.float64
        )

    except (TypeError, ValueError) as erro:
        raise ValueError(
            "A matriz de distancias deve conter valores numericos."
        ) from erro

    quantidade_pontos = len(clientes) + 1

    if matriz_distancias.shape != (
        quantidade_pontos,
        quantidade_pontos
    ):
        raise ValueError(
            "A matriz deve conter o deposito e todos os clientes."
        )

    if not np.isfinite(matriz_distancias).all():
        raise ValueError(
            "As distancias devem possuir valores finitos."
        )

    if np.any(matriz_distancias < 0):
        raise ValueError(
            "As distancias nao podem ser negativas."
        )

    # O ACO utiliza a distancia como parte do calculo de atratividade.
    mascara_fora_diagonal = ~np.eye(
        quantidade_pontos,
        dtype=bool
    )

    if np.any(matriz_distancias[mascara_fora_diagonal] <= 0):
        raise ValueError(
            "As distancias entre pontos diferentes devem ser positivas."
        )

    # 2. Inicializa a matriz de feromonios.
    feromonios = criar_matriz_feromonios(
        quantidade_pontos
    )

    melhor_rota = []
    melhor_energia = float("inf")

    # 3. Executa as iteracoes do ACO.
    for _ in range(quantidade_iteracoes):

        resultados = []

        # Cada formiga constroi sua propria rota.
        for _ in range(quantidade_formigas):

            rota = construir_rota(
                matriz_distancias,
                feromonios
            )

            energia = calcular_energia_rota(
                rota,
                matriz_distancias,
                clientes,
                drone
            )

            resultados.append((rota, energia))

            # Preserva a melhor rota encontrada.
            if energia < melhor_energia:

                melhor_energia = energia
                melhor_rota = rota.copy()

        # 4. Atualiza os feromonios ao final de cada iteracao.
        feromonios = atualizar_feromonios(
            feromonios,
            resultados
        )

    return melhor_rota, melhor_energia
