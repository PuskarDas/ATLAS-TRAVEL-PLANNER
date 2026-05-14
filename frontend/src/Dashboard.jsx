import React, { useCallback, useEffect, useMemo, useState } from "react";
import {
  Backpack,
  CalendarDays,
  Cloud,
  Compass,
  Download,
  FileJson,
  IdCard,
  IndianRupee,
  LayoutDashboard,
  Lightbulb,
  MapPin,
  MessageCircle,
  Moon,
  Navigation2,
  Plane,
  Plus,
  Receipt,
  Search,
  Sparkles,
  Star,
  Sun,
  ThumbsUp,
  Trash2,
  Users,
  Wallet,
} from "lucide-react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { api, searchCities, fetchAttractionsDirect } from "./services/api";
import { useToast } from "./ToastProvider";
import { getHeroImageForDestination } from "./destinationHero";

// ─────────────────────────────────────────
// CITY SEARCH COMPONENT (world cities)
// ─────────────────────────────────────────

const CitySearch = ({ onSelect, defaultValue = "" }) => {
  const [query, setQuery] = useState(defaultValue);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (query && query.length > 1) {
        setLoading(true);
        searchCities(query).then((cities) => {
          setResults(cities);
          setLoading(false);
        });
      } else {
        setResults([]);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const handleSelect = (city) => {
    onSelect(city);
    setQuery(city.name);
    setOpen(false);
  };

  return (
    <div style={{ position: "relative" }}>
      <input
        className="form-input"
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        placeholder="Search destination worldwide..."
      />
      {open && (query.length > 1 || results.length > 0) && (
        <div style={{
          position: "absolute",
          top: "100%",
          left: 0,
          right: 0,
          background: "var(--card)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius-sm)",
          maxHeight: "300px",
          overflow: "auto",
          zIndex: 1000,
          marginTop: "4px",
        }}>
          {loading && <div style={{ padding: "12px", color: "var(--text-muted)" }}>Searching...</div>}
          {!loading && results.length === 0 && query.length > 1 && (
            <div style={{ padding: "12px", color: "var(--text-muted)" }}>No results found</div>
          )}
          {results.map((city) => (
            <button
              key={`${city.lat}-${city.lon}`}
              type="button"
              onClick={() => handleSelect(city)}
              style={{
                width: "100%",
                padding: "10px 12px",
                border: "none",
                background: "transparent",
                color: "var(--text)",
                textAlign: "left",
                cursor: "pointer",
                borderBottom: "1px solid var(--border)",
              }}
              onMouseEnter={(e) => (e.target.style.background = "var(--surface)")}
              onMouseLeave={(e) => (e.target.style.background = "transparent")}
            >
              <strong>{city.name}</strong>
              <div style={{ fontSize: "11px", color: "var(--text-muted)" }}>{city.country} {city.admin ? `• ${city.admin}` : ""}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

// ─────────────────────────────────────────
// TRIP WIZARD (with world cities)
// ─────────────────────────────────────────

const TripWizard = ({ onCreate }) => {
  const toast = useToast();
  const [trip, setTrip] = useState({
    title: "Spring friends escape",
    destination: "Bali",
    description: "Beach, food, and relaxed sightseeing.",
    start_date: "2026-06-12",
    end_date: "2026-06-16",
    budget: 1800,
    is_group: true,
    traveler_count: 4,
  });
  async function submit(event) {
    event.preventDefault();
    const payload = {
      ...trip,
      start_date: `${trip.start_date}T00:00:00`,
      end_date: `${trip.end_date}T00:00:00`,
      budget: Number(trip.budget),
      traveler_count: Math.min(99, Math.max(1, Number(trip.traveler_count) || 2)),
    };
    try {
      const created = await api.createTrip(payload);
      onCreate(created);
      toast(`Trip “${created.title}” created`, "success");
    } catch (e) {
      toast(e.message || "Could not create trip", "error");
    }
  }

  return (
    <section id="trip-wizard-anchor" className="panel trip-wizard-panel motion-panel" style={{ scrollMarginTop: "72px" }}>
      <div className="panel-title">
        <Plus size={18} />
        <h2>Trip Creation</h2>
      </div>
      <div className="wizard-layout">
        <div className="wizard-preview motion-hero-thumb" aria-hidden>
          <div
            key={trip.destination}
            className="wizard-preview-image"
            style={{ backgroundImage: `url(${getHeroImageForDestination(trip.destination)})` }}
          />
          <div className="wizard-preview-caption">
            <span className="eyebrow light">Preview</span>
            <strong>{trip.destination}</strong>
          </div>
        </div>
        <form onSubmit={submit} className="grid-form wizard-form">
          <input className="form-input" value={trip.title} onChange={(e) => setTrip({ ...trip, title: e.target.value })} placeholder="Trip title" />
          <CitySearch
            defaultValue={trip.destination}
            onSelect={(city) => {
              setTrip({ ...trip, destination: city.name });
            }}
          />
          <label className="field-label span-full" htmlFor="traveler-count">
            How many travelers?
          </label>
          <input
            id="traveler-count"
            className="form-input"
            type="number"
            min={1}
            max={99}
            value={trip.traveler_count}
            onChange={(e) => setTrip({ ...trip, traveler_count: e.target.value })}
            placeholder="Travelers"
          />
          <input className="form-input" type="date" value={trip.start_date} onChange={(e) => setTrip({ ...trip, start_date: e.target.value })} />
          <input className="form-input" type="date" value={trip.end_date} onChange={(e) => setTrip({ ...trip, end_date: e.target.value })} />
          <input className="form-input" type="number" value={trip.budget} onChange={(e) => setTrip({ ...trip, budget: e.target.value })} placeholder="Budget" />
          <input className="form-input span-full" value={trip.description} onChange={(e) => setTrip({ ...trip, description: e.target.value })} placeholder="Description" />
          <button className="primary span-full" type="submit">
            Create Trip
          </button>
        </form>
      </div>
    </section>
  );
};

// ─────────────────────────────────────────
// WEATHER PANEL
// ─────────────────────────────────────────

const WeatherPanel = ({ trip }) => {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip) return;
    setLoading(true);
    api
      .getWeather(trip.destination)
      .then(setWeather)
      .catch((e) => console.error("Weather error:", e))
      .finally(() => setLoading(false));
  }, [trip?.destination]);

  if (!trip) return null;

  return (
    <section className="panel">
      <div className="panel-title">
        <Cloud size={18} />
        <h2>Weather</h2>
      </div>
      {loading ? (
        <p className="muted">Loading...</p>
      ) : weather ? (
        <div>
          <div style={{ marginBottom: "16px" }}>
            <div style={{ fontSize: "28px", fontWeight: "700", color: "var(--accent-light)" }}>{weather.temperature}°C</div>
            <div style={{ color: "var(--text-muted)", fontSize: "13px" }}>Feels like {weather.feels_like}°C</div>
            <div style={{ color: "var(--text)", marginTop: "4px" }}>{weather.description}</div>
            <div style={{ marginTop: "8px", fontSize: "12px", color: "var(--text-muted)" }}>
              💧 {weather.humidity}% | 🌬️ {weather.wind_speed}km/h
            </div>
          </div>
          {weather.forecast && weather.forecast.length > 0 && (
            <div style={{ marginTop: "12px", borderTop: "1px solid var(--border)", paddingTop: "12px" }}>
              <p style={{ fontSize: "11px", fontWeight: "700", textTransform: "uppercase", color: "var(--text-muted)", marginBottom: "8px" }}>5-Day Forecast</p>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "6px" }}>
                {weather.forecast.map((day, i) => (
                  <div key={i} style={{ textAlign: "center", fontSize: "11px" }}>
                    <div style={{ fontWeight: "600", marginBottom: "4px" }}>{day.day}</div>
                    <div style={{ color: "var(--accent-light)", fontSize: "12px", fontWeight: "700" }}>{day.high}°</div>
                    <div style={{ color: "var(--text-muted)", fontSize: "10px" }}>{day.low}°</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <p className="muted">Could not load weather</p>
      )}
    </section>
  );
};

// ─────────────────────────────────────────
// FLIGHTS & HOTELS PANEL
// ─────────────────────────────────────────

const FlightHotelPanel = ({ trip }) => {
  const [flights, setFlights] = useState(null);
  const [hotels, setHotels] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip) return;
    setLoading(true);
    Promise.all([
      api.getFlightEstimates("Current City", trip.destination),
      api.getHotelEstimates(trip.destination, trip.start_date, trip.end_date),
    ])
      .then(([f, h]) => {
        setFlights(f);
        setHotels(h);
      })
      .catch((e) => console.error("Flight/hotel error:", e))
      .finally(() => setLoading(false));
  }, [trip?.destination]);

  if (!trip) return null;

  return (
    <section className="panel">
      <div className="panel-title">
        <Plane size={18} />
        <h2>Flights & Hotels</h2>
      </div>
      {loading ? (
        <p className="muted">Loading...</p>
      ) : (
        <div>
          {flights && (
            <div style={{ marginBottom: "14px", paddingBottom: "14px", borderBottom: "1px solid var(--border)" }}>
              <p style={{ fontSize: "12px", fontWeight: "700", color: "var(--accent-light)", marginBottom: "6px" }}>✈️ FLIGHTS</p>
              <div style={{ fontSize: "14px", fontWeight: "600", color: "var(--text)" }}>{flights.price_range}</div>
              <div style={{ fontSize: "11px", color: "var(--text-muted)", marginTop: "4px" }}>{flights.note}</div>
            </div>
          )}
          {hotels && (
            <div>
              <p style={{ fontSize: "12px", fontWeight: "700", color: "var(--accent-light)", marginBottom: "6px" }}>🏨 HOTELS</p>
              <div style={{ fontSize: "11px", color: "var(--text)" }}>
                <div>💰 Budget: {hotels.budget_range}</div>
                <div style={{ marginTop: "4px" }}>⭐ Midrange: {hotels.midrange_range}</div>
                <div style={{ marginTop: "4px" }}>👑 Luxury: {hotels.luxury_range}</div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

// ─────────────────────────────────────────
// GROUP VOTING PANEL
// ─────────────────────────────────────────

const GroupVotingPanel = ({ trip }) => {
  const toast = useToast();
  const [votes, setVotes] = useState(null);
  const [newVoteDestination, setNewVoteDestination] = useState("");
  const [newVoteScore, setNewVoteScore] = useState(5);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip) return;
    loadVotes();
  }, [trip?.id]);

  async function loadVotes() {
    try {
      const data = await api.getVotes(trip.id);
      setVotes(data);
    } catch (e) {
      console.error("Votes error:", e);
    }
  }

  async function submitVote(e) {
    e.preventDefault();
    try {
      await api.voteDestination(trip.id, { destination: newVoteDestination, score: newVoteScore });
      setNewVoteDestination("");
      setNewVoteScore(5);
      loadVotes();
      toast("Vote saved", "success");
    } catch (e) {
      toast(e.message || "Vote failed", "error");
    }
  }

  if (!trip) return null;

  return (
    <section className="panel">
      <div className="panel-title">
        <Users size={18} />
        <h2>Group Voting</h2>
      </div>
      {votes && votes.aggregated && votes.aggregated.length > 0 && (
        <div style={{ marginBottom: "14px" }}>
          {votes.aggregated.slice(0, 3).map((item) => (
            <div key={item.destination} style={{ marginBottom: "8px", padding: "10px", background: "var(--surface)", borderRadius: "var(--radius-sm)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong style={{ fontSize: "13px" }}>{item.destination}</strong>
                <div style={{ color: "var(--accent-light)", fontWeight: "700" }}>⭐ {item.average}/5</div>
              </div>
              <div style={{ fontSize: "11px", color: "var(--text-muted)", marginTop: "4px" }}>{item.vote_count} votes</div>
            </div>
          ))}
        </div>
      )}
      <form onSubmit={submitVote} className="compact-form" style={{ gridTemplateColumns: "1fr auto auto" }}>
        <input
          className="form-input"
          type="text"
          value={newVoteDestination}
          onChange={(e) => setNewVoteDestination(e.target.value)}
          placeholder="Vote for destination"
        />
        <select
          className="form-select"
          value={newVoteScore}
          onChange={(e) => setNewVoteScore(Number(e.target.value))}
        >
          {[5, 4, 3, 2, 1].map((n) => (
            <option key={n} value={n}>
              {n}★
            </option>
          ))}
        </select>
        <button className="icon-button" title="Vote" disabled={!newVoteDestination}>
          <ThumbsUp size={16} />
        </button>
      </form>
    </section>
  );
};

// ─────────────────────────────────────────
// PACKING LIST PANEL
// ─────────────────────────────────────────

const PackingListPanel = ({ trip }) => {
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip) return;
    loadPackingList();
  }, [trip?.id]);

  async function loadPackingList() {
    setLoading(true);
    try {
      const data = await api.getPackingList(trip.id);
      setItems(data.items);
    } catch (e) {
      // Generate if not exists
      await api.generatePackingList(trip.id).then((data) => setItems(data.items));
    } finally {
      setLoading(false);
    }
  }

  async function toggleItem(itemId, checked) {
    try {
      await api.togglePackingItem(trip.id, itemId, checked);
      setItems(items.map((item) => (item.id === itemId ? { ...item, checked } : item)));
    } catch (e) {
      console.error("Toggle error:", e);
    }
  }

  if (!trip) return null;

  const checkedCount = items ? items.filter((i) => i.checked).length : 0;
  const totalCount = items ? items.length : 0;

  return (
    <section className="panel">
      <div className="panel-title">
        <Backpack size={18} />
        <h2>Packing List</h2>
      </div>
      {loading ? (
        <p className="muted">Loading...</p>
      ) : items ? (
        <div>
          <div style={{ marginBottom: "12px", fontSize: "12px", color: "var(--text-muted)" }}>
            {checkedCount} of {totalCount} packed
          </div>
          <div style={{ maxHeight: "250px", overflow: "auto" }}>
            {items.slice(0, 8).map((item) => (
              <label key={item.id} style={{ display: "flex", alignItems: "center", gap: "8px", padding: "8px", cursor: "pointer" }}>
                <input type="checkbox" checked={item.checked} onChange={(e) => toggleItem(item.id, e.target.checked)} />
                <span style={{ color: item.checked ? "var(--text-muted)" : "var(--text)", textDecoration: item.checked ? "line-through" : "none", fontSize: "13px" }}>
                  {item.name}
                </span>
                <span style={{ fontSize: "10px", color: "var(--text-dim)" }}>({item.category})</span>
              </label>
            ))}
          </div>
          {totalCount > 8 && <p style={{ fontSize: "11px", color: "var(--text-muted)", marginTop: "8px" }}>+ {totalCount - 8} more items</p>}
        </div>
      ) : (
        <button className="secondary" onClick={loadPackingList} style={{ width: "100%" }}>
          <Download size={14} /> Generate Packing List
        </button>
      )}
    </section>
  );
};

// ─────────────────────────────────────────
// VISA REQUIREMENTS PANEL
// ─────────────────────────────────────────

const VisaPanel = ({ trip }) => {
  const [visa, setVisa] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip) return;
    setLoading(true);
    api
      .getVisaRequirements("IN", trip.destination) // Default to Indian passport
      .then(setVisa)
      .catch((e) => console.error("Visa error:", e))
      .finally(() => setLoading(false));
  }, [trip?.destination]);

  if (!trip) return null;

  return (
    <section className="panel">
      <div className="panel-title">
        <IdCard size={18} />
        <h2>Visa Requirements</h2>
      </div>
      {loading ? (
        <p className="muted">Loading...</p>
      ) : visa ? (
        <div>
          <div style={{ marginBottom: "12px" }}>
            <div style={{ fontWeight: "700", fontSize: "14px", color: visa.visa_required ? "#d96c5a" : "var(--green-text)", marginBottom: "6px" }}>
              {visa.visa_required ? "✓ Visa Required" : "✓ Visa-Free"}
            </div>
            <div style={{ fontSize: "12px", color: "var(--text)" }}>
              <div>Type: {visa.visa_type}</div>
              <div style={{ marginTop: "4px" }}>Duration: {visa.duration}</div>
            </div>
          </div>
          <div style={{ fontSize: "11px", color: "var(--text-muted)", padding: "8px", background: "var(--surface)", borderRadius: "var(--radius-sm)" }}>
            {visa.notes}
          </div>
        </div>
      ) : (
        <p className="muted">Could not load visa info</p>
      )}
    </section>
  );
};

// ─────────────────────────────────────────
// BUDGET TRACKER (Enhanced with splits)
// ─────────────────────────────────────────

const BudgetTracker = ({ trip }) => {
  const toast = useToast();
  const [budget, setBudget] = useState(null);
  const [expense, setExpense] = useState({ description: "Dinner", amount: 60, category: "food", paid_by: 1 });

  useEffect(() => {
    if (trip) api.getBudget(trip.id).then(setBudget).catch(() => {});
  }, [trip]);

  async function addExpense(event) {
    event.preventDefault();
    try {
      await api.addExpense(trip.id, { ...expense, amount: Number(expense.amount), paid_by: Number(expense.paid_by) });
      setBudget(await api.getBudget(trip.id));
      toast("Expense added", "success");
    } catch (e) {
      toast(e.message || "Could not add expense", "error");
    }
  }

  return (
    <section className="panel budget-tracker-panel">
      <div className="panel-title">
        <Wallet size={18} />
        <h2>Budget Tracker</h2>
      </div>
      <div className="metric-row">
        <div>
          <span>Spent</span>
          <strong>${budget?.analytics?.total_spent || 0}</strong>
        </div>
        <div>
          <span>Remaining</span>
          <strong>${Math.round(budget?.analytics?.remaining || 0)}</strong>
        </div>
        <div>
          <span>Status</span>
          <strong>{budget?.analytics?.status || "Ready"}</strong>
        </div>
      </div>
      <form className="compact-form" onSubmit={addExpense}>
        <input className="form-input" value={expense.description} onChange={(e) => setExpense({ ...expense, description: e.target.value })} placeholder="Expense" />
        <input className="form-input" type="number" value={expense.amount} onChange={(e) => setExpense({ ...expense, amount: e.target.value })} placeholder="Amount" />
        <button className="icon-button" title="Add" disabled={!trip}>
          <Receipt size={16} />
        </button>
      </form>
    </section>
  );
};

// ─────────────────────────────────────────
// ITINERARY BUILDER
// ─────────────────────────────────────────

const ItineraryBuilder = ({ trip, onUpdate }) => {
  const toast = useToast();
  const [loading, setLoading] = useState(false);
  const days = trip?.itinerary?.data?.itinerary || [];

  async function generate() {
    if (!trip) return;
    setLoading(true);
    try {
      await api.generateItinerary({
        trip_id: trip.id,
        preferences: { interests: ["beach", "food", "culture"], travel_style: "mid-range" },
      });
      const full = await api.getTrip(trip.id);
      onUpdate(full, { keepTab: true });
      toast("Itinerary generated", "success");
    } catch (e) {
      toast(e.message || "Itinerary failed", "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel itinerary-builder-panel">
      <div className="panel-title">
        <CalendarDays size={18} />
        <h2>Itinerary Builder</h2>
      </div>
      <button className="secondary" onClick={generate} disabled={!trip || loading}>
        <Sparkles size={16} /> {loading ? "Generating" : "Generate AI Itinerary"}
      </button>
      <div className="timeline">
        {days.map((day) => (
          <article className="day" key={day.day}>
            <strong>Day {day.day}: {day.theme}</strong>
            {day.activities.map((activity) => (
              <p key={activity.id}>
                <span>{activity.time}</span>
                {activity.name}
              </p>
            ))}
          </article>
        ))}
        {!days.length && <p className="muted">Create a trip, then generate an itinerary.</p>}
      </div>
    </section>
  );
};

// ─────────────────────────────────────────
// CHATBOT
// ─────────────────────────────────────────

const Chatbot = ({ user, trip }) => {
  const toast = useToast();
  const [message, setMessage] = useState("What activities should we do?");
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);

  async function send(event) {
    event.preventDefault();
    if (!trip) return;
    setSending(true);
    try {
      const result = await api.chat({ user_id: user.id, trip_id: trip.id, message });
      setMessages((prev) => [...prev, result]);
      setMessage("");
    } catch (e) {
      toast(e.message || "Message failed", "error");
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="panel chatbot-panel">
      <div className="panel-title">
        <MessageCircle size={18} />
        <h2>Chatbot</h2>
      </div>
      <div className="chat-log">
        {messages.map((item, index) => (
          <div className="chat-pair" key={`${item.timestamp}-${index}`}>
            <p className="user-msg">{item.user_message}</p>
            <p className="bot-msg">{item.bot_response}</p>
          </div>
        ))}
      </div>
      <form className="chat-form" onSubmit={send}>
        <input className="form-input" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Ask the travel assistant" />
        <button className="primary" disabled={!trip || sending}>
          {sending ? "Sending…" : "Send"}
        </button>
      </form>
    </section>
  );
};

// ─────────────────────────────────────────
// AI DESTINATION IDEAS (authenticated)
// ─────────────────────────────────────────

const RecommendationsPanel = ({ trip }) => {
  const toast = useToast();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!trip) return;
    setLoading(true);
    const start = trip.start_date ? new Date(trip.start_date) : null;
    const end = trip.end_date ? new Date(trip.end_date) : null;
    let duration = 5;
    if (start && end && !Number.isNaN(end - start)) {
      duration = Math.max(1, Math.round((end - start) / 86400000) + 1);
    }
    api
      .recommendations("destinations", {
        activities: ["beach", "food", "culture", "nightlife"],
        budget: trip.budget || undefined,
        travel_style: "mid-range",
        duration_days: duration,
      })
      .then((res) => setRows(res.recommendations || []))
      .catch((e) => {
        toast(e.message || "Could not load ideas", "error");
        setRows([]);
      })
      .finally(() => setLoading(false));
  }, [trip?.id, trip?.budget]);

  if (!trip) return null;

  return (
    <section className="panel recommendations-panel">
      <div className="panel-title">
        <Lightbulb size={18} />
        <h2>AI destination ideas</h2>
      </div>
      <p className="muted" style={{ marginTop: "-8px" }}>
        Ranked for your budget and group style — use voting to shortlist with friends.
      </p>
      {loading ? (
        <div className="skeleton-stack">
          <div className="skeleton-line" />
          <div className="skeleton-line short" />
          <div className="skeleton-line" />
        </div>
      ) : (
        <div className="reco-card-list">
          {rows.slice(0, 5).map((d) => (
            <article key={d.id ?? d.name} className="reco-card">
              <div>
                <strong>{d.name}</strong>
                <span className="reco-meta">{d.country}</span>
              </div>
              <div className="reco-scores">
                <span className="reco-chip">{Math.round(d.match_score ?? 0)} match</span>
                <span className="reco-chip muted-chip">${d.cost_per_day}/day</span>
              </div>
            </article>
          ))}
          {!rows.length && <p className="muted">No suggestions yet.</p>}
        </div>
      )}
    </section>
  );
};

// ─────────────────────────────────────────
// MAP VIEWER (with attractions)
// ─────────────────────────────────────────

const MapViewer = ({ trip }) => {
  const [attractions, setAttractions] = useState([]);
  const mapId = `map-${trip?.id || "empty"}`;

  useEffect(() => {
    if (!trip) return;

    // Initialize map
    const map = L.map(mapId, { zoomControl: false }).setView([20, 77], 4);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    // For now, show trip destination (in real app, geocode it first)
    // L.marker([lat, lon]).addTo(map).bindPopup(trip.destination);

    return () => map.remove();
  }, [trip?.id]);

  // Fetch attractions when map loads
  useEffect(() => {
    if (!trip) return;
    // Example coordinates (in real app, geocode the destination)
    const lat = 20.5937; // Default to India
    const lon = 78.9629;

    fetchAttractionsDirect(lat, lon, 2000)
      .then(setAttractions)
      .catch((e) => console.error("Attractions error:", e));
  }, [trip?.destination]);

  return (
    <section className="panel map-viewer-panel">
      <div className="panel-title">
        <MapPin size={18} />
        <h2>Map Viewer</h2>
      </div>
      <div id={mapId} className="map" />
      {attractions.length > 0 && (
        <div style={{ marginTop: "12px", maxHeight: "150px", overflow: "auto", fontSize: "12px" }}>
          <p style={{ fontSize: "11px", fontWeight: "700", textTransform: "uppercase", color: "var(--text-muted)", marginBottom: "6px" }}>
            📍 Nearby Attractions
          </p>
          {attractions.slice(0, 5).map((attr, i) => (
            <div key={i} style={{ padding: "6px", background: "var(--surface)", marginBottom: "4px", borderRadius: "4px" }}>
              <strong style={{ fontSize: "12px" }}>{attr.name}</strong>
              <div style={{ fontSize: "10px", color: "var(--text-muted)" }}>{attr.category}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

// ─────────────────────────────────────────
// DASHBOARD
// ─────────────────────────────────────────

const WORKSPACE_TABS = [
  { id: "overview", label: "Overview", Icon: LayoutDashboard },
  { id: "plan", label: "Plan & vote", Icon: CalendarDays },
  { id: "logistics", label: "Logistics", Icon: Wallet },
  { id: "explore", label: "Explore map", Icon: MapPin },
  { id: "assistant", label: "Assistant", Icon: MessageCircle },
];

export function Dashboard({ user, onLogout }) {
  const toast = useToast();
  const [trips, setTrips] = useState([]);
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [tripQuery, setTripQuery] = useState("");
  const [workspaceTab, setWorkspaceTab] = useState("overview");
  const [theme, setTheme] = useState(() => localStorage.getItem("gtp-theme") || "dark");
  const [budgetSnap, setBudgetSnap] = useState(null);
  const [travelerDraft, setTravelerDraft] = useState(2);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("gtp-theme", theme);
  }, [theme]);

  useEffect(() => {
    api.listTrips().then((data) => {
      setTrips(data.trips);
      setSelectedTrip((prev) => {
        if (prev && data.trips.some((t) => t.id === prev.id)) return prev;
        return data.trips[0] || null;
      });
    });
  }, []);

  useEffect(() => {
    if (!selectedTrip) {
      setBudgetSnap(null);
      return;
    }
    api
      .getBudget(selectedTrip.id)
      .then(setBudgetSnap)
      .catch(() => setBudgetSnap(null));
  }, [selectedTrip?.id]);

  useEffect(() => {
    setTravelerDraft(Number(selectedTrip?.traveler_count) || 2);
  }, [selectedTrip?.id, selectedTrip?.traveler_count]);

  const filteredTrips = useMemo(() => {
    const q = tripQuery.trim().toLowerCase();
    if (!q) return trips;
    return trips.filter((t) => `${t.title} ${t.destination}`.toLowerCase().includes(q));
  }, [trips, tripQuery]);

  const tripDurationDays = useMemo(() => {
    if (!selectedTrip?.start_date || !selectedTrip?.end_date) return 0;
    const a = new Date(selectedTrip.start_date);
    const b = new Date(selectedTrip.end_date);
    if (Number.isNaN(a - b)) return 0;
    return Math.max(1, Math.round((b - a) / 86400000) + 1);
  }, [selectedTrip]);

  const daysUntilStart = useMemo(() => {
    if (!selectedTrip?.start_date) return null;
    const a = new Date();
    a.setHours(0, 0, 0, 0);
    const b = new Date(selectedTrip.start_date);
    b.setHours(0, 0, 0, 0);
    return Math.ceil((b - a) / 86400000);
  }, [selectedTrip]);

  const budgetPct = useMemo(() => {
    if (!selectedTrip?.budget || !budgetSnap?.analytics) return null;
    const spent = Number(budgetSnap.analytics.total_spent || 0);
    const cap = Number(selectedTrip.budget) || 1;
    return Math.min(100, Math.round((spent / cap) * 100));
  }, [selectedTrip, budgetSnap]);

  function upsertTrip(trip, { keepTab } = {}) {
    const nextTrips = [trip, ...trips.filter((item) => item.id !== trip.id)];
    setTrips(nextTrips);
    setSelectedTrip(trip);
    if (!keepTab) setWorkspaceTab("overview");
  }

  const exportTripJson = useCallback(() => {
    if (!selectedTrip) return;
    const blob = new Blob([JSON.stringify(selectedTrip, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `trip-${selectedTrip.id}-${selectedTrip.destination || "export"}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    toast("Trip JSON downloaded", "success");
  }, [selectedTrip, toast]);

  const deleteSelectedTrip = useCallback(async () => {
    if (!selectedTrip) return;
    if (!window.confirm(`Delete “${selectedTrip.title}”? This cannot be undone.`)) return;
    try {
      await api.deleteTrip(selectedTrip.id);
      const next = trips.filter((t) => t.id !== selectedTrip.id);
      setTrips(next);
      setSelectedTrip(next[0] || null);
      toast("Trip deleted", "success");
    } catch (e) {
      toast(e.message || "Delete failed", "error");
    }
  }, [selectedTrip, trips, toast]);

  const saveTravelerCount = useCallback(async () => {
    if (!selectedTrip) return;
    const n = Math.min(99, Math.max(1, Number(travelerDraft) || 1));
    if (n === Number(selectedTrip.traveler_count ?? 2)) {
      toast("Already saved", "info");
      return;
    }
    try {
      const updated = await api.updateTrip(selectedTrip.id, { traveler_count: n });
      setTrips((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
      setSelectedTrip(updated);
      toast("Traveler count saved", "success");
    } catch (e) {
      toast(e.message || "Could not update travelers", "error");
    }
  }, [selectedTrip, travelerDraft, toast]);

  const heroImage = useMemo(
    () => getHeroImageForDestination(selectedTrip?.destination || ""),
    [selectedTrip?.destination]
  );

  const heroPlace = {
    mood: selectedTrip
      ? `${selectedTrip.destination} · ${selectedTrip.start_date?.slice(0, 10) || "?"} → ${selectedTrip.end_date?.slice(0, 10) || "?"}`
      : "Plan together. Vote transparently. Travel confidently.",
    rating: 4.8,
    cost:
      selectedTrip && tripDurationDays > 0
        ? Math.round((selectedTrip.budget || 0) / tripDurationDays)
        : selectedTrip?.budget || 100,
  };

  const memberCount =
    Number(selectedTrip?.traveler_count) > 0
      ? Number(selectedTrip.traveler_count)
      : selectedTrip?.members?.length || 1;

  return (
    <main className="app-layout app-layout-pro">
      <aside className="sidebar sidebar-pro">
        <div className="sidebar-brand">
          <div className="brand-mark" aria-hidden>
            <Navigation2 size={20} />
          </div>
          <div>
            <p className="eyebrow light">Workspace</p>
            <h1>Atlas Planner</h1>
          </div>
        </div>
        <label className="sidebar-search">
          <Search size={16} className="sidebar-search-icon" aria-hidden />
          <input
            type="search"
            className="sidebar-search-input"
            value={tripQuery}
            onChange={(e) => setTripQuery(e.target.value)}
            placeholder="Search trips…"
            autoComplete="off"
          />
        </label>
        <div className="sidebar-toolbar">
          <button
            type="button"
            className="icon-button theme-toggle"
            title={theme === "dark" ? "Light mode" : "Dark mode"}
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <button
            type="button"
            className="secondary sidebar-action"
            onClick={() => {
              api.clearToken();
              onLogout();
            }}
          >
            Logout
          </button>
        </div>
        <div className="trip-list trip-list-scroll">
          {filteredTrips.map((trip) => (
            <button
              type="button"
              className={selectedTrip?.id === trip.id ? "active trip-item" : "trip-item"}
              key={trip.id}
              onClick={() => setSelectedTrip(trip)}
            >
              <strong>{trip.title}</strong>
              <span>{trip.destination}</span>
            </button>
          ))}
          {!filteredTrips.length && (
            <p className="sidebar-empty">{trips.length ? "No matches." : "Create a trip to pin it here."}</p>
          )}
        </div>
        <p className="sidebar-count">{filteredTrips.length} trip{filteredTrips.length === 1 ? "" : "s"}</p>
      </aside>
      <section className="main-content-area">
        <header className="hero hero-enhanced hero-motion">
          <div className="hero-visual" aria-hidden>
            <div
              key={heroImage}
              className="hero-bg-layer"
              style={{ backgroundImage: `url(${heroImage})` }}
            />
          </div>
          <div className="hero-content motion-hero-text">
            <p className="eyebrow light">Signed in as {user.username}</p>
            <h2>{selectedTrip ? selectedTrip.title : "Design your first group trip"}</h2>
            <p>{heroPlace.mood}</p>
            <div className="hero-metrics">
              <span>
                <Star size={15} /> {heroPlace.rating}
              </span>
              <span>
                <IndianRupee size={15} /> ~${heroPlace.cost}/day est.
              </span>
              <span>
                <Users size={15} /> {memberCount} traveler{memberCount === 1 ? "" : "s"}
              </span>
              {tripDurationDays > 0 && (
                <span>
                  <CalendarDays size={15} /> {tripDurationDays} days
                </span>
              )}
            </div>
          </div>
        </header>

        <div className="command-bar">
          <nav className="breadcrumb" aria-label="Breadcrumb">
            <span>Workspace</span>
            <span className="bc-sep">/</span>
            <span className="bc-current">{selectedTrip?.title || "No trip selected"}</span>
          </nav>
          <div className="command-actions">
            <button
              type="button"
              className="secondary"
              onClick={() => {
                setWorkspaceTab("overview");
                document.getElementById("trip-wizard-anchor")?.scrollIntoView({ behavior: "smooth", block: "start" });
              }}
            >
              <Plus size={16} /> New trip
            </button>
            <button type="button" className="secondary" disabled={!selectedTrip} onClick={exportTripJson}>
              <FileJson size={16} /> Export JSON
            </button>
            <button type="button" className="secondary danger-outline" disabled={!selectedTrip} onClick={deleteSelectedTrip}>
              <Trash2 size={16} /> Delete trip
            </button>
          </div>
        </div>

        {selectedTrip && (
          <div className="insight-strip">
            <div className="insight-card motion-fade-up">
              <span className="insight-label">Countdown</span>
              <strong>{daysUntilStart == null ? "—" : daysUntilStart > 0 ? `${daysUntilStart}d` : "Started"}</strong>
              <span className="insight-hint">until departure</span>
            </div>
            <div className="insight-card motion-fade-up" style={{ animationDelay: "0.04s" }}>
              <span className="insight-label">Budget used</span>
              <strong>{budgetPct == null ? "—" : `${budgetPct}%`}</strong>
              <div className="insight-bar">
                <div className="insight-bar-fill" style={{ width: `${budgetPct ?? 0}%` }} />
              </div>
            </div>
            <div className="insight-card motion-fade-up" style={{ animationDelay: "0.08s" }}>
              <span className="insight-label">Trip budget</span>
              <strong>${selectedTrip.budget ?? "—"}</strong>
              <span className="insight-hint">total envelope</span>
            </div>
            <div className="insight-card insight-card-interactive motion-fade-up" style={{ animationDelay: "0.12s" }}>
              <span className="insight-label">Travelers</span>
              <div className="traveler-edit-row">
                <input
                  className="insight-input"
                  type="number"
                  min={1}
                  max={99}
                  value={travelerDraft}
                  onChange={(e) => setTravelerDraft(e.target.value)}
                  aria-label="Number of travelers"
                />
                <button type="button" className="secondary insight-save" onClick={saveTravelerCount}>
                  Save
                </button>
              </div>
              <span className="insight-hint">{selectedTrip.is_group ? "Group trip · voting & splits" : "Solo trip"}</span>
            </div>
          </div>
        )}

        <div className="workspace-tabs motion-tabs" role="tablist" aria-label="Workspace sections">
          {WORKSPACE_TABS.map(({ id, label, Icon }) => (
            <button
              key={id}
              type="button"
              role="tab"
              aria-selected={workspaceTab === id}
              className={workspaceTab === id ? "workspace-tab active" : "workspace-tab"}
              onClick={() => setWorkspaceTab(id)}
            >
              <Icon size={16} aria-hidden />
              <span>{label}</span>
            </button>
          ))}
        </div>

        <div className="quick-picks">
          <div>
            <Compass size={18} />
            <strong>Inspiration</strong>
          </div>
          <div className="chip-row">
            {["Bali", "Paris", "Tokyo", "Dubai", "New York", "London", "Sydney", "Barcelona"].map((place) => (
              <button type="button" className="chip chip-button" key={place} onClick={() => setTripQuery(place)}>
                {place}
              </button>
            ))}
          </div>
        </div>

        <div className="dashboard-panels-grid tab-panel tab-panel-animated">
          {workspaceTab === "overview" && (
            <>
              <TripWizard onCreate={upsertTrip} />
              <RecommendationsPanel trip={selectedTrip} />
            </>
          )}
          {workspaceTab === "plan" && (
            <>
              <GroupVotingPanel trip={selectedTrip} />
              <ItineraryBuilder trip={selectedTrip} onUpdate={upsertTrip} />
            </>
          )}
          {workspaceTab === "logistics" && (
            <>
              <BudgetTracker trip={selectedTrip} />
              <PackingListPanel trip={selectedTrip} />
              <VisaPanel trip={selectedTrip} />
              <WeatherPanel trip={selectedTrip} />
              <FlightHotelPanel trip={selectedTrip} />
            </>
          )}
          {workspaceTab === "explore" && <MapViewer trip={selectedTrip} />}
          {workspaceTab === "assistant" && <Chatbot user={user} trip={selectedTrip} />}
        </div>
      </section>
    </main>
  );
}
