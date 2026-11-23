def atualizar_feromonios(
    feromonios: list[list[float]],
    resultados: list[tuple[list[int], float]],
    taxa_evaporacao: float = 0.2,
    fator_deposito: float = 100.0
) -> list[list[float]]:

    if not 0 < taxa_evaporacao < 1:
        raise ValueError(
            "A taxa de evaporacao deve estar entre 0 e 1."
        )

    if fator_deposito <= 0:
        raise ValueError(
            "O fator de deposito deve ser positivo."
        )

    if not resultados:
        raise ValueError(
            "E necessario ter pelo menos uma rota."
        )

    quantidade_pontos = len(feromonios)

    if any(
        len(linha) != quantidade_pontos
        for linha in feromonios
    ):
        raise ValueError(
            "A matriz de feromonios deve ser quadrada."
        )

    # 1. Evaporacao: reduz o feromonio das conexoes.
    nova_matriz = []

    for origem in range(quantidade_pontos):
        linha = []

        for destino in range(quantidade_pontos):

            if origem == destino:
                linha.append(0.0)
            else:
                valor = feromonios[origem][destino]
                linha.append(valor * (1 - taxa_evaporacao))

        nova_matriz.append(linha)

    # 2. Deposito: reforca as conexoes das rotas.
    for rota, energia_total in resultados:

        if energia_total <= 0:
            raise ValueError(
                "O consumo energetico deve ser positivo."
            )

        deposito = fator_deposito / energia_total

        for i in range(len(rota) - 1):

            origem = rota[i]
            destino = rota[i + 1]

            nova_matriz[origem][destino] += deposito

    return nova_matriz