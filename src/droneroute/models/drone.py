class Drone:

    def __init__(
        self,
        drone_id: str,
        max_payload_kg: float,
        battery_capacity_wh: float,
        base_consumption_wh_per_km: float = 40.0,
        payload_consumption_wh_per_km_kg: float = 10.0,
    ) -> None:

        if not drone_id.strip():
            raise ValueError("O ID do drone não pode ser vazio.")

        if max_payload_kg <= 0:
            raise ValueError("A capacidade de carga deve ser positiva.")

        if battery_capacity_wh <= 0:
            raise ValueError("A capacidade da bateria deve ser positiva.")

        if base_consumption_wh_per_km <= 0:
            raise ValueError("O consumo base deve ser positivo.")

        if payload_consumption_wh_per_km_kg < 0:
            raise ValueError("O fator de carga não pode ser negativo.")

        self.drone_id = drone_id
        self.max_payload_kg = max_payload_kg
        self.battery_capacity_wh = battery_capacity_wh
        self.current_battery_wh = battery_capacity_wh

        self.base_consumption_wh_per_km = base_consumption_wh_per_km
        self.payload_consumption_wh_per_km_kg = (
            payload_consumption_wh_per_km_kg
        )

    def consumir_bateria(self, consumo_wh: float) -> None:

        if consumo_wh <= 0:
            raise ValueError("O consumo deve ser positivo.")

        if consumo_wh > self.current_battery_wh:
            raise ValueError("Bateria insuficiente.")

        self.current_battery_wh = max(
            0.0,
            self.current_battery_wh - consumo_wh
        )

    def recarregar_bateria(self, energia_wh: float) -> float:

        if energia_wh <= 0:
            raise ValueError("A energia fornecida deve ser positiva.")

        bateria_anterior = self.current_battery_wh

        self.current_battery_wh = min(
            self.current_battery_wh + energia_wh,
            self.battery_capacity_wh
        )

        return self.current_battery_wh - bateria_anterior

    def calcular_consumo_voo(
        self,
        distance_km: float,
        payload_kg: float
    ) -> float:

        if distance_km <= 0:
            raise ValueError("A distância deve ser positiva.")

        if payload_kg < 0:
            raise ValueError("O peso da carga não pode ser negativo.")

        if payload_kg > self.max_payload_kg:
            raise ValueError("Carga acima da capacidade do drone.")

        consumo_por_km = (
            self.base_consumption_wh_per_km
            + payload_kg * self.payload_consumption_wh_per_km_kg
        )

        return distance_km * consumo_por_km

    def voar(
        self,
        distance_km: float,
        payload_kg: float
    ) -> float:

        consumo = self.calcular_consumo_voo(
            distance_km,
            payload_kg
        )

        self.consumir_bateria(consumo)

        return consumo