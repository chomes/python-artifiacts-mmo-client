from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests
from python_artifacts_mmo_client.models.character import Character
from python_artifacts_mmo_client.utils.logger import create_logger
from logging import Logger

class InvalidCharacterError(Exception):
    def __init__(self, character: str) -> None:
        super().__init__(f"You tried to get character {character} but it doesn't exist, please try again")

class InvalidMovementError(Exception):
    def __init__(self) -> None:
        super().__init__("The position you specified is exactly where you, we can't make this request")

logger: Logger = create_logger("character_client")

class CharacterClient:
    def __init__(self, artifacts_requests: ArtifactsRequests = ArtifactsRequests()) -> None:
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
    
    def get_current_location(self) -> None:
        logger.info(f"{self.character.name} is at {self.character.x}, {self.character.y}")

    def change_direction(self, direction: str) -> tuple[int, int]:
        directions: dict[str, int] = {"UP": -1, "DOWN": 1, "LEFT": -1, "RIGHT": 1}
        position_x: int = self.character.x + directions.get(direction, 0) if direction in ("LEFT", "RIGHT") else self.character.x
        position_y: int = self.character.y + directions.get(direction, 0) if direction in ("UP", "DOWN") else self.character.y
        return (position_x, position_y)
    
    def move_character(self, new_position: tuple[int, int] | None=None, direction: str | None=None) -> None:
        if direction:
            logger.info(f"User is choosing to move via direction, this will move to {direction}")

            position: tuple[int, int] = self.change_direction(direction.upper())
        else:
            logger.info(f"User is choosing to move via position, this will be {new_position}")
            position: tuple[int, int] = new_position
        
        self.is_valid_move(position[0], position[1])
        movement: dict[str, int] = {"x": position[0], "y": position[1]}
        response = self.artifacts_requests.post(f"/my/{self.character.name}/action/move", data=movement)
        if "error" in response:
            logger.error(f"Failed to make movement due to error {response['error']['message']}")
            raise InvalidMovementError()
        else:
            self.character = Character(response["data"]["character"])
            logger.info(f"You are now at position X: {response['data']['destination']['x']} Y {response['data']['destination']['y']}")


