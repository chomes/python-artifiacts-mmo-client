from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests
from python_artifacts_mmo_client.models.character import Character
from python_artifacts_mmo_client.models.fight import Fight
from python_artifacts_mmo_client.utils.logger import create_logger
from logging import Logger


class InvalidCharacterError(Exception):
    def __init__(self, character: str) -> None:
        super().__init__(
            f"You tried to get character {character} but it doesn't exist, please try again"
        )


class CooldownActiveError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "The cooldown is still active on this character, please try again later"
        )


class InvalidMovementError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "The position you specified is exactly where you, we can't make this request"
        )


class ItemEquipError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to equip item to character due to error")


class AttackMonsterError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to attack the monster due to an error")


logger: Logger = create_logger("character_client")


class CharacterClient:
    def __init__(
        self, artifacts_requests: ArtifactsRequests = ArtifactsRequests()
    ) -> None:
        self.artifacts_requests: ArtifactsRequests = artifacts_requests
        self.character: Character | None = None

    def get_character(self, name: str) -> None:
        response: dict[str, str] = self.artifacts_requests.get(f"/characters/{name}")
        if "error" in response:
            logger.error(f"{name} is not a valid character, try again")
            raise InvalidCharacterError(Character)
        else:
            logger.info("Found character, populating character data")
            self.character = Character(response["data"])

    def is_valid_move(self, position_x, position_y) -> bool:
        old_position: tuple[int, int] = self.character.x, self.character.y
        if old_position == (position_x, position_y):
            raise InvalidMovementError()

    def error_handler(
        self, response: dict[str, str], exception_handler: Exception
    ) -> None:
        if "error" in response:
            logger.error(
                f"Failed to do action due to error {response['error']['message']}"
            )
            raise exception_handler()

    def get_current_location(self) -> None:
        logger.info(
            f"{self.character.name} is at {self.character.x}, {self.character.y}"
        )

    def validate_cooldown_completed(self) -> None:
        if self.character.is_cooldown_active():
            logger.error(
                f"The cooldown period is not ready yet, please wait, the expire time for the cooldown is {self.character.cooldown_expiration.ctime()}"
            )
            raise CooldownActiveError()

    def __change_direction(self, direction: str) -> tuple[int, int]:
        directions: dict[str, int] = {"UP": -1, "DOWN": 1, "LEFT": -1, "RIGHT": 1}
        position_x: int = (
            self.character.x + directions.get(direction, 0)
            if direction in ("LEFT", "RIGHT")
            else self.character.x
        )
        position_y: int = (
            self.character.y + directions.get(direction, 0)
            if direction in ("UP", "DOWN")
            else self.character.y
        )
        return (position_x, position_y)

    def move_character(
        self, new_position: tuple[int, int] | None = None, direction: str | None = None
    ) -> None:
        self.validate_cooldown_completed()
        if direction:
            logger.info(
                f"User is choosing to move via direction, this will move to {direction}"
            )

            position: tuple[int, int] = self.__change_direction(direction.upper())
        elif new_position:
            logger.info(
                f"User is choosing to move via position, this will be {new_position}"
            )
            position: tuple[int, int] = new_position
        else:
            logger.error(
                "You have provided neither a new position or a direction, please do this before trying again"
            )

        self.is_valid_move(position[0], position[1])
        movement: dict[str, int] = {"x": position[0], "y": position[1]}
        response = self.artifacts_requests.post(
            f"/my/{self.character.name}/action/move", data=movement
        )
        self.error_handler(response, InvalidMovementError)
        self.character = Character(response["data"]["character"])
        logger.info(
            f"You are now at position X: {response['data']['destination']['x']} Y {response['data']['destination']['y']}"
        )

    def equip_item(self, item: str, slot: str) -> None:
        self.validate_cooldown_completed()
        item_to_equip: dict[str, str] = {"code": item, "slot": slot}
        response = self.artifacts_requests.post(
            f"/my/{self.character.name}/action/equip", data=item_to_equip
        )
        self.error_handler(response, ItemEquipError)
        self.character = Character(response["data"]["character"])
        logger.info(
            f"Item {response['data']['item']['name']} was equipped onto {self.character.name}"
        )

    def attack_monster(self, monster: str) -> None:
        self.validate_cooldown_completed()
        logger.info(f"Attacking monster {monster}")
        response = self.artifacts_requests.post(
            f"/my/{self.character.name}/action/fight", data={}
        )
        self.error_handler(response, AttackMonsterError)
        fight_result: Fight = Fight(response["data"]["fight"])
        self.character = Character(response["data"]["character"])

        if fight_result.result == "win":
            logger.info(
                f"Character {self.character.name} has {fight_result.result} the fight"
            )
            logger.info(
                f"You have received {fight_result.gold} gold and the following drops {fight_result.drops}"
            )
        else:
            logger.info(
                f"Character {self.character.name} did not win the fight, here's the stats of what happened"
            )
            for log in fight_result.logs:
                logger.info(log)
