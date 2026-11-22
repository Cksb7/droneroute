import random


def gerar_cromossomo(
    quantidade_clientes: int,
    quantidade_drones: int
) -> list[int]:

    cromossomo = []

    for _ in range(quantidade_clientes):
        drone = random.randint(1, quantidade_drones)
        cromossomo.append(drone)

    return cromossomo

def gerar_populacao(
    tamanho_populacao: int,
    quantidade_clientes: int,
    quantidade_drones: int
) -> list[list[int]]:

    populacao = []

    for _ in range(tamanho_populacao):
        cromossomo = gerar_cromossomo(
            quantidade_clientes,
            quantidade_drones
        )

        populacao.append(cromossomo)

    return populacao