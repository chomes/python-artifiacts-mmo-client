from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests
from python_artifacts_mmo_client.models.character import Character
from python_artifacts_mmo_client.models.fight import Fight
from python_artifacts_mmo_client.utils.logger import create_logger
from logging import Logger


class NoCharactersExistError(Exception):
    def __init__(self) -> None:
        super().__init__("No characters currently exist for your account, create one!")


class CreateCharacterError(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Failed to create character due to error, see logs for details"
        )


class InvalidCharacterError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "You tried to get a character but it doesn't exist, please try again"
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

    def __error_handler(
        self, response: dict[str, str], exception_handler: Exception
    ) -> None:
        """Error handler for the class, takes in the response and checks if the dict
        has error as a key, if it does, logs the error message to explain why the
        request failed

        Args:
            response (dict[str, str]): {"error": {"message": "Bad request"}}
            exception_handler (Exception): Pass in an exception class to be raised,
            exception classes shouldn't take in an argument for this to work
        Raises:
            exception_handler: This depends on the error being handled
        """
        if "error" in response:
            logger.error(
                f"Failed to do action due to error {response['error']['message']}"
            )
            raise exception_handler()

    def get_characters(self) -> list[Character]:
        """Gets a list of characters the user owns to the allow them to choose to
        play one

        Returns:
            list[Character]: [Character<Dummy>, Character<Nageto>]
        """
        response: dict[list[dict[str, str | int]]] = self.artifacts_requests.get(
            "/characters/"
        )
        self.__error_handler(response, NoCharactersExistError)
        characters: list[Character] = [
            Character(character_data) for character_data in response["data"]
        ]
        logger.debug(f"Here are your characters {characters}")
        return characters

    def get_character(self, name: str) -> None:
        """Gets a single character you have chosen to play

        Args:
            name (str): Nageto
        """
        response: dict[str, str] = self.artifacts_requests.get(f"/characters/{name}")
        self.__error_handler(response, InvalidCharacterError)
        logger.info("Found character, populating character data")
        self.character = Character(response["data"])

    def create_character(self, name: str, skin: str) -> Character:
        """Creates a new character into your account, you must provide
        a name and a skin type (info below).  This method will error out
        if you provide an unsupported skin type.

        Args:
            name (str): Nageto
            skin (str): Either ("men1", "men2", "men3", "women1", "women2", "women3")

        Raises:
            CreateCharacterError: Raised when you choose a wrong skin type

        Returns:
            Character: Character<Nageto>
        """
        skin_types: tuple[str] = ("men1", "men2", "men3", "women1", "women2", "women3")
        if skin.lower() not in skin_types:
            logger.error(
                f"Failed to create character due to wrong skin type, please choose from {skin_types}"
            )
            raise CreateCharacterError()
        response: dict[str, str | int] = self.artifacts_requests.post(
            "/characters/create", data={"name": name, "skin": skin.lower()}
        )
        self.__error_handler(response, CreateCharacterError)
        logger.debug(f"Here's the response from creating a character {response}")
        return Character(response["data"])

    def __is_valid_move(self, position_x: int, position_y: int) -> None:
        """Checks if the place you want to move to is the same place
        you currently are, errors out if it is.

        Args:
            position_x (int): 2
            position_y (int): 1

        Raises:
            InvalidMovementError: Raised when both positions equal the same
        """
        old_position: tuple[int, int] = self.character.x, self.character.y
        if old_position == (position_x, position_y):
            raise InvalidMovementError()

    def get_current_location(self) -> None:
        """Logs the current location to the user to see"""
        logger.info(
            f"{self.character.name} is at {self.character.x}, {self.character.y}"
        )

    def __validate_cooldown_completed(self) -> None:
        """Checks if the cooldown of movement/action is completed, if not it will raise an error

        Raises:
            CooldownActiveError: Raised when cooldown is still active.
        """
        if self.character.is_cooldown_active():
            logger.error(
                f"The cooldown period is not ready yet, please wait, the expire time for the cooldown is {self.character.cooldown_expiration.ctime()}"
            )
            raise CooldownActiveError()

    def __change_direction(self, direction: str) -> tuple[int, int]:
        """Creates a tuple of position to move your character to based on
        you choosing to move in a direction.

        Args:
            direction (str): Either ("UP", "DOWN", "LEFT", "RIGHT")

        Returns:
            tuple[int, int]: _description_
        """
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
        """Moves the character based on two choices, the user can either provide a direction
        to move the character (see __change_direction for details).  Or they can provide
        an absolute position which will be a tuple of 2 integers representing x and y.

        The request then gets sent to move the character and updates the Character class on
        the client with the new position and cooldown activity.

        Args:
            new_position (tuple[int, int] | None, optional): (1, 3). Defaults to None.
            direction (str | None, optional): Either ("UP", "DOWN", "LEFT", "RIGHT"). Defaults to None.

        Raises:
            ValueError: Raised when neither new_psotion or direction are chosen by the user.
        """
        self.__validate_cooldown_completed()
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
            raise ValueError("No arguments passed in")

        self.__is_valid_move(position[0], position[1])
        movement: dict[str, int] = {"x": position[0], "y": position[1]}
        response = self.artifacts_requests.post(
            f"/my/{self.character.name}/action/move", data=movement
        )
        self.__error_handler(response, InvalidMovementError)
        self.character = Character(response["data"]["character"])
        logger.info(
            f"You are now at position X: {response['data']['destination']['x']} Y {response['data']['destination']['y']}"
        )

    def __is_valid_item_slot(self, item_slot: str) -> None:
        """For use with equip item, checks if the item the user
        wants to equip is a valid item slot, if it is no error
        will occur, or exception is raised

        Args:
            item_slot (str): "weapon"

        Raises:
            ValueError: Raised when user provides a bad item_slot to choose
            from.
        """
        slots: tuple[str] = (
            "weapon",
            "shield",
            "helmet",
            "body_armour",
            "leg_armour",
            "boots",
            "ring1",
            "ring2",
            "amulet",
            "artifact1",
            "artifact2",
            "artifact3",
            "consumable1",
            "consumable2",
        )
        if item_slot.lower() in slots:
            pass
        else:
            raise ValueError("Not a valid item slot")

    def equip_item(self, item: str, slot: str) -> None:
        """Equips an item onto the user, the developer
        must provide an item and a slot to associate it with.

        Args:
            item (str): "Sword of a thousand truths"
            slot (str): "weapon"
        """
        self.__validate_cooldown_completed()
        self.__is_valid_item_slot(slot)
        item_to_equip: dict[str, str] = {"code": item, "slot": slot}
        response = self.artifacts_requests.post(
            f"/my/{self.character.name}/action/equip", data=item_to_equip
        )
        self.__error_handler(response, ItemEquipError)
        self.character = Character(response["data"]["character"])
        logger.info(
            f"Item {response['data']['item']['name']} was equipped onto {self.character.name}"
        )

    def attack_monster(self, monster: str) -> None:
        """Attacks a monster that is in the position where the Character is
        the user will either succeed or fail in attacking the monster.

        Logs will be output if the user fails to beat the monster, otherwise
        the user will be told the gold, equip, and xp they earned during the
        fight.

        Args:
            monster (str): "Diablo"
        """
        self.__validate_cooldown_completed()
        logger.info(f"Attacking monster {monster}")
        response = self.artifacts_requests.post(
            f"/my/{self.character.name}/action/fight", data={}
        )
        self.__error_handler(response, AttackMonsterError)
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
