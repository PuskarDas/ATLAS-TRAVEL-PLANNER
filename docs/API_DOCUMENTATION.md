# API Documentation

Interactive docs are available at `http://localhost:8000/api/docs` after starting the backend.

Core routes:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/trips`
- `POST /api/trips`
- `GET /api/trips/{trip_id}`
- `PUT /api/trips/{trip_id}`
- `DELETE /api/trips/{trip_id}`
- `POST /api/recommendations/destinations`
- `POST /api/recommendations/activities`
- `POST /api/recommendations/accommodations`
- `POST /api/itinerary/generate`
- `GET /api/budget/{trip_id}`
- `POST /api/budget/{trip_id}/add-expense`
- `POST /api/chat/message`
- `WS /ws/trips/{trip_id}`
