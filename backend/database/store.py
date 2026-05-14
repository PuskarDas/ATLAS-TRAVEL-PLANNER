"""In-memory data store for local development and testing.

The project can later swap this for SQLAlchemy repositories without changing
the route contracts.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any


class InMemoryStore:
    """Tiny repository with auto-incrementing integer identifiers."""

    def __init__(self) -> None:
        self.reset()
        self.votes = {}
        self.packing_lists = {}

    def reset(self) -> None:
        self.users: dict[int, dict[str, Any]] = {}
        self.trips: dict[int, dict[str, Any]] = {}
        self.trip_members: dict[int, dict[str, Any]] = {}
        self.itineraries: dict[int, dict[str, Any]] = {}
        self.expenses: dict[int, dict[str, Any]] = {}
        self.chat_history: dict[int, list[dict[str, Any]]] = {}
        self.refresh_tokens: dict[str, int] = {}
        self._counters = {
            "users": 1,
            "trips": 1,
            "trip_members": 1,
            "itineraries": 1,
            "expenses": 1,
        }

    def next_id(self, bucket: str) -> int:
        next_value = self._counters[bucket]
        self._counters[bucket] += 1
        return next_value

    def insert(self, bucket: str, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.utcnow()
        item = deepcopy(payload)
        item["id"] = self.next_id(bucket)
        item.setdefault("created_at", now)
        item.setdefault("updated_at", now)
        getattr(self, bucket)[item["id"]] = item
        return deepcopy(item)

    def update(
        self, bucket: str, item_id: int, payload: dict[str, Any]
    ) -> dict[str, Any] | None:
        collection = getattr(self, bucket)
        if item_id not in collection:
            return None
        for key, value in payload.items():
            if value is not None:
                collection[item_id][key] = value
        collection[item_id]["updated_at"] = datetime.utcnow()
        return deepcopy(collection[item_id])

    def get(self, bucket: str, item_id: int) -> dict[str, Any] | None:
        item = getattr(self, bucket).get(item_id)
        return deepcopy(item) if item else None

    def delete(self, bucket: str, item_id: int) -> bool:
        collection = getattr(self, bucket)
        if item_id not in collection:
            return False
        del collection[item_id]
        return True


store = InMemoryStore()
# In store.py, add to the Store class __init__:
