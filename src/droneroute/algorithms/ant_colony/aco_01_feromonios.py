def criar_matriz_feromonios(
    quantidade_pontos: int,
    feromonio_inicial: float = 1.0
) -> list[list[float]]:

    if quantidade_pontos < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")

    if feromonio_inicial <= 0:
        raise ValueError("O feromônio inicial deve ser positivo.")

    matriz = []

    for origem in range(quantidade_pontos):
        linha = []

        for destino in range(quantidade_pontos):

            if origem == destino:
                linha.append(0.0)
            else:
                linha.append(feromonio_inicial)

        matriz.append(linha)

    return matriz