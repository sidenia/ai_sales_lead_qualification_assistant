import pytest
from unittest.mock import AsyncMock, patch

from app.services.llm import LLMService, llm_service


class TestLLMService:
    @pytest.fixture
    def llm_service_instance(self):
        return LLMService()

    @patch("app.services.llm.async_openai_client")
    async def test_generate_response_success(self, mock_client, llm_service_instance):
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await llm_service_instance.generate_response("Hello", "Context info")
        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch("app.services.llm.async_openai_client")
    async def test_generate_response_empty_context(self, mock_client, llm_service_instance):
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await llm_service_instance.generate_response("Hello", "")
        assert result == "Test response"

        call_args = mock_client.chat.completions.create.call_args
        system_prompt = call_args[1]["messages"][0]["content"]
        assert "No relevant information available" in system_prompt

    @patch("app.services.llm.async_openai_client")
    async def test_generate_response_whitespace_context(self, mock_client, llm_service_instance):
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await llm_service_instance.generate_response("Hello", "   ")
        assert result == "Test response"

        call_args = mock_client.chat.completions.create.call_args
        system_prompt = call_args[1]["messages"][0]["content"]
        assert "No relevant information available" in system_prompt

    @patch("app.services.llm.async_openai_client")
    async def test_generate_response_with_context(self, mock_client, llm_service_instance):
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await llm_service_instance.generate_response("Hello", "Plan info")
        assert result == "Test response"

        call_args = mock_client.chat.completions.create.call_args
        system_prompt = call_args[1]["messages"][0]["content"]
        assert "Plan info" in system_prompt
        assert "Hello" in system_prompt

    @patch("app.services.llm.async_openai_client")
    async def test_generate_response_strips_whitespace(self, mock_client, llm_service_instance):
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "  Test response  "
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        result = await llm_service_instance.generate_response("Hello", "Context")
        assert result == "Test response"


class TestGlobalLLMService:
    def test_global_llm_service_instance(self):
        assert isinstance(llm_service, LLMService)