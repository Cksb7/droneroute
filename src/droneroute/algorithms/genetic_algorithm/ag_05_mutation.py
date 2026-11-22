import random


def mutar(
    cromossomo: list[int],
    quantidade_drones: int,
    taxa_mutacao: float = 0.1
) -> list[int]:

    if quantidade_drones < 2:
        raise ValueError("São necessários pelo menos 2 drones.")

    if not 0 <= taxa_mutacao <= 1:
        raise ValueError("A taxa de mutação deve estar entre 0 e 1.")

    mutado = cromossomo.copy()

    for indice in range(len(mutado)):

        if random.random() < taxa_mutacao:

            opcoes = [
                drone
                for drone in range(1, quantidade_drones + 1)
                if drone != mutado[indice]
            ]

            mutado[indice] = random.choice(opcoes)

    return mutado