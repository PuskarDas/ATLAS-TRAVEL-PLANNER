"""Itinerary generation routes + packing list management."""

import json
import logging

from database.store import store
from fastapi import APIRouter, Depends, HTTPException
from models.schemas import PackingListResponse
from pydantic import BaseModel
from services.itinerary_service import ItineraryService
from utils.auth_utils import get_current_user
from utils.helpers import calculate_trip_duration

router = APIRouter(prefix="/api/itinerary", tags=["itinerary"])
service = ItineraryService()
logger = logging.getLogger(__name__)


class GenerateItineraryRequest(BaseModel):
    trip_id: int
    preferences: dict = {}


class UpdateItineraryRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    data: dict


class ToggleParkingItemRequest(BaseModel):
    checked: bool


# ─────────────────────────────────────────
# EXISTING: ITINERARY GENERATION
# ─────────────────────────────────────────


@router.post("/generate")
async def generate(
    payload: GenerateItineraryRequest, current_user: dict = Depends(get_current_user)
):
    trip = store.get("trips", payload.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    data = service.generate_itinerary(
        trip["destination"],
        trip["start_date"],
        trip["end_date"],
        payload.preferences,
        trip.get("budget"),
    )

    existing = next(
        (
            item
            for item in store.itineraries.values()
            if item["trip_id"] == trip["id"]
        ),
        None,
    )

    fields = {
        "trip_id": trip["id"],
        "title": f"{trip['destination']} itinerary",
        "description": "AI-generated itinerary",
        "data": data,
    }

    if existing:
        return store.update("itineraries", existing["id"], fields)
    return store.insert("itineraries", fields)


@router.get("/{trip_id}")
async def get_itinerary(trip_id: int, current_user: dict = Depends(get_current_user)):
    itinerary = next(
        (
            item
            for item in store.itineraries.values()
            if item["trip_id"] == trip_id
        ),
        None,
    )
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary


@router.put("/{trip_id}")
async def update_itinerary(
    trip_id: int,
    payload: UpdateItineraryRequest,
    current_user: dict = Depends(get_current_user),
):
    itinerary = next(
        (
            item
            for item in store.itineraries.values()
            if item["trip_id"] == trip_id
        ),
        None,
    )
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return store.update("itineraries", itinerary["id"], payload.model_dump())


# ─────────────────────────────────────────
# NEW: PACKING LIST GENERATION & MANAGEMENT
# ─────────────────────────────────────────

# Packing templates by destination type
PACKING_TEMPLATES = {
    "beach": [
        "Swimsuit",
        "Sunscreen SPF 50+",
        "Beach towel",
        "Flip flops",
        "Sunglasses",
        "Sun hat",
        "Waterproof bag",
        "Aloe vera gel",
    ],
    "cold": [
        "Winter jacket",
        "Thermal underwear",
        "Wool gloves",
        "Warm socks",
        "Scarf",
        "Winter boots",
        "Hat",
        "Hand warmer",
    ],
    "business": [
        "Formal shirts",
        "Dress pants",
        "Blazer",
        "Formal shoes",
        "Business cards",
        "Laptop",
        "Portfolio",
    ],
    "adventure": [
        "Hiking boots",
        "Backpack (50L+)",
        "Water bottle",
        "First aid kit",
        "Rain jacket",
        "Hiking socks",
        "Insect repellent",
        "Headlamp",
    ],
    "general": [
        "Passport",
        "Travel insurance docs",
        "Phone charger",
        "Power bank",
        "Universal adapter",
        "Medications",
        "Travel-size toiletries",
        "Phone",
    ],
}

# Destination profiles (which templates to use)
DESTINATION_PROFILES = {
    "Bali": ["beach", "adventure"],
    "Goa": ["beach"],
    "Kerala": ["beach", "adventure"],
    "Jaipur": ["adventure"],
    "Tokyo": ["general"],
    "Paris": ["general"],
    "London": ["cold", "general"],
    "Dubai": ["general"],
    "Santorini": ["beach"],
    "Cape Town": ["adventure"],
    "Sydney": ["beach", "adventure"],
    "Seoul": ["general"],
    "Istanbul": ["general"],
    "Bangkok": ["beach"],
    "Singapore": ["general"],
    "New York": ["general"],
    "Barcelona": ["beach"],
}


@router.post("/packing-list/{trip_id}", status_code=201)
async def generate_packing_list(
    trip_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Generate a packing list for the trip based on destination and duration.
    """
    trip = store.get("trips", trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    destination = trip.get("destination", "")
    profiles = DESTINATION_PROFILES.get(destination, ["general"])

    items = []
    item_id = 1
    categories_added = set()

    # Always include general items first
    if "general" not in profiles:
        profiles = list(profiles) + ["general"]

    for profile in profiles:
        template = PACKING_TEMPLATES.get(profile, [])
        category = profile.capitalize()

        if category not in categories_added:
            categories_added.add(category)
            for item_name in template:
                items.append(
                    {
                        "id": item_id,
                        "name": item_name,
                        "category": category,
                        "checked": False,
                        "quantity": 1,
                    }
                )
                item_id += 1

    # Add clothing based on trip duration
    try:
        duration = calculate_trip_duration(trip["start_date"], trip["end_date"])
        num_outfits = min(duration + 1, 7)

        for i in range(num_outfits):
            items.append(
                {
                    "id": item_id,
                    "name": f"Outfit {i + 1}",
                    "category": "Clothing",
                    "checked": False,
                    "quantity": 1,
                }
            )
            item_id += 1
    except Exception as e:
        logger.warning(f"Could not calculate trip duration: {str(e)}")

    # Store it
    if hasattr(store, "packing_lists"):
        existing = next(
            (p for p in store.packing_lists.values() if p["trip_id"] == trip_id),
            None,
        )

        fields = {"trip_id": trip_id, "items": json.dumps(items)}

        if existing:
            result = store.update("packing_lists", existing["id"], fields)
        else:
            result = store.insert("packing_lists", fields)

        return {"trip_id": trip_id, "items": items}
    else:
        logger.warning("Packing lists table not available")
        return {"trip_id": trip_id, "items": items, "warning": "Data not persisted"}


@router.get("/packing-list/{trip_id}")
async def get_packing_list(
    trip_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Get the packing list for a trip.
    """
    trip = store.get("trips", trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if not hasattr(store, "packing_lists"):
        raise HTTPException(
            status_code=503, detail="Packing list feature not available"
        )

    packing = next(
        (p for p in store.packing_lists.values() if p["trip_id"] == trip_id), None
    )

    if not packing:
        raise HTTPException(
            status_code=404,
            detail="Packing list not found. Generate one first.",
        )

    items = (
        json.loads(packing["items"])
        if isinstance(packing["items"], str)
        else packing["items"]
    )

    return {
        "trip_id": trip_id,
        "items": items,
        "created_at": packing.get("created_at"),
    }


@router.patch("/packing-list/{trip_id}/item/{item_id}")
async def toggle_packing_item(
    trip_id: int,
    item_id: int,
    payload: ToggleParkingItemRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Toggle the checked status of a packing list item.
    """
    trip = store.get("trips", trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if not hasattr(store, "packing_lists"):
        raise HTTPException(
            status_code=503, detail="Packing list feature not available"
        )

    packing = next(
        (p for p in store.packing_lists.values() if p["trip_id"] == trip_id), None
    )

    if not packing:
        raise HTTPException(status_code=404, detail="Packing list not found")

    items = (
        json.loads(packing["items"])
        if isinstance(packing["items"], str)
        else packing["items"]
    )

    # Find and update the item
    found = False
    for item in items:
        if item["id"] == item_id:
            item["checked"] = payload.checked
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the packing list
    store.update("packing_lists", packing["id"], {"items": json.dumps(items)})

    return {"success": True, "item_id": item_id, "checked": payload.checked}


@router.delete("/packing-list/{trip_id}/item/{item_id}")
async def delete_packing_item(
    trip_id: int,
    item_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a packing list item.
    """
    trip = store.get("trips", trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if not hasattr(store, "packing_lists"):
        raise HTTPException(
            status_code=503, detail="Packing list feature not available"
        )

    packing = next(
        (p for p in store.packing_lists.values() if p["trip_id"] == trip_id), None
    )

    if not packing:
        raise HTTPException(status_code=404, detail="Packing list not found")

    items = (
        json.loads(packing["items"])
        if isinstance(packing["items"], str)
        else packing["items"]
    )

    # Remove the item
    items = [item for item in items if item["id"] != item_id]

    # Update the packing list
    store.update("packing_lists", packing["id"], {"items": json.dumps(items)})

    return {"success": True, "item_id": item_id}