from datetime import datetime
from decimal import Decimal

from services.budget_service import BudgetService
from services.group_consensus_service import GroupConsensusService
from services.itinerary_service import ItineraryService
from services.nlp_service import NLPService
from services.recommendation_service import RecommendationService


def test_recommendation_service_returns_ranked_destinations():
    service = RecommendationService()
    results = service.get_destination_recommendations(
        {"interests": ["beach"]}, budget=1000
    )
    assert results
    assert results[0]["match_score"] >= results[-1]["match_score"]


def test_itinerary_generation_has_daily_schedule():
    service = ItineraryService()
    itinerary = service.generate_itinerary(
        "Bali",
        datetime(2026, 6, 1),
        datetime(2026, 6, 3),
        {"interests": ["beach"]},
    )
    assert itinerary["duration_days"] == 3
    assert len(itinerary["itinerary"]) == 3


def test_budget_splits_and_settlements():
    service = BudgetService()
    split = service.split_expense_equally(Decimal("90"), 3)
    assert split[0] == Decimal("30")
    settlements = service.calculate_settlements(
        [{"paid_by": 1, "amount": 90}],
        [1, 2, 3],
    )
    assert settlements


def test_nlp_detects_budget_intent():
    result = NLPService().process_message("How much will a 5 day trip cost?")
    assert result["intent"] == "ask_budget"
    assert result["confidence"] > 0


def test_group_consensus_aggregates_preferences():
    result = GroupConsensusService().aggregate_preferences(
        [
            {"destinations": ["Bali"], "activities": ["food"], "budget": 1000},
            {
                "destinations": ["Bali", "Tokyo"],
                "activities": ["beach"],
                "budget": 1200,
            },
        ]
    )
    assert result["destinations"]["Bali"] == 100
    assert result["budget"] == 1100
