
import random
import unittest

from droneroute.models.drone import Drone
from droneroute.models.client import Client

from droneroute.algorithms.genetic_algorithm.ag_07_avaliacao import (
    avaliar_cromossomo
)

from droneroute.algorithms.genetic_algorithm.ag_08_execucao import (
    executar_algoritmo_hibrido
)


class TestAlgoritmoHibrido(unittest.TestCase):

    def setUp(self):
        self.clientes = [
            Client("C1", 0, 0, 2),
            Client("C2", 0, 0, 1)
        ]

        self.distancias = [
            [0, 2, 4],
            [2, 0, 3],
            [4, 3, 0]
        ]

    def test_consumo_energetico(self):
        drones = [Drone("D1", 5, 600)]

        fitness, energia, rotas = avaliar_cromossomo(
            [1, 1],
            self.clientes,
            drones,
            self.distancias
        )

        self.assertGreater(fitness, 0)
        self.assertEqual(energia, 450.0)
        self.assertEqual(rotas, [[0, 1, 2, 0]])

    def test_capacidade_excedida(self):
        drones = [Drone("D1", 2, 600)]

        fitness, energia, rotas = avaliar_cromossomo(
            [1, 1],
            self.clientes,
            drones,
            self.distancias
        )

        self.assertEqual(fitness, 0.0)
        self.assertEqual(energia, float("inf"))
        self.assertEqual(rotas, [])

    def test_bateria_insuficiente(self):
        drones = [Drone("D1", 5, 400)]

        fitness, energia, rotas = avaliar_cromossomo(
            [1, 1],
            self.clientes,
            drones,
            self.distancias
        )

        self.assertEqual(fitness, 0.0)
        self.assertEqual(energia, float("inf"))
        self.assertEqual(rotas, [])

    def test_evolucao_hibrida(self):
        random.seed(42)

        drones = [
            Drone("D1", 5, 600),
            Drone("D2", 5, 600)
        ]

        (
            cromossomo,
            energia,
            rotas,
            historico_energia,
            historico_melhor_fitness,
            historico_fitness_medio
        ) = executar_algoritmo_hibrido(
            self.clientes,
            drones,
            self.distancias
        )

        self.assertEqual(energia, 450.0)
        self.assertIn(cromossomo, ([1, 1], [2, 2]))

        self.assertEqual(len(historico_energia), 5)
        self.assertEqual(len(historico_melhor_fitness), 5)
        self.assertEqual(len(historico_fitness_medio), 5)

        # O melhor consumo nao pode aumentar.
        self.assertTrue(
            all(
                historico_energia[i] <= historico_energia[i - 1]
                for i in range(1, len(historico_energia))
            )
        )

        # O melhor fitness acumulado nao pode diminuir.
        self.assertTrue(
            all(
                historico_melhor_fitness[i]
                >= historico_melhor_fitness[i - 1]
                for i in range(1, len(historico_melhor_fitness))
            )
        )

        # O fitness medio deve ser valido.
        self.assertTrue(
            all(valor >= 0 for valor in historico_fitness_medio)
        )

        self.assertGreater(historico_melhor_fitness[-1], 0)


if __name__ == "__main__":
    unittest.main()
