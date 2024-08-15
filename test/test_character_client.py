from python_artifacts_mmo_client.character_client import (
    CharacterClient,
    InvalidCharacterError,
    InvalidMovementError,
    CooldownActiveError,
    ItemEquipError,
    AttackMonsterError
)

import pytest
from dummy_data import character_data

class MockArtifactRequests:
    def __init__(self, test_state: str = "success", data_to_send: dict[str, str] = None) -> None:
        self.test_state = test_state
        self.data = data_to_send
        self.error_type: dict[str, Exception] = {
            "invalid_character": InvalidCharacterError,
            "invalid_movement": InvalidMovementError,
            "cooldown_active": CooldownActiveError,
            "item_equip": ItemEquipError,
            "attack_monster": AttackMonsterError

        }
    
    def get(self, url) -> dict[str, str | int]:
        if self.test_state != "success":
            raise self.error_type[self.test_state]()
        else:
            return self.data if self.data else {"data": {"name": "fake name"}}
    
    def post(self, url, data) -> dict[str, str | int]:
        if self.test_state != "success":
            raise self.error_type[self.test_state]()
        else:
            return self.data if self.data else {"data": {"name": "fake name"}}


def test_getting_character() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(data_to_send=character_data)
    character_client: CharacterClient = CharacterClient(artifacts_requests)

    # Act
    character_client.get_character("Dummy character")

    # Assert
    assert character_client.character.skin == "men1"

def test_failing_to_get_character() -> None:
    # Arrange
    artifacts_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="invalid_character"
    )
    character_client: CharacterClient = CharacterClient(artifacts_requests)

    # Act & Assert
    with pytest.raises(InvalidCharacterError):
        character_client.get_character("Dummy character")
