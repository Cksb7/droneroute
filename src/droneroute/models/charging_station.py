from droneroute.models.drone import Drone


class ChargingStation:

    def __init__(
        self,
        station_id: str,
        x: float,
        y: float,
        charging_power_w: float,
    ) -> None:

        if not station_id.strip():
            raise ValueError("O ID da estação não pode ser vazio.")

        if charging_power_w <= 0:
            raise ValueError("A potência deve ser positiva.")

        self.station_id = station_id
        self.x = x
        self.y = y
        self.charging_power_w = charging_power_w

    def recarregar_drone(
        self,
        drone: Drone,
        duration_hours: float
    ) -> float:

        if duration_hours <= 0:
            raise ValueError("O tempo de recarga deve ser positivo.")

        energia_fornecida_wh = (
            self.charging_power_w * duration_hours
        )

        return drone.recarregar_bateria(energia_fornecida_wh)