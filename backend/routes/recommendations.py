"""Recommendation service routes."""

from fastapi import APIRouter, Depends
from models.schemas import RecommendationRequest
from services.recommendation_service import RecommendationService
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
service = RecommendationService()


def _preferences(payload: RecommendationRequest) -> dict:
    return {
        "interests": payload.activities or [],
        "travel_style": payload.travel_style,
        "accommodation_preferences": (
            [payload.travel_style] if payload.travel_style else []
        ),
    }


@router.post("/destinations")
async def destinations(
    payload: RecommendationRequest, current_user: dict = Depends(get_current_user)
):
    recommendations = service.get_destination_recommendations(
        _preferences(payload), payload.budget
    )
    return {"recommendations": recommendations, "total_count": len(recommendations)}


@router.post("/activities")
async def activities(
    payload: RecommendationRequest, current_user: dict = Depends(get_current_user)
):
    recommendations = service.get_activity_recommendations(
        _preferences(payload), payload.destination
    )
    return {"recommendations": recommendations, "total_count": len(recommendations)}


@router.post("/accommodations")
async def accommodations(
    payload: RecommendationRequest, current_user: dict = Depends(get_current_user)
):
    per_night_budget = (
        payload.budget // max(payload.duration_days or 1, 1) if payload.budget else None
    )
    recommendations = service.get_accommodation_recommendations(
        _preferences(payload), per_night_budget
    )
    return {"recommendations": recommendations, "total_count": len(recommendations)}
