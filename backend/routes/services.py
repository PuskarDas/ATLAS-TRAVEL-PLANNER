"""Direct service utility endpoints for demos and external API proxies."""

import logging
from decimal import Decimal
from typing import Optional

import httpx
from config import get_settings
from fastapi import APIRouter, Depends, HTTPException, Query
from models.schemas import (
    FlightEstimate,
    HotelEstimate,
    VisaRequirement,
    WeatherResponse,
)
from pydantic import BaseModel
from services.budget_service import BudgetService
from services.group_consensus_service import GroupConsensusService
from services.itinerary_service import ItineraryService
from services.nlp_service import NLPService
from services.recommendation_service import RecommendationService
from utils.auth_utils import get_current_user
from utils.helpers import json_safe

router = APIRouter(prefix="/api/services", tags=["services"])
settings = get_settings()
logger = logging.getLogger(__name__)

recommendations = RecommendationService()
itineraries = ItineraryService()
budgets = BudgetService()
nlp = NLPService()
consensus = GroupConsensusService()


# ─────────────────────────────────────────
# EXISTING ENDPOINTS
# ─────────────────────────────────────────


class ConsensusRequest(BaseModel):
    preferences: list[dict]


class BudgetOptimizeRequest(BaseModel):
    available_budget: float
    preferences: dict = {}
    duration_days: int = 5


@router.post("/consensus")
async def aggregate_consensus(
    payload: ConsensusRequest, current_user: dict = Depends(get_current_user)
):
    return consensus.aggregate_preferences(payload.preferences)


@router.post("/budget/optimize")
async def optimize_budget(
    payload: BudgetOptimizeRequest, current_user: dict = Depends(get_current_user)
):
    return json_safe(
        budgets.optimize_budget(
            Decimal(str(payload.available_budget)),
            payload.preferences,
            payload.duration_days,
        )
    )


@router.post("/trip-plan")
async def trip_plan(
    payload: BudgetOptimizeRequest, current_user: dict = Depends(get_current_user)
):
    return recommendations.get_personalized_trip_plan(
        payload.preferences, int(payload.available_budget), payload.duration_days
    )


# ─────────────────────────────────────────
# NEW: WEATHER ENDPOINT
# ─────────────────────────────────────────


@router.get("/weather/{city}")
async def get_weather(city: str, current_user: dict = Depends(get_current_user)):
    """
    Get weather forecast for a city.
    Proxies OpenWeatherMap API if key available, else returns mock data.
    """
    api_key = settings.openweather_api_key

    if not api_key:
        # Return realistic mock data
        return {
            "city": city,
            "temperature": 28,
            "feels_like": 31,
            "description": "Partly cloudy",
            "humidity": 65,
            "wind_speed": 12.5,
            "icon": "02d",
            "forecast": [
                {"day": "Mon", "high": 30, "low": 24, "icon": "01d"},
                {"day": "Tue", "high": 28, "low": 22, "icon": "10d"},
                {"day": "Wed", "high": 26, "low": 21, "icon": "09d"},
                {"day": "Thu", "high": 29, "low": 23, "icon": "01d"},
                {"day": "Fri", "high": 31, "low": 25, "icon": "02d"},
            ],
        }

    async with httpx.AsyncClient() as client:
        try:
            # Current weather
            res = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": api_key, "units": "metric"},
                timeout=8,
            )

            if res.status_code != 200:
                logger.warning(f"OpenWeatherMap API error: {res.status_code}")
                raise HTTPException(status_code=502, detail="Weather API error")

            data = res.json()

            # 5-day forecast
            forecast_res = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={
                    "q": city,
                    "appid": api_key,
                    "units": "metric",
                    "cnt": 40,
                },
                timeout=8,
            )

            forecast_data = (
                forecast_res.json() if forecast_res.status_code == 200 else {"list": []}
            )

            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            forecast = []
            seen_days = set()

            for item in forecast_data.get("list", []):
                day_index = len(seen_days) % 7
                day_name = days[day_index]

                if day_name not in seen_days and len(forecast) < 5:
                    seen_days.add(day_name)
                    forecast.append(
                        {
                            "day": day_name,
                            "high": round(item["main"]["temp_max"]),
                            "low": round(item["main"]["temp_min"]),
                            "icon": item["weather"][0]["icon"],
                        }
                    )

            return {
                "city": data["name"],
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"], 1),
                "icon": data["weather"][0]["icon"],
                "forecast": forecast,
            }

        except httpx.TimeoutException:
            logger.error("OpenWeatherMap API timeout")
            raise HTTPException(status_code=504, detail="Weather API timeout")
        except Exception as e:
            logger.error(f"Weather API error: {str(e)}")
            raise HTTPException(status_code=502, detail="Weather service unavailable")


# ─────────────────────────────────────────
# NEW: FLIGHT ESTIMATES
# ─────────────────────────────────────────


@router.get("/flights")
async def get_flight_estimates(
    origin: str = Query(...),
    destination: str = Query(...),
    date: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    """
    Get flight price estimates for origin → destination.
    Provides realistic estimates based on route categories.
    """

    budget_destinations = {
        "Goa",
        "Jaipur",
        "Kerala",
        "Bali",
        "Bangkok",
        "Hanoi",
        "Ho Chi Minh",
    }
    mid_destinations = {
        "Singapore",
        "Dubai",
        "Istanbul",
        "Seoul",
        "Tokyo",
        "Hong Kong",
        "Barcelona",
    }
    premium_destinations = {
        "New York",
        "London",
        "Paris",
        "Sydney",
        "Los Angeles",
        "Toronto",
    }

    if destination in budget_destinations:
        price_range = "$80 - $250"
        cheapest = 80
        average = 165
    elif destination in mid_destinations:
        price_range = "$300 - $700"
        cheapest = 300
        average = 500
    elif destination in premium_destinations:
        price_range = "$600 - $1500"
        cheapest = 600
        average = 1100
    else:
        price_range = "$200 - $800"
        cheapest = 200
        average = 500

    return {
        "origin": origin,
        "destination": destination,
        "price_range": price_range,
        "cheapest": cheapest,
        "average": average,
        "currency": "USD",
        "note": "Estimates only. Check Google Flights or Skyscanner for live prices.",
        "airlines": [
            "Emirates",
            "Lufthansa",
            "Singapore Airlines",
            "IndiGo",
            "Air India",
        ],
    }


# ─────────────────────────────────────────
# NEW: HOTEL ESTIMATES
# ─────────────────────────────────────────


@router.get("/hotels")
async def get_hotel_estimates(
    destination: str = Query(...),
    checkin: Optional[str] = Query(None),
    checkout: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    """
    Get hotel price estimates for destination.
    Returns budget, midrange, and luxury options.
    """

    budget_destinations = {"Goa", "Jaipur", "Kerala", "Bali", "Bangkok", "Hanoi"}

    if destination in budget_destinations:
        budget = "$15 - $40/night"
        midrange = "$40 - $100/night"
        luxury = "$100 - $300/night"
    else:
        budget = "$40 - $80/night"
        midrange = "$80 - $200/night"
        luxury = "$200 - $600/night"

    return {
        "destination": destination,
        "budget_range": budget,
        "midrange_range": midrange,
        "luxury_range": luxury,
        "currency": "USD",
        "note": "Estimates only. Check Booking.com or Hotels.com for live availability.",
        "popular_areas": ["City Center", "Tourist District", "Beach Area", "Old Town"],
    }


# ─────────────────────────────────────────
# NEW: VISA REQUIREMENTS
# ─────────────────────────────────────────

# Visa data for common passport/destination combinations
VISA_DATA = {
    ("US", "Japan"): {
        "required": False,
        "duration": "90 days",
        "type": "Visa-free",
        "notes": "Passport valid for duration of stay.",
    },
    ("US", "India"): {
        "required": True,
        "duration": "30-180 days",
        "type": "e-Visa",
        "notes": "Apply online at indianvisaonline.gov.in",
    },
    ("US", "France"): {
        "required": False,
        "duration": "90 days",
        "type": "Schengen visa-free",
        "notes": "Part of Schengen area.",
    },
    ("IN", "Bali"): {
        "required": False,
        "duration": "30 days",
        "type": "Visa on Arrival",
        "notes": "Free VOA for Indian passport holders.",
    },
    ("IN", "Thailand"): {
        "required": False,
        "duration": "30 days",
        "type": "Visa-free",
        "notes": "Recently established visa-free agreement.",
    },
    ("IN", "Singapore"): {
        "required": True,
        "duration": "30 days",
        "type": "Tourist Visa",
        "notes": "Apply at Singapore Embassy or online.",
    },
    ("IN", "Dubai"): {
        "required": True,
        "duration": "30/90 days",
        "type": "UAE Tourist Visa",
        "notes": "Apply through airline or hotel.",
    },
    ("IN", "UK"): {
        "required": True,
        "duration": "6 months",
        "type": "Standard Visitor Visa",
        "notes": "Apply at UKVI.",
    },
    ("IN", "US"): {
        "required": True,
        "duration": "Up to 10 years",
        "type": "B1/B2 Visa",
        "notes": "Interview required at US Embassy.",
    },
    ("IN", "Japan"): {
        "required": True,
        "duration": "15 days",
        "type": "Tourist Visa",
        "notes": "Apply at Japanese Embassy/Consulate.",
    },
    ("IN", "France"): {
        "required": True,
        "duration": "90 days",
        "type": "Schengen Visa",
        "notes": "Apply at French consulate/VFS Global.",
    },
    ("GB", "US"): {
        "required": True,
        "duration": "Up to 10 years",
        "type": "ESTA/Visitor Visa",
        "notes": "ESTA for short trips, visa for longer stays.",
    },
    ("AU", "Japan"): {
        "required": False,
        "duration": "90 days",
        "type": "Visa-free",
        "notes": "Australian passport holders visa-exempt.",
    },
}


@router.get("/visa")
async def get_visa_requirements(
    passport: str = Query(..., description="Passport country code (e.g., IN, US, GB)"),
    destination: str = Query(..., description="Destination country/city"),
    current_user: dict = Depends(get_current_user),
):
    """
    Get visa requirements for a passport/destination combination.
    """

    passport_code = passport.upper()
    dest_code = destination.upper()

    # Try exact match first
    data = VISA_DATA.get((passport_code, dest_code))

    # Try with normalized destination (first word only)
    if not data:
        dest_first_word = destination.split(",")[0].strip().upper()
        data = VISA_DATA.get((passport_code, dest_first_word))

    if not data:
        return {
            "passport_country": passport_code,
            "destination": destination,
            "visa_required": None,
            "visa_type": "Unknown",
            "duration": "N/A",
            "notes": f"Visa info not available. Check https://www.visadb.io or your country's embassy website.",
        }

    return {
        "passport_country": passport_code,
        "destination": destination,
        "visa_required": data["required"],
        "visa_type": data["type"],
        "duration": data["duration"],
        "notes": data["notes"],
    }


# ─────────────────────────────────────────
# NEW: LOCAL ATTRACTIONS (Overpass API)
# ─────────────────────────────────────────


@router.get("/attractions")
async def get_attractions(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: int = Query(2000, ge=500, le=5000),
    current_user: dict = Depends(get_current_user),
):
    """
    Fetch local attractions near coordinates via Overpass API.
    Returns museums, restaurants, parks, hotels, etc.
    """

    # Overpass API query for attractions
    query = f"""
    [out:json][timeout:10];
    (
      node["tourism"~"museum|attraction|viewpoint|gallery|zoo|theme_park|information"](around:{radius},{lat},{lon});
      node["amenity"~"restaurant|cafe|bar|pub|fast_food"](around:{radius},{lat},{lon});
      node["leisure"~"park|garden|playground|swimming_pool"](around:{radius},{lat},{lon});
      node["shop"~"mall|supermarket|department_store|market"](around:{radius},{lat},{lon});
      node["tourism"~"hotel|hostel|guest_house|apartment"](around:{radius},{lat},{lon});
    );
    out body 50;
    """

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                "https://overpass-api.de/api/interpreter",
                data={"data": query},
                timeout=15,
            )

            if res.status_code != 200:
                logger.warning(f"Overpass API error: {res.status_code}")
                return {"attractions": []}

            elements = res.json().get("elements", [])
            attractions = []

            for el in elements[:50]:
                tags = el.get("tags", {})
                name = tags.get("name")

                if not name:
                    continue

                # Determine category
                category = "attraction"
                if "tourism" in tags:
                    category = tags["tourism"]
                elif tags.get("amenity") in (
                    "restaurant",
                    "cafe",
                    "bar",
                    "pub",
                    "fast_food",
                ):
                    category = tags["amenity"]
                elif "leisure" in tags:
                    category = "park"
                elif "shop" in tags:
                    category = "shopping"

                attractions.append(
                    {
                        "name": name,
                        "lat": el.get("lat"),
                        "lon": el.get("lon"),
                        "category": category,
                        "cuisine": tags.get("cuisine"),
                        "opening_hours": tags.get("opening_hours"),
                        "website": tags.get("website"),
                    }
                )

            logger.info(f"Found {len(attractions)} attractions near {lat}, {lon}")
            return {"attractions": attractions}

        except httpx.TimeoutException:
            logger.error("Overpass API timeout")
            return {"attractions": [], "error": "Request timeout"}
        except Exception as e:
            logger.error(f"Attractions API error: {str(e)}")
            return {"attractions": [], "error": str(e)}