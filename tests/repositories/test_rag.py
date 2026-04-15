import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from app.repositories.rag import KnowledgeRepository, knowledge_repository


class TestKnowledgeRepository:
    @pytest.fixture
    def sample_data(self):
        return {
            "plans": [
                {"name": "basic", "description": "Basic plan", "price": "R$49/month"},
                {"name": "pro", "description": "Pro plan", "price": "R$79/month"}
            ],
            "faqs": [
                {"question": "Can I cancel?", "answer": "Yes"},
                {"question": "Is there a trial?", "answer": "Yes"}
            ]
        }

    @pytest.fixture
    def repo(self, sample_data):
        repo = KnowledgeRepository()
        return repo

    def test_init(self, repo):
        assert repo._data is None
        assert repo.knowledge_file is None

    def test_load_data(self, repo, sample_data):
        with patch("app.repositories.rag.KnowledgeRepository._get_knowledge_file", return_value="dummy_path"):
            with patch("builtins.open", mock_open(read_data=json.dumps(sample_data))):
                data = repo._load_data()
                assert data == sample_data
                assert repo._data == sample_data

    def test_load_data_cached(self, repo, sample_data):
        with patch("app.repositories.rag.KnowledgeRepository._get_knowledge_file", return_value="dummy_path"):
            with patch("builtins.open", mock_open(read_data=json.dumps(sample_data))):
                repo._load_data()
                repo._data = {"cached": True}
                data = repo._load_data()
                assert data == {"cached": True}

    def test_search_context_plan_found(self, repo, sample_data):
        repo._data = sample_data
        context = repo.search_context("I want the basic plan")
        expected = {
            "type": "plan",
            "name": "basic",
            "description": "Basic plan",
            "price": "R$49/month"
        }
        assert context == expected

    def test_search_context_faq_found(self, repo, sample_data):
        repo._data = sample_data
        context = repo.search_context("Can I cancel my subscription?")
        expected = {
            "type": "faq",
            "question": "Can I cancel?",
            "answer": "Yes"
        }
        assert context == expected

    def test_search_context_no_match(self, repo, sample_data):
        repo._data = sample_data
        context = repo.search_context("Random question")
        assert context is None

    def test_search_context_case_insensitive(self, repo, sample_data):
        repo._data = sample_data
        context = repo.search_context("BASIC PLAN")
        assert context is not None
        assert context["name"] == "basic"

    def test_build_context_text_plan(self, repo):
        context = {
            "type": "plan",
            "name": "basic",
            "description": "Basic plan",
            "price": "R$49/month"
        }
        text = repo.build_context_text(context)
        assert "Plan Name: basic" in text
        assert "Price: R$49/month" in text
        assert "Description: Basic plan" in text

    def test_build_context_text_faq(self, repo):
        context = {
            "type": "faq",
            "question": "Can I cancel?",
            "answer": "Yes"
        }
        text = repo.build_context_text(context)
        assert "FAQ Question: Can I cancel?" in text
        assert "FAQ Answer: Yes" in text

    def test_build_context_text_none(self, repo):
        text = repo.build_context_text(None)
        assert text == "No relevant information found."

    def test_build_context_text_invalid_type(self, repo):
        context = {"type": "invalid"}
        text = repo.build_context_text(context)
        assert text == "No relevant information found."


class TestGlobalKnowledgeRepository:
    def test_global_knowledge_repository_instance(self):
        assert isinstance(knowledge_repository, KnowledgeRepository)