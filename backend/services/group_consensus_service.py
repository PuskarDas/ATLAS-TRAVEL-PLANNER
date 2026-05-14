"""Group Consensus Service - Aggregates preferences and finds optimal group solutions."""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def variance(values: List[float]) -> float:
    if not values:
        return 0.0
    average = mean(values)
    return sum((value - average) ** 2 for value in values) / len(values)


class GroupConsensusService:
    """Service for group preference aggregation and consensus building."""

    def __init__(self):
        """Initialize group consensus service."""
        pass

    def aggregate_preferences(self, group_preferences: List[Dict]) -> Dict:
        """Aggregate preferences from group members."""
        try:
            aggregated = {
                "destinations": self._aggregate_destinations(group_preferences),
                "activities": self._aggregate_activities(group_preferences),
                "budget": self._aggregate_budget(group_preferences),
                "travel_style": self._aggregate_travel_style(group_preferences),
                "accommodation_type": self._aggregate_accommodation(group_preferences),
                "consensus_score": 0.0,
            }

            # Calculate overall consensus score
            aggregated["consensus_score"] = self._calculate_consensus_score(
                group_preferences
            )

            return aggregated

        except Exception as e:
            logger.error(f"Error aggregating preferences: {str(e)}")
            return {}

    def find_optimal_destination(
        self, group_preferences: List[Dict], available_destinations: List[Dict]
    ) -> Optional[Dict]:
        """Find destination that satisfies most group members."""
        try:
            best_destination = None
            best_score = 0

            for destination in available_destinations:
                satisfaction_scores = []

                for member_pref in group_preferences:
                    score = self._calculate_member_satisfaction(
                        member_pref, destination
                    )
                    satisfaction_scores.append(score)

                # Calculate group satisfaction (average with minimum threshold)
                avg_satisfaction = mean(satisfaction_scores)
                min_satisfaction = min(satisfaction_scores)

                # Weighted score: prioritize high average and avoid low outliers
                group_score = (avg_satisfaction * 0.7) + (min_satisfaction * 0.3)

                if group_score > best_score:
                    best_score = group_score
                    best_destination = {
                        **destination,
                        "group_satisfaction_score": float(group_score),
                        "average_satisfaction": float(avg_satisfaction),
                        "minimum_satisfaction": float(min_satisfaction),
                        "satisfaction_by_member": [
                            float(s) for s in satisfaction_scores
                        ],
                    }

            return best_destination

        except Exception as e:
            logger.error(f"Error finding optimal destination: {str(e)}")
            return None

    def suggest_compromise_activities(
        self,
        member_preferences: List[List[str]],
        available_activities: List[Dict],
        max_activities: int = 5,
    ) -> List[Dict]:
        """Suggest activities that appeal to most group members."""
        try:
            activity_scores = {}

            for activity in available_activities:
                activity_name = activity.get("name")
                members_interested = sum(
                    1
                    for prefs in member_preferences
                    if any(pref.lower() in activity_name.lower() for pref in prefs)
                )

                interest_ratio = members_interested / len(member_preferences)

                activity_scores[activity_name] = {
                    **activity,
                    "appeal_score": interest_ratio * 100,
                    "members_interested": members_interested,
                }

            # Sort by appeal score and return top activities
            sorted_activities = sorted(
                activity_scores.values(), key=lambda x: x["appeal_score"], reverse=True
            )

            return sorted_activities[:max_activities]

        except Exception as e:
            logger.error(f"Error suggesting compromise activities: {str(e)}")
            return []

    def resolve_conflicts(
        self, preferences: Dict, weights: Optional[Dict] = None
    ) -> Dict:
        """Resolve conflicts in group preferences."""
        try:
            if weights is None:
                weights = {}  # All members have equal weight

            resolution = {"conflicts": [], "resolutions": {}, "compromise_level": 0.0}

            # Identify conflicts
            conflicts = self._identify_conflicts(preferences)
            resolution["conflicts"] = conflicts

            # Resolve each conflict
            for conflict in conflicts:
                resolution["resolutions"][conflict["issue"]] = self._resolve_conflict(
                    conflict, weights
                )

            # Calculate compromise level
            resolution["compromise_level"] = self._calculate_compromise_level(conflicts)

            return resolution

        except Exception as e:
            logger.error(f"Error resolving conflicts: {str(e)}")
            return {}

    def calculate_group_satisfaction(
        self, group_preferences: List[Dict], proposed_itinerary: Dict
    ) -> Dict:
        """Calculate how satisfied each member would be with proposed itinerary."""
        try:
            satisfaction_scores = []
            member_details = []

            for idx, member_pref in enumerate(group_preferences):
                score = self._calculate_member_satisfaction(
                    member_pref, proposed_itinerary
                )
                satisfaction_scores.append(score)

                member_details.append(
                    {
                        "member_id": idx,
                        "satisfaction_score": float(score),
                        "satisfied": score >= 70,
                    }
                )

            overall_satisfaction = mean(satisfaction_scores)
            satisfaction_variance = variance(satisfaction_scores)

            return {
                "overall_satisfaction": float(overall_satisfaction),
                "satisfaction_by_member": member_details,
                "satisfaction_variance": float(satisfaction_variance),
                "fairness_score": self._calculate_fairness_score(satisfaction_scores),
                "recommendation": self._get_satisfaction_recommendation(
                    overall_satisfaction
                ),
            }

        except Exception as e:
            logger.error(f"Error calculating group satisfaction: {str(e)}")
            return {}

    def weight_member_preferences(
        self, preferences: List[Dict], weights: Dict[int, float]
    ) -> Dict:
        """Weight preferences by member importance."""
        try:
            weighted_aggregation = {
                "destinations": {},
                "activities": {},
                "total_weight": sum(weights.values()),
            }

            for member_id, preference in enumerate(preferences):
                weight = weights.get(member_id, 1.0)

                # Weight destinations
                for dest in preference.get("destinations", []):
                    weighted_aggregation["destinations"][dest] = (
                        weighted_aggregation["destinations"].get(dest, 0) + weight
                    )

                # Weight activities
                for activity in preference.get("activities", []):
                    weighted_aggregation["activities"][activity] = (
                        weighted_aggregation["activities"].get(activity, 0) + weight
                    )

            # Normalize
            for key in weighted_aggregation["destinations"]:
                weighted_aggregation["destinations"][key] /= weighted_aggregation[
                    "total_weight"
                ]

            for key in weighted_aggregation["activities"]:
                weighted_aggregation["activities"][key] /= weighted_aggregation[
                    "total_weight"
                ]

            return weighted_aggregation

        except Exception as e:
            logger.error(f"Error weighting preferences: {str(e)}")
            return {}

    def _aggregate_destinations(self, preferences: List[Dict]) -> Dict:
        """Aggregate destination preferences."""
        dest_counts = {}
        for pref in preferences:
            for dest in pref.get("destinations", []):
                dest_counts[dest] = dest_counts.get(dest, 0) + 1

        total = len(preferences)
        return {
            dest: (count / total) * 100
            for dest, count in sorted(
                dest_counts.items(), key=lambda x: x[1], reverse=True
            )
        }

    def _aggregate_activities(self, preferences: List[Dict]) -> Dict:
        """Aggregate activity preferences."""
        activity_counts = {}
        for pref in preferences:
            for activity in pref.get("activities", []):
                activity_counts[activity] = activity_counts.get(activity, 0) + 1

        total = len(preferences)
        return {
            activity: (count / total) * 100
            for activity, count in sorted(
                activity_counts.items(), key=lambda x: x[1], reverse=True
            )
        }

    def _aggregate_budget(self, preferences: List[Dict]) -> float:
        """Aggregate budget preferences."""
        budgets = [p.get("budget", 0) for p in preferences if p.get("budget")]
        return float(mean(budgets)) if budgets else 0.0

    def _aggregate_travel_style(self, preferences: List[Dict]) -> str:
        """Aggregate travel style preferences."""
        styles = [p.get("travel_style") for p in preferences]
        style_counts = {}
        for style in styles:
            if style:
                style_counts[style] = style_counts.get(style, 0) + 1

        return max(style_counts, key=style_counts.get) if style_counts else "mid-range"

    def _aggregate_accommodation(self, preferences: List[Dict]) -> str:
        """Aggregate accommodation preferences."""
        accommodations = [p.get("accommodation_type") for p in preferences]
        acc_counts = {}
        for acc in accommodations:
            if acc:
                acc_counts[acc] = acc_counts.get(acc, 0) + 1

        return max(acc_counts, key=acc_counts.get) if acc_counts else "hotel"

    def _calculate_consensus_score(self, preferences: List[Dict]) -> float:
        """Calculate overall consensus score."""
        if not preferences:
            return 0.0

        # Calculate variance in preferences
        destinations = [p.get("destinations", []) for p in preferences]
        common_destinations = set(destinations[0]) if destinations else set()
        for d in destinations[1:]:
            common_destinations &= set(d)

        common_ratio = len(common_destinations) / max(
            max(len(d) for d in destinations) if destinations else 1, 1
        )

        return min(common_ratio * 100, 100.0)

    def _calculate_member_satisfaction(self, member_pref: Dict, item: Dict) -> float:
        """Calculate satisfaction score for a member."""
        score = 0.0

        # Check destination match
        if item.get("name") in member_pref.get("destinations", []):
            score += 30

        # Check activity match
        item_activities = set(item.get("activities", []))
        member_activities = set(member_pref.get("activities", []))
        if item_activities & member_activities:
            score += 20

        # Check budget match
        member_budget = member_pref.get("budget", 1000)
        item_budget = item.get("estimated_cost", 0)
        if item_budget <= member_budget:
            score += 25

        # Check travel style match
        if item.get("travel_style") == member_pref.get("travel_style"):
            score += 25

        return score

    def _identify_conflicts(self, preferences: Dict) -> List[Dict]:
        """Identify conflicts in group preferences."""
        conflicts = []

        # Check destination conflicts
        if len(preferences.get("destinations", {})) > 1:
            conflicts.append(
                {
                    "issue": "destination_conflict",
                    "details": preferences["destinations"],
                }
            )

        # Check budget conflicts
        if preferences.get("budget_variance", 0) > 50:
            conflicts.append(
                {
                    "issue": "budget_mismatch",
                    "details": f"Variance: {preferences['budget_variance']}",
                }
            )

        return conflicts

    def _resolve_conflict(self, conflict: Dict, weights: Dict) -> str:
        """Resolve a specific conflict."""
        if conflict["issue"] == "destination_conflict":
            return "Rotate destinations: visit multiple preferred locations"
        elif conflict["issue"] == "budget_mismatch":
            return "Allocate flexible budget for optional activities"

        return "Find compromise option"

    def _calculate_compromise_level(self, conflicts: List[Dict]) -> float:
        """Calculate compromise level needed."""
        if not conflicts:
            return 0.0

        return min(len(conflicts) * 25, 100)

    def _calculate_fairness_score(self, scores: List[float]) -> float:
        """Calculate fairness in satisfaction scores."""
        if not scores:
            return 100.0

        score_variance = variance(scores)
        score_mean = mean(scores)

        # Lower variance = more fair
        fairness = 100 - min((score_variance / max(score_mean, 1)) * 10, 100)

        return float(fairness)

    def _get_satisfaction_recommendation(self, satisfaction: float) -> str:
        """Get recommendation based on satisfaction level."""
        if satisfaction >= 80:
            return "Excellent - Group will be very happy"
        elif satisfaction >= 60:
            return "Good - Most members will be satisfied"
        elif satisfaction >= 40:
            return "Fair - Consider adjustments to improve satisfaction"
        else:
            return "Poor - Need significant revisions to satisfy group"
