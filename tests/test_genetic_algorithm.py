import unittest

from droneroute.models.drone import Drone
from droneroute.models.client import Client

from droneroute.algorithms.genetic_algorithm.ag_01_population import gerar_populacao
from droneroute.algorithms.genetic_algorithm.ag_02_fitness import (
    distribuicao_respeita_carga,
    calcular_fitness
)
from droneroute.algorithms.genetic_algorithm.ag_05_mutation import mutar
from droneroute.algorithms.genetic_algorithm.ag_06_evolution import criar_nova_geracao


class GeneticAlgorithmTests(unittest.TestCase):

    def test_gerar_populacao(self):
        populacao = gerar_populacao(10, 6, 2)

        self.assertEqual(len(populacao), 10)

        for cromossomo in populacao:
            self.assertEqual(len(cromossomo), 6)
            self.assertTrue(all(gene in (1, 2) for gene in cromossomo))

    def test_validacao_carga(self):
        drones = [
            Drone("DR-01", 3.0, 600.0),
            Drone("DR-02", 3.0, 600.0)
        ]

        clientes = [
            Client("C1", 1.0, 1.0, 2.0),
            Client("C2", 2.0, 2.0, 2.0),
            Client("C3", 3.0, 3.0, 1.0)
        ]

        self.assertTrue(
            distribuicao_respeita_carga([1, 2, 1], clientes, drones)
        )

        self.assertFalse(
            distribuicao_respeita_carga([1, 1, 2], clientes, drones)
        )

    def test_fitness(self):
        self.assertGreater(
            calcular_fitness(350.0, True),
            calcular_fitness(500.0, True)
        )

        self.assertEqual(calcular_fitness(200.0, False), 0.0)

    def test_mutacao(self):
        original = [1, 2, 1, 2]

        mutado = mutar(original, 2, 1.0)

        self.assertEqual(mutado, [2, 1, 2, 1])
        self.assertEqual(original, [1, 2, 1, 2])

    def test_elitismo(self):
        populacao = [
            [1, 1, 2],
            [1, 2, 1],
            [2, 1, 2],
            [2, 2, 1]
        ]

        fitnesses = [0.004, 0.002, 0.006, 0.003]

        nova = criar_nova_geracao(populacao, fitnesses, 2)

        self.assertEqual(len(nova), 4)
        self.assertEqual(nova[0], [2, 1, 2])


if __name__ == "__main__":
    unittest.main()