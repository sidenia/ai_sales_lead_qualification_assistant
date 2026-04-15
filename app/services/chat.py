from typing import Dict, Any

from app.models.chat import ChatRequest, ChatResponse
from app.repositories.rag import knowledge_repository
from app.services.cache import cache_service
from app.services.llm import llm_service
from app.services.lead_scoring import lead_scoring_service


class ChatService:

    async def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        cached_response = cache_service.get(request.message)
        if cached_response:
            return self._build_response(
                response=cached_response,
                message=request.message,
                source="cache"
            )

        context_data = knowledge_repository.search_context(request.message)
        context_text = knowledge_repository.build_context_text(context_data)

        response = await llm_service.generate_response(request.message, context_text)

        cache_service.set(request.message, response)

        return self._build_response(
            response=response,
            message=request.message,
            source="llm"
        )

    def _build_response(self, response: str, message: str, source: str) -> ChatResponse:
        score = lead_scoring_service.score_lead(message)
        category = lead_scoring_service.categorize_lead(score)
        call_to_action = lead_scoring_service.get_call_to_action(category)

        return ChatResponse(
            response=response,
            score=score,
            lead_category=category,
            call_to_action=call_to_action,
            source=source
        )


chat_service = ChatService() # global instance