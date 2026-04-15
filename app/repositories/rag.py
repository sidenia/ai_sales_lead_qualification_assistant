import json
from pathlib import Path
from typing import Dict, Optional, Any

from app.core.config import settings


class KnowledgeRepository:

    def __init__(self):
        self.knowledge_file = None
        self._data: Optional[Dict[str, Any]] = None

    def _get_knowledge_file(self) -> Path:
        if self.knowledge_file is None:
            if settings is None:
                # During testing, use a default path
                self.knowledge_file = Path(__file__).parent.parent / "data" / "knowledge.json"
            else:
                self.knowledge_file = settings.knowledge_file_path
        return self.knowledge_file

    def _load_data(self) -> Dict[str, Any]:
        if self._data is None:
            with open(self._get_knowledge_file(), "r", encoding="utf-8") as f:
                self._data = json.load(f)
        return self._data

    def search_context(self, message: str) -> Optional[Dict[str, Any]]:
        message = message.lower().replace('?', '')
        data = self._load_data()

        for plan in data.get("plans", []):
            if plan["name"].lower().replace('?', '') in message:
                return {
                    "type": "plan",
                    "name": plan["name"],
                    "description": plan.get("description"),
                    "price": plan.get("price")
                }

        for faq in data.get("faqs", []):
            if faq["question"].lower().replace('?', '') in message:
                return {
                    "type": "faq",
                    "question": faq["question"],
                    "answer": faq["answer"]
                }

        return None

    def build_context_text(self, context: Optional[Dict[str, Any]]) -> str:
        if not context:
            return "No relevant information found."

        if context["type"] == "plan":
            return f"""
                Plan Name: {context['name']}
                Price: {context['price']}
                Description: {context['description']}
                """
        elif context["type"] == "faq":
            return f"""
                FAQ Question: {context['question']}
                FAQ Answer: {context['answer']}
                """
        return "No relevant information found."


knowledge_repository = KnowledgeRepository() # global instance