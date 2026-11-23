import random


def escolher_proximo_ponto(
    atual: int,
    candidatos: list[int],
    distancias: list[list[float]],
    feromonios: list[list[float]]
) -> int:

    if not candidatos:
        raise ValueError("Não há destinos candidatos.")

    pesos = []

    for destino in candidatos:

        distancia = distancias[atual][destino]
        feromonio = feromonios[atual][destino]

        if distancia <= 0:
            raise ValueError("A distância deve ser positiva.")

        if feromonio < 0:
            raise ValueError("O feromônio não pode ser negativo.")

        atratividade = feromonio / distancia

        pesos.append(atratividade)

    if sum(pesos) <= 0:
        raise ValueError("Nenhum destino possui atratividade positiva.")

    escolhido = random.choices(
        candidatos,
        weights=pesos,
        k=1
    )[0]

    return escolhido