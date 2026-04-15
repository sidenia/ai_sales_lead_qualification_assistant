import pytest
from unittest.mock import AsyncMock, patch

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService, chat_service


class TestChatService:
    @pytest.fixture
    def chat_service_instance(self):
        return ChatService()

    @patch("app.services.chat.cache_service")
    @patch("app.services.chat.lead_scoring_service")
    async def test_process_chat_request_cached(self, mock_scoring, mock_cache, chat_service_instance):
        mock_cache.get.return_value = "Cached response"
        mock_scoring.score_lead.return_value = 0.5
        mock_scoring.categorize_lead.return_value = "warm"
        mock_scoring.get_call_to_action.return_value = "Send follow-up email"

        request = ChatRequest(user_id="user123", message="Hello")
        response = await chat_service_instance.process_chat_request(request)

        assert response.response == "Cached response"
        assert response.score == 0.5
        assert response.lead_category == "warm"
        assert response.call_to_action == "Send follow-up email"
        assert response.source == "cache"
        mock_cache.get.assert_called_once_with("Hello")

    @patch("app.services.chat.cache_service")
    @patch("app.services.chat.knowledge_repository")
    @patch("app.services.chat.llm_service")
    @patch("app.services.chat.lead_scoring_service")
    async def test_process_chat_request_llm(self, mock_scoring, mock_llm, mock_repo, mock_cache, chat_service_instance):
        mock_cache.get.return_value = None
        mock_repo.search_context.return_value = {"type": "plan", "name": "basic"}
        mock_repo.build_context_text.return_value = "Context text"
        mock_llm.generate_response = AsyncMock(return_value="LLM response")
        mock_scoring.score_lead.return_value = 0.8
        mock_scoring.categorize_lead.return_value = "hot"
        mock_scoring.get_call_to_action.return_value = "Schedule demo"

        request = ChatRequest(user_id="user123", message="Tell me about basic plan")
        response = await chat_service_instance.process_chat_request(request)

        assert response.response == "LLM response"
        assert response.score == 0.8
        assert response.lead_category == "hot"
        assert response.call_to_action == "Schedule demo"
        assert response.source == "llm"
        mock_cache.get.assert_called_once_with("Tell me about basic plan")
        mock_repo.search_context.assert_called_once_with("Tell me about basic plan")
        mock_repo.build_context_text.assert_called_once_with({"type": "plan", "name": "basic"})
        mock_llm.generate_response.assert_called_once_with("Tell me about basic plan", "Context text")
        mock_cache.set.assert_called_once_with("Tell me about basic plan", "LLM response")

    @patch("app.services.chat.cache_service")
    @patch("app.services.chat.knowledge_repository")
    @patch("app.services.chat.llm_service")
    @patch("app.services.chat.lead_scoring_service")
    async def test_process_chat_request_no_context(self, mock_scoring, mock_llm, mock_repo, mock_cache, chat_service_instance):
        mock_cache.get.return_value = None
        mock_repo.search_context.return_value = None
        mock_repo.build_context_text.return_value = "No relevant information found."
        mock_llm.generate_response = AsyncMock(return_value="General response")
        mock_scoring.score_lead.return_value = 0.2
        mock_scoring.categorize_lead.return_value = "cold"
        mock_scoring.get_call_to_action.return_value = "Add to nurture"

        request = ChatRequest(user_id="user123", message="Random question")
        response = await chat_service_instance.process_chat_request(request)

        assert response.response == "General response"
        assert response.score == 0.2
        assert response.lead_category == "cold"
        assert response.call_to_action == "Add to nurture"
        assert response.source == "llm"
        mock_repo.build_context_text.assert_called_once_with(None)

    def test_build_response(self, chat_service_instance):
        with patch("app.services.chat.lead_scoring_service") as mock_scoring:
            mock_scoring.score_lead.return_value = 0.6
            mock_scoring.categorize_lead.return_value = "warm"
            mock_scoring.get_call_to_action.return_value = "Send email"

            response = chat_service_instance._build_response("Test response", "Test message", "llm")

            assert response.response == "Test response"
            assert response.score == 0.6
            assert response.lead_category == "warm"
            assert response.call_to_action == "Send email"
            assert response.source == "llm"


class TestGlobalChatService:
    def test_global_chat_service_instance(self):
        assert isinstance(chat_service, ChatService)