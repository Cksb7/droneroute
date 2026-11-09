class DistributionCenter:

    def __init__(
        self,
        center_id: str,
        x: float,
        y: float,
    ) -> None:

        if not center_id.strip():
            raise ValueError("O ID do centro não pode ser vazio.")

        self.center_id = center_id
        self.x = x
        self.y = y