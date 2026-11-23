
import math
import random

from droneroute.models.drone import Drone
from droneroute.models.client import Client
from droneroute.models.distribution_center import DistributionCenter

from droneroute.simulation.geometry import (
    calcular_matriz_distancias
)

from droneroute.algorithms.genetic_algorithm.ag_08_execucao import (
    executar_algoritmo_hibrido
)

from droneroute.visualization.graficos import mostrar_graficos


# Numero inteiro: permite reproduzir o experimento.
SEED = None


def main():

    # 1. Configuracao da simulacao.

    if SEED is not None:
        random.seed(SEED)

    # Parametros do Algoritmo Genetico.
    tamanho_populacao = 30
    quantidade_geracoes = 40
    taxa_mutacao = 0.1

    # Parametros da Colonia de Formigas.
    quantidade_formigas_aco = 10
    quantidade_iteracoes_aco = 20

    centro = DistributionCenter("CD1", 0, 0)

    # 2. Frota de drones.

    drones = [
        Drone("D1", 10, 3500),
        Drone("D2", 10, 3500),
        Drone("D3", 10, 3500),
        Drone("D4", 10, 3500),
        Drone("D5", 10, 3500)
    ]

    # 3. Clientes e encomendas.

    clientes = [
        Client("C1", 2, 3, 2),
        Client("C2", 5, 4, 1),
        Client("C3", 7, 2, 2),
        Client("C4", 4, 7, 1),
        Client("C5", 0, 6, 2),
        Client("C6", -3, 5, 1),
        Client("C7", -6, 4, 2),
        Client("C8", -4, 8, 1),
        Client("C9", -7, 1, 1),
        Client("C10", -5, -3, 2),
        Client("C11", -7, -5, 1),
        Client("C12", -3, -7, 2),
        Client("C13", 0, -6, 1),
        Client("C14", 3, -5, 2),
        Client("C15", 6, -4, 1),
        Client("C16", 8, -2, 2),
        Client("C17", 5, -7, 1),
        Client("C18", 1, 1, 2),
        Client("C19", -2, -1, 1),
        Client("C20", 2, -2, 2)
    ]

    # 4. Calcula a matriz de distancias.

    pontos = [centro] + clientes

    distancias = calcular_matriz_distancias(pontos)

    # 5. Executa a integracao AG + ACO.

    (
        cromossomo,
        energia,
        rotas,
        historico_energia,
        historico_melhor_fitness,
        historico_fitness_medio
    ) = executar_algoritmo_hibrido(
        clientes,
        drones,
        distancias,
        tamanho_populacao=tamanho_populacao,
        quantidade_geracoes=quantidade_geracoes,
        taxa_mutacao=taxa_mutacao,
        quantidade_formigas_aco=quantidade_formigas_aco,
        quantidade_iteracoes_aco=quantidade_iteracoes_aco
    )

    # 6. Apresenta os resultados.

    print("\n=== DRONEROUTE | AG + ACO ===")

    print(f"\nClientes: {len(clientes)}")
    print(f"Drones disponiveis: {len(drones)}")

    print(f"Tamanho da populacao: {tamanho_populacao}")
    print(f"Quantidade de geracoes: {quantidade_geracoes}")
    print(f"Taxa de mutacao: {taxa_mutacao}")

    print(f"Quantidade de formigas ACO: {quantidade_formigas_aco}")
    print(f"Quantidade de iteracoes ACO: {quantidade_iteracoes_aco}")

    print("\nDistribuicao encontrada:")
    print(cromossomo)

    print(f"\nConsumo energetico total: {energia:.2f} Wh")

    print(
        f"Fitness final: "
        f"{historico_melhor_fitness[-1]:.8e}"
    )

    # Melhoria em relacao a primeira geracao viavel.

    energia_inicial = historico_energia[0]

    if math.isfinite(energia_inicial) and energia_inicial > 0:

        melhoria = (
            (energia_inicial - energia)
            / energia_inicial
        ) * 100

        print(
            f"Melhoria desde a geracao 1: "
            f"{melhoria:.2f}%"
        )

    else:
        print(
            "Melhoria desde a geracao 1: "
            "indisponivel (sem solucao viavel inicial)"
        )

    # 7. Apresenta as rotas.

    print("\n=== ROTAS DOS DRONES ===")

    for indice, rota in enumerate(rotas):

        if len(rota) <= 2:
            print(f"{drones[indice].drone_id}: Sem entregas")
            continue

        nomes = [
            "Deposito" if ponto == 0
            else clientes[ponto - 1].client_id
            for ponto in rota
        ]

        print(
            f"{drones[indice].drone_id}: "
            + " -> ".join(nomes)
        )

    # 8. Historico da evolucao.

    print("\n=== EVOLUCAO POR GERACAO ===")

    for indice in range(len(historico_energia)):

        print(
            f"Geracao {indice + 1:02d} | "
            f"Energia: {historico_energia[indice]:.2f} Wh | "
            f"Melhor fitness: "
            f"{historico_melhor_fitness[indice]:.8e} | "
            f"Fitness medio: "
            f"{historico_fitness_medio[indice]:.8e}"
        )

    # 9. Apresenta a visualizacao.

    mostrar_graficos(
        centro,
        clientes,
        rotas,
        historico_energia,
        historico_melhor_fitness,
        historico_fitness_medio
    )


if __name__ == "__main__":
    main()
