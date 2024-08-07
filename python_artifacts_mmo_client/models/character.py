from datetime import datetime


class Character:
    def __init__(self, data: dict[str, str | int]):
        self.name = data["name"]
        self.skin = data["skin"]
        self.level = data["level"]
        self.xp = data["xp"]
        self.max_xp = data["max_xp"]
        self.total_xp = data["total_xp"]
        self.gold = data["gold"]
        self.speed = data["speed"]
        self.mining_level = data["mining_level"]
        self.mining_xp = data["mining_xp"]
        self.mining_max_xp = data["mining_max_xp"]
        self.woodcutting_level = data["woodcutting_level"]
        self.woodcutting_xp = data["woodcutting_xp"]
        self.woodcutting_max_xp = data["woodcutting_max_xp"]
        self.fishing_level = data["fishing_level"]
        self.fishing_xp = data["fishing_xp"]
        self.fishing_max_xp = data["fishing_max_xp"]
        self.weaponcrafting_level = data["weaponcrafting_level"]
        self.weaponcrafting_xp = data["weaponcrafting_xp"]
        self.weaponcrafting_max_xp = data["weaponcrafting_max_xp"]
        self.gearcrafting_level = data["gearcrafting_level"]
        self.gearcrafting_xp = data["gearcrafting_xp"]
        self.gearcrafting_max_xp = data["gearcrafting_max_xp"]
        self.jewelrycrafting_level = data["jewelrycrafting_level"]
        self.jewelrycrafting_xp = data["jewelrycrafting_xp"]
        self.jewelrycrafting_max_xp = data["jewelrycrafting_max_xp"]
        self.cooking_level = data["cooking_level"]
        self.cooking_xp = data["cooking_xp"]
        self.cooking_max_xp = data["cooking_max_xp"]
        self.hp = data["hp"]
        self.haste = data["haste"]
        self.critical_strike = data["critical_strike"]
        self.stamina = data["stamina"]
        self.attack_fire = data["attack_fire"]
        self.attack_earth = data["attack_earth"]
        self.attack_water = data["attack_water"]
        self.attack_air = data["attack_air"]
        self.dmg_fire = data["dmg_fire"]
        self.dmg_earth = data["dmg_earth"]
        self.dmg_water = data["dmg_water"]
        self.dmg_air = data["dmg_air"]
        self.res_fire = data["res_fire"]
        self.res_earth = data["res_earth"]
        self.res_water = data["res_water"]
        self.res_air = data["res_air"]
        self.x = data["x"]
        self.y = data["y"]
        self.cooldown = data["cooldown"]
        self.cooldown_expiration = datetime.fromisoformat(
            data["cooldown_expiration"].replace("Z", "+00:00")
        )
        self.weapon_slot = data["weapon_slot"]
        self.shield_slot = data["shield_slot"]
        self.helmet_slot = data["helmet_slot"]
        self.body_armor_slot = data["body_armor_slot"]
        self.leg_armor_slot = data["leg_armor_slot"]
        self.boots_slot = data["boots_slot"]
        self.ring1_slot = data["ring1_slot"]
        self.ring2_slot = data["ring2_slot"]
        self.amulet_slot = data["amulet_slot"]
        self.artifact1_slot = data["artifact1_slot"]
        self.artifact2_slot = data["artifact2_slot"]
        self.artifact3_slot = data["artifact3_slot"]
        self.consumable1_slot = data["consumable1_slot"]
        self.consumable1_slot_quantity = data["consumable1_slot_quantity"]
        self.consumable2_slot = data["consumable2_slot"]
        self.consumable2_slot_quantity = data["consumable2_slot_quantity"]
        self.task = data["task"]
        self.task_type = data["task_type"]
        self.task_progress = data["task_progress"]
        self.task_total = data["task_total"]
        self.inventory_max_items = data["inventory_max_items"]
        self.inventory = data["inventory"]
        self.inventory_slots = [
            {
                "slot": i + 1,
                "code": data.get(f"inventory_slot{i + 1}", ""),
                "quantity": data.get(f"inventory_slot{i + 1}_quantity", 0),
            }
            for i in range(20)
        ]

    def __repr__(self):
        return f"Character(name={self.name}, level={self.level}, hp={self.hp}, location=({self.x}, {self.y}))"

    def is_cooldown_active(self) -> str:
        current_time = datetime.now()
        cooldown_diff = (
            self.cooldown_expiration - current_time.astimezone()
        ).total_seconds()
        return cooldown_diff > 0
