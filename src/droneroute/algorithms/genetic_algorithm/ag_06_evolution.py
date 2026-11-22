from droneroute.algorithms.genetic_algorithm.ag_03_selection import selecao_torneio
from droneroute.algorithms.genetic_algorithm.ag_04_crossover import cruzamento
from droneroute.algorithms.genetic_algorithm.ag_05_mutation import mutar


def criar_nova_geracao(
    populacao: list[list[int]],
    fitnesses: list[float],
    quantidade_drones: int,
    taxa_mutacao: float = 0.1
) -> list[list[int]]:

    if len(populacao) < 2:
        raise ValueError("A população precisa ter pelo menos 2 cromossomos.")

    if len(populacao) != len(fitnesses):
        raise ValueError("Cada cromossomo precisa ter um fitness.")

    # Encontra o melhor cromossomo
    indice_melhor = fitnesses.index(max(fitnesses))

    # Preserva o melhor cromossomo (elitismo)
    nova_populacao = [populacao[indice_melhor].copy()]

    # Gera os demais cromossomos
    while len(nova_populacao) < len(populacao):

        pai1 = selecao_torneio(populacao, fitnesses)
        pai2 = selecao_torneio(populacao, fitnesses)

        filho = cruzamento(pai1, pai2)

        filho = mutar(
            filho,
            quantidade_drones,
            taxa_mutacao
        )

        nova_populacao.append(filho)

    return nova_populacao