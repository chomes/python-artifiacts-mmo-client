class Fight:
    def __init__(self, data: dict[str, str | int]) -> None:
        self.xp: int = data.get("xp", 0)
        self.gold: int = data.get("gold", 0)
        self.drops: list[dict[str, str | int]] = data.get("drops", [])
        self.turns: int = data.get("turns", 0)
        self.monster_blocked_hits: dict[str, int] = data.get("monster_blocked_hits", {})
        self.player_blocked_hits: dict[str, int] = data.get("player_blocked_hits", {})
        self.logs: list[str] = data.get("logs", [])
        self.result: str = data.get("result", "win?")
