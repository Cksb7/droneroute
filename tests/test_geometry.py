import unittest

from droneroute.simulation.geometry import calcular_distancia_km


class GeometryTests(unittest.TestCase):

    def test_euclidean_distance(self):

        distance = calcular_distancia_km(
            0.0,
            0.0,
            3.0,
            4.0
        )

        self.assertEqual(distance, 5.0)

    def test_same_position(self):

        distance = calcular_distancia_km(
            5.0,
            5.0,
            5.0,
            5.0
        )

        self.assertEqual(distance, 0.0)


if __name__ == "__main__":
    unittest.main()