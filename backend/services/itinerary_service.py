"""Itinerary Service - AI-powered itinerary generation and optimization."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from utils.helpers import calculate_trip_duration

logger = logging.getLogger(__name__)


class ItineraryService:
    """Itinerary generation and optimization service."""

    def __init__(self):
        """Initialize itinerary service."""
        pass

    def generate_itinerary(
        self,
        destination: str,
        start_date: datetime,
        end_date: datetime,
        group_preferences: Dict,
        budget: Optional[int] = None,
    ) -> Dict:
        """Generate AI-powered itinerary."""
        try:
            duration = calculate_trip_duration(start_date, end_date)

            # Generate day-by-day itinerary
            daily_itineraries = []
            current_date = start_date

            for day_num in range(1, duration + 1):
                day_plan = self._generate_day_plan(
                    destination, day_num, duration, group_preferences, current_date
                )
                daily_itineraries.append(day_plan)
                current_date += timedelta(days=1)

            return {
                "destination": destination,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "duration_days": duration,
                "itinerary": daily_itineraries,
                "total_activities": sum(
                    len(day["activities"]) for day in daily_itineraries
                ),
                "optimization_score": self._calculate_optimization_score(
                    daily_itineraries
                ),
            }

        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            return {}

    def optimize_itinerary(
        self, itinerary: Dict, constraints: Optional[Dict] = None
    ) -> Dict:
        """Optimize existing itinerary based on constraints."""
        try:
            optimized = itinerary.copy()

            # Apply constraints
            if constraints:
                if "max_daily_activities" in constraints:
                    max_activities = constraints["max_daily_activities"]
                    for day in optimized["itinerary"]:
                        if len(day["activities"]) > max_activities:
                            day["activities"] = day["activities"][:max_activities]

                if "priority_activities" in constraints:
                    # Prioritize certain activities
                    priority = constraints["priority_activities"]
                    for day in optimized["itinerary"]:
                        day["activities"].sort(
                            key=lambda x: priority.get(x.get("name"), 0), reverse=True
                        )

            optimized["optimization_score"] = self._calculate_optimization_score(
                optimized["itinerary"]
            )

            return optimized

        except Exception as e:
            logger.error(f"Error optimizing itinerary: {str(e)}")
            return {}

    def add_activity_to_itinerary(
        self,
        itinerary: Dict,
        day_number: int,
        activity: Dict,
        insert_position: Optional[int] = None,
    ) -> Dict:
        """Add activity to specific day."""
        try:
            if day_number < 1 or day_number > len(itinerary.get("itinerary", [])):
                logger.error(f"Invalid day number: {day_number}")
                return itinerary

            day_plan = itinerary["itinerary"][day_number - 1]

            if insert_position is None:
                day_plan["activities"].append(activity)
            else:
                day_plan["activities"].insert(insert_position, activity)

            return itinerary

        except Exception as e:
            logger.error(f"Error adding activity: {str(e)}")
            return itinerary

    def remove_activity_from_itinerary(
        self, itinerary: Dict, day_number: int, activity_id: int
    ) -> Dict:
        """Remove activity from itinerary."""
        try:
            day_plan = itinerary["itinerary"][day_number - 1]
            day_plan["activities"] = [
                a for a in day_plan["activities"] if a.get("id") != activity_id
            ]
            return itinerary

        except Exception as e:
            logger.error(f"Error removing activity: {str(e)}")
            return itinerary

    def get_itinerary_summary(self, itinerary: Dict) -> Dict:
        """Get summary of itinerary."""
        try:
            summary = {
                "destination": itinerary.get("destination"),
                "duration_days": itinerary.get("duration_days"),
                "total_activities": itinerary.get("total_activities"),
                "activities_by_category": {},
                "daily_schedule": [],
            }

            # Count activities by category
            for day in itinerary.get("itinerary", []):
                for activity in day.get("activities", []):
                    category = activity.get("category", "other")
                    summary["activities_by_category"][category] = (
                        summary["activities_by_category"].get(category, 0) + 1
                    )

            # Generate daily schedule
            for idx, day in enumerate(itinerary.get("itinerary", []), 1):
                day_summary = {
                    "day": idx,
                    "date": day.get("date"),
                    "activity_count": len(day.get("activities", [])),
                    "activities": [
                        {
                            "name": a.get("name"),
                            "time": a.get("time"),
                            "duration_hours": a.get("duration_hours"),
                        }
                        for a in day.get("activities", [])
                    ],
                }
                summary["daily_schedule"].append(day_summary)

            return summary

        except Exception as e:
            logger.error(f"Error getting itinerary summary: {str(e)}")
            return {}

    def _generate_day_plan(
        self,
        destination: str,
        day_number: int,
        total_days: int,
        preferences: Dict,
        date: datetime,
    ) -> Dict:
        """Generate plan for a single day."""
        activities = self._get_recommended_activities(
            destination, day_number, preferences
        )

        return {
            "day": day_number,
            "date": date.isoformat(),
            "theme": self._get_day_theme(day_number, total_days),
            "activities": activities,
            "estimated_cost": sum(a.get("estimated_cost", 0) for a in activities),
            "morning_activities": activities[: len(activities) // 2],
            "afternoon_activities": activities[len(activities) // 2 :],
        }

    def _get_recommended_activities(
        self, destination: str, day_number: int, preferences: Dict
    ) -> List[Dict]:
        """Get recommended activities for a day."""
        # Sample activities for different days
        activities_map = {
            1: [
                {
                    "id": 1,
                    "name": "Arrive and settle in",
                    "time": "09:00",
                    "duration_hours": 2,
                    "category": "transport",
                    "estimated_cost": 0,
                },
                {
                    "id": 2,
                    "name": "Lunch",
                    "time": "12:00",
                    "duration_hours": 1,
                    "category": "food",
                    "estimated_cost": 20,
                },
                {
                    "id": 3,
                    "name": "City orientation walk",
                    "time": "14:00",
                    "duration_hours": 2,
                    "category": "sightseeing",
                    "estimated_cost": 0,
                },
            ],
            2: [
                {
                    "id": 4,
                    "name": "Breakfast",
                    "time": "08:00",
                    "duration_hours": 1,
                    "category": "food",
                    "estimated_cost": 15,
                },
                {
                    "id": 5,
                    "name": "Main attraction visit",
                    "time": "09:30",
                    "duration_hours": 3,
                    "category": "sightseeing",
                    "estimated_cost": 25,
                },
                {
                    "id": 6,
                    "name": "Lunch",
                    "time": "12:30",
                    "duration_hours": 1.5,
                    "category": "food",
                    "estimated_cost": 20,
                },
                {
                    "id": 7,
                    "name": "Shopping",
                    "time": "14:00",
                    "duration_hours": 2,
                    "category": "shopping",
                    "estimated_cost": 50,
                },
            ],
            3: [
                {
                    "id": 8,
                    "name": "Adventure activity",
                    "time": "08:00",
                    "duration_hours": 4,
                    "category": "adventure",
                    "estimated_cost": 60,
                },
                {
                    "id": 9,
                    "name": "Lunch with local food",
                    "time": "12:30",
                    "duration_hours": 1.5,
                    "category": "food",
                    "estimated_cost": 25,
                },
                {
                    "id": 10,
                    "name": "Evening relaxation",
                    "time": "15:00",
                    "duration_hours": 2,
                    "category": "relaxation",
                    "estimated_cost": 30,
                },
            ],
        }

        default_activities = [
            {
                "id": 11,
                "name": "Breakfast",
                "time": "08:00",
                "duration_hours": 1,
                "category": "food",
                "estimated_cost": 15,
            },
            {
                "id": 12,
                "name": "Main activity",
                "time": "10:00",
                "duration_hours": 3,
                "category": "sightseeing",
                "estimated_cost": 30,
            },
            {
                "id": 13,
                "name": "Lunch",
                "time": "13:00",
                "duration_hours": 1,
                "category": "food",
                "estimated_cost": 20,
            },
            {
                "id": 14,
                "name": "Evening activity",
                "time": "16:00",
                "duration_hours": 2,
                "category": "relaxation",
                "estimated_cost": 20,
            },
        ]

        return activities_map.get(day_number, default_activities)

    def _get_day_theme(self, day_number: int, total_days: int) -> str:
        """Get theme for the day."""
        if day_number == 1:
            return "Arrival & Orientation"
        elif day_number == total_days:
            return "Departure Day"
        elif day_number == 2:
            return "Main Attractions"
        else:
            return "Exploration"

    def _calculate_optimization_score(self, itinerary: List[Dict]) -> float:
        """Calculate optimization score for itinerary."""
        try:
            total_score = 0.0
            max_score = 0.0

            for day in itinerary:
                activities = day.get("activities", [])

                # Score based on activity count (2-4 activities is ideal)
                activity_count = len(activities)
                if 2 <= activity_count <= 4:
                    total_score += 10
                elif activity_count < 2:
                    total_score += 5
                else:
                    total_score += max(0, 10 - (activity_count - 4))

                # Score based on variety
                categories = set(a.get("category") for a in activities)
                total_score += len(categories) * 2

                # Score based on timing (no overlaps)
                total_score += 5  # Assuming no overlaps

                max_score += 20

            return (total_score / max(max_score, 1)) * 100

        except Exception as e:
            logger.error(f"Error calculating optimization score: {str(e)}")
            return 0.0
