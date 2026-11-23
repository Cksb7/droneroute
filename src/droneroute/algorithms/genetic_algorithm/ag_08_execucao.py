
from droneroute.models.drone import Drone
from droneroute.models.client import Client

from droneroute.algorithms.genetic_algorithm.ag_01_population import (
    gerar_populacao
)
from droneroute.algorithms.genetic_algorithm.ag_06_evolution import (
    criar_nova_geracao
)
from droneroute.algorithms.genetic_algorithm.ag_07_avaliacao import (
    avaliar_cromossomo
)


def executar_algoritmo_hibrido(
    clientes: list[Client],
    drones: list[Drone],
    distancias: list[list[float]],
    tamanho_populacao: int = 8,
    quantidade_geracoes: int = 5,
    taxa_mutacao: float = 0.1,
    quantidade_formigas_aco: int = 10,
    quantidade_iteracoes_aco: int = 20
) -> tuple[
    list[int],
    float,
    list[list[int]],
    list[float],
    list[float],
    list[float]
]:

    if not clientes or not drones:
        raise ValueError("Informe clientes e drones.")

    if tamanho_populacao < 2 or quantidade_geracoes < 1:
        raise ValueError("Parametros de evolucao invalidos.")

    if (
        not isinstance(quantidade_formigas_aco, int)
        or isinstance(quantidade_formigas_aco, bool)
        or quantidade_formigas_aco < 1
    ):
        raise ValueError(
            "A quantidade de formigas deve ser um inteiro positivo."
        )

    if (
        not isinstance(quantidade_iteracoes_aco, int)
        or isinstance(quantidade_iteracoes_aco, bool)
        or quantidade_iteracoes_aco < 1
    ):
        raise ValueError(
            "A quantidade de iteracoes deve ser um inteiro positivo."
        )

    # 1. Cria a populacao inicial do AG.
    populacao = gerar_populacao(
        tamanho_populacao,
        len(clientes),
        len(drones)
    )

    melhor_cromossomo = []
    melhor_energia = float("inf")
    melhor_fitness_acumulado = 0.0
    melhores_rotas = []

    historico_energia = []
    historico_melhor_fitness = []
    historico_fitness_medio = []

    # 2. Executa as geracoes do AG.
    for geracao in range(quantidade_geracoes):

        fitnesses = []

        # 3. Avalia cada cromossomo usando o ACO.
        for cromossomo in populacao:

            fitness, energia, rotas = avaliar_cromossomo(
                cromossomo,
                clientes,
                drones,
                distancias,
                quantidade_formigas_aco=quantidade_formigas_aco,
                quantidade_iteracoes_aco=quantidade_iteracoes_aco
            )

            fitnesses.append(fitness)

            # Guarda a melhor solucao encontrada.
            if fitness > 0 and energia < melhor_energia:

                melhor_energia = energia
                melhor_cromossomo = cromossomo.copy()

                melhores_rotas = [
                    rota.copy() for rota in rotas
                ]

        # 4. Registra a evolucao energetica.
        historico_energia.append(melhor_energia)

        # 5. Registra o melhor fitness acumulado.
        melhor_fitness_geracao = max(fitnesses)

        melhor_fitness_acumulado = max(
            melhor_fitness_acumulado,
            melhor_fitness_geracao
        )

        historico_melhor_fitness.append(
            melhor_fitness_acumulado
        )

        # 6. Registra o fitness medio da populacao.
        fitness_medio = sum(fitnesses) / len(fitnesses)

        historico_fitness_medio.append(fitness_medio)

        # 7. Cria a proxima geracao.
        if geracao < quantidade_geracoes - 1:

            populacao = criar_nova_geracao(
                populacao,
                fitnesses,
                len(drones),
                taxa_mutacao
            )

    if melhor_energia == float("inf"):
        raise ValueError(
            "Nenhuma distribuicao viavel foi encontrada."
        )

    return (
        melhor_cromossomo,
        melhor_energia,
        melhores_rotas,
        historico_energia,
        historico_melhor_fitness,
        historico_fitness_medio
    )
