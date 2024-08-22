from python_artifacts_mmo_client.artifacts_requests import ArtifactsRequests


class MockResponse:
    @staticmethod
    def json() -> dict[str, str]:
        return {"data": {"name": "Dummy Character"}}


class MockRequests:
    @staticmethod
    def get(url: str, headers: dict[str, str]) -> MockResponse:
        return MockResponse()

    @staticmethod
    def post(
        url: str,
        json: dict[str, str],
        headers: dict[str, str],
    ) -> MockResponse:
        return MockResponse()


def test_get() -> None:
    # Arrange
    artifacts_request: ArtifactsRequests = ArtifactsRequests(MockRequests())

    # Act
    response: dict[str, str] = artifacts_request.get("/dummy/endpoint")

    # Assert
    assert response == {"data": {"name": "Dummy Character"}}


def test_post() -> None:
    # Arrange
    artifacts_request: ArtifactsRequests = ArtifactsRequests(MockRequests())
    dummy_data: dict[str, str] = {"character": "attack"}

    # Act
    response: dict[str, str] = artifacts_request.post("/dummy/endpoint", dummy_data)

    # Assert
    assert response == {"data": {"name": "Dummy Character"}}
