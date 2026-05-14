"""Trip CRUD and membership routes + group voting."""

from database.store import store
from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import TripCreate, TripMemberCreate, TripUpdate, VoteCreate
from pydantic import BaseModel
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/api/trips", tags=["trips"])


def _trip_with_related(trip: dict) -> dict:
    members = [
        member
        for member in store.trip_members.values()
        if member["trip_id"] == trip["id"]
    ]
    itinerary = next(
        (item for item in store.itineraries.values() if item["trip_id"] == trip["id"]),
        None,
    )
    expenses = [
        expense
        for expense in store.expenses.values()
        if expense["trip_id"] == trip["id"]
    ]
    return {**trip, "members": members, "itinerary": itinerary, "expenses": expenses}


def _can_access(trip: dict, user_id: int) -> bool:
    if trip["creator_id"] == user_id:
        return True
    return any(
        member["trip_id"] == trip["id"] and member["user_id"] == user_id
        for member in store.trip_members.values()
    )


@router.get("")
async def list_trips(current_user: dict = Depends(get_current_user)):
    trips = [
        _trip_with_related(trip)
        for trip in store.trips.values()
        if _can_access(trip, current_user["id"])
    ]
    return {"trips": trips, "total_count": len(trips)}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_trip(
    payload: TripCreate, current_user: dict = Depends(get_current_user)
):
    trip = store.insert(
        "trips",
        {
            **payload.model_dump(),
            "creator_id": current_user["id"],
            "status": "planning",
        },
    )
    store.insert(
        "trip_members",
        {"trip_id": trip["id"], "user_id": current_user["id"], "role": "owner"},
    )
    return _trip_with_related(trip)


@router.get("/{trip_id}")
async def get_trip(trip_id: int, current_user: dict = Depends(get_current_user)):
    trip = store.get("trips", trip_id)
    if not trip or not _can_access(trip, current_user["id"]):
        raise HTTPException(status_code=404, detail="Trip not found")
    return _trip_with_related(trip)


@router.put("/{trip_id}")
async def update_trip(
    trip_id: int, payload: TripUpdate, current_user: dict = Depends(get_current_user)
):
    trip = store.get("trips", trip_id)
    if not trip or trip["creator_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Trip not found")
    updated = store.update("trips", trip_id, payload.model_dump())
    return _trip_with_related(updated)


@router.delete("/{trip_id}")
async def delete_trip(trip_id: int, current_user: dict = Depends(get_current_user)):
    trip = store.get("trips", trip_id)
    if not trip or trip["creator_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Trip not found")
    store.delete("trips", trip_id)
    return {"message": "Trip deleted"}


@router.post("/{trip_id}/members", status_code=status.HTTP_201_CREATED)
async def add_member(
    trip_id: int,
    payload: TripMemberCreate,
    current_user: dict = Depends(get_current_user),
):
    trip = store.get("trips", trip_id)
    if not trip or trip["creator_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Trip not found")
    if not store.get("users", payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    member = store.insert("trip_members", {"trip_id": trip_id, **payload.model_dump()})
    return member


# ─────────────────────────────────────────
# GROUP VOTING ENDPOINTS
# ─────────────────────────────────────────


@router.post("/{trip_id}/vote", status_code=status.HTTP_201_CREATED)
async def vote_destination(
    trip_id: int,
    payload: VoteCreate,
    current_user: dict = Depends(get_current_user),
):
    """
    Vote on a destination for the trip.
    Each user can vote once per destination (updates previous vote).
    """
    trip = store.get("trips", trip_id)
    if not trip or not _can_access(trip, current_user["id"]):
        raise HTTPException(status_code=404, detail="Trip not found")

    # Remove existing vote from this user for this destination
    if hasattr(store, "votes"):
        existing_votes = [
            v
            for v in store.votes.values()
            if v["trip_id"] == trip_id
            and v["user_id"] == current_user["id"]
            and v["destination"] == payload.destination
        ]
        for v in existing_votes:
            store.delete("votes", v["id"])

        vote = store.insert(
            "votes",
            {
                "trip_id": trip_id,
                "user_id": current_user["id"],
                "destination": payload.destination,
                "score": payload.score,
                "comment": payload.comment,
            },
        )
        return vote
    else:
        raise HTTPException(status_code=501, detail="Voting not enabled")


@router.get("/{trip_id}/votes")
async def get_votes(trip_id: int, current_user: dict = Depends(get_current_user)):
    """
    Get all votes for a trip, aggregated by destination.
    """
    trip = store.get("trips", trip_id)
    if not trip or not _can_access(trip, current_user["id"]):
        raise HTTPException(status_code=404, detail="Trip not found")

    if not hasattr(store, "votes"):
        return {"votes": [], "aggregated": [], "total_votes": 0}

    votes = [v for v in store.votes.values() if v["trip_id"] == trip_id]

    # Aggregate by destination
    aggregated = {}
    for vote in votes:
        dest = vote["destination"]
        if dest not in aggregated:
            aggregated[dest] = {
                "destination": dest,
                "total_score": 0,
                "vote_count": 0,
                "average": 0.0,
                "votes": [],
            }
        aggregated[dest]["total_score"] += vote["score"]
        aggregated[dest]["vote_count"] += 1
        aggregated[dest]["votes"].append(vote)

    for dest in aggregated:
        aggregated[dest]["average"] = round(
            aggregated[dest]["total_score"] / aggregated[dest]["vote_count"], 1
        )

    # Sort by average score
    aggregated_list = sorted(
        aggregated.values(), key=lambda x: x["average"], reverse=True
    )

    return {
        "votes": votes,
        "aggregated": aggregated_list,
        "total_votes": len(votes),
    }