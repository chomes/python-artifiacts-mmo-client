from python_artifacts_mmo_client.character_client import (
    CharacterClient,
    InvalidCharacterError,
    InvalidMovementError,
    CooldownActiveError,
    ItemEquipError,
    AttackMonsterError,
)
from python_artifacts_mmo_client.models.character import Character


import pytest
from dummy_data import character_data, movement_data
import datetime


class MockArtifactRequests:
    def __init__(
        self, test_state: str = "success", data_to_send: dict[str, str] = None
    ) -> None:
        self.test_state = test_state
        self.data = data_to_send

    def get(self, url) -> dict[str, str | int]:
        if self.test_state != "success":
            return {"error": {"message": "bad option"}}
        else:
            return self.data if self.data else {"data": {"name": "fake name"}}

    def post(self, url, data) -> dict[str, str | int]:
        if self.test_state == "post_failure":
            return {"error": {"message": "bad option"}}
        else:
            return self.data if self.data else {"data": {"name": "fake name"}}


def test_getting_character() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)

    # Act
    character_client.get_character("Dummy character")

    # Assert
    assert character_client.character.skin == "men1"


def test_failing_to_get_character() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="invalid_character", data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)

    # Act & Assert
    with pytest.raises(InvalidCharacterError):
        character_client.get_character("Dummy character")


def test_checking_valid_move() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.get_character("Dummy Character")

    # Act
    response: None = character_client._CharacterClient__is_valid_move(1, 2)

    # Assert
    assert not response


def test_failing_to_check_valid_move() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.get_character("Dummy Character")

    # Act & Assert
    with pytest.raises(InvalidMovementError):
        character_client._CharacterClient__is_valid_move(0, 0)


def test_error_handler() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    bad_response: dict[str, str] = {"error": {"message": "Ya dun goofed kid"}}

    # Act & Assert
    with pytest.raises(InvalidMovementError):
        character_client._CharacterClient__error_handler(
            bad_response, InvalidMovementError
        )


def test_cooldown_is_not_active() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.get_character("Dummy Character")

    # Act
    response: None = character_client._CharacterClient__validate_cooldown_completed()

    # Assert
    assert not response


def test_cooldown_is_active() -> None:  # Arrange
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.get_character("Dummy Character")
    current_time = datetime.datetime.now()
    future_time = current_time + datetime.timedelta(days=2)
    future_time = future_time.astimezone(datetime.timezone.utc)
    character_client.character.cooldown_expiration = future_time

    # Act & Assert
    with pytest.raises(CooldownActiveError):
        response: None = (
            character_client._CharacterClient__validate_cooldown_completed()
        )


@pytest.mark.parametrize(
    "direction, positions",
    [
        ("UP", (0, -1)),
        ("DOWN", (0, 1)),
        ("LEFT", (-1, 0)),
        ("RIGHT", (1, 0)),
        ("NOWHERE", (0, 0)),
    ],
)
def test_setting_character_direction(direction, positions) -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=character_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.get_character("Dummy Character")

    # Act
    movement: tuple[int] = character_client._CharacterClient__change_direction(
        direction
    )

    # Assert
    assert movement == positions


@pytest.mark.parametrize(
    "movement_type, movement", [("direction", "UP"), ("position", (1, 1))]
)
def test_moving_character(movement_type, movement) -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])

    # Act
    if movement_type == "direction":
        response: None = character_client.move_character(direction=movement)
    elif movement_type == "position":
        response: None = character_client.move_character(new_position=movement)

    # Assert
    assert not response


def test_failing_to_move_due_to_no_data() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])
    # Act & Assert
    with pytest.raises(ValueError):
        character_client.move_character()


def test_failing_to_move_due_to_invalid_move() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])
    # Act & Assert
    with pytest.raises(InvalidMovementError):
        character_client.move_character(new_position=(0, 0))


def test_failing_to_move_due_to_post_failure() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data, test_state="post_failure"
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])

    # Act & Assert
    with pytest.raises(InvalidMovementError):
        character_client.move_character(new_position=(2, 2))


def test_valid_item_slot() -> None:
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)

    # Act
    response: None = character_client._CharacterClient__is_valid_item_slot("weapon")

    # Assert
    assert not response


def test_invalid_item_slot() -> None:
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)

    # Act & Assert
    with pytest.raises(ValueError):
        character_client._CharacterClient__is_valid_item_slot("fake")


def test_equipping_item() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])

    # Act
    response: None = character_client.equip_item("Sword", "weapon")

    # Assert
    assert not response


def test_failure_to_equip_item_due_to_error_in_request() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data, test_state="post_failure"
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])

    # Act & Assert
    with pytest.raises(ItemEquipError):
        character_client.equip_item("Sword", "weapon")


def test_attacking_monster() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])

    # Act
    response: None = character_client.attack_monster("Goliath")

    # Assert
    assert not response


def test_failing_to_attack_monster_due_to_error_in_request() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=movement_data, test_state="post_failure"
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)
    character_client.character = Character(movement_data["data"]["character"])

    # Act & Assert
    with pytest.raises(AttackMonsterError):
        character_client.attack_monster("Goliath")
