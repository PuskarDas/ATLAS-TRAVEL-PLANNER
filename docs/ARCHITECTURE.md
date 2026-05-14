# Architecture

The application is split into three working parts:

- `backend/`: FastAPI REST API, JWT auth, WebSocket trip updates, service layer, and local in-memory storage.
- `frontend/`: Vite React dashboard for auth, trip creation, itinerary generation, budget tracking, chatbot, and Leaflet maps.
- `ml_training/`: Synthetic data generation, recommendation model training, and evaluation notebooks.

The backend currently uses `database/store.py` for demo-friendly in-memory persistence. Replace that repository layer with SQLAlchemy or MongoDB when you need durable production storage.
