from droneroute.algorithms.ant_colony.aco_02_escolha import (
    escolher_proximo_ponto
)
from droneroute.models.drone import Drone
from droneroute.models.client import Client


# 1. Construção da rota pelo ACO
def construir_rota(
    distancias: list[list[float]],
    feromonios: list[list[float]]
) -> list[int]:

    if len(distancias) < 2:
        raise ValueError("A rota precisa ter pelo menos 2 pontos.")

    rota = [0]
    atual = 0

    nao_visitados = list(range(1, len(distancias)))

    while nao_visitados:

        proximo = escolher_proximo_ponto(
            atual,
            nao_visitados,
            distancias,
            feromonios
        )

        rota.append(proximo)
        nao_visitados.remove(proximo)

        atual = proximo

    rota.append(0)

    return rota


# 2. Cálculo da distância total da rota
def calcular_distancia_rota(
    rota: list[int],
    distancias: list[list[float]]
) -> float:

    if len(rota) < 2:
        raise ValueError("A rota precisa conter pelo menos 2 pontos.")

    distancia_total = 0.0

    for i in range(len(rota) - 1):

        origem = rota[i]
        destino = rota[i + 1]

        distancia_total += distancias[origem][destino]

    return distancia_total


# 3. Cálculo do consumo energético da rota
def calcular_energia_rota(
    rota: list[int],
    distancias: list[list[float]],
    clientes: list[Client],
    drone: Drone
) -> float:

    if len(rota) < 2 or rota[0] != 0 or rota[-1] != 0:
        raise ValueError(
            "A rota deve começar e terminar no depósito."
        )

    if sorted(rota[1:-1]) != list(range(1, len(clientes) + 1)):
        raise ValueError(
            "A rota deve visitar cada cliente uma vez."
        )

    carga_atual = sum(
        cliente.package_weight_kg for cliente in clientes
    )

    if carga_atual > drone.max_payload_kg:
        raise ValueError(
            "Carga acima da capacidade do drone."
        )

    energia_total = 0.0

    for i in range(len(rota) - 1):

        origem = rota[i]
        destino = rota[i + 1]

        distancia = distancias[origem][destino]

        consumo = drone.calcular_consumo_voo(
            distancia,
            carga_atual
        )

        energia_total += consumo

        # Após a entrega, a carga transportada diminui.
        if destino != 0:
            carga_atual -= clientes[destino - 1].package_weight_kg

    return energia_total