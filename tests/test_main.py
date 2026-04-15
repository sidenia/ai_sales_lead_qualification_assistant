import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestMainApp:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_app_creation(self):
        assert app.title == "Sales Assistant API"
        assert app.description == "AI-powered sales assistant with simple RAG and lead scoring"
        assert app.version == "1.0.0"

    def test_health_check_at_root(self, client):
        response = client.get("/health-check")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}