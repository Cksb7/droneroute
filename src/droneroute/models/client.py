class Client:

    def __init__(
        self,
        client_id: str,
        x: float,
        y: float,
        package_weight_kg: float,
    ) -> None:

        if not client_id.strip():
            raise ValueError("O ID do cliente não pode ser vazio.")

        if package_weight_kg <= 0:
            raise ValueError("O peso da encomenda deve ser positivo.")

        self.client_id = client_id
        self.x = x
        self.y = y
        self.package_weight_kg = package_weight_kg