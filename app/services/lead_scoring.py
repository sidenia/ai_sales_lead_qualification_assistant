from typing import Literal


class LeadScoringService:
    LEAD_WEIGHTS = {
        "buy": 30,
        "purchase": 30,
        "want": 20,
        "need": 20,
        "price": 15,
        "cost": 15,
        "budget": 10,
        "interested": 10,
        "demo": 10
    }

    def score_lead(self, message: str) -> float:
        message = message.lower()
        score = sum(
            weight for word, weight in self.LEAD_WEIGHTS.items()
            if word in message
        )
        return min(score / 100, 1.0)

    def categorize_lead(self, score: float) -> Literal["hot", "warm", "cold"]:
        if score >= 0.7:
            return "hot"
        elif score >= 0.4:
            return "warm"
        else:
            return "cold"

    def get_call_to_action(self, category: str) -> str:
        actions = {
            "hot": "Schedule a demo or call with the sales team.",
            "warm": "Send a follow-up email with more information.",
            "cold": "Add to nurture campaign for future engagement."
        }
        return actions.get(category, "Add to nurture campaign for future engagement.")


lead_scoring_service = LeadScoringService() # global instance