"""Pydantic request/response schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """User response schema."""

    id: int
    profile_picture: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Authentication Schemas
class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserResponse


# User Preference Schemas
class UserPreferenceCreate(BaseModel):
    """User preference creation schema."""

    preferred_destinations: Optional[List[str]] = None
    preferred_activities: Optional[List[str]] = None
    budget_range: Optional[str] = None
    travel_style: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None
    mobility_needs: Optional[str] = None


class UserPreferenceResponse(UserPreferenceCreate):
    """User preference response schema."""

    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Trip Schemas
class TripBase(BaseModel):
    """Base trip schema."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    destination: str = Field(..., min_length=1)
    start_date: datetime
    end_date: datetime
    budget: Optional[int] = None
    is_group: bool = False
    traveler_count: int = Field(default=2, ge=1, le=99)


class TripCreate(TripBase):
    """Trip creation schema."""

    pass


class TripUpdate(BaseModel):
    """Trip update schema."""

    title: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[int] = None
    status: Optional[str] = None
    traveler_count: Optional[int] = Field(None, ge=1, le=99)


class TripResponse(TripBase):
    """Trip response schema."""

    id: int
    creator_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Trip Member Schemas
class TripMemberCreate(BaseModel):
    """Trip member creation schema."""

    user_id: int
    role: str = "member"


class TripMemberResponse(BaseModel):
    """Trip member response schema."""

    id: int
    trip_id: int
    user_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


# Itinerary Schemas
class ItineraryBase(BaseModel):
    """Base itinerary schema."""

    title: Optional[str] = None
    description: Optional[str] = None


class ItineraryCreate(ItineraryBase):
    """Itinerary creation schema."""

    data: dict  # Day-wise activities


class ItineraryResponse(ItineraryBase):
    """Itinerary response schema."""

    id: int
    trip_id: int
    data: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Expense Schemas
class ExpenseCreate(BaseModel):
    """Expense creation schema."""

    description: str = Field(..., min_length=1)
    amount: int = Field(..., gt=0)
    category: str
    paid_by: int


class ExpenseResponse(ExpenseCreate):
    """Expense response schema."""

    id: int
    trip_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationRequest(BaseModel):
    """Recommendation request schema."""

    destination: Optional[str] = None
    budget: Optional[int] = None
    travel_style: Optional[str] = None
    activities: Optional[List[str]] = None
    duration_days: Optional[int] = None


class Recommendation(BaseModel):
    """Single recommendation."""

    name: str
    type: str  # destination, activity, hotel, etc.
    rating: float
    description: str
    price_range: Optional[str] = None
    match_score: float


class RecommendationResponse(BaseModel):
    """Recommendation response schema."""

    recommendations: List[Recommendation]
    total_count: int


# Chatbot Schemas
class ChatMessage(BaseModel):
    """Chat message schema."""

    user_id: int
    trip_id: int
    message: str
    timestamp: Optional[datetime] = None


class ChatResponse(BaseModel):
    """Chat response schema."""

    user_message: str
    bot_response: str
    intent: str
    confidence: float
    timestamp: datetime


# ─────────────────────────────────────────
# NEW SCHEMAS FOR ADDITIONAL FEATURES
# ─────────────────────────────────────────

# Voting Schemas
class VoteCreate(BaseModel):
    """Create a destination vote."""

    destination: str
    score: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    comment: Optional[str] = None


class VoteResponse(VoteCreate):
    """Vote response."""

    id: int
    trip_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class VoteAggregated(BaseModel):
    """Aggregated votes for a destination."""

    destination: str
    total_score: int
    vote_count: int
    average: float
    votes: List[VoteResponse]


# Packing List Schemas
class PackingItem(BaseModel):
    """Single packing item."""

    id: int
    name: str
    category: str
    checked: bool = False
    quantity: int = 1


class PackingListResponse(BaseModel):
    """Packing list response."""

    trip_id: int
    items: List[PackingItem]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Weather Schemas
class WeatherForecastDay(BaseModel):
    """Single day forecast."""

    day: str
    high: int
    low: int
    icon: str


class WeatherResponse(BaseModel):
    """Weather API response."""

    city: str
    temperature: int
    feels_like: int
    description: str
    humidity: int
    wind_speed: float
    icon: str
    forecast: List[WeatherForecastDay] = []


# Flight Schemas
class FlightEstimate(BaseModel):
    """Flight price estimate."""

    origin: str
    destination: str
    price_range: str
    cheapest: int
    average: int
    currency: str = "USD"
    note: str = ""
    airlines: List[str] = []


# Hotel Schemas
class HotelEstimate(BaseModel):
    """Hotel price estimate."""

    destination: str
    budget_range: str
    midrange_range: str
    luxury_range: str
    currency: str = "USD"
    note: str = ""
    popular_areas: List[str] = []


# Visa Schemas
class VisaRequirement(BaseModel):
    """Visa requirement info."""

    passport_country: str
    destination: str
    visa_required: Optional[bool] = None
    visa_type: Optional[str] = None
    duration: Optional[str] = None
    notes: str


# Attraction Schemas
class Attraction(BaseModel):
    """Local attraction."""

    name: str
    lat: float
    lon: float
    category: str  # museum, restaurant, park, etc.
    cuisine: Optional[str] = None
    opening_hours: Optional[str] = None
    website: Optional[str] = None


class AttractionsResponse(BaseModel):
    """Attractions response."""

    attractions: List[Attraction]
    error: Optional[str] = None