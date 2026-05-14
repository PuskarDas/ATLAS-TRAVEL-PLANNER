import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles/app.css";
import { api } from "./services/api";
import { ToastProvider } from "./ToastProvider";
import { Dashboard } from "./Dashboard";

const AuthPanel = ({ onAuth }) => {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({
    username: "",
    email: "planner@example.com",
    password: "password123",
    first_name: "Group",
    last_name: "Planner",
  });
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const action = mode === "login" ? api.login : api.register;
      const result = await action(form);
      api.setToken(result.access_token);
      localStorage.setItem("refreshToken", result.refresh_token || "");
      onAuth(result.user);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="auth-screen-wrapper">
      <section className="auth-hero-section">
        <div className="auth-hero-content">
          <p className="eyebrow light">AI Group Travel Planner</p>
          <h1>Turn scattered group chats into one beautiful trip plan.</h1>
          <div className="auth-stat-grid">
            <span>Worldwide destinations</span>
            <span>AI itinerary</span>
            <span>Live budget</span>
          </div>
        </div>
      </section>
      <section className="auth-form-panel">
        <div className="auth-panel-header">
          <p className="eyebrow">Welcome</p>
          <h2>{mode === "login" ? "Login to your planner" : "Create your travel workspace"}</h2>
        </div>
        <div className="segmented">
          <button type="button" className={mode === "login" ? "active" : ""} onClick={() => setMode("login")}>
            Login
          </button>
          <button type="button" className={mode === "register" ? "active" : ""} onClick={() => setMode("register")}>
            Register
          </button>
        </div>
        <form onSubmit={submit} className="auth-form-stack">
          {mode === "register" && (
            <input
              className="auth-input"
              value={form.username}
              onChange={(event) => setForm({ ...form, username: event.target.value })}
              placeholder="Username"
            />
          )}
          <input
            className="auth-input"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            placeholder="Email"
          />
          <input
            className="auth-input"
            type="password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
            placeholder="Password"
          />
          {error && <p className="error">{error}</p>}
          <button className="primary" type="submit">
            {mode === "login" ? "Login" : "Create account"}
          </button>
        </form>
      </section>
    </main>
  );
};

function App() {
  const [user, setUser] = useState(null);
  return (
    <ToastProvider>
      {user ? <Dashboard user={user} onLogout={() => setUser(null)} /> : <AuthPanel onAuth={setUser} />}
    </ToastProvider>
  );
}

createRoot(document.getElementById("root")).render(<App />);
