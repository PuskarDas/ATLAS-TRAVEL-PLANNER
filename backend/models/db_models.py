"""Database models for SQLAlchemy/Mongoose."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile_picture = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trips = relationship("Trip", back_populates="creator")
    preferences = relationship("UserPreference", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class UserPreference(Base):
    """User preferences model."""

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    preferred_destinations = Column(String(500))  # JSON string
    preferred_activities = Column(String(500))
    budget_range = Column(String(50))
    travel_style = Column(String(50))  # luxury, budget, adventure, etc.
    dietary_restrictions = Column(String(500))
    mobility_needs = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference user_id={self.user_id}>"


class Trip(Base):
    """Trip model."""

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    destination = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    budget = Column(Integer)  # in USD
    status = Column(
        String(20), default="planning"
    )  # planning, approved, ongoing, completed
    is_group = Column(Boolean, default=False)
    traveler_count = Column(Integer, nullable=False, default=2)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="trips")
    members = relationship("TripMember", back_populates="trip")
    itinerary = relationship("Itinerary", back_populates="trip")
    expenses = relationship("Expense", back_populates="trip")

    def __repr__(self):
        return f"<Trip {self.title}>"


class TripMember(Base):
    """Trip member model."""

    __tablename__ = "trip_members"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    role = Column(String(50), default="member")  # admin, member
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="members")

    def __repr__(self):
        return f"<TripMember trip_id={self.trip_id} user_id={self.user_id}>"


class Itinerary(Base):
    """Itinerary model."""

    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    title = Column(String(200))
    description = Column(String(1000))
    data = Column(String(5000))  # JSON string for day-wise activities
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="itinerary")

    def __repr__(self):
        return f"<Itinerary trip_id={self.trip_id}>"


class Expense(Base):
    """Expense model."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Integer, nullable=False)  # in USD cents
    category = Column(String(50))  # accommodation, food, transport, activity, etc.
    paid_by = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.description}>"
"""Database models for SQLAlchemy/Mongoose."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile_picture = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trips = relationship("Trip", back_populates="creator")
    preferences = relationship("UserPreference", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class UserPreference(Base):
    """User preferences model."""

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    preferred_destinations = Column(String(500))  # JSON string
    preferred_activities = Column(String(500))
    budget_range = Column(String(50))
    travel_style = Column(String(50))  # luxury, budget, adventure, etc.
    dietary_restrictions = Column(String(500))
    mobility_needs = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference user_id={self.user_id}>"


class Trip(Base):
    """Trip model."""

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    destination = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    budget = Column(Integer)  # in USD
    status = Column(
        String(20), default="planning"
    )  # planning, approved, ongoing, completed
    is_group = Column(Boolean, default=False)
    traveler_count = Column(Integer, nullable=False, default=2)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="trips")
    members = relationship("TripMember", back_populates="trip")
    itinerary = relationship("Itinerary", back_populates="trip")
    expenses = relationship("Expense", back_populates="trip")

    def __repr__(self):
        return f"<Trip {self.title}>"


class TripMember(Base):
    """Trip member model."""

    __tablename__ = "trip_members"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    role = Column(String(50), default="member")  # admin, member
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="members")

    def __repr__(self):
        return f"<TripMember trip_id={self.trip_id} user_id={self.user_id}>"


class Itinerary(Base):
    """Itinerary model."""

    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    title = Column(String(200))
    description = Column(String(1000))
    data = Column(String(5000))  # JSON string for day-wise activities
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="itinerary")

    def __repr__(self):
        return f"<Itinerary trip_id={self.trip_id}>"


class Expense(Base):
    """Expense model."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Integer, nullable=False)  # in USD cents
    category = Column(String(50))  # accommodation, food, transport, activity, etc.
    paid_by = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="expenses")

    def __repr__(self):
        return f"<Expense {self.description}>"


# ─────────────────────────────────────────
# NEW TABLES FOR ADDITIONAL FEATURES
# ─────────────────────────────────────────

class Vote(Base):
    """Group destination voting model."""

    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    destination = Column(String(200), nullable=False)
    score = Column(Integer, default=5)  # 1-5 rating
    comment = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Vote trip_id={self.trip_id} destination={self.destination}>"


class PackingList(Base):
    """Trip packing list model."""

    __tablename__ = "packing_lists"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, index=True, nullable=False, unique=True)
    items = Column(String(10000))  # JSON string with packing items
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PackingList trip_id={self.trip_id}>"