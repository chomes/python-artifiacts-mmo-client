from credentials import bearer_token
import requests
from python_artifacts_mmo_client.utils.logger import create_logger
from logging import Logger

logger: Logger = create_logger("artifacts_requests")

BEARER_TOKEN: str = bearer_token["bearer_auth"]
API_ENDPOINT: str = "https://api.artifactsmmo.com"
HEADERS: dict[str, str] = {
    "Accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}


class ArtifactsRequests:
    def __init__(self, requests_module: requests = requests) -> None:
        self.requests_module: requests = requests_module

    def get(self, endpoint: str) -> dict[str, str]:

        response: requests.Response = self.requests_module.get(
            f"{API_ENDPOINT}{endpoint}", headers=HEADERS
        )
        logger.debug(f"Response from GET request {response.json()}")
        return response.json()

    def post(self, endpoint: str, data: dict[str, str]) -> dict[str, str]:
        response: requests.Response = self.requests_module.post(
            f"{API_ENDPOINT}{endpoint}", headers=HEADERS, json=data
        )
        logger.debug(f"Response from POST request {response.json()}")
        return response.json()
