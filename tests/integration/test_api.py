def test_auth_trip_itinerary_budget_and_chat_flow(client, auth_headers):
    trip_response = client.post(
        "/api/trips",
        headers=auth_headers,
        json={
            "title": "Bali crew",
            "description": "Food and beaches",
            "destination": "Bali",
            "start_date": "2026-06-01T00:00:00",
            "end_date": "2026-06-04T00:00:00",
            "budget": 1600,
            "is_group": True,
        },
    )
    assert trip_response.status_code == 201
    trip = trip_response.json()

    trips = client.get("/api/trips", headers=auth_headers).json()
    assert trips["total_count"] == 1

    itinerary = client.post(
        "/api/itinerary/generate",
        headers=auth_headers,
        json={"trip_id": trip["id"], "preferences": {"interests": ["beach"]}},
    )
    assert itinerary.status_code == 200
    assert itinerary.json()["data"]["duration_days"] == 4

    expense = client.post(
        f"/api/budget/{trip['id']}/add-expense",
        headers=auth_headers,
        json={"description": "Dinner", "amount": 80, "category": "food", "paid_by": 1},
    )
    assert expense.status_code == 201

    budget = client.get(f"/api/budget/{trip['id']}", headers=auth_headers)
    assert budget.status_code == 200
    assert budget.json()["analytics"]["total_spent"] == 80

    chat = client.post(
        "/api/chat/message",
        headers=auth_headers,
        json={"user_id": 1, "trip_id": trip["id"], "message": "Suggest activities"},
    )
    assert chat.status_code == 200
    assert "bot_response" in chat.json()


def test_demo_login_user_is_available_after_startup(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "planner@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "planner"


def test_recommendation_endpoint_requires_auth(client):
    response = client.post(
        "/api/recommendations/destinations", json={"activities": ["food"]}
    )
    assert response.status_code == 401
