
import random
from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _escolher_proximo_ponto_validado(
    atual: int,
    candidatos: Sequence[int],
    matriz_distancias: NDArray[np.float64],
    matriz_feromonios: NDArray[np.float64]
) -> int:

    if len(candidatos) == 0:
        raise ValueError("Não há destinos candidatos.")

    indices = np.asarray(candidatos)

    if indices.ndim != 1 or not np.issubdtype(
        indices.dtype, np.integer
    ):
        raise ValueError("Os candidatos devem ser índices inteiros.")

    indices = indices.astype(np.intp, copy=False)

    if not 0 <= atual < matriz_distancias.shape[0]:
        raise ValueError("O ponto atual é inválido.")

    if np.any(indices < 0) or np.any(
        indices >= matriz_distancias.shape[0]
    ):
        raise ValueError("Existe um candidato com índice inválido.")

    # Obtém as distâncias e os feromônios dos candidatos.
    distancias_candidatos = matriz_distancias[atual, indices]
    feromonios_candidatos = matriz_feromonios[atual, indices]

    if (
        not np.all(np.isfinite(distancias_candidatos))
        or np.any(distancias_candidatos <= 0)
    ):
        raise ValueError("As distâncias devem ser positivas e finitas.")

    if (
        not np.all(np.isfinite(feromonios_candidatos))
        or np.any(feromonios_candidatos < 0)
    ):
        raise ValueError(
            "Os feromônios devem ser não negativos e finitos."
        )

    # Calcula a atratividade dos destinos simultaneamente.
    pesos = feromonios_candidatos / distancias_candidatos

    soma_pesos = np.sum(pesos)

    if not np.isfinite(soma_pesos) or soma_pesos <= 0:
        raise ValueError(
            "Nenhum destino possui atratividade positiva."
        )

    # Sorteia o próximo destino conforme sua atratividade.
    escolhido = random.choices(
        candidatos,
        weights=pesos,
        k=1
    )[0]

    return int(escolhido)


def escolher_proximo_ponto(
    atual: int,
    candidatos: Sequence[int],
    distancias: ArrayLike,
    feromonios: ArrayLike
) -> int:

    if len(candidatos) == 0:
        raise ValueError("Não há destinos candidatos.")

    try:
        matriz_distancias = np.asarray(
            distancias,
            dtype=np.float64
        )

        matriz_feromonios = np.asarray(
            feromonios,
            dtype=np.float64
        )

    except (TypeError, ValueError) as erro:
        raise ValueError(
            "As matrizes devem conter valores numéricos."
        ) from erro

    if matriz_distancias.ndim != 2 or matriz_feromonios.ndim != 2:
        raise ValueError("As matrizes devem ser bidimensionais.")

    if matriz_distancias.shape != matriz_feromonios.shape:
        raise ValueError(
            "As matrizes devem possuir as mesmas dimensões."
        )

    if (
        matriz_distancias.shape[0]
        != matriz_distancias.shape[1]
    ):
        raise ValueError("As matrizes devem ser quadradas.")

    return _escolher_proximo_ponto_validado(
        atual,
        candidatos,
        matriz_distancias,
        matriz_feromonios
    )