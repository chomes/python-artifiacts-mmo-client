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
        super().__init__(
            "Failed to get resource due to error, see logs for more details"
        )


class GetMonsterError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Failed to get monster details due to error, see logs for more details"
        )


class GetMapError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to get map due to error, see logs for more details")


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

    def get_server_status(self) -> dict[str, str | int]:
        """Checks the status of the server

        Returns:
            dict[str, str | int]: {"data": "status": "online"}
        """
        response: dict[str, str | int] = self.artifacts_requests.get("/")
        logger.debug(f"Server status details {response}")
        return response["data"]

    def get_resource(self, resource_name: str) -> Resource:
        """Get a resource the user wants to have

        Args:
            resource_name (str): "iron_ore"

        Returns:
            Resource: Object containing resource
        """
        response: dict[str, str | int] = self.artifacts_requests.get(
            f"/resources/{resource_name}"
        )
        self.__error_handler(response, GetResourceError)
        return Resource(response["data"])

    def get_monster(self, monster: str) -> Monster:
        """Get the characteristics of a monster

        Args:
            monster (str): "Diablo"

        Returns:
            Monster: Monster<Diablo>
        """
        response: dict[str, str | int] = self.artifacts_requests.get(
            f"/monsters/{monster}"
        )
        self.__error_handler(response, GetMonsterError)
        return Monster(response["data"])

    def get_map(self, position_x: int, position_y: int) -> Map:
        """Get information about the current map position

        Args:
            position_x (int): 1
            position_y (int): 2

        Returns:
            Map: Map<1, 2>
        """
        response: dict[str, str | int] = self.artifacts_requests.get(
            f"/maps/{position_x}/{position_y}"
        )
        self.__error_handler(response, GetMapError)
        return Map(response["data"])

    def get_events(self) -> list[dict[str, str | int]]:
        """Events are what your character has done (mining, attacking, farming, etc).
        This gets the events of what your character has done to date.

        Returns:
            list[dict[str, str | int]]: {"data": {"name": "monster"}}
        """
        response: dict[str, list[dict[str, str | int]]] = self.artifacts_requests.get(
            "/events/"
        )
        self.__error_handler(response, GetEventsError)
        return response["data"]

    @staticmethod
    def is_character_higher_level_then_monster(
        character: Character, monster: Monster
    ) -> bool:
        """Recommended to use before attacking a monster in CC
        Checks if the monster is higher level then your character

        Args:
            character (Character): Character<Negato>
            monster (Monster): Monster<Diablo>

        Returns:
            bool: True/False
        """
        return character.level > monster.level
