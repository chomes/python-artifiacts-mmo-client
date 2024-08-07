from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests
from python_artifacts_mmo_client.utils.logger import create_logger
from python_artifacts_mmo_client.models.monster import Monster
from logging import Logger

logger: Logger = create_logger("gm_client")


class GMClient:
    def __init__(
        self, artifacts_request_client: ArtifactsRequests = ArtifactsRequests()
    ) -> None:
        self.artifacts_requests: ArtifactsRequests = artifacts_request_client
        self.monster: Monster | None = None
