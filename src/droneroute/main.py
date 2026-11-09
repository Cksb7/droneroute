from droneroute.models.drone import Drone
from droneroute.models.client import Client
from droneroute.models.charging_station import ChargingStation
from droneroute.models.distribution_center import DistributionCenter

from droneroute.simulation.geometry import calcular_distancia_km


def main():

    # 1. Criando o centro de distribuição

    center = DistributionCenter(
        "DEPOT-01",
        0.0,
        0.0
    )

    # 2. Criando o drone

    drone = Drone(
        "DR-01",
        3.0,
        600.0,
        40.0,
        10.0
    )

    # 3. Criando o cliente

    client = Client(
        "C-01",
        6.0,
        0.0,
        2.0
    )

    # 4. Criando a estação de recarga

    station = ChargingStation(
        "ST-01",
        3.0,
        0.0,
        500.0
    )

    print("\n=== DRONEROUTE ===")

    print(f"Drone: {drone.drone_id}")
    print(f"Bateria inicial: {drone.current_battery_wh} Wh")

    # 5. Voo do centro até o cliente

    print("\n--- ENTREGA ---")

    distance = calcular_distancia_km(
        center.x,
        center.y,
        client.x,
        client.y
    )

    consumption = drone.voar(
        distance,
        client.package_weight_kg
    )

    print(f"Distância: {distance:.2f} km")
    print(f"Energia consumida: {consumption:.2f} Wh")
    print(f"Bateria restante: {drone.current_battery_wh:.2f} Wh")

    print(f"\nEntrega realizada ao cliente {client.client_id}.")

    # 6. Voo do cliente até a estação

    print("\n--- IDA PARA A ESTAÇÃO ---")

    distance = calcular_distancia_km(
        client.x,
        client.y,
        station.x,
        station.y
    )

    consumption = drone.voar(
        distance,
        0.0
    )

    print(f"Distância: {distance:.2f} km")
    print(f"Energia consumida: {consumption:.2f} Wh")
    print(f"Bateria restante: {drone.current_battery_wh:.2f} Wh")

    # 7. Recarga na estação

    print("\n--- RECARGA ---")

    energy_added = station.recarregar_drone(
        drone,
        0.25
    )

    print(f"Estação: {station.station_id}")
    print(f"Potência: {station.charging_power_w} W")
    print(f"Energia adicionada: {energy_added:.2f} Wh")
    print(f"Bateria atual: {drone.current_battery_wh:.2f} Wh")

    # 8. Retorno ao centro de distribuição

    print("\n--- RETORNO AO CENTRO ---")

    distance = calcular_distancia_km(
        station.x,
        station.y,
        center.x,
        center.y
    )

    consumption = drone.voar(
        distance,
        0.0
    )

    print(f"Distância: {distance:.2f} km")
    print(f"Energia consumida: {consumption:.2f} Wh")
    print(f"Bateria final: {drone.current_battery_wh:.2f} Wh")

    print("\n=== SIMULAÇÃO FINALIZADA ===")


if __name__ == "__main__":
    main()