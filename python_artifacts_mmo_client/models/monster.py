from python_artifacts_mmo_client.models.drop import Drop


class Monster:
    def __init__(self, data: dict[str, str | int]) -> None:
        self.name = data.get("name", "ScaryMonster")
        self.code = data.get("code")
        self.level = data.get("level")
        self.hp = data.get("hp")
        self.attack_fire = data.get("attack_fire")
        self.attack_water = data.get("attack_water")
        self.attack_earth = data.get("attack_earth")
        self.attack_air = data.get("attack_air")
        self.res_fire = data.get("res_fire")
        self.res_water = data.get("res_water")
        self.res_earth = data.get("res_earth")
        self.res_air = data.get("res_air")
        self.min_gold = data.get("min_gold")
        self.max_gold = data.get("max_gold")
        self.drops = [Drop(item) for item in data.get("drops", [])]

    def get_highest_attack_type(self) -> tuple[str, int]:
        attack_type: dict[str, int] = {
            "fire": self.attack_fire,
            "water": self.attack_water,
            "earth": self.attack_earth,
            "air": self.attack_air,
        }
        highest_attack_name = ""
        highest_attack_power = 0

        for attack, power in attack_type.items():
            if power > highest_attack_power:
                highest_attack_name = attack
                highest_attack_power = power

        return highest_attack_name, highest_attack_power

    def get_highest_res_type(self) -> tuple[str, int]:
        res_type: dict[str, int] = {
            "fire": self.res_fire,
            "water": self.res_water,
            "earth": self.res_earth,
            "air": self.res_air,
        }
        highest_res_name = ""
        highest_res_power = 0

        for res, power in res_type.items():
            if power > highest_res_power:
                highest_res_name = res
                highest_res_power = power

        return highest_res_name, highest_res_power

    def __repr__(self) -> str:
        res_name, res_power = self.get_highest_res_type()
        attack_name, attack_power = self.get_highest_attack_type()
        return f"Monster(name={self.name}, level={self.level}, highest_res_name={res_name}, res_power={res_power}, highest_attack_name={attack_name}, attack_power={attack_power})"
