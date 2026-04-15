import pytest
from app.models.chat import ChatRequest, ChatResponse


class TestChatRequest:
    def test_chat_request_creation(self):
        request = ChatRequest(user_id="user123", message="Hello")
        assert request.user_id == "user123"
        assert request.message == "Hello"


class TestChatResponse:
    def test_chat_response_creation(self):
        response = ChatResponse(
            response="Hi there",
            score=0.5,
            lead_category="warm",
            call_to_action="Send follow-up email",
            source="llm"
        )
        assert response.response == "Hi there"
        assert response.score == 0.5
        assert response.lead_category == "warm"
        assert response.call_to_action == "Send follow-up email"
        assert response.source == "llm"