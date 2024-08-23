from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests
from python_artifacts_mmo_client.utils.logger import create_logger
from python_artifacts_mmo_client.models.monster import Monster
from python_artifacts_mmo_client.models.resource import Resource
from python_artifacts_mmo_client.models.character import Character
from python_artifacts_mmo_client.models.map import Map
from logging import Logger

logger: Logger = create_logger("gm_client")


class GetResourceError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get resource due to error, see logs for more details")


class GetMonsterError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Failed to get monster details due to error, see logs for more details"
        )


class GetMapError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Failed to get map due to error, see logs for more details"
        )


class GetEventsError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get events due to error, see logs for more details")


class GMClient:
    def __init__(
        self, artifacts_request_client: ArtifactsRequests = ArtifactsRequests()
    ) -> None:
        self.artifacts_requests: ArtifactsRequests = artifacts_request_client

    def __error_handler(
        self, response: dict[str, str], exception_handler: Exception
    ) -> None:
        if "error" in response:
            logger.error(
                f"Failed to do action due to error {response['error']['message']}"
            )
            raise exception_handler()

    def get_resource(self, resource_name: str) -> dict[str, str | int]:
        response: dict[str, str | int] = self.artifacts_requests.get(
            f"/resources/{resource_name}"
        )
        self.__error_handler(response, GetResourceError)
        return Resource(response["data"])

    def get_monster(self, monster: str) -> Monster:
        response: dict[str, str | int] = self.artifacts_requests.get(
            f"/monsters/{monster}"
        )
        self.__error_handler(response, GetMonsterError)
        return Monster(response["data"])

    def get_map(self, position_x: int, position_y: int) -> Map:
        response: dict[str, str | int] = self.artifacts_requests.get(
            f"/maps/{position_x}/{position_y}"
        )
        self.__error_handler(response, GetMapError)
        return Map(response["data"])

    def get_events(self) -> list[dict[str, str | int]]:
        response: dict[str, list[dict[str, str | int]]] = self.artifacts_requests.get(
            "/events/"
        )
        self.__error_handler(response, GetEventsError)
        return response["data"]

    @staticmethod
    def is_character_higher_level_then_monster(
        character: Character, monster: Monster
    ) -> bool:
        return character.level > monster.level
