"""Budget and expense routes."""

from decimal import Decimal

from database.store import store
from fastapi import APIRouter, Depends, HTTPException
from models.schemas import ExpenseCreate
from pydantic import BaseModel
from services.budget_service import BudgetService
from utils.auth_utils import get_current_user
from utils.helpers import calculate_trip_duration, json_safe

router = APIRouter(prefix="/api/budget", tags=["budget"])
service = BudgetService()


class SplitRequest(BaseModel):
    amount: float | None = None
    members: list[int] | None = None


@router.get("/{trip_id}")
async def get_budget(trip_id: int, current_user: dict = Depends(get_current_user)):
    trip = store.get("trips", trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    expenses = [
        expense for expense in store.expenses.values() if expense["trip_id"] == trip_id
    ]
    duration = calculate_trip_duration(trip["start_date"], trip["end_date"])
    members = [
        member for member in store.trip_members.values() if member["trip_id"] == trip_id
    ]
    estimate = service.calculate_trip_budget(
        trip["destination"],
        duration,
        max(len(members), 1),
        "mid-range",
    )
    analytics = service.get_budget_analytics(
        expenses,
        Decimal(str(trip.get("budget") or estimate["group_total"]["with_contingency"])),
    )
    return json_safe(
        {"estimate": estimate, "expenses": expenses, "analytics": analytics}
    )


@router.post("/{trip_id}/add-expense", status_code=201)
async def add_expense(
    trip_id: int,
    payload: ExpenseCreate,
    current_user: dict = Depends(get_current_user),
):
    if not store.get("trips", trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    expense = store.insert("expenses", {"trip_id": trip_id, **payload.model_dump()})
    return expense


@router.post("/{trip_id}/split")
async def split_expenses(
    trip_id: int,
    payload: SplitRequest,
    current_user: dict = Depends(get_current_user),
):
    expenses = [
        expense for expense in store.expenses.values() if expense["trip_id"] == trip_id
    ]
    members = payload.members or [
        member["user_id"]
        for member in store.trip_members.values()
        if member["trip_id"] == trip_id
    ]
    if not members:
        raise HTTPException(
            status_code=400, detail="No members available for splitting"
        )
    amount = (
        Decimal(str(payload.amount))
        if payload.amount
        else sum(Decimal(str(item["amount"])) for item in expenses)
    )
    equal_split = service.split_expense_equally(amount, len(members))
    settlements = service.calculate_settlements(expenses, members)
    return json_safe(
        {
            "amount": amount,
            "per_person": {
                members[index]: value for index, value in equal_split.items()
            },
            "settlements": settlements,
        }
    )
