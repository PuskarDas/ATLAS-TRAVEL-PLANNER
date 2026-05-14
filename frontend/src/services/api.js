function resolveApiBase() {
  const fromEnv = import.meta.env.VITE_API_URL;
  if (fromEnv != null && String(fromEnv).trim() !== "") {
    return String(fromEnv).replace(/\/$/, "");
  }
  if (import.meta.env.PROD) {
    return "http://localhost:8000";
  }
  return "";
}

const API_URL = resolveApiBase();

let accessToken = localStorage.getItem("accessToken") || "";

export function setToken(token) {
  accessToken = token;
  localStorage.setItem("accessToken", token);
}

export function clearToken() {
  accessToken = "";
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        ...(options.headers || {}),
      },
    });
  } catch (error) {
    const hint =
      error && typeof error.message === "string" ? ` (${error.message})` : "";
    throw new Error(
      `Cannot reach backend at ${API_URL || "(same origin /api — is uvicorn on :8000 running?)"}${hint}. Start the FastAPI server and try again.`
    );
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Request failed");
  }
  return data;
}

export const api = {
  setToken,
  clearToken,

  // ─────────────────────────────────────────
  // AUTH
  // ─────────────────────────────────────────
  register: (payload) =>
    request("/api/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload) =>
    request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email: payload.email, password: payload.password }),
    }),

  // ─────────────────────────────────────────
  // TRIPS
  // ─────────────────────────────────────────
  listTrips: () => request("/api/trips"),
  createTrip: (payload) => request("/api/trips", { method: "POST", body: JSON.stringify(payload) }),
  getTrip: (tripId) => request(`/api/trips/${tripId}`),
  updateTrip: (tripId, payload) =>
    request(`/api/trips/${tripId}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTrip: (tripId) => request(`/api/trips/${tripId}`, { method: "DELETE" }),

  // ─────────────────────────────────────────
  // GROUP VOTING
  // ─────────────────────────────────────────
  voteDestination: (tripId, payload) =>
    request(`/api/trips/${tripId}/vote`, { method: "POST", body: JSON.stringify(payload) }),
  getVotes: (tripId) => request(`/api/trips/${tripId}/votes`),

  // ─────────────────────────────────────────
  // ITINERARY
  // ─────────────────────────────────────────
  generateItinerary: (payload) =>
    request("/api/itinerary/generate", { method: "POST", body: JSON.stringify(payload) }),
  getItinerary: (tripId) => request(`/api/itinerary/${tripId}`),
  updateItinerary: (tripId, payload) =>
    request(`/api/itinerary/${tripId}`, { method: "PUT", body: JSON.stringify(payload) }),

  // ─────────────────────────────────────────
  // PACKING LIST
  // ─────────────────────────────────────────
  generatePackingList: (tripId) =>
    request(`/api/itinerary/packing-list/${tripId}`, { method: "POST" }),
  getPackingList: (tripId) => request(`/api/itinerary/packing-list/${tripId}`),
  togglePackingItem: (tripId, itemId, checked) =>
    request(`/api/itinerary/packing-list/${tripId}/item/${itemId}`, {
      method: "PATCH",
      body: JSON.stringify({ checked }),
    }),
  deletePackingItem: (tripId, itemId) =>
    request(`/api/itinerary/packing-list/${tripId}/item/${itemId}`, { method: "DELETE" }),

  // ─────────────────────────────────────────
  // BUDGET & EXPENSES
  // ─────────────────────────────────────────
  getBudget: (tripId) => request(`/api/budget/${tripId}`),
  addExpense: (tripId, payload) =>
    request(`/api/budget/${tripId}/add-expense`, { method: "POST", body: JSON.stringify(payload) }),
  splitBudget: (tripId, payload) =>
    request(`/api/budget/${tripId}/split`, { method: "POST", body: JSON.stringify(payload || {}) }),

  // ─────────────────────────────────────────
  // CHAT
  // ─────────────────────────────────────────
  chat: (payload) =>
    request("/api/chat/message", { method: "POST", body: JSON.stringify(payload) }),

  // ─────────────────────────────────────────
  // RECOMMENDATIONS
  // ─────────────────────────────────────────
  recommendations: (type, payload) =>
    request(`/api/recommendations/${type}`, { method: "POST", body: JSON.stringify(payload) }),

  // ─────────────────────────────────────────
  // SERVICES: WEATHER
  // ─────────────────────────────────────────
  getWeather: (city) => request(`/api/services/weather/${encodeURIComponent(city)}`),

  // ─────────────────────────────────────────
  // SERVICES: FLIGHTS & HOTELS
  // ─────────────────────────────────────────
  getFlightEstimates: (origin, destination, date) =>
    request(
      `/api/services/flights?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(
        destination
      )}${date ? `&date=${date}` : ""}`
    ),
  getHotelEstimates: (destination, checkin, checkout) =>
    request(
      `/api/services/hotels?destination=${encodeURIComponent(destination)}${
        checkin ? `&checkin=${checkin}` : ""
      }${checkout ? `&checkout=${checkout}` : ""}`
    ),

  // ─────────────────────────────────────────
  // SERVICES: VISA
  // ─────────────────────────────────────────
  getVisaRequirements: (passport, destination) =>
    request(
      `/api/services/visa?passport=${encodeURIComponent(passport)}&destination=${encodeURIComponent(
        destination
      )}`
    ),

  // ─────────────────────────────────────────
  // SERVICES: ATTRACTIONS
  // ─────────────────────────────────────────
  getAttractions: (lat, lon, radius = 2000) =>
    request(`/api/services/attractions?lat=${lat}&lon=${lon}&radius=${radius}`),
};

// ─────────────────────────────────────────
// CITY SEARCH (using Open-Meteo geocoding - FREE, no API key needed)
// ─────────────────────────────────────────

export async function searchCities(query) {
  if (!query || query.length < 2) return [];

  try {
    const response = await fetch(
      `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(
        query
      )}&count=10&language=en&format=json`
    );

    if (!response.ok) return [];

    const data = await response.json();

    return (
      data.results?.map((result) => ({
        name: result.name,
        country: result.country,
        countryCode: result.country_code,
        lat: result.latitude,
        lon: result.longitude,
        admin: result.admin1,
        population: result.population,
      })) || []
    );
  } catch (error) {
    console.error("City search error:", error);
    return [];
  }
}

// ─────────────────────────────────────────
// MAP ATTRACTIONS (using Overpass API - FREE, no API key needed)
// ─────────────────────────────────────────
// Note: Backend already has /api/services/attractions endpoint
// This is an alternative for direct frontend calls if needed
export async function fetchAttractionsDirect(lat, lon, radius = 2000) {
  const query = `
    [out:json][timeout:10];
    (
      node["tourism"~"museum|attraction|viewpoint|gallery|zoo|theme_park"](around:${radius},${lat},${lon});
      node["amenity"~"restaurant|cafe|bar"](around:${radius},${lat},${lon});
      node["leisure"~"park|garden"](around:${radius},${lat},${lon});
      node["shop"~"mall|department_store"](around:${radius},${lat},${lon});
    );
    out body 50;
  `;

  try {
    const response = await fetch("https://overpass-api.de/api/interpreter", {
      method: "POST",
      body: new URLSearchParams({ data: query }),
    });

    if (!response.ok) return [];

    const data = await response.json();

    return data.elements
      .filter((el) => el.tags?.name)
      .slice(0, 50)
      .map((el) => {
        let category = "attraction";
        const tags = el.tags || {};

        if ("tourism" in tags) {
          category = tags.tourism;
        } else if (["restaurant", "cafe", "bar"].includes(tags.amenity)) {
          category = tags.amenity;
        } else if ("leisure" in tags) {
          category = "park";
        } else if ("shop" in tags) {
          category = "shopping";
        }

        return {
          name: tags.name,
          lat: el.lat,
          lon: el.lon,
          category,
          cuisine: tags.cuisine,
          website: tags.website,
        };
      });
  } catch (error) {
    console.error("Attractions fetch error:", error);
    return [];
  }
}