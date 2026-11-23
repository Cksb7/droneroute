
import numpy as np
from numpy.typing import NDArray


def criar_matriz_feromonios(
    quantidade_pontos: int,
    feromonio_inicial: float = 1.0
) -> NDArray[np.float64]:

    if quantidade_pontos < 2:
        raise ValueError("São necessários pelo menos 2 pontos.")

    if not np.isfinite(feromonio_inicial) or feromonio_inicial <= 0:
        raise ValueError("O feromônio inicial deve ser positivo e finito.")

    # Cria uma matriz preenchida com o valor inicial dos feromônios.
    matriz = np.full(
        (quantidade_pontos, quantidade_pontos),
        feromonio_inicial,
        dtype=np.float64
    )

    # Zera a diagonal principal, pois um ponto não possui distância
    # de deslocamento para ele mesmo.
    np.fill_diagonal(matriz, 0.0)

    return matriz
