import unittest

from droneroute.models.drone import Drone
from droneroute.models.client import Client
from droneroute.models.charging_station import ChargingStation
from droneroute.models.distribution_center import DistributionCenter


class DroneTests(unittest.TestCase):

    def setUp(self):
        self.drone = Drone(
            "DR-01",
            3.0,
            500.0,
            40.0,
            10.0
        )

    def test_initial_battery(self):
        self.assertEqual(
            self.drone.current_battery_wh,
            500.0
        )

    def test_battery_consumption(self):
        self.drone.consumir_bateria(100.0)

        self.assertEqual(
            self.drone.current_battery_wh,
            400.0
        )

    def test_insufficient_battery(self):
        with self.assertRaises(ValueError):
            self.drone.consumir_bateria(600.0)

    def test_battery_recharge(self):
        self.drone.consumir_bateria(200.0)
        self.drone.recarregar_bateria(100.0)

        self.assertEqual(
            self.drone.current_battery_wh,
            400.0
        )

    def test_recharge_limit(self):
        self.drone.consumir_bateria(100.0)
        self.drone.recarregar_bateria(200.0)

        self.assertEqual(
            self.drone.current_battery_wh,
            500.0
        )

    def test_flight_consumption(self):
        consumption = self.drone.voar(2.0, 1.0)

        self.assertEqual(consumption, 100.0)

        self.assertEqual(
            self.drone.current_battery_wh,
            400.0
        )

    def test_payload_limit(self):
        with self.assertRaises(ValueError):
            self.drone.voar(2.0, 4.0)


class ChargingStationTests(unittest.TestCase):

    def test_station_recharge(self):

        drone = Drone("DR-02", 3.0, 500.0)

        drone.consumir_bateria(200.0)

        station = ChargingStation(
            "ST-01",
            5.0,
            3.0,
            500.0
        )

        energy_added = station.recarregar_drone(
            drone,
            0.25
        )

        self.assertEqual(energy_added, 125.0)

        self.assertEqual(
            drone.current_battery_wh,
            425.0
        )


class ClientTests(unittest.TestCase):

    def test_client_creation(self):

        client = Client(
            "C-01",
            10.0,
            20.0,
            2.0
        )

        self.assertEqual(client.client_id, "C-01")
        self.assertEqual(client.package_weight_kg, 2.0)


class DistributionCenterTests(unittest.TestCase):

    def test_center_creation(self):

        center = DistributionCenter(
            "DEPOT-01",
            0.0,
            0.0
        )

        self.assertEqual(center.center_id, "DEPOT-01")


if __name__ == "__main__":
    unittest.main()