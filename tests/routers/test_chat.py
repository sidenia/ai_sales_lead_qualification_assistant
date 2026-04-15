import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app


class TestChatRouter:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @patch("app.routers.chat.chat_service")
    def test_chat_endpoint_success(self, mock_service, client):
        from app.models.chat import ChatResponse
        mock_response = ChatResponse(
            response="Test response",
            score=0.5,
            lead_category="warm",
            call_to_action="Send email",
            source="llm"
        )
        mock_service.process_chat_request = AsyncMock(return_value=mock_response)

        response = client.post("/chat", json={"user_id": "user123", "message": "Hello"})

        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Test response"
        assert data["score"] == 0.5
        assert data["lead_category"] == "warm"
        assert data["call_to_action"] == "Send email"
        assert data["source"] == "llm"
        assert data["source"] == "llm"

    @patch("app.routers.chat.chat_service")
    def test_chat_endpoint_exception(self, mock_service, client):
        mock_service.process_chat_request = AsyncMock(side_effect=Exception("Test error"))

        response = client.post("/chat", json={"user_id": "user123", "message": "Hello"})

        assert response.status_code == 500
        data = response.json()
        assert "Internal server error" in data["detail"]

    def test_health_check_endpoint(self, client):
        response = client.get("/health-check")

        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "healthy"}

    def test_health_check_root_endpoint(self, client):
        response = client.get("/health-check")

        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "healthy"}