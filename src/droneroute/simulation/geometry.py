
from collections.abc import Sequence
from math import hypot
from typing import Protocol

import numpy as np


class Ponto(Protocol):
    x: float
    y: float


def calcular_distancia_km(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> float:

    distancia = hypot(
        x2 - x1,
        y2 - y1
    )

    return distancia


def calcular_matriz_distancias(
    pontos: Sequence[Ponto]
) -> np.ndarray:
    """Calcula as distâncias euclidianas entre todos os pontos."""

    if not pontos:
        raise ValueError(
            "Informe pelo menos um ponto para calcular as distâncias."
        )

    coordenadas = np.asarray(
        [(ponto.x, ponto.y) for ponto in pontos],
        dtype=float
    )

    if not np.isfinite(coordenadas).all():
        raise ValueError(
            "As coordenadas dos pontos devem ser valores finitos."
        )

    # Calcula as diferenças entre todas as coordenadas.
    diferencas = (
        coordenadas[:, np.newaxis, :]
        - coordenadas[np.newaxis, :, :]
    )

    # Calcula as distâncias euclidianas simultaneamente.
    matriz_distancias = np.linalg.norm(
        diferencas,
        axis=2
    )

    return matriz_distancias