class Drop:
    def __init__(self, data: dict[str, str | int]) -> None:
        self.code: str = data.get("code", "No Code")
        self.rate: int = data.get("rate", 1)
        self.min_quantity: int = data.get("min_quantity", 1)
        self.max_quantity: int = data.get("max_quantity", 1)