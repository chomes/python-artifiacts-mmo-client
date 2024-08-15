from python_artifacts_mmo_client.models.drop import Drop


class Resource:
    def __init__(self, data: dict[str, str | int]) -> None:
        self.name: str = data.get("name", "No Name")
        self.code: str = data.get("code", "No Code")
        self.skill: str = data.get("skill", "No Skill")
        self.level: int = data.get("level", 0)
        self.gold: int = data.get("gold", 0)
        self.drops: list[dict[str, str | int]] = [
            Drop(item) for item in data.get("drops", [])
        ]
