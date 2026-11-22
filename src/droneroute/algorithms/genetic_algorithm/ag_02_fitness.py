from droneroute.models.drone import Drone
from droneroute.models.client import Client


def distribuicao_respeita_carga(
    cromossomo: list[int],
    clientes: list[Client],
    drones: list[Drone]
) -> bool:

    if len(cromossomo) != len(clientes):
        return False

    cargas = [0.0] * len(drones)

    for indice_cliente, numero_drone in enumerate(cromossomo):

        if not 1 <= numero_drone <= len(drones):
            return False

        cargas[numero_drone - 1] += (
            clientes[indice_cliente].package_weight_kg
        )

    for indice_drone, carga_total in enumerate(cargas):

        if carga_total > drones[indice_drone].max_payload_kg:
            return False

    return True

def calcular_fitness(
    energia_total_wh: float,
    viavel: bool
) -> float:

    if not viavel:
        return 0.0

    if energia_total_wh < 0:
        raise ValueError("A energia não pode ser negativa.")

    return 1.0 / (1.0 + energia_total_wh)