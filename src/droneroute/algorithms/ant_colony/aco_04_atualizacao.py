
from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray


def atualizar_feromonios(
    feromonios: ArrayLike,
    resultados: Sequence[tuple[Sequence[int], float]],
    taxa_evaporacao: float = 0.2,
    fator_deposito: float = 100.0
) -> NDArray[np.float64]:

    if not np.isfinite(taxa_evaporacao) or not 0 < taxa_evaporacao < 1:
        raise ValueError(
            "A taxa de evaporacao deve estar entre 0 e 1."
        )

    if not np.isfinite(fator_deposito) or fator_deposito <= 0:
        raise ValueError(
            "O fator de deposito deve ser positivo e finito."
        )

    if not resultados:
        raise ValueError(
            "E necessario ter pelo menos uma rota."
        )

    try:
        matriz = np.asarray(feromonios, dtype=np.float64)

    except (TypeError, ValueError) as erro:
        raise ValueError(
            "A matriz de feromonios deve conter valores numericos."
        ) from erro

    if matriz.ndim != 2 or matriz.shape[0] != matriz.shape[1]:
        raise ValueError(
            "A matriz de feromonios deve ser quadrada."
        )

    if matriz.shape[0] < 2:
        raise ValueError(
            "A matriz deve possuir pelo menos 2 pontos."
        )

    if not np.isfinite(matriz).all() or np.any(matriz < 0):
        raise ValueError(
            "Os feromonios devem ser valores nao negativos e finitos."
        )

    quantidade_pontos = matriz.shape[0]

    # 1. Evaporacao: reduz o feromonio de todas as conexoes.
    nova_matriz = matriz * (1.0 - taxa_evaporacao)

    # As conexoes de um ponto com ele mesmo nao recebem feromonio.
    np.fill_diagonal(nova_matriz, 0.0)

    # 2. Deposito: reforca as conexoes utilizadas pelas formigas.
    for rota, energia_total in resultados:

        energia_total = float(energia_total)

        if not np.isfinite(energia_total) or energia_total <= 0:
            raise ValueError(
                "O consumo energetico deve ser positivo e finito."
            )

        indices = np.asarray(rota)

        if (
            indices.ndim != 1
            or len(indices) < 2
            or not np.issubdtype(indices.dtype, np.integer)
        ):
            raise ValueError(
                "A rota deve conter indices inteiros validos."
            )

        indices = indices.astype(np.intp, copy=False)

        if np.any(indices < 0) or np.any(indices >= quantidade_pontos):
            raise ValueError(
                "A rota possui indices fora dos limites da matriz."
            )

        # Calcula a quantidade de feromonio depositada pela formiga.
        deposito = fator_deposito / energia_total

        if not np.isfinite(deposito):
            raise ValueError(
                "O deposito de feromonio deve ser finito."
            )

        # Identifica todas as conexoes percorridas pela rota.
        origens = indices[:-1]
        destinos = indices[1:]

        # Adiciona o feromonio em todas as conexoes simultaneamente.
        np.add.at(
            nova_matriz,
            (origens, destinos),
            deposito
        )

    # Garante que a diagonal permaneça zerada.
    np.fill_diagonal(nova_matriz, 0.0)

    return nova_matriz
