import random


def cruzamento(
    pai1: list[int],
    pai2: list[int]
) -> list[int]:

    if len(pai1) != len(pai2):
        raise ValueError("Os pais devem ter o mesmo tamanho.")

    if len(pai1) < 2:
        raise ValueError("Os pais precisam ter pelo menos 2 genes.")

    ponto_corte = random.randint(1, len(pai1) - 1)

    filho = pai1[:ponto_corte] + pai2[ponto_corte:]

    return filho
