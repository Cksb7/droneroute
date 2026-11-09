from math import hypot


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