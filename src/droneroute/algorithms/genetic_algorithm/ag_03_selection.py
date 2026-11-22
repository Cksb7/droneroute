import random


def selecao_torneio(
    populacao: list[list[int]],
    fitnesses: list[float]
) -> list[int]:

    if len(populacao) < 2:
        raise ValueError("A população precisa ter pelo menos 2 cromossomos.")

    if len(populacao) != len(fitnesses):
        raise ValueError("Cada cromossomo precisa ter um fitness.")

    indice_a, indice_b = random.sample(
        range(len(populacao)),
        2
    )

    if fitnesses[indice_a] >= fitnesses[indice_b]:
        return populacao[indice_a].copy()

    return populacao[indice_b].copy()