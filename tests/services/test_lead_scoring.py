import pytest
from app.services.lead_scoring import LeadScoringService, lead_scoring_service


class TestLeadScoringService:
    @pytest.fixture
    def scoring_service(self):
        return LeadScoringService()

    def test_score_lead_no_keywords(self, scoring_service):
        score = scoring_service.score_lead("Hello world")
        assert score == 0.0

    def test_score_lead_single_keyword(self, scoring_service):
        score = scoring_service.score_lead("I want to buy")
        assert score == 0.5  # want=20, buy=30, total=50/100=0.5

    def test_score_lead_multiple_keywords(self, scoring_service):
        score = scoring_service.score_lead("I want to buy the product")
        assert score == 0.5  # want=20, buy=30, total=50/100=0.5

    def test_score_lead_max_score(self, scoring_service):
        score = scoring_service.score_lead("buy purchase want need price cost budget interested demo")
        assert score == 1.0

    def test_score_lead_case_insensitive(self, scoring_service):
        score = scoring_service.score_lead("BUY PURCHASE")
        assert score == 0.6

    def test_score_lead_partial_matches(self, scoring_service):
        score = scoring_service.score_lead("I want to buy something")
        assert score == 0.5  # want=20, buy=30

    def test_score_lead_combined_high_score(self, scoring_service):
        score = scoring_service.score_lead("buy purchase want need price cost budget interested demo extra")
        assert score == 1.0

    def test_categorize_lead_hot(self, scoring_service):
        assert scoring_service.categorize_lead(0.7) == "hot"
        assert scoring_service.categorize_lead(0.8) == "hot"
        assert scoring_service.categorize_lead(1.0) == "hot"

    def test_categorize_lead_warm(self, scoring_service):
        assert scoring_service.categorize_lead(0.4) == "warm"
        assert scoring_service.categorize_lead(0.5) == "warm"
        assert scoring_service.categorize_lead(0.69) == "warm"

    def test_categorize_lead_cold(self, scoring_service):
        assert scoring_service.categorize_lead(0.0) == "cold"
        assert scoring_service.categorize_lead(0.1) == "cold"
        assert scoring_service.categorize_lead(0.39) == "cold"

    def test_get_call_to_action_hot(self, scoring_service):
        action = scoring_service.get_call_to_action("hot")
        assert action == "Schedule a demo or call with the sales team."

    def test_get_call_to_action_warm(self, scoring_service):
        action = scoring_service.get_call_to_action("warm")
        assert action == "Send a follow-up email with more information."

    def test_get_call_to_action_cold(self, scoring_service):
        action = scoring_service.get_call_to_action("cold")
        assert action == "Add to nurture campaign for future engagement."

    def test_get_call_to_action_invalid(self, scoring_service):
        action = scoring_service.get_call_to_action("invalid")
        assert action == "Add to nurture campaign for future engagement."

    def test_integration_score_and_categorize(self, scoring_service):
        message = "I want to buy the product"
        score = scoring_service.score_lead(message)
        category = scoring_service.categorize_lead(score)
        action = scoring_service.get_call_to_action(category)
        assert score == 0.5  # want=20, buy=30
        assert category == "warm"
        assert action == "Send a follow-up email with more information."


class TestGlobalLeadScoringService:
    def test_global_lead_scoring_service_instance(self):
        assert isinstance(lead_scoring_service, LeadScoringService)