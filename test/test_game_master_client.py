from python_artifacts_mmo_client.game_master_client import (
    GetResourceError,
    GetMapError,
    GetMonsterError,
    GetEventsError,
    GMClient,
)
from python_artifacts_mmo_client.models.map import Map
from python_artifacts_mmo_client.models.monster import Monster
from python_artifacts_mmo_client.models.resource import Resource
from python_artifacts_mmo_client.models.character import Character

from dummy_data import (
    resource_data,
    monster_data,
    map_data,
    character_data,
    events_data,
)

import pytest


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


def test_getting_resource() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=resource_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act
    response: Resource = gm_client.get_resource("dummy resource")

    # Assert
    assert isinstance(response, Resource)
    assert response.gold == 0


def test_failing_to_get_resource() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="failure", data_to_send=resource_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act & Assert
    with pytest.raises(GetResourceError):
        gm_client.get_resource("dummy resource")


def test_getting_monster() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=monster_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act
    response: Monster = gm_client.get_monster("Dummy monster")

    # Assert
    assert isinstance(response, Monster)
    assert response.attack_air == 0


def test_failing_to_get_monster() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="failure", data_to_send=monster_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act & Assert
    with pytest.raises(GetMonsterError):
        gm_client.get_monster("dummy monster")


def test_getting_map() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=map_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act
    response: Map = gm_client.get_map(1, 2)

    # Assert
    assert isinstance(response, Map)
    assert response.name == "candy_land"


def test_failing_to_get_map() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="failure", data_to_send=map_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act & Assert
    with pytest.raises(GetMapError):
        gm_client.get_map(1, 2)


def test_getting_events() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        data_to_send=events_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)
    response_output = events_data["data"]

    # Act
    response: list[dict[str, str | int]] = gm_client.get_events()

    # Assert
    assert response == response_output


def test_failing_to_get_map() -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="failure", data_to_send=events_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)

    # Act & Assert
    with pytest.raises(GetEventsError):
        gm_client.get_events()


@pytest.mark.parametrize(
    "character_level, monster_level, response_bool", [(1, 2, False), (2, 1, True)]
)
def test_if_character_higher_than_monster(
    character_level, monster_level, response_bool
) -> None:
    # Arrange
    mock_artifact_requests: MockArtifactRequests = MockArtifactRequests(
        test_state="failure", data_to_send=map_data
    )
    gm_client: GMClient = GMClient(mock_artifact_requests)
    character: Character = Character(character_data["data"])
    monster: Monster = Monster(monster_data["data"])
    character.level = character_level
    monster.level = monster_level

    # Act
    response: bool = gm_client.is_character_higher_level_then_monster(
        character, monster
    )

    # Assert
    assert response == response_bool
