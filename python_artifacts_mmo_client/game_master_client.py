from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests
from python_artifacts_mmo_client.utils.logger import create_logger
from python_artifacts_mmo_client.models.monster import Monster
from python_artifacts_mmo_client.models.resource import Resource
from python_artifacts_mmo_client.models.character import Character
from python_artifacts_mmo_client.models.map import Map
from logging import Logger

logger: Logger = create_logger("gm_client")


class GMClient:
    def __init__(
        self, artifacts_request_client: ArtifactsRequests = ArtifactsRequests()
    ) -> None:
        self.artifacts_requests: ArtifactsRequests = artifacts_request_client


    def get_resource(self, resource_name: str) -> dict[str, str | int]:
        response: dict[str, str | int] = self.artifacts_requests.get(f"/resources/{resource_name}")
        return Resource(response["data"])
    
    def get_monster(self, monster: str) -> Monster:
        response: dict[str, str | int] = self.artifacts_requests.get(f"/monsters/{monster}")
        return Monster(response["data"])
    
    def get_map(self, position_x: int, position_y: int) -> Map:
        response: dict[str, str | int] = self.artifacts_requests.get(f"/maps/{position_x}/{position_y}")
        return Map(response["data"])
    
    @staticmethod
    def is_character_higher_level_then_monster(character: Character, monster: Monster) -> bool:
        return character.level > monster.level
    

    
