"""Budget Service - Smart budget calculation and expense splitting."""

import logging
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class BudgetService:
    """Budget management and optimization service."""

    def __init__(self):
        """Initialize budget service."""
        pass

    def calculate_trip_budget(
        self,
        destination: str,
        duration_days: int,
        group_size: int,
        travel_style: str = "mid-range",
    ) -> Dict:
        """Calculate total trip budget."""
        try:
            # Cost per day estimates by travel style
            daily_costs = {"budget": 50, "mid-range": 100, "luxury": 200}

            cost_per_day = daily_costs.get(travel_style, 100)

            # Accommodation (typically 40% of daily cost)
            accommodation_cost = cost_per_day * 0.4 * duration_days

            # Food & dining (typically 30% of daily cost)
            food_cost = cost_per_day * 0.3 * duration_days

            # Activities & entertainment (typically 20% of daily cost)
            activities_cost = cost_per_day * 0.2 * duration_days

            # Transport within destination (typically 10% of daily cost)
            transport_cost = cost_per_day * 0.1 * duration_days

            # Total per person
            total_per_person = (
                accommodation_cost + food_cost + activities_cost + transport_cost
            )

            # Group total
            group_total = total_per_person * group_size

            # Add 15% contingency
            contingency = group_total * 0.15

            return {
                "duration_days": duration_days,
                "group_size": group_size,
                "travel_style": travel_style,
                "breakdown": {
                    "accommodation": accommodation_cost,
                    "food": food_cost,
                    "activities": activities_cost,
                    "transport": transport_cost,
                    "contingency": contingency,
                },
                "per_person": {
                    "accommodation": accommodation_cost,
                    "food": food_cost,
                    "activities": activities_cost,
                    "transport": transport_cost,
                    "subtotal": total_per_person,
                    "with_contingency": total_per_person + (contingency / group_size),
                },
                "group_total": {
                    "subtotal": group_total,
                    "with_contingency": group_total + contingency,
                },
            }

        except Exception as e:
            logger.error(f"Error calculating trip budget: {str(e)}")
            return {}

    def split_expense_equally(
        self, total_amount: Decimal, num_people: int
    ) -> Dict[int, Decimal]:
        """Split expense equally among group members."""
        try:
            if num_people <= 0:
                logger.error("Invalid number of people")
                return {}

            per_person = total_amount / num_people
            return {i: per_person for i in range(num_people)}

        except Exception as e:
            logger.error(f"Error splitting expense equally: {str(e)}")
            return {}

    def split_expense_proportional(
        self, total_amount: Decimal, contributions: Dict[int, Decimal]
    ) -> Dict[int, Decimal]:
        """Split expense based on contribution ratios."""
        try:
            total_contribution = sum(contributions.values())
            if total_contribution <= 0:
                logger.error("Total contribution must be positive")
                return {}

            result = {}
            for person_id, contribution in contributions.items():
                ratio = contribution / total_contribution
                result[person_id] = total_amount * ratio

            return result

        except Exception as e:
            logger.error(f"Error splitting expense proportionally: {str(e)}")
            return {}

    def split_expense_weighted(
        self, total_amount: Decimal, weights: Dict[int, float]
    ) -> Dict[int, Decimal]:
        """Split expense based on weighted distribution."""
        try:
            total_weight = sum(weights.values())
            if total_weight <= 0:
                logger.error("Total weight must be positive")
                return {}

            result = {}
            for person_id, weight in weights.items():
                result[person_id] = total_amount * (weight / total_weight)

            return result

        except Exception as e:
            logger.error(f"Error splitting expense with weights: {str(e)}")
            return {}

    def calculate_settlements(
        self, expenses: List[Dict], group_members: List[int]
    ) -> List[Dict]:
        """Calculate who owes whom."""
        try:
            # Calculate total each person paid
            paid = {member: Decimal(0) for member in group_members}
            for expense in expenses:
                payer = expense.get("paid_by")
                amount = Decimal(str(expense.get("amount", 0)))
                if payer in paid:
                    paid[payer] += amount

            # Calculate total owed by each person
            total_expenses = sum(paid.values())
            per_person = total_expenses / len(group_members)

            # Calculate balances (positive = owed money, negative = owes money)
            balances = {member: per_person - paid[member] for member in group_members}

            # Generate settlements
            settlements = self._generate_settlements(balances)

            return settlements

        except Exception as e:
            logger.error(f"Error calculating settlements: {str(e)}")
            return []

    def track_trip_expenses(self, expenses: List[Dict]) -> Dict:
        """Get expense tracking summary."""
        try:
            summary = {
                "total_expenses": Decimal(0),
                "by_category": {},
                "by_person": {},
                "daily_breakdown": [],
            }

            for expense in expenses:
                amount = Decimal(str(expense.get("amount", 0)))
                category = expense.get("category", "other")
                payer = expense.get("paid_by")
                date = expense.get("date")

                # Total
                summary["total_expenses"] += amount

                # By category
                if category not in summary["by_category"]:
                    summary["by_category"][category] = Decimal(0)
                summary["by_category"][category] += amount

                # By person
                if payer not in summary["by_person"]:
                    summary["by_person"][payer] = Decimal(0)
                summary["by_person"][payer] += amount

            return summary

        except Exception as e:
            logger.error(f"Error tracking expenses: {str(e)}")
            return {}

    def get_budget_analytics(
        self, expenses: List[Dict], initial_budget: Decimal
    ) -> Dict:
        """Get budget analytics and insights."""
        try:
            total_spent = Decimal(0)
            for expense in expenses:
                total_spent += Decimal(str(expense.get("amount", 0)))

            remaining = initial_budget - total_spent
            spent_percentage = (
                (total_spent / initial_budget * 100) if initial_budget > 0 else 0
            )

            return {
                "initial_budget": float(initial_budget),
                "total_spent": float(total_spent),
                "remaining": float(remaining),
                "spent_percentage": spent_percentage,
                "status": self._get_budget_status(spent_percentage),
                "daily_average": float(total_spent / len(expenses)) if expenses else 0,
                "forecast": self._forecast_budget(expenses, initial_budget),
            }

        except Exception as e:
            logger.error(f"Error getting budget analytics: {str(e)}")
            return {}

    def optimize_budget(
        self, available_budget: Decimal, preferences: Dict, duration_days: int
    ) -> Dict:
        """Optimize budget allocation based on preferences."""
        try:
            preference_weights = {
                "accommodation": preferences.get("accommodation_priority", 0.4),
                "food": preferences.get("food_priority", 0.25),
                "activities": preferences.get("activities_priority", 0.25),
                "transport": preferences.get("transport_priority", 0.1),
            }

            total_weight = sum(preference_weights.values())
            normalized_weights = {
                k: v / total_weight for k, v in preference_weights.items()
            }

            allocation = {}
            for category, weight in normalized_weights.items():
                allocation[category] = float(available_budget * weight)

            return {
                "available_budget": float(available_budget),
                "allocation": allocation,
                "daily_breakdown": {
                    category: float(amount / duration_days)
                    for category, amount in allocation.items()
                },
            }

        except Exception as e:
            logger.error(f"Error optimizing budget: {str(e)}")
            return {}

    def _generate_settlements(self, balances: Dict) -> List[Dict]:
        """Generate settlement transactions."""
        settlements = []

        # Separate creditors and debtors
        creditors = [(id_, amount) for id_, amount in balances.items() if amount > 0]
        debtors = [(id_, amount) for id_, amount in balances.items() if amount < 0]

        # Match creditors with debtors
        for creditor_id, credit_amount in creditors:
            for debtor_id, debt_amount in debtors:
                if debt_amount < 0:  # Still owes money
                    settlement_amount = min(credit_amount, abs(debt_amount))
                    settlements.append(
                        {
                            "from": debtor_id,
                            "to": creditor_id,
                            "amount": float(settlement_amount),
                        }
                    )
                    credit_amount -= settlement_amount
                    debt_amount += settlement_amount

                    if credit_amount <= 0:
                        break

        return settlements

    def _get_budget_status(self, spent_percentage: float) -> str:
        """Get budget status."""
        if spent_percentage < 50:
            return "On Track"
        elif spent_percentage < 80:
            return "Moderate"
        elif spent_percentage < 100:
            return "Caution"
        else:
            return "Over Budget"

    def _forecast_budget(self, expenses: List[Dict], total_budget: Decimal) -> Dict:
        """Forecast budget trajectory."""
        if not expenses:
            return {"daily_average": 0, "projected_final_cost": 0}

        total_spent = sum(Decimal(str(e.get("amount", 0))) for e in expenses)
        days_passed = len(set(e.get("date") for e in expenses))

        if days_passed > 0:
            daily_average = total_spent / days_passed
            projected_final = daily_average * 30  # Assume 30-day trip
        else:
            daily_average = Decimal(0)
            projected_final = Decimal(0)

        return {
            "daily_average": float(daily_average),
            "projected_final_cost": float(projected_final),
            "on_budget": float(projected_final) <= float(total_budget),
        }
