
import numpy as np

from collections.abc import Sequence
from numpy.typing import ArrayLike, NDArray

from droneroute.algorithms.ant_colony.aco_02_escolha import (
    escolher_proximo_ponto
)

from droneroute.models.drone import Drone
from droneroute.models.client import Client


def _converter_matriz_distancias(
    distancias: ArrayLike
) -> NDArray[np.float64]:

    try:
        matriz = np.asarray(distancias, dtype=np.float64)

    except (TypeError, ValueError) as erro:
        raise ValueError(
            "A matriz de distancias deve conter valores numericos."
        ) from erro

    if matriz.ndim != 2 or matriz.shape[0] != matriz.shape[1]:
        raise ValueError("A matriz de distancias deve ser quadrada.")

    if not np.isfinite(matriz).all():
        raise ValueError(
            "A matriz de distancias deve conter valores finitos."
        )

    if np.any(matriz < 0):
        raise ValueError(
            "As distancias nao podem ser negativas."
        )

    return matriz


# 1. Construcao da rota pelo ACO.

def construir_rota(
    distancias: ArrayLike,
    feromonios: ArrayLike
) -> list[int]:

    matriz_distancias = _converter_matriz_distancias(distancias)

    quantidade_pontos = matriz_distancias.shape[0]

    if quantidade_pontos < 2:
        raise ValueError("A rota precisa ter pelo menos 2 pontos.")

    try:
        matriz_feromonios = np.asarray(
            feromonios,
            dtype=np.float64
        )

    except (TypeError, ValueError) as erro:
        raise ValueError(
            "A matriz de feromonios deve conter valores numericos."
        ) from erro

    if matriz_feromonios.shape != matriz_distancias.shape:
        raise ValueError(
            "As matrizes de distancias e feromonios "
            "devem possuir as mesmas dimensoes."
        )

    if not np.isfinite(matriz_feromonios).all():
        raise ValueError(
            "Os feromonios devem possuir valores finitos."
        )

    if np.any(matriz_feromonios < 0):
        raise ValueError(
            "Os feromonios nao podem ser negativos."
        )

    rota = [0]
    atual = 0

    nao_visitados = list(range(1, quantidade_pontos))

    while nao_visitados:

        proximo = escolher_proximo_ponto(
            atual,
            nao_visitados,
            matriz_distancias,
            matriz_feromonios
        )

        rota.append(proximo)
        nao_visitados.remove(proximo)

        atual = proximo

    rota.append(0)

    return rota


# 2. Calculo da distancia total da rota.

def calcular_distancia_rota(
    rota: Sequence[int],
    distancias: ArrayLike
) -> float:

    if len(rota) < 2:
        raise ValueError(
            "A rota precisa conter pelo menos 2 pontos."
        )

    matriz_distancias = _converter_matriz_distancias(distancias)

    indices = np.asarray(rota)

    if not np.issubdtype(indices.dtype, np.integer):
        raise ValueError(
            "Os pontos da rota devem ser indices inteiros."
        )

    indices = indices.astype(np.intp, copy=False)

    if np.any(indices < 0) or np.any(indices >= matriz_distancias.shape[0]):
        raise ValueError("A rota possui indices invalidos.")

    # Seleciona todas as distancias entre pontos consecutivos.
    distancias_trechos = matriz_distancias[
        indices[:-1],
        indices[1:]
    ]

    return float(np.sum(distancias_trechos))


# 3. Calculo do consumo energetico da rota.

def calcular_energia_rota(
    rota: Sequence[int],
    distancias: ArrayLike,
    clientes: list[Client],
    drone: Drone
) -> float:

    if len(rota) < 2:
        raise ValueError(
            "A rota precisa conter pelo menos 2 pontos."
        )

    indices = np.asarray(rota)

    if not np.issubdtype(indices.dtype, np.integer):
        raise ValueError(
            "Os pontos da rota devem ser indices inteiros."
        )

    indices = indices.astype(np.intp, copy=False)

    if indices[0] != 0 or indices[-1] != 0:
        raise ValueError(
            "A rota deve comecar e terminar no deposito."
        )

    # Verifica se todos os clientes aparecem exatamente uma vez.
    if not np.array_equal(
        np.sort(indices[1:-1]),
        np.arange(1, len(clientes) + 1)
    ):
        raise ValueError(
            "A rota deve visitar cada cliente uma vez."
        )

    matriz_distancias = _converter_matriz_distancias(distancias)

    if matriz_distancias.shape != (
        len(clientes) + 1,
        len(clientes) + 1
    ):
        raise ValueError(
            "A matriz de distancias nao corresponde aos clientes."
        )

    # Calcula a carga inicial do drone.
    carga_atual = sum(
        cliente.package_weight_kg
        for cliente in clientes
    )

    if carga_atual > drone.max_payload_kg:
        raise ValueError(
            "Carga acima da capacidade do drone."
        )

    # Extrai as distancias de todos os trechos da rota.
    distancias_trechos = matriz_distancias[
        indices[:-1],
        indices[1:]
    ]

    energia_total = 0.0

    # O processamento permanece sequencial porque a carga
    # diminui a cada entrega realizada.
    for distancia, destino in zip(
        distancias_trechos,
        indices[1:]
    ):

        consumo = drone.calcular_consumo_voo(
            float(distancia),
            carga_atual
        )

        energia_total += consumo

        # Apos a entrega, a carga transportada diminui.
        if destino != 0:
            carga_atual -= clientes[int(destino) - 1].package_weight_kg

    return energia_total