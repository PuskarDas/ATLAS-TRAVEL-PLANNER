"""Recommendation Service - AI-powered recommendations using hybrid approach."""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class RecommendationService:
    """Recommendation engine using hybrid approach."""

    def __init__(self):
        """Initialize recommendation service."""
        # Sample destination data
        self.destinations_db = [
            {
                "id": 1,
                "name": "Paris",
                "country": "France",
                "rating": 4.8,
                "cost_per_day": 120,
                "tags": ["romance", "culture", "history"],
            },
            {
                "id": 2,
                "name": "Tokyo",
                "country": "Japan",
                "rating": 4.7,
                "cost_per_day": 100,
                "tags": ["technology", "culture", "food"],
            },
            {
                "id": 3,
                "name": "Bali",
                "country": "Indonesia",
                "rating": 4.6,
                "cost_per_day": 50,
                "tags": ["beach", "relaxation", "adventure"],
            },
            {
                "id": 4,
                "name": "New York",
                "country": "USA",
                "rating": 4.5,
                "cost_per_day": 150,
                "tags": ["urban", "entertainment", "shopping"],
            },
            {
                "id": 5,
                "name": "Barcelona",
                "country": "Spain",
                "rating": 4.6,
                "cost_per_day": 110,
                "tags": ["beach", "culture", "nightlife"],
            },
            {
                "id": 6,
                "name": "Dubai",
                "country": "UAE",
                "rating": 4.6,
                "cost_per_day": 150,
                "tags": ["luxury", "desert", "shopping"],
            },
            {
                "id": 7,
                "name": "Singapore",
                "country": "Singapore",
                "rating": 4.7,
                "cost_per_day": 130,
                "tags": ["food", "gardens", "family"],
            },
            {
                "id": 8,
                "name": "London",
                "country": "United Kingdom",
                "rating": 4.6,
                "cost_per_day": 145,
                "tags": ["museums", "history", "theatre"],
            },
            {
                "id": 9,
                "name": "Santorini",
                "country": "Greece",
                "rating": 4.8,
                "cost_per_day": 125,
                "tags": ["sea", "views", "romance"],
            },
            {
                "id": 10,
                "name": "Jaipur",
                "country": "India",
                "rating": 4.6,
                "cost_per_day": 45,
                "tags": ["palaces", "food", "culture"],
            },
            {
                "id": 11,
                "name": "Goa",
                "country": "India",
                "rating": 4.5,
                "cost_per_day": 55,
                "tags": ["beach", "music", "food"],
            },
            {
                "id": 12,
                "name": "Kerala",
                "country": "India",
                "rating": 4.7,
                "cost_per_day": 60,
                "tags": ["nature", "wellness", "food"],
            },
            {
                "id": 13,
                "name": "Istanbul",
                "country": "Turkey",
                "rating": 4.7,
                "cost_per_day": 85,
                "tags": ["history", "food", "markets"],
            },
            {
                "id": 14,
                "name": "Seoul",
                "country": "South Korea",
                "rating": 4.6,
                "cost_per_day": 105,
                "tags": ["food", "fashion", "nightlife"],
            },
            {
                "id": 15,
                "name": "Sydney",
                "country": "Australia",
                "rating": 4.7,
                "cost_per_day": 155,
                "tags": ["harbor", "beaches", "nature"],
            },
            {
                "id": 16,
                "name": "Cape Town",
                "country": "South Africa",
                "rating": 4.8,
                "cost_per_day": 95,
                "tags": ["nature", "wine", "adventure"],
            },
        ]

        # Sample activities
        self.activities_db = [
            {
                "id": 1,
                "name": "Museum Tour",
                "category": "culture",
                "cost": 25,
                "rating": 4.5,
                "tags": ["history", "educational"],
            },
            {
                "id": 2,
                "name": "Beach Day",
                "category": "relaxation",
                "cost": 0,
                "rating": 4.8,
                "tags": ["beach", "swimming"],
            },
            {
                "id": 3,
                "name": "Food Tour",
                "category": "food",
                "cost": 50,
                "rating": 4.7,
                "tags": ["local", "culinary"],
            },
            {
                "id": 4,
                "name": "Mountain Hike",
                "category": "adventure",
                "cost": 30,
                "rating": 4.6,
                "tags": ["outdoors", "exercise"],
            },
            {
                "id": 5,
                "name": "Shopping District",
                "category": "shopping",
                "cost": 100,
                "rating": 4.4,
                "tags": ["retail", "culture"],
            },
        ]

        # Sample hotels
        self.hotels_db = [
            {
                "id": 1,
                "name": "Luxury Hotel",
                "rating": 4.9,
                "price_per_night": 200,
                "type": "hotel",
                "tags": ["luxury", "service"],
            },
            {
                "id": 2,
                "name": "Budget Hostel",
                "rating": 4.2,
                "price_per_night": 25,
                "type": "hostel",
                "tags": ["budget", "social"],
            },
            {
                "id": 3,
                "name": "Beach Resort",
                "rating": 4.8,
                "price_per_night": 150,
                "type": "resort",
                "tags": ["beach", "luxury"],
            },
            {
                "id": 4,
                "name": "Airbnb Apartment",
                "rating": 4.5,
                "price_per_night": 80,
                "type": "apartment",
                "tags": ["local", "affordable"],
            },
            {
                "id": 5,
                "name": "Boutique Hotel",
                "rating": 4.7,
                "price_per_night": 120,
                "type": "hotel",
                "tags": ["unique", "upscale"],
            },
        ]

    def _tag_match_score(
        self, item_tags: List[str], user_preferences: Dict
    ) -> float:
        interests = set(user_preferences.get("interests") or [])
        tags = set(item_tags or [])
        union = interests | tags
        if not union:
            return 0.0
        return len(interests & tags) / len(union)

    def _calculate_destination_score(
        self, dest: Dict, user_preferences: Dict
    ) -> float:
        jaccard = self._tag_match_score(dest.get("tags", []), user_preferences)
        rating = float(dest.get("rating") or 0)
        return jaccard * 70.0 + (rating / 5.0) * 30.0

    def _get_best_for(self, dest: Dict, user_preferences: Dict) -> str:
        overlaps = set(dest.get("tags", [])) & set(
            user_preferences.get("interests") or []
        )
        if overlaps:
            return ", ".join(sorted(overlaps)[:3])
        return "discover & explore"

    def _calculate_activity_score(
        self, activity: Dict, user_preferences: Dict
    ) -> float:
        jaccard = self._tag_match_score(activity.get("tags", []), user_preferences)
        rating = float(activity.get("rating") or 0)
        return jaccard * 65.0 + (rating / 5.0) * 35.0

    def _get_suitability(
        self, activity: Dict, user_preferences: Dict
    ) -> str:
        overlaps = set(activity.get("tags", [])) & set(
            user_preferences.get("interests") or []
        )
        if len(overlaps) >= 2:
            return "high"
        if overlaps:
            return "medium"
        return "mixed"

    def _calculate_hotel_score(
        self, hotel: Dict, user_preferences: Dict
    ) -> float:
        jaccard = self._tag_match_score(hotel.get("tags", []), user_preferences)
        rating = float(hotel.get("rating") or 0)
        base = jaccard * 50.0 + (rating / 5.0) * 50.0
        return base if jaccard else base * 0.5 + 15.0

    def _calculate_value_for_money(self, hotel: Dict) -> float:
        price = float(hotel.get("price_per_night") or 1)
        rating = float(hotel.get("rating") or 0)
        return round(rating / max(price / 50.0, 0.1), 2)

    def get_destination_recommendations(
        self, user_preferences: Dict, budget: Optional[int] = None, top_n: int = 5
    ) -> List[Dict]:
        """Get destination recommendations."""
        try:
            recommendations = []

            for dest in self.destinations_db:
                # Check budget compatibility
                if budget and dest["cost_per_day"] * 7 > budget:
                    continue

                # Calculate match score
                match_score = self._calculate_destination_score(dest, user_preferences)

                recommendations.append(
                    {
                        **dest,
                        "match_score": match_score,
                        "best_for": self._get_best_for(dest, user_preferences),
                    }
                )

            # Sort by match score and return top N
            recommendations.sort(key=lambda x: x["match_score"], reverse=True)
            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error getting destination recommendations: {str(e)}")
            return []

    def get_activity_recommendations(
        self, user_preferences: Dict, destination: Optional[str] = None, top_n: int = 5
    ) -> List[Dict]:
        """Get activity recommendations."""
        try:
            recommendations = []

            for activity in self.activities_db:
                match_score = self._calculate_activity_score(activity, user_preferences)

                recommendations.append(
                    {
                        **activity,
                        "match_score": match_score,
                        "suitability": self._get_suitability(
                            activity, user_preferences
                        ),
                    }
                )

            recommendations.sort(key=lambda x: x["match_score"], reverse=True)
            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error getting activity recommendations: {str(e)}")
            return []

    def get_accommodation_recommendations(
        self, user_preferences: Dict, budget: Optional[int] = None, top_n: int = 5
    ) -> List[Dict]:
        """Get accommodation recommendations."""
        try:
            recommendations = []

            for hotel in self.hotels_db:
                # Check budget compatibility
                if budget and hotel["price_per_night"] > budget:
                    continue

                match_score = self._calculate_hotel_score(hotel, user_preferences)

                recommendations.append(
                    {
                        **hotel,
                        "match_score": match_score,
                        "value_for_money": self._calculate_value_for_money(hotel),
                    }
                )

            recommendations.sort(key=lambda x: x["match_score"], reverse=True)
            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error getting accommodation recommendations: {str(e)}")
            return []

    def collaborative_filter_recommendations(
        self,
        user_id: int,
        user_travel_history: List[Dict],
        similar_users_history: List[List[Dict]],
        top_n: int = 5,
    ) -> List[Dict]:
        """Get recommendations using collaborative filtering."""
        try:
            # Extract features from user's travel history
            user_destinations = set(t.get("destination") for t in user_travel_history)

            # Find destinations visited by similar users but not by current user
            similar_user_destinations = set()
            for history in similar_users_history:
                for trip in history:
                    dest = trip.get("destination")
                    if dest not in user_destinations:
                        similar_user_destinations.add(dest)

            # Score and rank
            recommendations = [
                d
                for d in self.destinations_db
                if d["name"] in similar_user_destinations
            ]

            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error in collaborative filtering: {str(e)}")
            return []

    def content_based_recommendations(
        self, preferences: Dict, top_n: int = 5
    ) -> List[Dict]:
        """Get content-based recommendations."""
        try:
            recommendations = []
            user_tags = set(preferences.get("interests", []))

            for dest in self.destinations_db:
                dest_tags = set(dest.get("tags", []))
                # Calculate Jaccard similarity
                union_size = len(user_tags | dest_tags)
                similarity = len(user_tags & dest_tags) / union_size if union_size > 0 else 0.0
                
                recommendations.append(
                    {
                        **dest,
                        "match_score": similarity * 100,
                    }
                )

            # Sort by match score and return top N
            recommendations.sort(key=lambda x: x["match_score"], reverse=True)
            return recommendations[:top_n]

        except Exception as e:
            logger.error(f"Error in content-based recommendations: {str(e)}")
            return []